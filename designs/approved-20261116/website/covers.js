(() => {
 const items=[
  {id:'01',name:'사진 전체형',note:'기본 추천',desc:'사진은 꽉 채우고, 두 줄 제목은 왼쪽 위에.'},
  {id:'02',name:'상단 제목형',note:'내용 전달',desc:'짧은 제목과 시술 사진을 차분하게 나눕니다.'},
  {id:'03',name:'작은 라벨형',note:'사진 우선',desc:'작은 라벨 하나로 사진을 가장 넓게 보여줍니다.'},
  {id:'04',name:'임산부 전용',note:'예비맘 상담',desc:'원본 사진과 문구를 살린 편안한 상담형 표지.'},
  {id:'05',name:'비포애프터형',note:'전후 비교',desc:'실제 전후 두 장을 크게, 차이가 한눈에.'}
 ];
 const grid=document.querySelector('#covers-grid'),dialog=document.querySelector('#cover-viewer');let selected=null,opened=null,returnFocus=null;
 const github='https://github.com/qwer777qq/sunshine-waxing-handoff/raw/refs/heads/main/samples/shorts-covers/';
 grid.innerHTML=items.map(c=>`<article class="cover-card" data-cover-card="${c.id}"><div class="short-number"><span>COVER ${c.id}</span><small>${c.note}</small></div><button class="cover-image" data-cover-open="${c.id}" aria-label="썸네일 ${c.id} ${c.name} 확대"><img src="covers/${c.id}.webp" width="1080" height="1920" loading="lazy" alt="${c.name} 쇼츠 썸네일 시안"><span>전체 보기 ↗</span></button><h3>${c.name}</h3><p>${c.desc}</p><button class="short-choice" data-cover-choice="${c.id}" aria-label="썸네일 ${c.id} ${c.name} 선택" aria-pressed="false">이 썸네일 선택 <span>↗</span></button><div class="cover-downloads"><a href="${github}${c.id}.png" target="_blank" rel="noopener">PNG 받기 ↓</a><a href="${github}${c.id}.svg" target="_blank" rel="noopener">편집 SVG ↓</a></div></article>`).join('');
 function select(id){
  selected=items.find(c=>c.id===id)||null;
  grid.querySelectorAll('[data-cover-choice]').forEach(b=>{const on=b.dataset.coverChoice===selected?.id;b.setAttribute('aria-pressed',String(on));b.closest('.cover-card').classList.toggle('is-selected',on);b.innerHTML=on?'선택한 썸네일 <span>✓</span>':'이 썸네일 선택 <span>↗</span>';});
  document.querySelector('#cover-selection').textContent=selected?`선택한 썸네일 · ${selected.id} ${selected.name}`:'마음에 드는 썸네일을 골라 주세요';
  document.querySelector('#copy-cover-choice').disabled=!selected;document.querySelector('#clear-cover-choice').hidden=!selected;document.querySelector('#cover-copy-status').textContent='';document.querySelector('#cover-copy-fallback').hidden=true;
  try{if(selected)localStorage.setItem('sunshine-cover-choice',selected.id);else localStorage.removeItem('sunshine-cover-choice');}catch{}
  const url=new URL(location.href);if(selected)url.searchParams.set('cover',selected.id);else url.searchParams.delete('cover');history.replaceState(null,'',url);
 }
 function open(id){opened=items.find(c=>c.id===id);returnFocus=document.activeElement;document.querySelector('#cover-viewer-title').textContent=`COVER ${id} · ${opened.name}`;const im=document.querySelector('#cover-viewer-image');im.src=`covers/${id}.webp`;im.alt=opened.name+' 전체 시안';document.querySelector('#cover-png').href=github+id+'.png';document.querySelector('#cover-svg').href=github+id+'.svg';dialog.showModal();document.body.classList.add('modal-open');document.querySelector('#close-cover-viewer').focus();}
 grid.addEventListener('click',e=>{const o=e.target.closest('[data-cover-open]'),s=e.target.closest('[data-cover-choice]');if(o)open(o.dataset.coverOpen);if(s)select(s.dataset.coverChoice);});
 document.querySelector('#close-cover-viewer').addEventListener('click',()=>dialog.close());
 document.querySelector('#choose-viewed-cover').addEventListener('click',()=>{select(opened.id);dialog.close();document.querySelector('#cover-selection').focus();});
 dialog.addEventListener('close',()=>{document.body.classList.remove('modal-open');returnFocus?.focus();});
 dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});
 document.querySelector('#clear-cover-choice').addEventListener('click',()=>select(null));
 document.querySelector('#copy-cover-choice').addEventListener('click',async()=>{
  if(!selected)return;const url=new URL(location.href);url.hash='shorts-covers';const short=url.searchParams.get('short');const text=`선샤인왁싱 시안 선택\n${short?'쇼츠: '+short+'번\n':''}썸네일: ${selected.id} ${selected.name}\n${url.href}`;
  try{await navigator.clipboard.writeText(text);document.querySelector('#cover-copy-status').textContent='선택한 썸네일과 링크를 복사했습니다.';}
  catch{const field=document.querySelector('#cover-copy-fallback');field.hidden=false;field.value=text;field.focus();field.select();document.querySelector('#cover-copy-status').textContent='아래 내용을 복사해 보내 주세요.';}
 });
 let initial=new URL(location.href).searchParams.get('cover');if(!initial){try{initial=localStorage.getItem('sunshine-cover-choice');}catch{}}
 if(items.some(c=>c.id===initial))select(initial);
})();
