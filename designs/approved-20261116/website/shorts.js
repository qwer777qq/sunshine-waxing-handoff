(() => {
 const items=[
  {id:'01',name:'전체 화면',en:'FULL PHOTO',duration:12,type:'실제 시술 영상',description:'첫 제목 뒤에는 시술 장면을 화면 가득. 가장 기본으로 쓰기 좋은 구성.',file:'01-fullscreen'},
  {id:'02',name:'제목 띠',en:'CLEAN CAPTION',duration:12,type:'실제 시술 영상',description:'위에는 짧은 제목, 아래에는 큰 시술 장면. 내용을 차분하게 전달하는 구성.',file:'02-top-strip'},
  {id:'03',name:'최소 로고',en:'MINIMAL',duration:12,type:'실제 시술 영상',description:'시작 로고만 작게. 사진과 시술 동작을 가장 넓게 보여주는 구성.',file:'03-minimal'},
  {id:'04',name:'임산부',en:'MATERNITY',duration:9,type:'사진 기반 영상',description:'사진의 원래 영역과 문구를 살린 예비맘 전용 구성.',file:'04-maternity'},
  {id:'05',name:'비포·애프터',en:'BEFORE & AFTER',duration:9,type:'사진 기반 영상',description:'실제 시술 전후를 위아래로 크게. 변화가 한눈에 들어오는 비교 구성.',file:'05-before-after'}
 ];
 const root=document.querySelector('#shorts-grid');
 const compare=document.querySelector('#shorts-compare');
 const compareBody=document.querySelector('#compare-videos');
 const compareButton=document.querySelector('#open-short-comparison');
 const compareIds=new Set();let chosen=null,lastFocus=null;
 const github='https://github.com/qwer777qq/sunshine-waxing-handoff/raw/refs/heads/main/samples/shorts/';
 root.innerHTML=items.map(t=>`<article class="short-card" id="short-${t.id}" data-short-card="${t.id}">
  <div class="short-number"><span>SHORT ${t.id}</span><small>${t.duration}초 · 9:16</small></div>
  <div class="short-player"><video data-short-video="${t.id}" controls playsinline muted preload="none" poster="videos/${t.id}.webp" width="720" height="1280" aria-label="쇼츠 ${t.id} ${t.name} 영상"><source src="videos/${t.id}.mp4" type="video/mp4">브라우저에서 영상을 재생할 수 없습니다.</video><button class="video-play" data-play="${t.id}" aria-label="쇼츠 ${t.id} ${t.name} 재생"><span aria-hidden="true">▶</span><small>미리보기</small></button></div>
  <p class="video-error" hidden>영상을 불러오지 못했습니다. 아래 MP4 다운로드를 이용해 주세요.</p>
  <div class="short-title"><h3>${t.name}</h3><span>${t.type}</span></div><p class="short-description">${t.description}</p>
  <label class="compare-check"><input type="checkbox" data-compare="${t.id}" aria-label="쇼츠 ${t.id} ${t.name} 비교 담기"> 비교 담기</label>
  <button class="short-choice" data-choice="${t.id}" aria-pressed="false" aria-label="쇼츠 ${t.id} ${t.name} 선택">이 시안 선택 <span>↗</span></button>
  <a class="short-download" href="${github}${t.file}.mp4" target="_blank" rel="noopener noreferrer">원본 MP4 받기 ↓</a>
 </article>`).join('');
 const cardVideos=[...root.querySelectorAll('video')];
 function pauseAll(){[...cardVideos,...compareBody.querySelectorAll('video')].forEach(v=>v.pause());}
 cardVideos.forEach(v=>{
  const shell=v.closest('.short-player');
  v.addEventListener('play',()=>{cardVideos.filter(other=>other!==v).forEach(other=>other.pause());shell.classList.add('playing');});
  v.addEventListener('pause',()=>shell.classList.remove('playing'));
  v.addEventListener('ended',()=>shell.classList.remove('playing'));
  v.addEventListener('error',()=>{v.closest('.short-card').querySelector('.video-error').hidden=false;});
 });
 root.addEventListener('click',e=>{
  const play=e.target.closest('[data-play]');if(play){const v=root.querySelector(`[data-short-video="${play.dataset.play}"]`);if(v.ended)v.currentTime=0;v.play().catch(()=>{v.closest('.short-card').querySelector('.video-error').hidden=false;});}
  const choice=e.target.closest('[data-choice]');if(choice)choose(choice.dataset.choice);
 });
 function syncCompare(){
  root.querySelectorAll('[data-compare]').forEach(el=>{el.checked=compareIds.has(el.dataset.compare);el.disabled=compareIds.size===2&&!el.checked;});
  compareButton.disabled=compareIds.size!==2;
  document.querySelector('#comparison-count').textContent=`${compareIds.size}/2 선택`;
  document.querySelector('#clear-comparison').disabled=compareIds.size===0;
 }
 root.addEventListener('change',e=>{const box=e.target.closest('[data-compare]');if(!box)return;if(box.checked&&compareIds.size<2)compareIds.add(box.dataset.compare);else compareIds.delete(box.dataset.compare);syncCompare();});
 document.querySelector('#clear-comparison').addEventListener('click',()=>{compareIds.clear();syncCompare();});
 compareButton.addEventListener('click',()=>{
  pauseAll();lastFocus=document.activeElement;
  compareBody.innerHTML=[...compareIds].map(id=>{const t=items.find(x=>x.id===id);return `<div class="compare-item"><h3><small>${id}</small> ${t.name}</h3><video controls playsinline muted preload="metadata" width="720" height="1280" poster="videos/${id}.webp" aria-label="비교 ${id} ${t.name} 영상"><source src="videos/${id}.mp4" type="video/mp4"></video><button class="short-choice" data-compare-choice="${id}">${id} ${t.name} 선택</button></div>`;}).join('');
  document.querySelector('#compare-status').textContent='무음 미리보기 · 각 영상의 전체 비율을 유지합니다.';
  compare.showModal();document.body.classList.add('modal-open');document.querySelector('#close-short-comparison').focus();
 });
 document.querySelector('#compare-play').addEventListener('click',async()=>{
  const vs=[...compareBody.querySelectorAll('video')];vs.forEach(v=>{v.pause();v.currentTime=0;});
  const results=await Promise.allSettled(vs.map(v=>v.play()));
  document.querySelector('#compare-status').textContent=results.some(r=>r.status==='rejected')?'각 영상의 재생 버튼을 눌러 주세요.':'두 영상을 처음부터 재생 중입니다.';
 });
 document.querySelector('#compare-pause').addEventListener('click',()=>{pauseAll();document.querySelector('#compare-status').textContent='두 영상을 일시정지했습니다.';});
 document.querySelector('#close-short-comparison').addEventListener('click',()=>compare.close());
 compare.addEventListener('close',()=>{pauseAll();document.body.classList.remove('modal-open');lastFocus?.focus();});
 compare.addEventListener('click',e=>{if(e.target===compare){const r=compare.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)compare.close();}});
 compareBody.addEventListener('click',e=>{const b=e.target.closest('[data-compare-choice]');if(b){choose(b.dataset.compareChoice);compare.close();document.querySelector('#selection-title').focus();}});
 function choose(id){
  chosen=items.find(t=>t.id===id)||null;
  root.querySelectorAll('[data-choice]').forEach(b=>{const on=b.dataset.choice===chosen?.id;b.setAttribute('aria-pressed',String(on));b.closest('.short-card').classList.toggle('is-selected',on);b.innerHTML=on?'선택한 시안 <span>✓</span>':'이 시안 선택 <span>↗</span>';});
  document.querySelector('#selection-title').textContent=chosen?`선택한 시안 · ${chosen.id} ${chosen.name}`:'마음에 드는 시안을 골라 주세요';
  document.querySelector('#selection-description').textContent=chosen?'선택 내용을 복사해 담당자에게 보내 주세요.':'영상을 재생하고, 두 가지를 나란히 비교한 뒤 선택할 수 있습니다.';
  document.querySelector('#copy-short-choice').disabled=!chosen;document.querySelector('#clear-short-choice').hidden=!chosen;
  document.querySelector('#choice-copy-fallback').hidden=true;document.querySelector('#choice-status').textContent='';
  try{if(chosen)localStorage.setItem('sunshine-short-choice',chosen.id);else localStorage.removeItem('sunshine-short-choice');}catch{}
  const url=new URL(location.href);if(chosen)url.searchParams.set('short',chosen.id);else url.searchParams.delete('short');history.replaceState(null,'',url);
 }
 document.querySelector('#clear-short-choice').addEventListener('click',()=>choose(null));
 document.querySelector('#copy-short-choice').addEventListener('click',async()=>{
  if(!chosen)return;const url=new URL(location.href);url.hash='shorts';url.searchParams.set('short',chosen.id);
  const cover=url.searchParams.get('cover');
  const text=`선샤인왁싱 쇼츠 시안 선택: ${chosen.id} ${chosen.name}\n${cover?'썸네일: '+cover+'번\n':''}${url.href}`;
  try{await navigator.clipboard.writeText(text);document.querySelector('#choice-status').textContent='선택 내용과 링크를 복사했습니다.';}
  catch{const field=document.querySelector('#choice-copy-fallback');field.hidden=false;field.value=text;field.focus();field.select();document.querySelector('#choice-status').textContent='아래 내용을 복사해 보내 주세요.';}
 });
 let initial=new URL(location.href).searchParams.get('short');if(!initial){try{initial=localStorage.getItem('sunshine-short-choice');}catch{}}
 if(items.some(t=>t.id===initial))choose(initial);
 syncCompare();document.addEventListener('visibilitychange',()=>{if(document.hidden)pauseAll();});
})();
