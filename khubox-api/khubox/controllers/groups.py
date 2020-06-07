from django.http import JsonResponse, Http404
from ..services import groups


def index(request):
    # 그룹 생성
    if request.method == 'POST':
        return JsonResponse(groups.create(request))
    raise Http404


def invite(request, invite_code):
    # 그룹 초대장 조회
    if request.method == 'GET':
        return JsonResponse(groups.find_invite(request, invite_code))
    # 그룹 초대장 사용
    elif request.method == 'POST':
        return JsonResponse(groups.use_invite(request, invite_code))
    raise Http404


def me(request):
    # 그룹 목록
    if request.method == 'GET':
        return JsonResponse(groups.list_me(request))
    raise Http404


def item(request, group_id):
    # 그룹 조회
    if request.method == 'GET':
        return JsonResponse(groups.find_item(request, group_id))
    # 그룹 수정
    elif request.method == 'PATCH':
        return JsonResponse(groups.update_item(request, group_id))
    # 그룹 삭제
    elif request.method == 'DELETE':
        return JsonResponse(groups.delete_item(request, group_id))
    raise Http404


def remove_user(request, group_id, user_id):
    # 그룹 사용자 삭제
    if request.method == 'DELETE':
        return JsonResponse(groups.remove_user(request, group_id, user_id))
    raise Http404
