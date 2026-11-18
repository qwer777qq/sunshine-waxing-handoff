# 사진 중심 릴스·쇼츠 템플릿

2026-11-16 승인한 클린 베이지 시안을 영상에 적용한 새 템플릿입니다. 과거 주황 v2와 별도로 보관합니다.
무료 로컬 Python + FFmpeg로 실행합니다. API 호출, 유료 TTS 생성, SNS 업로드는 하지 않습니다.

## 5가지 기본형

|설정|쓰임|사진·영상 영역|
|---|---|---|
|`presets/01-fullscreen.json`|추천. 왼쪽 위 두 줄 제목|전체 화면, 제목은 2.8초 뒤 사라짐|
|`presets/02-top-strip.json`|제목과 시술 장면 분리|상단 제목 공간 420px, 시술 화면 1500px|
|`presets/03-minimal.json`|시술만 크게 보여주기|전체 화면, 시작 로고만 2초|
|`presets/04-maternity.json`|임산부 사진 전용|원본 전체를 보존하는 contain 배치|
|`presets/06-before-after.json`|실제 전후 비교|상하 사진이 9:16 화면의 약 86% 차지|

모두 1080×1920, 30fps, MP4(H.264/AAC), 영상 기본 1.2배속입니다. 12초 출력에는 원본 14.4초가 필요합니다. 일반형은 한 파일의 한 구간, 전후형은 실제 사진 두 장을 입력합니다. 다중 클립 편집기는 아닙니다.

## 비포·애프터 사진 강조형

```powershell
python templates/photo-first-v1/render_pair.py --output outputs/before-after-01
```

포함된 업체 원본에서 위 Before와 아래 After를 분리해 순서를 유지합니다. 피부·털은 보정하지 않습니다. 상하 사진 중심 크롭을 쓰며 큰 글상자나 가운데 대형 로고가 시술 부위를 가리지 않게 했습니다. 현재 샘플은 공개된 560px 사진 기반이므로 고화질 고객 원본으로 교체하면 더 선명해집니다.

새 고객 사진은 같은 고객·부위인 것을 확인한 뒤:

```powershell
python templates/photo-first-v1/render_pair.py --before "D:/고객소재/before.jpg" --after "D:/고객소재/after.jpg" --output outputs/before-after-02
```

`06-before-after.json`을 복사해 제목, pair_evidence, before_center/after_center를 해당 사진에 맞게 바꿉니다. `pair_verified`는 실제 확인 후에만 true로 지정합니다. `fit: contain`은 원본 전체를 보존하고, `fit: cover`는 사진 영역을 꽉 채웁니다. 먼저 `--cover-only`로 중요한 변화가 잘리지 않는지 확인합니다.

`comparison-story.png`, `comparison-portrait.png`, `comparison-square.png`와 `video/shorts.mp4`가 생성됩니다. 전후형 영상은 두 사진을 동시에 크게 보여주는 9초 비교형입니다.

## 처음 실행

Python 3와 FFmpeg/ffprobe를 PATH에 준비합니다. FFmpeg는 libass·zscale·tonemap 지원 빌드를 사용합니다. 저장소 루트에서:

```powershell
python -m pip install -r templates/photo-first-v1/requirements.txt
python templates/photo-first-v1/render.py --config templates/photo-first-v1/presets/05-photo-demo.json --output outputs/photo-demo-01
```

이 명령은 포함된 실제 뒷목 사진으로 8초 디자인 데모를 만듭니다. 시술 동영상이나 여성 TTS가 들어간 게시 완성본으로 표현하지 않습니다.

## 내 시술 영상으로 만들기

`templates/photo-first-v1/media/input.mp4`에 영상을 넣고 실행합니다. 결과 폴더는 매번 새로운 이름을 사용합니다.

```powershell
python templates/photo-first-v1/render.py --config templates/photo-first-v1/presets/01-fullscreen.json --output outputs/reels-01
```

다른 위치의 파일과 원하는 구간을 직접 지정할 수도 있습니다.

```powershell
python templates/photo-first-v1/render.py --config templates/photo-first-v1/presets/01-fullscreen.json --input "D:/고객소재/다리시술.mov" --start 52 --duration 12 --output outputs/reels-02
```

가로 영상의 특정 부위를 잡으려면 `--crop x,y,너비,높이`를 추가합니다. 좌표는 회전 메타데이터 적용 후 화면 기준입니다. 기존 샘플의 `700,40,540,960`은 그 다리 원본에만 맞으므로 새 영상에 그대로 적용하지 않습니다. HDR HLG/PQ는 SDR BT.709로 변환하며 피부·털 보정은 하지 않습니다.

## 바꾸는 값

- `title`: 최대 두 줄. 화면에 맞게 줄이고, 의미 없는 긴 설명은 넣지 않습니다.
- `input`: 설정 JSON 기준 상대 경로 또는 절대 경로.
- `media_type`: `video` 또는 `image`. 사진은 EXIF 회전을 반영합니다.
- `start`: 원본 시작 초. `duration`: 최종 출력 길이. `speed`: 영상 배속.
- `fit`: 화면을 채우는 `cover`, 원본 전체를 보존하는 `contain`.
- `crop`: `[x,y,너비,높이]` 또는 `null`.
- `hook_duration`: 제목을 보여주는 시간. 로고는 항상 첫 2초입니다.
- `captions`: 최종 출력 시간 기준의 `start`, `end`, `text`, 선택 `highlight`.
- `voice`: 승인된 여성 음성 파일 경로. 없으면 디자인 데모용 무음 AAC 트랙을 만듭니다. 원본의 사적 대화는 자동으로 가져오지 않습니다.
- `voice_speed`: 기본 1.2. 이미 배속된 음성이면 1.0. 음성이 영상보다 길면 문장을 자르지 않고 길이 조정을 요청하며 종료합니다.

```json
{"start":3.0,"end":5.5,"text":"실제 뒷목 시술 기록","highlight":"뒷목"}
```

여성 음성 합성:

```powershell
python templates/photo-first-v1/render.py --config templates/photo-first-v1/presets/01-fullscreen.json --voice "D:/승인음성/voice.mp3" --output outputs/reels-with-voice-01
```

대본과 자막 시간을 음성에 맞춰 조정합니다. 템플릿이 실제 음성의 화자·권한·자연스러움까지 판정하지는 않습니다. 승인된 선샤인 여성 음성은 별도 준비하고, 다른 음성이나 새 클론으로 자동 대체하지 않습니다.

## 출력과 재편집

- `shorts.mp4`: 릴스·쇼츠 공용 영상
- `cover.png`: 같은 구도의 별도 9:16 표지
- `title-overlay.png`, `brand-overlay.png`: 투명 PNG 레이어. CapCut/Premiere 등에 올릴 수 있습니다.
- `captions.ass`: 수정 가능한 자막
- `render-settings.local.json`, `probe.json`: 실제 설정과 기술 확인값. 고객 경로가 있어 Git에는 넣지 않습니다.

`--cover-only`를 추가하면 전체 영상을 렌더하지 않고 표지부터 확인합니다. 실제 출력 첫·중간·끝, 시술 부위, 한글 잘림, 음성을 확인한 뒤 게시합니다. 안전 여백은 실무 시작값이며 플랫폼별 현재 UI에서 최종 확인합니다.

임산부 데모는 네이버 플레이스에 공개된 업체의 예비맘 사진을 사용했습니다. Instagram 임산부 게시물 다운로드는 로그인 단계에서 미완료입니다. 사진 속 기존 문구를 유지했으며 주수·효과·의학적 안전성을 새로 단정하지 않습니다.

폰트: Noto Sans KR, SIL OFL 1.1. `fonts/OFL.txt` 동봉. libass 자막은 함께 넣은 600 굵기의 정적 인스턴스를 사용합니다.

## 공통 텍스트 안전 기준

새 출력의 제목·로고·자막은 1080×1920에서 대체로 x=160~880, y=420~1500 안에 놓습니다. 자막이 너무 길거나 두 줄을 넘으면 렌더가 중단됩니다. 플랫폼과 기기에 따라 UI와 크롭이 달라지므로 각 게시 미리보기에서 확인하고, 원본 이미지에 박힌 글자도 별도로 확인하세요.

## 자막 가독성

자막은 Noto Sans KR 88px, 고정된 크림색 바 위에 짙은 글씨와 빨강 핵심어로 표시하며 680px 폭에 맞춰 단어 단위로 최대 두 줄로 나눕니다. 들어가지 않는 문장은 줄이거나 여러 시점으로 나누세요. 실제 모바일과 각 플랫폼 미리보기에서 검수합니다.

스킬5 응용 자막바는 장면별 `caption_bar_y`(420~1160, 기본 850)로 시술 부위를 피해 조정합니다. 자막바는 자막이 없는 시간에는 표시되지 않습니다.
