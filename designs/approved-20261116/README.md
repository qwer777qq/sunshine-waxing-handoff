# 승인 디자인 묶음 · 2026-11-16

- [고객용 시안 사이트](https://sunshine-waxing-design-collection.alalshow3.chatgpt.site)
- [기존 36종 Figma 파일](https://www.figma.com/design/7PooDi7T7IgsQkwAF97Ftx)
- `website/`: 현재 공개 사이트의 HTML/CSS/JS와 실제 사진 적용 시안 24종 × 3비율 = 72종. 정적 서버로 열면 필터·확대·PNG 다운로드를 사용할 수 있습니다.
- `editable-svg/`: 새 사진 중심 8종 + 임산부 4종 × 3비율 = 36개 SVG. 사진, 텍스트, 도형 레이어를 분리했습니다. Figma 가져오기를 위한 편집 원본이며 네이티브 Figma 파일을 새로 갱신했다는 뜻은 아닙니다.
- `figma/clean-beige-library.fig`: 이전에 정리한 클린 베이지 12종 × 3비율의 네이티브 편집본. 사진 교체용 기본형이며 최신 사이트의 실제 사진을 모두 넣은 Figma 파일은 아닙니다.
- `renderers/`: 사진 중심 시안 생성 코드. 텍스트 수정이나 새 사진 교체에 사용할 수 있습니다.
- `overview.jpg`: 신규 12종 모아보기.
- `video-previews/`: 5가지 쇼츠 템플릿의 시작·끝 화면과 사진 강조형 전후 표지 3비율. 영상 렌더 소스는 `templates/photo-first-v1/`에 있습니다.

사이트를 로컬에서 열기:

```powershell
python -m http.server 8876 --directory designs/approved-20261116/website
```

브라우저에서 http://localhost:8876 에 접속합니다. `index.html`을 직접 열어도 기본 시안 보기 기능을 사용할 수 있습니다.

이미지 출처: 선샤인왁싱 네이버 플레이스의 업체 사진, 제공된 다리 영상의 기존 공개 시안용 정지 이미지. 실제 피부나 털을 생성·보정하지 않았습니다. 고객 원본 MOV, 개인 음성, 인증정보는 이 묶음에 없습니다.

피드 미리보기는 이미지 높이를 자동으로 설정하고 `object-fit: contain`을 적용해 표지 전체 비율을 보존합니다.
