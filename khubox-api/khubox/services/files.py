import json
import uuid
from django.utils import timezone
from ..aws import sign
from ..models import File, GroupUser


# TODO: 폴더/파일 목록
def list_item(request):
    return {'result': True}


# 폴더 생성, 파일 업로드
def create(request):
    # TODO: Auth
    request.user_id = 1

    # Load
    received = json.loads(request.body.decode('utf-8'))

    # Validate
    if 'parent_id' not in received \
            or 'type' not in received \
            or 'name' not in received:
        return {'result': False, 'error': '입력이 누락되었습니다.'}
    if (received['type'] != 'folder' and received['type'] != 'file') \
            or received['name'] == '':
        return {'result': False, 'error': '입력이 잘못되었습니다.'}

    # Get Parent
    parent = File.objects.filter(id=received['parent_id'], is_trahsed=0, deleted_at__isnull=True)

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
        name=received['name'],
        size=0,
        created_at=timezone.now()
    )

    # Return Folder
    if received['type'] == 'folder':
        return {'result': True, 'file_id': file_id}

    # Return File
    upload_url = 'https://khubox-files.khunet.net/%s' % file_id
    upload_url = sign(upload_url)
    return {'result': True, 'file_id': file_id, 'upload_url': upload_url}


# TODO: 휴지통 비우기
def empty_trash(request):
    # TODO: Auth
    request.user_id = 1

    # Query Files
    files = File.objects.filter(owner_user_id=request.user_id, is_trahsed=1, deleted_at__isnull=True)

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

    # TODO: S3 Delete

    # Update
    File.objects.filter(id__in=del_list).update(is_trahsed=1, deleted_at=timezone.now())

    return {'result': True, 'affected': del_list}


# TODO: 폴더/파일 조회, 파일 다운로드
def find_item(request, file_id):
    return {'result': True}


# TODO: 폴더/파일 수정
def update_item(request, file_id):
    return {'result': True}


# TODO: 파일 복제
def copy(request, file_id):
    return {'result': True}
