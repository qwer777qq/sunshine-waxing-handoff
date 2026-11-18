# 선샤인 작업 상태와 반복 절차

- 선샤인 `sunshine-photo-first-template` 스킬을 사용하고, `CURRENT_DESIGN.md`와 `BENCHMARK_TEMPLATE.md`를 읽는다. 최신 사용자 지시가 우선이다.
- 제목 첫 화면은 x=160, y=570 기준으로 통일하고 표지와 같은 문구·줄바꿈을 쓴다. 영상 및 썸네일의 실제 출력에서 가독성과 시술 부위 가림을 확인한다.
- 반복 검수: `python skills/sunshine-photo-first-template/scripts/crop_review.py --video <mp4> --cover <png> --times 0.5 4 --output <새 폴더>`; 필요한 자막 시점을 추가한다. 9:16·4:5·3:4·1:1 중앙 크롭의 비교이며 플랫폼 UI 검증은 아니다.
- SCV `scv@scv-codex` 활성 0.94.0-codex.1, Graphify 0.9.104 PATH 우선(2026-11-18 확인). 프로젝트 SCV 초기화는 별도다. 미디어·고객 자료를 그래프 대상에 자동으로 넣지 않는다.
- 역할: 포맷 검수는 `sunshine_format_qa`; 개발 도구·기억은 기존 `goni_workflow_maintainer`. 사용자 위임이 있는 경우 역할을 호출하고, 없으면 주 에이전트가 수행한다.
- Aside 데몬 미연결로 실제 인스타그램·스레드·유튜브·네이버 클립 업로드 미리보기는 미확인이다. 실서비스 확인 후 플랫폼·기기·시점·결과를 별도로 기록한다. 콘텐츠는 별도 게시 요청 없이 게시하지 않는다.
- 자격증명과 고객 개인정보는 기억·Git에 넣지 않는다. 결과물은 바탕화면이 아니라 작업 폴더에 저장한다.
