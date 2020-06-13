import datetime
import json
import jwt
import uuid
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils import timezone
from ..models import File, User


# 회원가입
def create(request):
    # Load
    try:
        received = json.loads(request.body.decode('utf-8'))
    except json.decoder.JSONDecodeError:
        return {'result': False, 'error': '입력이 잘못되었습니다.'}

    # Validate
    if 'email' not in received \
            or 'password' not in received \
            or 'name' not in received:
        return {'result': False, 'error': '입력이 누락되었습니다.'}

    # Validate Email
    try:
        validate_email(received['email'])
    except ValidationError:
        return {'result': False, 'error': '이메일 형식이 잘못되었습니다.'}

    # Validate Password
    if len(received['password']) < 8:
        return {'result': False, 'error': '비밀번호는 최소 8글자 입니다.'}

    # Validate Name
    if len(received['name']) > 50:
        return {'result': False, 'error': '이름은 최대 50글자 입니다.'}

    # Check Duplicates
    is_exists = User.objects.filter(email=received['email'])
    if len(is_exists) > 0:
        return {'result': False, 'error': '이미 사용중인 이메일 주소 입니다.'}

    # Insert
    root_folder = uuid.uuid4()
    user = User.objects.create(
        email=received['email'],
        password=make_password(received['password']),
        name=received['name'],
        root_folder=root_folder,
        created_at=timezone.now()
    )
    File.objects.create(
        id=uuid.uuid4(),
        owner_user_id=user.id,
        type='folder',
        name='user_%s' % user.id,
        size=0,
        created_at=timezone.now()
    )

    return {'result': True}


# 로그인
def login(request):
    # Load
    try:
        received = json.loads(request.body.decode('utf-8'))
    except json.decoder.JSONDecodeError:
        return {'result': False, 'error': '입력이 잘못되었습니다.'}

    # Validate
    if 'email' not in received \
            or 'password' not in received:
        return {'result': False, 'error': '입력이 누락되었습니다.'}

    # Select
    user = User.objects.filter(email=received['email'])

    # Not Exists
    if len(user) != 1:
        return {'result': False, 'error': '로그인에 실패하였습니다.'}

    # Check
    if check_password(received['password'], user[0].password) is False:
        return {'result': False, 'error': '로그인에 실패하였습니다.'}

    # Token Generate
    token = jwt.encode({'id': user[0].id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=6)},
                       key=settings.SECRET_KEY, algorithm='HS256')

    return {'result': True, 'token': token.decode('utf-8')}


# 회원정보 조회
def find_me(request):
    # TODO: Auth
    request.user_id = 1

    # Query
    user = User.objects.filter(id=request.user_id)

    # Check Exists
    if len(user) != 1:
        return {'result': False, 'error': '잘못된 요청입니다.'}

    # Serialize
    data = {
        'id': user[0].id,
        'email': user[0].email,
        'name': user[0].name,
        'root_folder': user[0].root_folder,
        'created_at': str(user[0].created_at)
    }

    return {'result': True, 'data': data}


# 회원정보 수정
def update_me(request):
    # TODO: Auth
    request.user_id = 1

    # Load
    try:
        received = json.loads(request.body.decode('utf-8'))
    except json.decoder.JSONDecodeError:
        return {'result': False, 'error': '입력이 잘못되었습니다.'}

    # Validate
    if 'name' not in received \
            and ('old_password' not in received and 'password' not in received):
        return {'result': False, 'error': '입력이 누락되었습니다.'}

    # Query
    user = User.objects.filter(id=request.user_id)

    # Check Exists
    if len(user) != 1:
        return {'result': False, 'error': '잘못된 요청입니다.'}

    # Change Name
    if 'name' in received:
        user[0].name = received['name']

    # Change Password
    if 'old_password' in received and 'password' in received:
        if check_password(received['old_password'], user[0].password) is False:
            return {'result': False, 'error': '이전 비밀번호가 잘못되었습니다.'}
        if len(received['password']) < 8:
            return {'result': False, 'error': '비밀번호는 최소 8글자 입니다.'}
        user[0].password = make_password(received['password'])

    # Save
    user[0].save()

    return {'result': True}
