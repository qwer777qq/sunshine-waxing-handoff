from pathlib import Path
import os,sys,requests,subprocess
O=Path(__file__).resolve().parent
T=Path(os.environ.get('ELEVENLABS_TTS_ROOT', 'C:/Users/mach7/Desktop/ElevenLabs-TTS'))
sys.path.insert(0,str(T))
from pipeline.core.tts import load,headers,load_preset
cfg=load();r=requests.get('https://api.elevenlabs.io/v1/voices',headers=headers(cfg),timeout=45);r.raise_for_status()
v=[x for x in r.json()['voices'] if x['name']=='Sunshine_Female_Reference_5Y_oTqtzqHA_20261101']
if len(v)!=1:raise RuntimeError('Required Sunshine voice unavailable')
text='올림머리 하면 보이는 뒷목, 이 차이 보이세요? 잔머리를 정리하기 전과 후를 확인해 보세요. 원하는 라인은 화곡역 선샤인왁싱에서 상담해요.'
(O/'대본.txt').write_text(text,encoding='utf8')
p=load_preset('natural',cfg);p.pop('speed',None)
r=requests.post('https://api.elevenlabs.io/v1/text-to-speech/'+v[0]['voice_id'],headers={**headers(cfg),'Content-Type':'application/json'},params={'output_format':'mp3_44100_128'},json={'text':text,'model_id':'eleven_multilingual_v2','voice_settings':{**p,'speed':1.0}},timeout=120);r.raise_for_status()
(O/'voice_raw.mp3').write_bytes(r.content)
subprocess.run([sys.executable,'-m','pipeline.audio.voice_natural',str(O/'voice_raw.mp3'),'-I','-14'],cwd=T,check=True)
subprocess.run([sys.executable,'-m','pipeline.stt.stt_timed',str(O/'voice_raw_N.mp3'),'sunshine_bench_nape_20261109'],cwd=T,check=True)
print('Voice completed')
