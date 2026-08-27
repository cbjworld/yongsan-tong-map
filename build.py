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
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, 'src')

KAKAO_KEY = 'd42eb2a3ed96b83cec2ba9aeaadfb84f'


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
    write('editor.html', out)


def build_viewer():
    tpl = read('viewer_template.html')
    tong_data = read('hannam_tong.json')
    all_dong = read('all_dong_boundaries.json')

    out = tpl.replace('__KAKAO_KEY__', KAKAO_KEY)
    out = out.replace('/* __TONG_DATA__ */', tong_data)
    out = out.replace('/* __ALL_DONG_BOUNDARIES__ */', all_dong)
    write('index.html', out)


if __name__ == '__main__':
    build_editor()
    build_viewer()
    print('done. index.html(뷰어) / editor.html(편집기) 가 갱신되었습니다.')
