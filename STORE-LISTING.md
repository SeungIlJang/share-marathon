# 모두의 마라톤 — Play 스토어 등록 자료

- 패키지명: `com.moduseries.marathon` · 퍼블리셔: 모두의시리즈 · 카테고리: **게임 > 캐주얼** (또는 음악)
- 버전: versionCode **4** / versionName **3.2** · targetSdk **36** · minSdk 24 · Capacitor 8
- AAB: `android/app/build/outputs/bundle/release/app-release.aab` (아래 "릴리스 빌드"로 서명 후 생성)
- 업로드 키: `C:\dev\keystores\marathon-upload.jks` (alias `marathon`) — ⚠️ **repo에 커밋 금지, 반드시 백업**(분실 시 업데이트 불가 → Play 지원팀에 키 재설정 요청 필요)
- 개인정보처리방침 URL: `https://seungiljang.github.io/games/marathon-privacy.html`
- 스토어 이미지: `store-assets/icon-512.png` · `store-assets/feature-1024x500.png` · 스크린샷 `store-assets/shot-*.png`(1080×1920, 5장)
- 이미지 재생성: `python tools/make_brand_assets.py`(아이콘·스플래시·피처) / 스크린샷은 `tools/shot.html` + 헤드리스 Chrome
- 빌드 구조: OTA형 — 앱이 `seungiljang.github.io/games/marathon.html`을 불러오고, 오프라인이면 앱에 내장된 `www/game.html`로 실행. **게임 수정은 games 레포 푸시로 즉시 반영**(앱 재업로드 불필요)

---

## 🇰🇷 한국어

### 앱 이름 (최대 30자)
모두의 마라톤

### 간단한 설명 (최대 80자)
음악 비트에 맞춰 달리는 리듬 런, 10명과 겨루는 전략 레이스! 42.195km를 완주하라 🏃

### 자세한 설명 (최대 4000자)
◆ 모두의 마라톤 ◆
비트에 맞춰 발을 구르고, 라이벌을 제치고, 결승 테이프를 끊어라!
두 가지 방식으로 즐기는 캐주얼 마라톤 게임입니다.

🎵 리듬 런
음악에 맞춰 왼발·오른발을 탭하는 리듬 게임!
· 왼발(L)·오른발(R) 노트, 길게 눌러 오르는 ⛰️ 업힐 홀드, 양쪽 동시에 🦘 점프, 💧 급수 노트
· PERFECT·GREAT 판정과 콤보 — 30콤보부터 FEVER 점수 2배
· 워밍업 5K부터 풀코스 피날레까지 5곡, S~F 랭크와 별 수집
· 싱크 보정·노트 속도 설정으로 내 손에 딱 맞게

🏁 레이스
10명의 러너가 함께 달리는 90초 전략 마라톤!
· 꾹 눌러 가속, 손을 떼면 회복 — 체력 관리가 승부
· 앞사람 뒤에 붙는 🌀 드래프팅, 빠져나오며 🚀 슬링샷
· 업힐·다운힐, 비·맞바람·폭염 날씨, 급수대와 파워젤
· 35km 마의 벽, 근육 경련, 3:30 페이서 풍선까지 진짜 마라톤처럼
· 서울에서 시작해 도쿄·베를린·시카고·런던·보스턴·뉴욕 — 월드 메이저 정복, 식스스타 피니셔
· 내 최고기록 👻 고스트와 경쟁, 매일 바뀌는 🗓️ 오늘의 레이스

🏅 함께 즐기는 성장
· 업적 20개, 훈련으로 능력치 강화, 유니폼 꾸미기
· 구간 페이스 그래프와 공유용 📜 완주 기록증

■ 이런 분께 추천해요
· 짧게 한 판씩 즐기는 리듬 게임을 좋아하는 분
· 마라톤·러닝을 좋아하거나 서브4·서브3를 꿈꾸는 러너
· 광고 없이 깔끔하게 즐기고 싶은 분

※ 광고·결제·개인정보 수집이 없습니다. 게임 기록은 기기에만 저장돼요.

---

## 🇺🇸 English (선택)

### Title
Everyone's Marathon

### Short description
Tap to the beat in Rhythm Run, outsmart 9 rivals in Race mode — finish 42.195km!

### Full description
Two ways to run a marathon:
🎵 Rhythm Run — tap left/right feet to the music, hold through uphills, jump with both thumbs, grab water notes. 5 songs, S–F ranks, FEVER combos.
🏁 Race — a 90-second tactical marathon against 9 rivals. Hold to sprint, release to recover, draft and slingshot past runners, survive hills, rain, headwind and heat, and conquer the six World Marathon Majors.
Achievements, training upgrades, outfits, PB ghost and a shareable finisher certificate. No ads, no purchases, no data collection.

---

## Play Console 입력 가이드

| 항목 | 입력값 |
|---|---|
| 앱/게임 | 게임 · 무료 |
| 광고 포함 | **아니요** |
| 콘텐츠 등급 설문 | 폭력·선정성·도박·사용자 간 소통·위치 공유 모두 "아니요" → 전체이용가 예상 |
| 타겟층 | **13세 이상** 권장 (13세 미만 포함 시 '가족 정책' 추가 심사 대상) |
| 데이터 보안 | 데이터 수집 **없음** · 데이터 공유 **없음** (진행도는 기기에만 저장, 서버 전송 없음) |
| 개인정보처리방침 | `https://seungiljang.github.io/games/marathon-privacy.html` |
| 앱 액세스 | 모든 기능 제한 없음(로그인 없음) |
| 정부 앱 / 금융 / 건강 | 해당 없음 |

---

## 릴리스 빌드 (업로드 키 생성 후)

1. 업로드 키 만들기(최초 1회, 비밀번호는 직접 입력·보관)
2. `android/keystore.properties.example` → `android/keystore.properties`로 복사 후 비밀번호 입력 (git 제외됨)
3. 서명된 AAB 빌드:
   - `cd android` → `JAVA_HOME`을 JDK 21로 설정 → `./gradlew bundleRelease`
   - 결과: `android/app/build/outputs/bundle/release/app-release.aab`
4. Play Console → 테스트(내부/비공개) 트랙에 업로드 → Play 앱 서명 사용(권장)

## 출시 전 체크리스트

- [ ] **실제 폰 테스트**: 설치 → 첫 실행 OTA 로딩, 리듬 소리·싱크, 뒤로가기, 노치/제스처바 화면 가림, 기록증 공유
- [ ] games 레포에 최신 게임(v3.2: 뒤로가기·안전영역 포함)과 `marathon-privacy.html` 배포
- [ ] 업로드 키 생성·백업 → 서명된 AAB 빌드
- [ ] 신규 개인 개발자 계정이면 **비공개 테스트 12명 이상 · 14일 연속** 후 프로덕션 신청 가능
- [ ] 스토어 등록정보: 아이콘 512 · 피처 그래픽 · 스크린샷(최소 2장) · 설명 입력
