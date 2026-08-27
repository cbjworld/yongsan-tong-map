#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
용산구 통/반 경계 뷰어·에디터 빌드 스크립트.

src/ 안의 템플릿(*_template.html)과 데이터(JSON)를 하나로 합쳐서
저장소 루트에 index.html(뷰어), editor.html(편집기)를 만듭니다.

사용법:
    python3 build.py

카카오맵 앱키를 바꾸고 싶으면 아래 KAKAO_KEY 값을 바꾸세요.
(카카오 디벨로퍼스 콘솔에서 이 앱키에 배포할 도메인을 "플랫폼 > Web"에
반드시 등록해야 지도가 뜹니다. README.md 참고.)

GH_OWNER/GH_REPO 를 채워두면, 뷰어(index.html)가 열릴 때마다 이 저장소의
GH_TONG_PATH_PATTERN 경로에서 최신 통/반 데이터를 직접 받아옵니다 (편집기의
"깃허브에 저장" 기능과 짝을 이룸). 비워두면 이 기능은 그냥 꺼지고 내장된
기본 데이터만 씁니다.

GH_TOKEN 을 채우면 그 값이 editor.html 안에 그대로 내장돼서, 어느 컴퓨터에서 열어도
비밀번호만 입력하면 편집기의 "깃허브에서 불러오기/저장" 이 바로 됩니다. 그 대신 이
토큰은 editor.html 을 보는 누구나 볼 수 있는 상태가 됩니다 — 그래서 반드시 "이 저장소
Contents(Read and write)"로만 좁힌 fine-grained 토큰을 쓰고, 다른 권한은 절대 주지
마세요. 유출됐다고 판단되면 깃허브에서 그 토큰을 바로 폐기(revoke)하고 새로 만들어서
여기 값을 바꾼 뒤 다시 빌드하면 됩니다.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, 'src')

KAKAO_KEY = 'd42eb2a3ed96b83cec2ba9aeaadfb84f'

GH_OWNER = ''  # 예: 'myuser' (본인 깃허브 사용자명/조직명으로 채우세요)
GH_REPO = 'yongsan-tong-map'
GH_BRANCH = 'main'
GH_TONG_PATH_PATTERN = 'data/{dong}_tong.json'
GH_TOKEN = ''  # fine-grained 토큰 (이 저장소, Contents: Read and write 권한만). editor.html 에 그대로 노출됨 — 위 설명 참고.


def read(relpath):
    with open(os.path.join(SRC_DIR, relpath), encoding='utf-8') as f:
        return f.read()


def write(relpath, content):
    path = os.path.join(BASE_DIR, relpath)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('wrote', relpath, '(%d bytes)' % len(content))


def build_editor():
    tpl = read('editor_template.html')
    turf_js = read('vendor/turf.min.js')
    all_dong = read('all_dong_boundaries.json')
    parcels = read('parcels_by_dong.json')

    out = tpl.replace('/* __TURF_JS__ */', turf_js)
    out = out.replace('__KAKAO_KEY__', KAKAO_KEY)
    out = out.replace('/* __ALL_DONG_BOUNDARIES__ */', all_dong)
    out = out.replace('/* __PARCELS_BY_DONG__ */', parcels)
    out = out.replace('__GH_OWNER__', GH_OWNER)
    out = out.replace('__GH_REPO__', GH_REPO)
    out = out.replace('__GH_BRANCH__', GH_BRANCH)
    out = out.replace('__GH_TONG_PATH_PATTERN__', GH_TONG_PATH_PATTERN)
    out = out.replace('__GH_TOKEN__', GH_TOKEN)
    write('editor.html', out)


def build_viewer():
    tpl = read('viewer_template.html')
    tong_data = read('hannam_tong.json')
    all_dong = read('all_dong_boundaries.json')

    out = tpl.replace('__KAKAO_KEY__', KAKAO_KEY)
    out = out.replace('/* __TONG_DATA__ */', tong_data)
    out = out.replace('/* __ALL_DONG_BOUNDARIES__ */', all_dong)
    out = out.replace('__GH_OWNER__', GH_OWNER)
    out = out.replace('__GH_REPO__', GH_REPO)
    out = out.replace('__GH_BRANCH__', GH_BRANCH)
    out = out.replace('__GH_TONG_PATH_PATTERN__', GH_TONG_PATH_PATTERN)
    write('index.html', out)


if __name__ == '__main__':
    build_editor()
    build_viewer()
    print('done. index.html(뷰어) / editor.html(편집기) 가 갱신되었습니다.')
