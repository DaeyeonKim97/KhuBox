import json
import uuid
from django.utils import timezone
from pathvalidate import sanitize_filename
from ..aws import sign_upload, sign_download, s3_copy, s3_delete, s3_update_and_return_size
from ..models import File, GroupUser


# 폴더/파일 목록
def list_item(request):
    # Check Login
    if request.user_id is None:
        return {'result': False, 'error': '로그인을 해주세요.'}

    # Validate
    if request.GET.get('is_public') != 'true' \
            and request.GET.get('is_starred') != 'true' \
            and request.GET.get('is_trashed') != 'true':
        return {'result': False, 'error': '잘못된 요청입니다.'}

    # Query Files
    files = None
    if request.GET.get('is_public') == 'true':
        files = File.objects.filter(owner_user_id=request.user_id, is_public=1, deleted_at__isnull=True)
    elif request.GET.get('is_starred') == 'true':
        files = File.objects.filter(owner_user_id=request.user_id, is_starred=1, deleted_at__isnull=True)
    elif request.GET.get('is_trashed') == 'true':
        files = File.objects.filter(owner_user_id=request.user_id, is_trashed=1, deleted_at__isnull=True)

    # Serialize
    data = []
    for file in files:
        data.append({
            'id': file.id,
            'type': file.type,
            'name': file.name,
            'size': file.size,
            'is_public': file.is_public,
            'is_starred': file.is_starred,
            'is_trashed': file.is_trashed,
            'created_at': file.created_at,
        })

    return {'result': True, 'data': data}


# 폴더 생성, 파일 업로드
def create(request):
    # Check Login
    if request.user_id is None:
        return {'result': False, 'error': '로그인을 해주세요.'}

    # Load
    try:
        received = json.loads(request.body.decode('utf-8'))
    except json.decoder.JSONDecodeError:
        return {'result': False, 'error': '잘못된 요청입니다.'}

    # Validate
    if 'parent_id' not in received \
            or 'type' not in received \
            or 'name' not in received:
        return {'result': False, 'error': '잘못된 요청입니다.'}
    if (received['type'] != 'folder' and received['type'] != 'file') \
            or received['name'] == '':
        return {'result': False, 'error': '잘못된 요청입니다.'}

    # Get Parent
    parent = File.objects.filter(id=received['parent_id'], is_trashed=0, deleted_at__isnull=True)

    # Check Exists
    if len(parent) == 0:
        return {'result': False, 'error': '경로가 잘못되었습니다.'}

    # Check Owner
    is_auth = False
    if parent[0].owner_user_id == request.user_id:
        is_auth = True
    is_my_group = GroupUser.objects.filter(group_id=parent[0].owner_group_id, user_id=request.user_id)
    if len(is_my_group) != 0:
        is_auth = True
    if is_auth is False:
        return {'result': False, 'error': '경로가 잘못되었습니다.'}

    # Insert
    file_id = uuid.uuid4()
    File.objects.create(
        id=file_id,
        parent_id=received['parent_id'],
        owner_user_id=parent[0].owner_user_id,
        owner_group_id=parent[0].owner_group_id,
        uploader_id=request.user_id,
        type=received['type'],
        name=sanitize_filename(received['name']),
        size=0,
        created_at=timezone.now()
    )

    # Return Folder
    if received['type'] == 'folder':
        return {'result': True, 'file_id': file_id}

    # Return File
    upload_url = sign_upload(str(file_id))
    return {'result': True, 'file_id': file_id, 'upload_url': upload_url}


# 휴지통 비우기
def empty_trash(request):
    # Check Login
    if request.user_id is None:
        return {'result': False, 'error': '로그인을 해주세요.'}

    # Query Files
    files = File.objects.filter(owner_user_id=request.user_id, is_trashed=1, deleted_at__isnull=True)

    # First Depth
    del_list = []
    del_check = []
    for del_file in files:
        del_check.append(del_file.id)

    # Child Depth
    while True:
        if not del_check:
            break
        child_files = File.objects.filter(parent_id__in=del_check)
        del_list.extend(del_check)
        del_check.clear()
        for del_file in child_files:
            del_check.append(del_file.id)

    # S3 Delete
    s3_delete(del_list)

    # Update
    File.objects.filter(id__in=del_list).update(is_trashed=1, deleted_at=timezone.now())

    return {'result': True, 'affected': del_list}


# 폴더/파일 조회
def find_item(request, file_id):
    # Check Login
    if request.user_id is None:
        return {'result': False, 'error': '로그인을 해주세요.'}

    # Query
    file = File.objects.filter(id=file_id, deleted_at__isnull=True)

    # Check Exists
    if len(file) == 0:
        return {'result': False, 'error': '잘못된 요청입니다.'}

    # Check Owner
    is_auth = False
    if file[0].owner_user_id == request.user_id:
        is_auth = True
    is_my_group = GroupUser.objects.filter(group_id=file[0].owner_group_id, user_id=request.user_id)
    if len(is_my_group) != 0:
        is_auth = True

    # Check Public
    if file[0].is_public == 1:
        is_auth = True
    parent_id = file[0].parent_id
    while True:
        if parent_id is None or is_auth:
            break
        parent_file = File.objects.filter(id=parent_id)
        if parent_file[0].is_public == 1:
            is_auth = True
        parent_id = parent_file[0].parent_id

    # Check Auth
    if is_auth is False:
        return {'result': False, 'error': '잘못된 요청입니다.'}

    # Return File
    if file[0].type == 'file':
        download_url = sign_download(file[0].id)
        data = {
            'id': file[0].id,
            'parent_id': file[0].parent_id,
            'name': file[0].name,
            'size': file[0].size,
            'is_public': file[0].is_public,
            'is_starred': file[0].is_starred,
            'is_trashed': file[0].is_trashed,
            'created_at': file[0].created_at,
            'download_url': download_url,
        }
        return {'result': True, 'data': data}

    # Query
    files = File.objects.filter(parent_id=file[0].id, is_trashed=0, deleted_at__isnull=True)

    # Structure
    data = []
    for file in files:
        data.append({
            'id': file.id,
            'type': file.type,
            'name': file.name,
            'size': file.size,
            'is_public': file.is_public,
            'is_starred': file.is_starred,
            'is_trashed': file.is_trashed,
            'created_at': file.created_at,
        })

    # Return Folder
    return {'result': True, 'data': data}


# 폴더/파일 수정
def update_item(request, file_id):
    # Check Login
    if request.user_id is None:
        return {'result': False, 'error': '로그인을 해주세요.'}

    # Load
    try:
        received = json.loads(request.body.decode('utf-8'))
    except json.decoder.JSONDecodeError:
        return {'result': False, 'error': '잘못된 요청입니다.'}

    # Validate
    if 'name' not in received \
            and 'parent_id' not in received \
            and 'is_public' not in received \
            and 'is_starred' not in received \
            and 'is_trashed' not in received:
        return {'result': False, 'error': '잘못된 요청입니다.'}

    # Query
    file = File.objects.filter(id=file_id, deleted_at__isnull=True)

    # Check Exists
    if len(file) == 0:
        return {'result': False, 'error': '잘못된 요청입니다.'}

    # Check Owner
    is_auth = False
    if file[0].owner_user_id == request.user_id:
        is_auth = True
    is_my_group = GroupUser.objects.filter(group_id=file[0].owner_group_id, user_id=request.user_id)
    if len(is_my_group) != 0 \
            and 'is_public' not in received \
            and 'is_starred' not in received \
            and 'is_trashed' not in received:
        is_auth = True

    # Check Parent
    if 'parent_id' in received:
        parent = File.objects.filter(id=received['parent_id'], type='folder', deleted_at__isnull=True)
        if len(parent) == 0:
            return {'result': False, 'error': '잘못된 요청입니다.'}
        if (is_auth is True or len(is_my_group) != 0) \
                and parent[0].owner_user_id == file[0].owner_user_id \
                and parent[0].owner_group_id == file[0].owner_group_id \
                and file_id != received['parent_id']:
            is_auth = True
        else:
            is_auth = False

    # Check Auth
    if is_auth is False:
        return {'result': False, 'error': '잘못된 요청입니다.'}

    # Update
    if 'name' in received:
        if received['name'] == '':
            return {'result': False, 'error': '이름을 제대로 입력해주세요.'}
        file[0].name = sanitize_filename(received['name'])
        s3_update_and_return_size(file_id, file[0].name)
    if 'parent_id' in received:
        file[0].parent_id = received['parent_id']
    if 'is_public' in received:
        file[0].is_public = 1 if received['is_public'] is True else 0
    if 'is_starred' in received:
        file[0].is_starred = 1 if received['is_starred'] is True else 0
    if 'is_trashed' in received:
        if file[0].parent_id is None:
            return {'result': False, 'error': '잘못된 요청입니다.'}
        file[0].is_trashed = 1 if received['is_trashed'] is True else 0
    file[0].save()

    return {'result': True}


# 파일 복제
def copy(request, file_id):
    # Check Login
    if request.user_id is None:
        return {'result': False, 'error': '로그인을 해주세요.'}

    # Get File
    file = File.objects.filter(id=file_id, type='file', is_trashed=0, deleted_at__isnull=True)

    # Check Exists
    if len(file) == 0:
        return {'result': False, 'error': '잘못된 요청입니다.'}

    # Check Owner
    is_auth = False
    if file[0].owner_user_id == request.user_id:
        is_auth = True
    is_my_group = GroupUser.objects.filter(group_id=file[0].owner_group_id, user_id=request.user_id)
    if len(is_my_group) != 0:
        is_auth = True
    if is_auth is False:
        return {'result': False, 'error': '경로가 잘못되었습니다.'}

    # Create UUID
    new_file_id = uuid.uuid4()

    # S3 Copy
    s3_copy(file_id, new_file_id)

    # Create
    File.objects.create(
        id=new_file_id,
        parent_id=file[0].parent_id,
        owner_user_id=file[0].owner_user_id,
        owner_group_id=file[0].owner_group_id,
        uploader_id=request.user_id,
        type=file[0].type,
        name='%s의 사본' % file[0].name,
        size=file[0].size,
        created_at=timezone.now()
    )

    return {'result': True, 'file_id': file_id}
