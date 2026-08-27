# 용산구 통·반 경계 지도

용산구 16개 동의 통(統)/반(班) 행정 경계를 지도에서 보고, 편집하고, 필지(지번) 단위로 배정할 수 있는 도구입니다.
서버 없이 동작하는 정적 HTML 파일 두 개로 구성됩니다.

- `index.html` — 조회용 뷰어. 통/반 경계, 통장/반장 이름을 지도와 목록에서 확인합니다.
- `editor.html` — 편집기. 통/반 경계를 직접 그리거나, 필지(지번) 단위로 특정 통/반에 편입시킬 수 있습니다.

두 파일 모두 접속 시 비밀번호를 입력해야 열립니다. (자세한 내용은 아래 "접속 비밀번호" 참고)

## GitHub Pages로 배포하기

1. 이 저장소를 GitHub에 올립니다 (아래 "이 저장소를 처음 올릴 때" 참고).
2. GitHub 저장소 페이지에서 **Settings → Pages**로 이동합니다.
3. **Source**를 `Deploy from a branch`로, **Branch**를 `main` / `/ (root)`로 설정하고 저장합니다.
4. 잠시 후 `https://<사용자이름>.github.io/<저장소이름>/` 주소에서 뷰어(`index.html`)가,
   `https://<사용자이름>.github.io/<저장소이름>/editor.html` 주소에서 편집기가 열립니다.

### ⚠️ 꼭 해야 하는 설정: 카카오맵 앱키에 도메인 등록

지도가 [카카오맵 JS SDK](https://apis.map.kakao.com/)를 쓰기 때문에, 배포한 도메인을
카카오 디벨로퍼스 콘솔에 등록하지 않으면 지도가 뜨지 않습니다.

1. [카카오 디벨로퍼스](https://developers.kakao.com/) 로그인 → 내 애플리케이션 → 해당 앱 선택
2. **앱 설정 → 플랫폼 → Web** 에 사이트 도메인 추가
3. `https://<사용자이름>.github.io` 를 등록 (GitHub Pages 커스텀 도메인을 쓴다면 그 도메인도 추가)

지금 파일에 들어있는 앱키는 원래 만들어 두신 카카오 앱키입니다. 다른 앱키로 바꾸려면
`build.py`의 `KAKAO_KEY` 값을 바꾸고 `python3 build.py`를 다시 실행하세요.

## 접속 비밀번호

정적 HTML 파일이라 파일 자체에 진짜 보안을 걸 수는 없습니다 (소스를 열어보면 내용이 다 보입니다).
그래도 링크를 우연히 아는 외부인이 바로 내용을 못 보도록, 두 파일 모두 열자마자 비밀번호를
입력해야 지도가 나오게 해뒀습니다. 비밀번호는 브라우저 세션에 저장되므로 같은 탭에서는
새로고침해도 다시 묻지 않습니다.

**회사 사람만 접속 가능하게** 하려면 이 비밀번호 화면만으로는 부족합니다 (진짜 접근 차단이
아니라 최소한의 문턱일 뿐입니다). 더 확실하게 막으려면 GitHub Pages 앞단에
[Cloudflare Access](https://developers.cloudflare.com/cloudflare-one/policies/access/)
같은 서비스를 무료로 연결해서, 회사 이메일 계정으로 로그인해야만 접속되게 하는 걸 추천합니다.

비밀번호를 바꾸고 싶으면 `src/editor_template.html`과 `src/viewer_template.html`에서
`PW_HASH` 값을 새 비밀번호의 SHA-256 해시로 바꾸고 `python3 build.py`를 다시 실행하세요.

```bash
python3 -c "import hashlib; print(hashlib.sha256('새비밀번호'.encode()).hexdigest())"
```

## 데이터를 수정하고 다시 빌드하기

`index.html`과 `editor.html`은 손으로 직접 고치는 파일이 아니라, `src/` 안의 템플릿과
데이터로부터 **자동 생성되는 결과물**입니다. 내용을 고치려면:

1. `src/editor_template.html` 또는 `src/viewer_template.html`(화면/기능 코드),
   혹은 `src/*.json`(통/반/필지 데이터)을 수정합니다.
2. 저장소 루트에서 빌드를 다시 돌립니다.

```bash
python3 build.py
```

3. 다시 생성된 `index.html` / `editor.html`을 커밋 + 푸시하면 GitHub Pages에 자동 반영됩니다.

### 폴더 구조

```
yongsan-tong-map/
├── index.html              뷰어 (빌드 결과물, GitHub Pages 진입점)
├── editor.html              편집기 (빌드 결과물)
├── build.py                 위 두 파일을 만드는 빌드 스크립트
├── README.md
└── src/
    ├── viewer_template.html   뷰어 원본 템플릿
    ├── editor_template.html   편집기 원본 템플릿
    ├── all_dong_boundaries.json   용산구 16개 동 외곽선 (뷰어·편집기 공통, 유일한 기준)
    ├── hannam_tong.json           한남동 통/반 경계 + 통장/반장 이름
    ├── parcels_by_dong.json       16개 동 전체 필지(지번) 데이터 (14MB, 지번 편입 기능용)
    └── vendor/
        └── turf.min.js            지오메트리 연산 라이브러리 (turf.js, 편집기 전용)
```

## 이 저장소를 처음 올릴 때

```bash
cd yongsan-tong-map
git init
git add .
git commit -m "용산구 통반 경계 지도 초기 배포"
git branch -M main
git remote add origin https://github.com/<사용자이름>/<저장소이름>.git
git push -u origin main
```

`src/parcels_by_dong.json`이 약 14MB라 저장소 전체 용량이 조금 크지만(약 15MB 안팎),
GitHub 파일 하나당 제한(100MB)보다 훨씬 작아서 별도 설정(Git LFS 등) 없이 그냥 올리면 됩니다.

## 알려진 제한사항

- 남영동, 보광동, 원효로2동, 이촌1동, 한강로동, 효창동 6개 동은 아직 정밀 경계가 아니라
  기존의 단순화된(점 25~100개 수준) 경계선을 쓰고 있습니다. 지적 필지를 합쳐서 다시
  계산해봤을 때 기존 대비 면적 차이가 커서(-25%~+57%), 정확도를 확신할 수 없어 임시로
  기존 경계를 유지했습니다. 국가공간정보포털/브이월드에서 정확한 행정동 경계 파일을
  구해서 `src/all_dong_boundaries.json`을 교체하는 게 가장 확실합니다.
- 통/반/필지 데이터는 한남동만 실제 값이 채워져 있고, 나머지 15개 동은 통/반 경계가
  비어있는 상태로 시작합니다 (기본 외곽선과 필지 데이터는 16개 동 모두 있음).
