# 모두의 마라톤 — 아트 제작 프롬프트 (Codex 전달용)

이 문서는 이미지 생성 담당(Codex)에게 넘기는 작업 지시서입니다.
생성만 해 주시면 게임 통합·검증은 Claude 세션에서 합니다.

## 0. 공통 규칙

- **저장 위치:** `D:/AI/workspace/game/images/marathon/` (없으면 생성). 파일명은 아래 표의 영어 이름 그대로.
- **형식:** PNG, 투명 배경(배경 띠 제외), 글자·워터마크·그림자 없음.
- **우선순위:** ① 러너 시트 → ② 도시 배경 → ③ 아이템·소품 → ④ 스토어 이미지. ①만 먼저 와도 통합을 시작합니다.
- **모든 프롬프트 앞에 아래 공통 스타일을 붙입니다.**

```
Cute chibi 2D game art, thick clean dark-brown outlines, flat cel shading with soft highlights, bright saturated colors, big head (about 45% of body height), friendly smiling face, mobile casual game style. Transparent background, no text, no watermark, no drop shadow.
```

- **스타일 기준:** 현재 게임의 러너 `share-marathon/runner-sprite.png`(14프레임, 빨간 머리띠·흰 셔츠·빨간 소매·검은 반바지·빨간 신발)와 같은 그림체여야 합니다. 가능하면 이 파일을 참고 이미지로 넣어 주세요.

---

## 1. 러너 스프라이트 시트 — 체형 5종 (최우선)

지금은 러너 21명이 그림 한 장을 늘여서 쓰고 있습니다. 체형별 시트 5장으로 바꿉니다.

### 규격 (반드시 지킬 것)

| 항목 | 값 |
|---|---|
| 전체 크기 | **3458 × 309 px** (가로 한 줄) |
| 프레임 | **14칸**, 칸마다 **247 × 309 px** |
| 방향 | 옆모습, **오른쪽을 보고 달림** |
| 동작 | 끊김 없이 이어지는 달리기 한 사이클(14번째 다음이 1번째로 자연스럽게 이어짐) |
| 발 위치 | 모든 칸에서 지면선이 같음 — 발바닥 최저점이 칸 아래에서 약 **8px** 위 |
| 정렬 | 캐릭터 몸통 중심이 칸의 가로 중앙 |
| 여백 | 머리띠 리본·팔다리가 칸 밖으로 잘리지 않게, 칸 사이 번짐 없음 |

### 색 규칙 (게임이 색을 바꿔 쓰므로 매우 중요)

- **순수한 빨강(#E8302A 안팎)은 머리띠·셔츠 소매·신발 세 군데에만** 씁니다.
- 피부·머리카락·입·볼터치 등 다른 곳에는 빨강 계열(색상 340°~18°, 채도 높은 색)을 쓰지 않습니다. 볼터치는 연한 분홍 대신 살구색으로.
- 게임이 이 빨간 부분만 러너별 색(파랑·초록·보라 등)으로 바꿉니다.

### 프롬프트

```
Sprite sheet of a marathon runner, side view facing right, 14-frame seamless running cycle in one horizontal strip, each frame exactly 247x309 px (total 3458x309), feet touching the same baseline in every frame, character centered in each cell, nothing cropped at cell edges. Outfit: red headband with two flying ribbon tails, white T-shirt with RED sleeves, black shorts, white socks, RED running shoes with white soles. Use pure saturated red (#E8302A range) ONLY for the headband, sleeves and shoes, and nowhere else on the character. Body type: {BODY}.
```

| 파일명 | `{BODY}` 에 넣을 문구 |
|---|---|
| `runner-slim.png` | `slim and tall elite runner with long legs and lean arms` |
| `runner-chubby.png` | `chubby round runner with a big belly and short legs, cheerful` |
| `runner-short.png` | `very short small runner with tiny legs, energetic` |
| `runner-muscle.png` | `muscular stocky runner with broad shoulders and thick arms` |
| `runner-granny.png` | `elderly grandmother runner, small, gray hair in a bun, gentle smile` |

### 납품 전 자체 확인

- [ ] 크기가 정확히 3458×309인가
- [ ] 14칸을 순서대로 돌렸을 때 달리기가 자연스럽게 반복되는가
- [ ] 모든 칸에서 발 높이가 같은가(캐릭터가 위아래로 튀지 않는가)
- [ ] 빨강이 머리띠·소매·신발에만 있는가
- [ ] 배경이 완전히 투명한가(흰색·체커 무늬가 남지 않았는가)

---

## 2. 도시 배경 — 코스 8종

지금은 색만 다른 사각형 빌딩입니다. 도시마다 알아볼 수 있는 풍경으로 바꿉니다.

### 규격

| 항목 | 값 |
|---|---|
| 크기 | **2048 × 512 px** |
| 이음매 | **좌우가 끊김 없이 이어짐**(가로로 반복해서 깔림) |
| 구성 | 위쪽 하늘은 **투명**(게임이 하늘색·날씨를 그림), 건물·산은 아래쪽에 실루엣+간단한 디테일 |
| 아래 20% | 도로가 겹치므로 단순하게(잔디·낮은 담 정도) |
| 색 | 파스텔, 멀리 있는 느낌의 옅은 안개 |

### 프롬프트

```
Seamless horizontally tileable city skyline strip for a side-scrolling running game, 2048x512 px, transparent sky, flat pastel colors, soft atmospheric haze, recognizable landmarks in silhouette with a few simple details, bottom 20% plain and low so a road can overlap it, left and right edges match perfectly when tiled. City: {CITY}.
```

| 파일명 | `{CITY}` 에 넣을 문구 |
|---|---|
| `bg-seoul.png` | `Seoul — N Seoul Tower on Namsan hill, Han River bridges, Lotte World Tower` |
| `bg-chuncheon.png` | `Chuncheon — calm lake, layered green mountains, a small bridge, countryside` |
| `bg-tokyo.png` | `Tokyo — Tokyo Tower, Tokyo Skytree, dense mid-rise buildings` |
| `bg-berlin.png` | `Berlin — Brandenburg Gate, Fernsehturm TV tower, linden trees` |
| `bg-chicago.png` | `Chicago — Willis Tower, lakefront skyscraper skyline` |
| `bg-london.png` | `London — Big Ben, Tower Bridge, London Eye` |
| `bg-boston.png` | `Boston — red brick townhouses, a church steeple, rolling hills` |
| `bg-nyc.png` | `New York — suspension bridge, Manhattan skyline, Central Park trees` |

---

## 3. 아이템·소품

지금은 이모지(🥤⚡📣)라서 기기마다 모양이 다릅니다.

### 3-1. 아이템 아이콘 (낱개 8장, 각 256×256)

```
Single game item icon, 256x256 px, 3/4 top-down view, centered, consistent soft top-left lighting: {ITEM}.
```

| 파일명 | `{ITEM}` |
|---|---|
| `item-water.png` | `paper water cup with a small splash` |
| `item-gel.png` | `orange energy gel packet with a lightning mark` |
| `item-sponge.png` | `wet yellow sponge dripping water` |
| `item-cheer.png` | `orange megaphone with sound waves` |
| `item-highfive.png` | `open hand reaching out for a high-five` |
| `item-barricade.png` | `yellow and black striped road barricade on two legs with red warning lights` |
| `item-puddle.png` | `dark blue rain puddle with ripples, seen from above at an angle` |
| `item-finishflag.png` | `black and white checkered finish flag` |

### 3-2. 급수대 (`aid-station.png`, 600×200)

```
Marathon aid station, side view, 600x200 px: long folding table with blue cloth, rows of paper cups, two volunteers in yellow vests holding cups out toward the road, a blue banner above the table left completely blank.
```

### 3-3. 관중 띠 (`crowd-a.png`, `crowd-b.png`, `crowd-c.png`, 각 1024×160)

같은 사람들의 팔 동작만 다른 3장(번갈아 보여 응원 애니메이션으로 씁니다).

```
Cheering marathon crowd strip, seamless horizontally tileable, 1024x160 px, side view standing behind a low barrier: diverse spectators waving small flags, clapping, holding blank signs. Pose variation {N} of 3 — same people and positions, only arm poses differ.
```

### 3-4. 결승 아치 (`finish-arch.png`, 400×420)

```
Marathon finish arch, front-side view, 400x420 px: red inflatable arch with a completely blank banner, a blank digital clock on top, colorful balloons on both pillars, checkered tape stretched across the road.
```

---

## 4. 스토어 이미지

### 4-1. 피처 그래픽 (`feature-1024x500.png`, 1024×500, 불투명)

```
Mobile game key art, 1024x500 px, opaque: a chibi runner with a red headband breaking the finish tape with arms raised, confetti in the air, many colorful rival runners of clearly different body shapes close behind, city skyline at golden hour, dynamic low camera angle. Keep the right 40% calmer and less detailed so a title can be placed there. No text.
```

### 4-2. 앱 아이콘 (`icon-512.png`, 512×512, 불투명)

```
Mobile game app icon, 512x512 px, opaque, full-bleed: close-up of a chibi runner with a red headband running to the right, speed lines, bright sky-blue background with a small sun, bold and readable at small sizes. No text, no rounded-corner mask.
```

---

## 5. 통합 메모 (Claude 세션용)

- 러너 시트는 현재 `runner-sprite.png`와 같은 규격이라, `BODIES`의 늘이기 방식을 걷어내고 러너별로 시트를 배정하면 됩니다. 색 변경은 `uniformTint()`가 빨강 계열만 바꿉니다.
- 배경은 `render()`의 빌딩 그리는 부분(`SKY` 배열)을 이미지 타일로 교체합니다. 호수 코스의 물 띠는 배경 이미지에 포함되면 제거합니다.
- OTA 로더가 `document.write`로 게임을 주입하므로 **상대 경로 이미지는 앱에서 깨질 수 있습니다.** 지금처럼 data URI로 내장하거나 절대 URL을 써야 합니다. 내장 시 파일 크기가 커지므로 시트는 가능한 한 가볍게(색 수 줄인 PNG) 받습니다.
