# 검증 기록 · 2026-11-16

- 전체 화면·제목 띠·최소 로고: 제공된 실제 다리 시술 원본의 52초부터 14.4초 구간, 1.2배속으로 각 12초 렌더.
- 임산부: 플레이스 업체 공개 예비맘 사진으로 9초 사진 기반 렌더.
- 전후 비교: 업체 원본의 Before/After 표시를 확인한 뒷목 두 사진으로 9초 렌더. 전후 순서를 유지하고 피부·털 보정 없음.
- 5종 모두 ffprobe로 1080×1920, 30fps, H.264/AAC, 지정 길이 확인. FFmpeg 전체 디코딩 오류 없음.
- 시작·끝 프레임을 모아 실제 사진, 제목, 라벨, 2초 뒤 로고 제거, 2.8초 뒤 전체형 제목 제거를 확인.
- 사진 데모로 ASS 자막과 빨간 강조 단어를 확인. 별도 3초 시험음으로 음성 파일 합성·배속·나머지 무음 패딩 경로 확인. 이는 승인 여성 TTS나 음성 자연스러움 검증이 아님.
- 5종 납품 샘플은 무음 디자인 데모. 승인된 여성 TTS는 별도 입력해야 하며 Instagram/YouTube 게시와 플랫폼별 최종 크롭 검수는 수행하지 않음.
- 고객 원본 MOV, 시험음, 로컬 절대 경로 설정, MP4 출력은 Git에 제외. 코드·설정·기존 공개 시안·표지·OFL 폰트만 저장.
- 독립 설치: `install_skill.py --dest <별도 폴더>`로 실제 복사한 스킬에서 `--check` 성공, 비포애프터 표지 및 8초 사진 데모 영상 렌더 성공. 원래 작업 폴더 대신 설치 스킬 내부 toolkit 경로 사용을 확인. Windows에서 확인했으며 macOS/Linux 실행은 직접 검증하지 않음.
- 새 스킬 `sunshine-photo-first-template`은 skill-creator의 quick_validate 검사 통과.

공식 구현 참고: [FFmpeg 필터](https://ffmpeg.org/ffmpeg-filters.html), [Noto Sans KR OFL](https://github.com/google/fonts/blob/main/ofl/notosanskr/OFL.txt).
