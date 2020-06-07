# 그룹 생성
def create(request):
    return {'result': True}


# 그룹 초대장 조회
def find_invite(request, invite_code):
    return {'result': True}


# 그룹 초대장 사용
def use_invite(request, invite_code):
    return {'result': True}


# 그룹 목록
def list_me(request):
    return {'result': True}


# 그룹 조회
def find_item(request, group_id):
    return {'result': True}


# 그룹 수정
def update_item(request, group_id):
    return {'result': True}


# 그룹 삭제
def delete_item(request, group_id):
    return {'result': True}


# 그룹 사용자 삭제
def remove_user(request, group_id, user_id):
    return {'result': True}
