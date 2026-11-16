# 다른 PC에서 받아 쓰기

## 1. GitHub ZIP 다운로드

[전체 ZIP 받기](https://github.com/qwer777qq/sunshine-waxing-handoff/archive/refs/heads/main.zip)를 내려받아 압축을 풉니다. Git을 쓴다면:

```text
git clone https://github.com/qwer777qq/sunshine-waxing-handoff.git
cd sunshine-waxing-handoff
```

ZIP에서 풀었다면 `install_skill.py`가 있는 폴더에서 터미널을 엽니다. 스킬 폴더 하나만 받으면 코드·폰트·사진이 빠지므로 전체 ZIP을 받습니다.

## 2. 필요한 프로그램 준비

Python 3.10 이상과 FFmpeg/ffprobe가 필요합니다. FFmpeg는 libass·zscale·tonemap을 포함한 빌드를 사용하고 PATH에 등록합니다. [FFmpeg 공식 다운로드](https://ffmpeg.org/download.html)에서 운영체제에 맞는 배포를 선택합니다.

```text
python -m pip install -r templates/photo-first-v1/requirements.txt
```

macOS/Linux에서 명령이 `python3`이면 이후 `python` 대신 `python3`를 사용합니다. 코드는 Windows 고정 경로를 요구하지 않으며 이 작업에서는 Windows에서 실제 실행했습니다.

## 3. 한 번 설치

```text
python install_skill.py
```

기본 위치는 `CODEX_HOME/skills`이며 변수가 없으면 사용자 홈의 `.codex/skills`입니다. 설치 위치를 따로 지정하려면:

```text
python install_skill.py --dest "D:/내스킬폴더"
```

**코드·설정·폰트·예시 사진·승인 시안이 스킬 내부로 함께 복사됩니다.** 설치가 끝나면 원래 다운로드 폴더 없이도 실행할 수 있습니다. 기존 동명 스킬은 덮어쓰지 않습니다. 업그레이드할 때는 기존 폴더를 백업해 이름을 바꾼 후 새로 설치합니다.

## 4. 확인하고 Codex에서 사용

설치 명령이 출력한 `Check:` 명령을 실행하면 필요한 프로그램과 파일을 확인합니다. Codex를 다시 열거나 스킬 목록을 새로고침한 후:

```text
$sunshine-photo-first-template
이 사진 두 장을 비포·애프터 사진 강조형 쇼츠로 만들어줘.
사진 영역은 크게, 문구는 짧게. 표지부터 보여줘.
```

```text
$sunshine-photo-first-template
이 시술 영상의 12초 구간을 전체 화면형 릴스로 만들어줘.
제목은 “다리 왁싱 / 시술 장면 그대로”로 적용해줘.
```

스킬을 지원하지 않는 환경에서도 [Python 실행 안내](templates/photo-first-v1/README.md)에 따라 직접 렌더할 수 있습니다. 다른 AI 도구의 스킬 설치 위치는 해당 도구 안내를 따르며, Codex 설치 경로를 그대로 사용할 수 있다고 가정하지 않습니다.

고객 원본·승인 여성 음성·계정 로그인·API 키는 포함하지 않습니다. 포함된 예시 사진으로는 무음 디자인 데모를 바로 만들 수 있고, 실제 게시용 음성은 승인된 파일을 넣습니다. 설치와 렌더는 유료 서비스나 자동 업로드를 호출하지 않습니다.
