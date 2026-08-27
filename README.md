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

## 편집기에서 고친 내용이 뷰어에 자동으로 뜨게 하기

기본적으로는 편집기에서 "통 경계 JSON"을 내려받아 뷰어에 수동으로 불러와야 합니다.
그 대신 이 저장소 자체를 데이터 저장소로 써서, **편집기에서 저장하면 뷰어를 새로고침할 때
자동으로 최신 내용이 뜨게** 할 수 있습니다.

### 1. 저장소 쪽 설정 (한 번만)

`build.py` 위쪽의 값을 채우고 `python3 build.py`를 다시 실행하세요.

```python
GH_OWNER = 'myuser'                          # 본인 깃허브 사용자명/조직명
GH_REPO = 'yongsan-tong-map'                 # 이 저장소 이름
GH_BRANCH = 'main'
GH_TONG_PATH_PATTERN = 'data/{dong}_tong.json'
```

이 값이 채워진 채로 빌드된 `index.html`(뷰어)은 열릴 때마다, 그리고 동을 바꾸거나
"최신 데이터 새로고침" 버튼을 누를 때마다 `data/<동이름>_tong.json` 파일을
`raw.githubusercontent.com`에서 직접 받아와 화면에 반영합니다. 저장소에 아직 그 동의
파일이 없으면 조용히 내장된 기본 데이터로 대체합니다.

### 2. 편집기에서 저장 / 불러오기

편집기(`editor.html`)를 열면 "깃허브에 자동 저장" 항목이 있습니다.

- **저장소 소유자 / 이름 / 브랜치 / 경로 / 토큰**: `build.py` 위쪽의 `GH_OWNER` ~
  `GH_TOKEN` 값을 채우고 다시 빌드하면, 이 값들이 `editor.html` 파일 안에 그대로
  내장됩니다. 그러면 **어느 컴퓨터에서 이 파일을 열어도 사이트 비밀번호(`yongsan8668`)
  하나만 입력하면 바로 불러오기·저장이 되고, 이 칸들을 따로 채울 필요가 없습니다.**
  다만 그만큼 이 토큰은 `editor.html`을 보는 사람이라면(=이 저장소에 접근 권한이 있는
  사람이라면) 누구나 볼 수 있는 상태가 됩니다. 그래서 반드시 "이 저장소만, Contents
  (Read and write) 권한만" 있는 fine-grained 토큰을 쓰세요 ([설정 방법](#3-개인-액세스-토큰-만들기)
  참고). 유출이 걱정되면 깃허브에서 그 토큰만 바로 폐기(revoke)하고 새로 만들어서
  `build.py`의 `GH_TOKEN` 값을 바꾼 뒤 다시 빌드하면 됩니다. (굳이 파일에 넣고 싶지
  않다면 `GH_TOKEN`을 비워두고, 편집기 화면에서 그때그때 직접 입력해도 됩니다 — 이
  경우 토큰은 그 브라우저의 localStorage에만 남고 파일에는 남지 않습니다.)
- **깃허브에서 불러오기** 버튼: 지금 이 저장소에 저장돼 있는 최신 데이터를 편집기로
  가져와서 이어서 편집할 수 있습니다.
- **깃허브에 저장** 버튼: 지금 편집기 화면의 통/반 경계를 그대로 저장소의
  `data/<동이름>_tong.json` 파일에 덮어씁니다 (파일이 없으면 새로 만듦).

즉, 실제 작업 흐름은: **편집기에서 "깃허브에서 불러오기" → 수정 → "깃허브에 저장"** 이고,
뷰어는 그 파일이 바뀔 때마다 새로고침만 하면 최신 내용을 보여줍니다.

> raw.githubusercontent.com은 CDN을 거치기 때문에 저장 직후 몇 초~1분 정도는 옛날 내용이
> 잠깐 보일 수 있습니다 (뷰어는 캐시를 우회하는 요청을 보내긴 하지만, 그래도 완전히 즉시는
> 아닐 수 있어요). "완전한 실시간"이 꼭 필요하면 Firebase 같은 실시간 DB로 바꾸는 방법도
> 있습니다.

### 3. 개인 액세스 토큰 만들기

1. GitHub 우측 상단 프로필 → **Settings → Developer settings → Personal access tokens
   → Fine-grained tokens → Generate new token**
2. **Repository access**를 "Only select repositories"로 하고 이 저장소만 선택
3. **Permissions → Repository permissions → Contents**를 "Read and write"로 설정
4. 나머지 권한은 전부 비활성 상태로 두고 토큰 생성 → 편집기의 "개인 액세스 토큰" 칸에 붙여넣기

이렇게 만들면 이 토큰이 새어나가도 이 저장소의 파일 읽기/쓰기 말고는 아무것도 할 수 없습니다.

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
├── data/
│   └── 한남동_tong.json      편집기가 "깃허브에 저장"할 때 갱신하는 실제 데이터 (뷰어가 읽어감)
└── src/
    ├── viewer_template.html   뷰어 원본 템플릿
    ├── editor_template.html   편집기 원본 템플릿
    ├── all_dong_boundaries.json   용산구 16개 동 외곽선 (뷰어·편집기 공통, 유일한 기준)
    ├── hannam_tong.json           한남동 통/반 경계 초기값 (index.html에 내장되는 기본값)
    ├── parcels_by_dong.json       16개 동 전체 필지(지번) 데이터 (14MB, 지번 편입 기능용)
    └── vendor/
        └── turf.min.js            지오메트리 연산 라이브러리 (turf.js, 편집기 전용)
```

`data/`는 `src/`와 달리 빌드에 쓰이는 원본이 아니라, 편집기가 실제로 읽고 쓰는 "살아있는"
데이터입니다. 편집기에서 저장할 때마다 이 폴더 안의 파일이 갱신됩니다.

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
