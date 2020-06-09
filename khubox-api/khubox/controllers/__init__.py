from django.conf.urls import url

from . import files, groups, users

urlpatterns = [
    url(r'^files$', files.index),  # 폴더 생성, 파일 업로드, 폴더/파일 목록
    url(r'^files/trash$', files.trash),  # 휴지통 비우기
    url(r'^files/(?P<file_id>[-\w]+)$', files.item),  # 폴더/파일 조회, 폴더/파일 수정
    url(r'^files/(?P<file_id>[-\w]+)/copy$', files.copy),  # 파일 복제
    url(r'^groups$', groups.index),  # 그룹 생성
    url(r'^groups/invite/(?P<invite_code>[-\w]+)$', groups.invite),  # 그룹 초대장 조회, 그룹 초대장 사용
    url(r'^groups/me$', groups.me),  # 그룹 목록
    url(r'^groups/(?P<group_id>\d+)$', groups.item),  # 그룹 조회, 그룹 수정, 그룹 삭제
    url(r'^groups/(?P<group_id>\d+)/users/(?P<user_id>\d+)$', groups.remove_user),  # 그룹 사용자 삭제
    url(r'^users$', users.index),  # 회원가입
    url(r'^users/login$', users.login),  # 로그인
    url(r'^users/me$', users.me),  # 회원정보 조회, 회원정보 수정
]
