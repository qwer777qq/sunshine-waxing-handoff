const templates=[
 {id:1,name:'릴스 표지',en:'REELS COVER',category:'reels',description:'시술 사진과 두 줄 후킹을 중심으로.'},
 {id:2,name:'고정 소개',en:'WELCOME',category:'info',description:'실제 매장 공간과 첫 방문 안내.'},
 {id:3,name:'시술 전후',en:'BEFORE & AFTER',category:'reels',description:'업체가 등록한 실제 전후 사진을 그대로.'},
 {id:4,name:'고객 후기',en:'REAL REVIEW',category:'info',description:'네이버 방문자 리뷰의 실제 키워드.'},
 {id:5,name:'캐러셀 표지',en:'CAROUSEL COVER',category:'carousel',description:'질문과 답변으로 시작하는 첫 장.'},
 {id:6,name:'캐러셀 본문',en:'CAROUSEL BODY',category:'carousel',description:'예약 전에 필요한 세 가지 정보.'},
 {id:7,name:'시술 메뉴',en:'WAXING MENU',category:'carousel',description:'다리·뒷목·눈썹, 원하는 부위별 안내.'},
 {id:8,name:'가격 안내',en:'PRICE LIST',category:'info',description:'첫 방문·해피타임 실제 등록 가격.'},
 {id:9,name:'예약 안내',en:'RESERVATION',category:'info',description:'예약 정보와 문의 번호를 한 장에.'},
 {id:10,name:'월간 일정',en:'MONTHLY',category:'info',description:'11월 달력과 현재 운영시간 안내.'},
 {id:11,name:'이벤트',en:'SPECIAL OFFER',category:'info',description:'플레이스에 등록된 첫 방문 혜택.'},
 {id:12,name:'공지',en:'NOTICE',category:'info',description:'매일 운영시간과 화곡역 방문 안내.'},
 {id:13,name:'사진 전체 · 상단 후킹',en:'FULL PHOTO / A',category:'photo',description:'추천 · 사진을 꽉 채우고 제목은 왼쪽 위에 짧게.'},
 {id:14,name:'사진 중심 · 하단 띠',en:'BOTTOM LABEL / B',category:'photo',description:'사진 아래 얇은 베이지 띠로 제목을 분리.'},
 {id:15,name:'시술 영상 · 두 줄 후킹',en:'TREATMENT / C',category:'photo',description:'실제 다리 시술 장면과 간결한 두 줄 제목.'},
 {id:16,name:'시술 영상 · 캡션 띠',en:'THIN CAPTION / D',category:'photo',description:'시술 장면을 크게, 설명은 아래에 한 줄로.'},
 {id:17,name:'슬림 프레임 · 작은 라벨',en:'SLIM FRAME / E',category:'photo',description:'얇은 테두리와 작은 제목 상자로 브랜드 톤만 더하기.'},
 {id:18,name:'공간 전체 · 소개 표지',en:'SPACE / F',category:'photo',description:'실제 매장 사진을 넓게 보여주는 소개형.'},
 {id:19,name:'사진 중심 · 상단 띠',en:'TOP LABEL / G',category:'photo',description:'제목을 상단에 모아 시술 부위를 가리지 않는 구성.'},
 {id:20,name:'사진 전체 · 최소 로고',en:'MINIMAL / H',category:'photo',description:'사진이 주인공. 작은 브랜드 라벨만 남긴 가장 심플한 구성.'},
 {id:21,name:'임산부 · 상단 제목',en:'MATERNITY / A',category:'maternity',description:'예비맘 사진 전체를 살리고 제목을 상단에 분리. 현재 플레이스 업체 사진 적용.'},
 {id:22,name:'임산부 · 하단 캡션',en:'MATERNITY / B',category:'maternity',description:'사진 속 문구까지 보존하는 원본 전체형. 현재 플레이스 업체 사진 적용.'},
 {id:23,name:'임산부 · 베이지 프레임',en:'MATERNITY / C',category:'maternity',description:'기존 베이지 컬렉션과 이어지는 예비맘 전용 표지. 현재 플레이스 업체 사진 적용.'},
 {id:24,name:'임산부 · 예약 상담',en:'MATERNITY / D',category:'maternity',description:'사진 아래 짧은 상담 안내만 더한 구성. 현재 플레이스 업체 사진 적용.'}
];
const grid=document.querySelector('#template-grid'),format=document.querySelector('#format'),viewer=document.querySelector('#viewer');
let activeFilter='new',activeIndex=0,viewerFormat='portrait',lastTrigger=null,viewerIds=[];
const file=(id,fmt,ext='webp')=>`assets/${String(id).padStart(2,'0')}-${fmt}.${ext}`;
function render(){
 const shown=templates.filter(t=>activeFilter==='all'||(activeFilter==='new'&&t.id>12)||(activeFilter==='base'&&t.id<=12)||t.category===activeFilter);
 grid.innerHTML=shown.map(t=>`<article class="template-card"><button class="template-image" data-template="${t.id}" aria-label="${t.name} 시안 크게 보기"><img src="${file(t.id,format.value)}" alt="${t.name} 실제 이미지 적용 시안" width="1080" height="${{portrait:1350,story:1920,square:1080}[format.value]}" loading="lazy"><span class="view-label">크게 보기 ↗</span></button><div class="card-label"><strong><span class="num">${String(t.id).padStart(2,'0')}</span>${t.name}</strong><small>${t.en}</small></div><p>${t.description}</p></article>`).join('');
 document.querySelector('#result-count').textContent=`${shown.length}개 시안 표시 중`;
}
function updateViewer(){const t=templates[activeIndex];document.querySelector('#viewer-category').textContent=t.en+' / '+{portrait:'4:5',story:'9:16',square:'1:1'}[viewerFormat];document.querySelector('#viewer-title').textContent=t.name;document.querySelector('#viewer-image').src=file(t.id,viewerFormat);document.querySelector('#viewer-image').alt=t.name+' 확대 시안';document.querySelector('#viewer-description').textContent=t.description;const d=document.querySelector('#download-template');d.href=file(t.id,viewerFormat,'png');d.download=`선샤인_${t.name}_${viewerFormat}.png`;}
function openViewer(id,fmt,trigger){activeIndex=id-1;viewerFormat=fmt;lastTrigger=trigger;viewerIds=Array.from(trigger.closest('#template-grid,#feed-grid').querySelectorAll('[data-template],[data-feed]')).map(b=>Number(b.dataset.template||b.dataset.feed));updateViewer();viewer.showModal();document.body.classList.add('modal-open');document.querySelector('#close-viewer').focus();}
grid.addEventListener('click',e=>{const btn=e.target.closest('[data-template]');if(btn)openViewer(Number(btn.dataset.template),format.value,btn);});
document.querySelectorAll('[data-filter]').forEach(button=>button.addEventListener('click',()=>{activeFilter=button.dataset.filter;document.querySelectorAll('[data-filter]').forEach(b=>{b.classList.toggle('active',b===button);b.setAttribute('aria-pressed',String(b===button));});render();}));
format.addEventListener('change',render);
document.querySelector('#close-viewer').addEventListener('click',()=>viewer.close());
viewer.addEventListener('close',()=>{document.body.classList.remove('modal-open');lastTrigger?.focus();});
viewer.addEventListener('click',e=>{if(e.target===viewer){const r=viewer.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)viewer.close();}});
function step(n){const at=viewerIds.indexOf(templates[activeIndex].id);activeIndex=viewerIds[(at+n+viewerIds.length)%viewerIds.length]-1;updateViewer();}
document.querySelector('#prev-template').addEventListener('click',()=>step(-1));document.querySelector('#next-template').addEventListener('click',()=>step(1));
document.addEventListener('keydown',e=>{if(viewer.open&&e.key==='ArrowRight')step(1);if(viewer.open&&e.key==='ArrowLeft')step(-1);});
const feed=document.querySelector('#feed-grid');
const feedSets={photo:[13,14,15,17,18,16,19,20,3],maternity:[21,22,23,24,18,9],base:[1,2,3,5,8,4,12,9,11]};
function renderFeed(){const ids=feedSets[document.querySelector('#feed-style').value];feed.innerHTML=ids.map(id=>`<button data-feed="${id}" aria-label="${templates[id-1].name} 시안 크게 보기"><img src="${file(id,'portrait')}" width="1080" height="1350" alt="${templates[id-1].name}" loading="lazy"><span>${String(id).padStart(2,'0')}</span></button>`).join('');}
document.querySelector('#feed-style').addEventListener('change',renderFeed);
feed.addEventListener('click',e=>{const btn=e.target.closest('[data-feed]');if(btn)openViewer(Number(btn.dataset.feed),'portrait',btn);});render();renderFeed();
