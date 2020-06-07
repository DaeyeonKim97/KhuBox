from django.http import JsonResponse, Http404
from ..services import files


def index(request):
    # 폴더/파일 목록
    if request.method == 'GET':
        return JsonResponse(files.list_item(request))
    # 폴더 생성, 파일 업로드
    elif request.method == 'POST':
        return JsonResponse(files.create(request))
    raise Http404


def trash(request):
    # 휴지통 비우기
    if request.method == 'DELETE':
        return JsonResponse(files.empty_trash(request))
    raise Http404


def item(request, file_id):
    # 폴더/파일 조회, 파일 다운로드
    if request.method == 'GET':
        return JsonResponse(files.find_item(request, file_id))
    # 폴더/파일 수정
    elif request.method == 'PATCH':
        return JsonResponse(files.update_item(request, file_id))
    raise Http404


def copy(request, file_id):
    # 파일 복제
    if request.method == 'POST':
        return JsonResponse(files.copy(request, file_id))
    raise Http404
