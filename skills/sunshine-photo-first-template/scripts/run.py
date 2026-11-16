"""Launch the self-contained installed toolkit or this downloaded repository."""
from pathlib import Path
import argparse,importlib.util,json,shutil,subprocess,sys

SKILL=Path(__file__).resolve().parents[1]
KIT=SKILL/'assets/toolkit'
if not (KIT/'templates/photo-first-v1/render.py').exists():KIT=SKILL.parents[1]
TEMPLATE=KIT/'templates/photo-first-v1'
PRESETS={'full':'01-fullscreen','strip':'02-top-strip','minimal':'03-minimal','maternity':'04-maternity','photo-demo':'05-photo-demo','before-after':'06-before-after'}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--preset',choices=PRESETS,default='full');p.add_argument('--check',action='store_true');a,rest=p.parse_known_args()
 if a.check:
  errors=[]
  if not importlib.util.find_spec('PIL'):errors.append('Pillow missing: python -m pip install Pillow')
  for executable in ['ffmpeg','ffprobe']:
   if not shutil.which(executable):errors.append(executable+' missing from PATH')
  for path in [TEMPLATE/'render.py',TEMPLATE/'render_pair.py',TEMPLATE/'fonts/NotoSansKR.ttf',TEMPLATE/'fonts/NotoSansKR-SemiBold.ttf',KIT/'designs/approved-20261116/website/assets/logo.webp',KIT/'designs/approved-20261116/website/assets/before-after.webp']:
   if not path.is_file():errors.append('Required bundled asset missing: '+path.name)
  if shutil.which('ffmpeg'):
   filters=subprocess.check_output(['ffmpeg','-hide_banner','-filters'],stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
   for name in [' ass ',' zscale ',' tonemap ',' atempo ']:
    if name not in filters:errors.append('FFmpeg filter missing: '+name.strip())
  print(json.dumps({'ready':not errors,'toolkit':str(KIT),'issues':errors},ensure_ascii=False,indent=2));return 1 if errors else 0
 script=TEMPLATE/('render_pair.py' if a.preset=='before-after' else 'render.py')
 return subprocess.call([sys.executable,str(script),'--config',str(TEMPLATE/'presets'/f'{PRESETS[a.preset]}.json'),*rest])

if __name__=='__main__':sys.exit(main())
