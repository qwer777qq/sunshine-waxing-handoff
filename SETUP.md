# 템플릿·스킬 사용하기

## 포함된 코드

| 폴더 | 내용 |
| --- | --- |
| `templates/original` | 초기 사진 전후 템플릿·ASS·설정·사용법 |
| `templates/premium-orange-v2` | 고급 주황 두 줄 후킹·빨강 강조·등장 확대/페이드 템플릿 |
| `templates/nape-v2` | 뒷목 실제 제작 버전의 렌더·TTS 호출 코드, 대본, 설정·ASS |
| `skills/sunshine-waxing-content` | 콘텐츠·검색·영상·여성 TTS 운영 기준 |
| `skills/sunshine-waxing-highlights` | 전후 선정·숏츠 제작·검수 기준 및 에이전트 메타데이터 |

현재 찾은 소스는 초기/v2다. v5 렌더 소스를 찾았다는 의미가 아니다. `README.md`의 v5 상태와 구분한다.

## 로컬 렌더

1. Python 3, FFmpeg(libass 지원), ffprobe를 설치하고 PATH에 둔다. 렌더 스크립트는 Python 표준 라이브러리를 사용한다.
2. 사용할 템플릿 폴더를 별도 작업 폴더로 복사한다.
3. 해당 폴더 아래 `assets/before.jpg`, `assets/after.jpg`, `assets/logo.png`, `assets/voice.mp3`를 준비하거나 `template.json`의 경로를 변경한다. 음성은 렌더에서 다시 1.2배속 처리되므로 이미 배속한 파일을 중복 배속하지 않는다.
4. 기존에 사용한 Pretendard Bold·ExtraBold 글꼴을 `fonts/`에 준비한다. 폰트 파일은 이번 업로드에 포함하지 않았다.
5. `template.json`의 대본·장면 길이·전환·자막 시간을 실제 소재와 음성에 맞게 변경한다.
6. 해당 템플릿 폴더에서 `python render_template.py`를 실행한다. 영상·썸네일·ASS 출력은 같은 폴더에서 덮어쓸 수 있다.
7. 출력 전 구간과 음성을 확인한다. 자동 문법 검사만으로 영상·음성 품질 검수가 끝난 것은 아니다.

로고 크롭 `980:330:100:690`은 기존 선샤인 로고 원본에 맞춘 값이다. 다른 로고는 크기·실제 그림을 확인해 스크립트의 크롭을 조정해야 한다. 이 템플릿은 사진 두 장용이며 시술 영상 클립을 직접 입력하는 범용 편집기는 아니다.

## TTS 코드

`templates/nape-v2/voice.py`는 기존 로컬 ElevenLabs-TTS 프로젝트의 `pipeline` 모듈과 설정을 읽는 연결 스크립트다. 그 외부 프로젝트 전체나 ElevenLabs 키는 이 저장소에 포함되지 않는다. 경로는 `ELEVENLABS_TTS_ROOT` 환경변수로 지정할 수 있다.

이 스크립트를 실행하면 실제 ElevenLabs TTS 생성 요청이 발생해 크레딧을 사용할 수 있다. 이번 패키징에서는 생성 요청을 실행하지 않았다. 사진 렌더 자체는 로컬 FFmpeg로 수행한다.

호출로 생성되는 음성은 `voice_raw_N.mp3`다. 이를 `assets/voice.mp3`에 준비하거나 `template.json`의 `audio`를 해당 파일로 바꾼다. 이는 v2 재현용 코드이며 v5의 문장별 호흡 개선 구현이라고 보장하지 않는다.

## 스킬 설치와 우선순위

두 스킬 폴더를 사용하는 Codex의 스킬 디렉터리로 복사한다. 같은 이름의 기존 스킬이 있다면 먼저 비교·백업하고 최신 내용을 보존한다. 이번 작업은 저장소에 복사본을 추가했으며 호스트 스킬을 덮어쓰지 않았다.

스킬에 기록된 절대 경로는 원래 PC의 이력이다. 새 PC에서 경로를 맞춰야 한다. `goni-reel-studio`, `local-brand-consulting` 등 다른 스킬과 외부 스크립트는 선택적 연계 자료로 이번 패키지에 포함하지 않았다. 과거 기준 사진 `assets/reference-brow.jpg`, `reference-body.jpg`도 미포함이다.

날짜가 다른 기준이 충돌하면 현재 사용자 지시와 최신 제작 기준을 우선한다. 새 숏츠는 전체화면·시작부 로고·고급 주황·빨강 강조·두 줄 후킹을 사용한다. 예전 고정 프레임·엔딩 로고·노랑 강조 설정을 최신 기본값으로 되돌리지 않는다. 예약 자동화는 임의 재가동하지 않는다.

## 비밀번호·API 키 보관

사용자가 전달한 네이버 검색광고·NAVER API HUB·YouTube API 인증값과 네이버·인스타그램·카카오·스레드·구글 비밀번호는 코드 대신 같은 저장소의 **GitHub Actions repository Secrets**에 보관한다. 당근 로그인 및 인증정보 등록은 제외한다.

등록 이름은 `.env.example`에서 확인한다. 실제 값은 소스 파일과 Git 기록에 포함하지 않는다. 저장소 설정의 `Settings → Secrets and variables → Actions`에서 이름을 확인·갱신할 수 있다. 등록된 값은 GitHub UI/API로 다시 읽을 수 없으므로 비밀번호를 내려받는 백업 파일로 사용할 수 없다.

Secrets는 로컬 프로그램에 자동 전달되지 않는다. 로컬 실행은 기존 승인된 설정을 사용하거나 필요한 환경변수를 별도로 설정한다. 이번 저장소에는 Secrets를 읽거나 외부로 보내는 Actions 워크플로가 없다. 등록 여부와 인증값의 유효성 검증은 별개다.
