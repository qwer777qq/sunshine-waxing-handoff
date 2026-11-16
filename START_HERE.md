# 선샤인왁싱 · 다른 PC에서 이어서 작업하기

기록일: 2026-11-16, Asia/Seoul. 이 문서는 현재 결과물과 다음 작업 방법을 묶은 시작 안내입니다. 새 사용자의 지시가 항상 우선합니다.

## 1. 지금 완성된 것

- [고객용 사이트](https://sunshine-waxing-design-collection.alalshow3.chatgpt.site): 쇼츠 5종 재생, 2개 나란히 비교, 영상·썸네일 각각 선택, 선택 내용과 링크 복사. 선택은 브라우저에 저장되며 담당자에게 자동 전송되지는 않습니다.
- [쇼츠 원본 MP4 5종](samples/shorts/README.md): 전체 화면, 제목 띠, 최소 로고, 임산부, 비포애프터. 1080×1920. 사이트용 파일은 가볍게 만든 720×1280 미리보기입니다.
- [새 쇼츠 썸네일 5안](samples/shorts-covers/README.md): 사진 전체형, 상단 제목형, 작은 라벨형, 임산부 전용, 비포애프터형. 1080×1920 PNG·WebP·편집 SVG.
- [기존 승인 디자인](designs/approved-20261116/README.md): 표지·캐러셀·공지 등 24종, 3비율의 PNG 총 72개. 기존 Figma 파일과 신규 사진 중심 SVG 원본 포함.
- [영상 렌더 코드](templates/photo-first-v1/README.md), [썸네일 렌더 코드](templates/shorts-covers-v1/README.md), [설치 가능한 Codex 스킬](INSTALL_SKILL.md).

이번 요청의 납품 위치는 GitHub입니다. 새 결과물을 바탕화면에 만들지 않습니다.

## 2. 확정된 방향과 선택 사항

반드시 [CURRENT_DESIGN.md](CURRENT_DESIGN.md)를 먼저 읽습니다. 오래된 주황 v2와 과거 게시 기록을 새 디자인의 기준으로 삼지 않습니다.

- 현재 방향은 **심플한 클린 베이지, 실제 사진·시술 장면을 크게, 짧은 문구**입니다.
- 영상 기본은 전체 화면 A형. 9:16, 30fps, 1.2배속, 작은 시작 로고 약 2초, 전체형 두 줄 제목 약 2.8초 후 제거.
- 새 썸네일 5안은 비교할 수 있게 제안한 상태입니다. 기본 추천은 01 사진 전체형, 전후 콘텐츠에는 05입니다. 특정 썸네일 번호를 최종 확정했다고 가정하지 않습니다.
- 비포애프터는 같은 고객·같은 부위·실제 순서를 확인합니다. 피부나 털을 수정해 결과를 만들지 않습니다.
- 임산부 사진의 기존 글자는 보존합니다. 확인되지 않은 안전성·효능·주수별 의무를 광고 문구로 추가하지 않습니다.

## 3. 영상과 사진 출처

| 항목 | 실제 사용한 자료 | 처리 |
| --- | --- | --- |
| 쇼츠 01~03 | 사용자가 제공한 Google Drive의 다리 왁싱 원본 MOV | 원본 52.0~66.4초, 14.4초를 1.2배속으로 편집한 12초. 같은 장면에 세 가지 레이아웃 적용 |
| 쇼츠 04 | 선샤인 네이버 플레이스 업체의 예비맘 사진 | 9초 사진 기반 영상. Instagram에서 받은 사진이라고 표현하지 않음 |
| 쇼츠 05 | 업체가 올린 실제 뒷목 전후 합성사진 | 원본의 Before/After 순서를 유지한 9초 사진 기반 영상 |
| 썸네일 01~03 | 위 다리 시술 영상에서 가져온 실제 프레임 | 사진 크기·위치와 문구만 구성 |
| 썸네일 04~05 | 위 예비맘·뒷목 사진 | 원본 문구와 실제 전후 관계 유지 |

공개 사진 출처: [선샤인 네이버 플레이스 업체 사진](https://pcmap.place.naver.com/place/1124966803/photo). 매장 정보는 2026-11-16 확인 기준이며 새 게시 전 변경 여부를 확인합니다.

**납품 쇼츠 5종은 무음 디자인 미리보기입니다.** 여성 TTS가 적용된 게시 완성본은 아닙니다. 고객 원본 MOV, 승인 여성 음성, 로그인 정보, API 키는 포함하지 않습니다. 새 촬영물로 제작할 때는 사용자가 원본을 제공해야 합니다.

## 4. 다운로드만 해서 보기

1. [전체 ZIP 다운로드](https://github.com/qwer777qq/sunshine-waxing-handoff/archive/refs/heads/main.zip).
2. 원하는 작업 폴더에 압축을 풉니다. 예: 문서 폴더 아래 `sunshine-work`. 바탕화면 경로는 필요하지 않습니다.
3. `samples/shorts/`에서 MP4 재생, `samples/shorts-covers/`에서 썸네일 PNG 확인.
4. 디자인 수정은 SVG를 Figma로 가져오거나 아래 렌더 코드를 사용합니다. Noto Sans KR 폰트는 `templates/photo-first-v1/fonts/`에 포함되어 있습니다.

새 썸네일 SVG는 편집 가능한 파일입니다. 기존 Figma 온라인 문서를 이번에 직접 수정한 결과는 아닙니다.

## 5. 실제로 제작하기

아래 명령은 `install_skill.py`가 보이는 저장소 루트에서 실행합니다. 필요한 프로그램 준비와 설치는 [INSTALL_SKILL.md](INSTALL_SKILL.md)를 따릅니다. Python 3.10+와 Pillow가 필요하며 영상은 FFmpeg/ffprobe도 필요합니다.

```sh
python -m pip install -r templates/photo-first-v1/requirements.txt
python skills/sunshine-photo-first-template/scripts/run.py --check
```

### 포함된 소재로 먼저 확인

썸네일 5종 생성:

```sh
python templates/shorts-covers-v1/render.py --output outputs/covers-new
```

포함된 전후 사진으로 비교형 영상 생성:

```sh
python skills/sunshine-photo-first-template/scripts/run.py --preset before-after --output outputs/pair-new
```

### 새 사진·영상으로 교체

썸네일은 `templates/shorts-covers-v1/presets.json`을 같은 폴더에 `my-presets.local.json`으로 복사해 `photo`, `title`, `label`을 바꿉니다. 사진 경로는 JSON 파일 위치 기준이며 절대 경로도 허용합니다.

```sh
python templates/shorts-covers-v1/render.py --config templates/shorts-covers-v1/my-presets.local.json --output outputs/covers-client-new
```

실제 시술 영상은 아래의 입력 경로와 시작 구간을 새 소재에 맞게 바꿉니다. 12초 출력에는 기본 배속 기준 원본 14.4초가 필요합니다.

```sh
python skills/sunshine-photo-first-template/scripts/run.py --preset full --input "원본영상.mp4" --start 0 --duration 12 --output outputs/reel-new
```

가로 촬영물은 화면을 먼저 확인하고 적절한 `--crop x,y,너비,높이`를 정합니다. 이전 샘플의 크롭 좌표를 새 원본에 그대로 적용하지 않습니다. 사진 두 장의 교체, 음성·자막 설정은 [영상 실행 안내](templates/photo-first-v1/README.md)를 읽습니다. 기존 출력 폴더는 덮어쓰지 않으며 새 폴더명을 사용합니다.

### Codex에 설치해 사용

```sh
python install_skill.py
```

코드·폰트·시안·영상 및 새 썸네일 템플릿이 스킬의 `assets/toolkit/`에 함께 들어갑니다. 동명 스킬이 있으면 보존하고 중단하므로 먼저 기존 폴더를 백업하거나 다른 `--dest`를 지정합니다. Codex의 스킬 목록을 새로고침한 뒤 `$sunshine-photo-first-template`을 호출합니다.

## 6. 사이트도 로컬에서 확인하려면

```sh
python -m http.server 8876 --directory designs/approved-20261116/website --bind 127.0.0.1
```

브라우저에서 `http://127.0.0.1:8876/`를 엽니다. 이 명령은 로컬 미리보기입니다. GitHub에 푸시하는 것만으로 기존 Sites 사이트가 자동 배포되지는 않습니다. 사이트를 실제 갱신할 때는 해당 Sites 프로젝트에 접근할 수 있는 계정과 기존 사이트의 소스·배포 절차가 필요합니다. 공개 사이트 URL과 GitHub 저장소는 서로 다른 배포 대상입니다.

## 7. 확인한 내용과 남은 범위

- 고객용 사이트는 2026-11-16에 버전 4 배포 성공을 확인했습니다. GitHub의 MP4 5개·썸네일 PNG 5개·SVG 5개 다운로드 주소는 모두 HTTP 200이며 Git에 저장된 파일 크기와 일치합니다.

- 쇼츠 원본 5종의 1080×1920·30fps·길이·전체 디코딩 검증 기록은 [VERIFICATION.md](templates/photo-first-v1/VERIFICATION.md)에 있습니다.
- 새 웹 미리보기 5종을 브라우저에서 각각 재생했고, 01과 05를 동시에 재생해 재생 시간이 증가하는 것을 확인했습니다.
- 2개 비교, 영상 선택, 썸네일 확대·선택, 복사 완료 표시를 확인했습니다. 모바일 375px에서 가로 넘침 없이 전체 비율을 유지했고, 1440px에서는 5열 배치를 확인했습니다.
- 별도 위치에 스킬을 설치한 후 설치 폴더 내부 코드로 썸네일 5종을 다시 생성했습니다. 원래 작업 폴더의 절대 경로가 필요하지 않습니다. Windows 실행 확인이며 macOS/Linux는 직접 실행 검증하지 않았습니다.
- 새 SVG의 Figma 온라인 가져오기, SNS 업로드 화면의 최종 크롭, 여성 TTS 음질 검수, 실제 채널 게시를 완료했다고 보고하지 않습니다.

## 8. 다음 대화에 보낼 메시지

아래 문구를 복사하고 마지막 줄에 이번 소재와 원하는 내용을 덧붙입니다.

```text
선샤인왁싱 콘텐츠 제작을 이어서 해주세요.
저장소: https://github.com/qwer777qq/sunshine-waxing-handoff
저장소 전체를 내려받고 START_HERE.md → CURRENT_DESIGN.md → INSTALL_SKILL.md 순서로 확인해주세요.
sunshine-photo-first-template 스킬과 포함된 영상·썸네일 템플릿을 사용해주세요.
확정 방향은 클린 베이지, 실제 사진·시술영상 크게, 짧은 제목입니다.
쇼츠는 전체 화면형을 기본으로, 실제 전후 자료는 비포애프터형으로 해주세요.
썸네일은 5안 중 소재에 맞는 안을 추천하고 사진·문구만 교체해주세요.
먼저 표지와 짧은 샘플을 보여주고, 선택한 안으로 마무리해주세요.
새 결과물은 바탕화면이 아닌 작업 폴더에 저장하고 GitHub에서 다른 PC로 받을 수 있게 해주세요.
같은 고객·부위의 전후를 확인하고, 사진을 보정해 효과를 만들지 마세요.
승인 음성이 없으면 무음 샘플이라고 표시하고 SNS 게시는 별도 요청 전까지 하지 마세요.
이번에 사용할 소재/원하는 내용: [여기에 폴더 경로 또는 공유 링크와 요청을 적기]
```
