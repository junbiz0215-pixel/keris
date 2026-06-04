# 보육현황 대시보드 — 데이터로 읽는 우리 교육 제6호

유치원 · 어린이집 2탭 구조의 인터랙티브 보육현황 대시보드입니다.
**Streamlit + Plotly + 카카오지도 API** 기반으로 구현되었습니다.

- **유치원 탭**: 제6호 보고서 기반 가상 데이터 (공립/사립)
- **어린이집 탭**: 2025년 12월말 기준 보육통계 Raw Data (실제 데이터, 17개 시도)

---

## 1. 로컬 실행

```bash
# 1) 패키지 설치
pip install -r requirements.txt

# 2) 실행 (기본 포트 8501)
streamlit run dashboard.py
```

브라우저에서 `http://localhost:8501` 접속.

---

## 2. 카카오지도 설정

지도는 카카오 JavaScript API 키가 필요합니다.

1. [developers.kakao.com](https://developers.kakao.com) → 앱 생성
2. **앱 설정 → 플랫폼 → Web → 사이트 도메인** 등록
   ```
   http://localhost:8501
   http://127.0.0.1:8501
   ```
   (클라우드 배포 시 `https://<앱이름>.streamlit.app` 추가 등록)
3. **앱 설정 → 앱 키 → JavaScript 키** 복사
4. 사이드바 하단 **🗺 카카오지도 API** 입력란에 붙여넣기

> 키 미입력 시에도 지도 외 모든 차트는 정상 작동합니다.

### 키 자동 입력 (선택)
`.streamlit/secrets.toml.example` → `.streamlit/secrets.toml` 로 복사 후 키 입력하면
사이드바에 자동으로 채워집니다.

---

## 3. Streamlit Community Cloud 배포

가장 간편한 무료 배포 방법입니다 (고정 HTTPS 주소 제공).

### 3-1. GitHub 저장소 준비
```bash
git init
git add dashboard.py requirements.txt kinder_data.csv \
        "812451774932644958_붙임 4. 2025년 12월말 기준 보육통계 Raw Data(수정).xlsx" \
        .streamlit/config.toml .gitignore README.md
git commit -m "보육현황 대시보드 초기 배포"
git branch -M main
git remote add origin https://github.com/<사용자명>/<저장소명>.git
git push -u origin main
```

### 3-2. 배포
1. [share.streamlit.io](https://share.streamlit.io) 접속 → GitHub 로그인
2. **New app** → 저장소 / 브랜치(`main`) / 메인 파일(`dashboard.py`) 선택
3. **Advanced settings → Secrets** 에 아래 입력 (지도 자동 표시용, 선택):
   ```toml
   KAKAO_API_KEY = "발급받은_JavaScript_키"
   ```
4. **Deploy** 클릭

### 3-3. 배포 후 카카오 도메인 등록
배포되면 `https://<앱이름>.streamlit.app` 주소가 생성됩니다.
이 주소를 카카오 **사이트 도메인**에 추가 등록해야 지도가 표시됩니다.

---

## 4. 파일 구성

| 파일 | 설명 |
|---|---|
| `dashboard.py` | 메인 대시보드 (유치원/어린이집 2탭) |
| `kinder_data.csv` | 유치원 데이터 (공립/사립) |
| `812451774932644958_붙임 4...xlsx` | 어린이집 보육통계 원본 (2025.12) |
| `requirements.txt` | 의존 패키지 |
| `.streamlit/config.toml` | 라이트 테마 설정 |
| `.streamlit/secrets.toml` | 카카오 키 (gitignore됨) |

---

## 5. 주요 기능

- **공통 시도 필터** — 양쪽 탭 동시 적용
- **카카오지도 버블맵** — 학교 모양 SVG 핀, 충족률 90%↑ 시 황색 경고
- **Plotly 차트** — 이중 도넛, 누적 막대, 수평 막대, 방사형 레이더
- **AI 인사이트** — 실시간 집계 수치 바인딩 + 스트리밍 연출
- **CSV 다운로드** — 필터링된 데이터 내보내기
