# 폴더/파일 목록
def list_item(request):
    return {'result': True}


# 폴더 생성, 파일 업로드
def create(request):
    return {'result': True}


# 휴지통 비우기
def empty_trash(request):
    return {'result': True}


# 폴더/파일 조회, 파일 다운로드
def find_item(request, file_id):
    return {'result': True}


# 폴더/파일 수정
def update_item(request, file_id):
    return {'result': True}


# 파일 복제
def copy(request, file_id):
    return {'result': True}
