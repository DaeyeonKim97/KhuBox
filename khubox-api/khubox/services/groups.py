import json
import uuid
from django.utils import timezone
from ..aws import s3_delete
from ..models import File, Group, GroupUser, User


# 그룹 생성
def create(request):
    # Check Login
    if request.user_id is None:
        return {'result': False, 'error': '권한이 없습니다.'}

    # Load
    try:
        received = json.loads(request.body.decode('utf-8'))
    except json.decoder.JSONDecodeError:
        return {'result': False, 'error': '입력이 잘못되었습니다.'}

    # Validate
    if 'name' not in received or received['name'] == '':
        return {'result': False, 'error': '입력이 누락되었습니다.'}

    # Create
    root_folder = uuid.uuid4()
    group = Group.objects.create(
        owner_id=request.user_id,
        name=received['name'],
        root_folder=root_folder,
        invite_code=uuid.uuid4(),
        created_at=timezone.now()
    )
    GroupUser.objects.create(
        group_id=group.id,
        user_id=request.user_id,
        joined_at=timezone.now()
    )
    File.objects.create(
        id=root_folder,
        owner_user_id=request.user_id,
        owner_group_id=group.id,
        type='folder',
        name='group_%s' % group.id,
        size=0,
        created_at=timezone.now()
    )

    return {'result': True, 'group_id': group.id}


# 그룹 초대장 조회
def find_invite(request, invite_code):
    # Check Login
    if request.user_id is None:
        return {'result': False, 'error': '권한이 없습니다.'}

    # Query
    group = Group.objects.filter(invite_code=invite_code)

    # Check Exists
    if len(group) == 0:
        return {'result': False, 'error': '존재하지 않는 초대장입니다.'}

    # Structure
    data = {
        'id': group[0].id,
        'name': group[0].name
    }

    # Check Joined
    joined = GroupUser.objects.filter(group_id=group[0].id, user_id=request.user_id)
    if len(joined) == 0:
        data['joined'] = False
    else:
        data['joined'] = True

    return {'result': True, 'data': data}


# 그룹 초대장 사용
def use_invite(request, invite_code):
    # Check Login
    if request.user_id is None:
        return {'result': False, 'error': '권한이 없습니다.'}

    # Query
    group = Group.objects.filter(invite_code=invite_code)

    # Check Exists
    if len(group) == 0:
        return {'result': False, 'error': '존재하지 않는 초대장입니다.'}

    # Check Joined
    joined = GroupUser.objects.filter(group_id=group[0].id, user_id=request.user_id)
    if len(joined) != 0:
        return {'result': False, 'error': '이미 가입된 그룹입니다.'}

    # Join
    GroupUser.objects.create(
        group_id=group[0].id,
        user_id=request.user_id,
        joined_at=timezone.now()
    )

    return {'result': True}


# 그룹 목록
def list_me(request):
    # Check Login
    if request.user_id is None:
        return {'result': False, 'error': '권한이 없습니다.'}

    # Query
    joined = GroupUser.objects.filter(user_id=request.user_id).values_list('group_id', flat=True)
    groups = Group.objects.filter(id__in=joined)

    # Structure
    data = []
    for group in groups:
        data.append({
            'id': group.id,
            'name': group.name,
            'root_folder': group.root_folder,
        })

    return {'result': True, 'data': data}


# 그룹 조회
def find_item(request, group_id):
    # Check Login
    if request.user_id is None:
        return {'result': False, 'error': '권한이 없습니다.'}

    # Check Joined
    joined = GroupUser.objects.filter(group_id=group_id, user_id=request.user_id)
    if len(joined) == 0:
        return {'result': False, 'error': '입력이 잘못되었습니다.'}

    # Query
    group = Group.objects.filter(id=group_id)

    # Check Exists
    if len(group) == 0:
        return {'result': False, 'error': '존재하지 않는 그룹입니다.'}

    # Structure
    data = {
        'id': group[0].id,
        'name': group[0].name,
        'root_folder': group[0].root_folder,
    }

    # If Owner
    if group[0].owner_id == request.user_id:
        user_ids = GroupUser.objects.filter(group_id=group_id).values_list('user_id', flat=True)
        users = User.objects.filter(id__in=user_ids)
        user_data = []
        for user in users:
            user_data.append({
                'id': user.id,
                'name': user.name,
            })
        data['user'] = user_data
        data['invite_code'] = group[0].invite_code
        data['created_at'] = group[0].created_at
        data['is_owner'] = True

    return {'result': True, 'data': data}


# 그룹 수정
def update_item(request, group_id):
    # Check Login
    if request.user_id is None:
        return {'result': False, 'error': '권한이 없습니다.'}

    # Load
    try:
        received = json.loads(request.body.decode('utf-8'))
    except json.decoder.JSONDecodeError:
        return {'result': False, 'error': '입력이 잘못되었습니다.'}

    # Validate
    if 'name' not in received or received['name'] == '':
        return {'result': False, 'error': '입력이 누락되었습니다.'}

    # Query
    group = Group.objects.filter(id=group_id)

    # Check Exists
    if len(group) == 0:
        return {'result': False, 'error': '존재하지 않는 그룹입니다.'}

    # Check Owner
    if group[0].owner_id != request.user_id:
        return {'result': False, 'error': '권한이 없습니다.'}

    # Update
    group[0].name = received['name']
    group[0].save()

    return {'result': True}


# 그룹 삭제
def delete_item(request, group_id):
    # Check Login
    if request.user_id is None:
        return {'result': False, 'error': '권한이 없습니다.'}

    # Query
    group = Group.objects.filter(id=group_id)

    # Check Exists
    if len(group) == 0:
        return {'result': False, 'error': '존재하지 않는 그룹입니다.'}

    # Check Owner
    if group[0].owner_id != request.user_id:
        return {'result': False, 'error': '권한이 없습니다.'}

    # S3 Delete
    del_list = File.objects.filter(owner_group_id=group_id).values_list('id', flat=True)
    s3_delete(del_list)

    # Delete
    del_list.update(is_trashed=1, deleted_at=timezone.now())
    GroupUser.objects.filter(group_id=group_id).delete()
    Group.objects.filter(id=group_id).delete()

    return {'result': True}


# 그룹 사용자 삭제
def remove_user(request, group_id, user_id):
    # Check Login
    if request.user_id is None:
        return {'result': False, 'error': '권한이 없습니다.'}

    # Query
    group = Group.objects.filter(id=group_id)

    # Check Owner
    if group[0].owner_id != request.user_id:
        return {'result': False, 'error': '권한이 없습니다.'}

    # Check Me
    if int(user_id) == request.user_id:
        return {'result': False, 'error': '본인은 삭제할 수 없습니다.'}

    # Remove
    GroupUser.objects.filter(group_id=group_id, user_id=user_id).delete()

    return {'result': True}
