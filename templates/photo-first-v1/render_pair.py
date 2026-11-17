"""Real before/after photo emphasis. Keeps pair order and never retouches skin/hair."""
import argparse,json,subprocess,sys
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
from render import font,CREAM,INK

ROOT=Path(__file__).resolve().parent

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--config',default=str(ROOT/'presets/06-before-after.json'));ap.add_argument('--before');ap.add_argument('--after');ap.add_argument('--output',required=True);ap.add_argument('--cover-only',action='store_true');args=ap.parse_args()
 if bool(args.before)!=bool(args.after):raise ValueError('Provide both --before and --after so a new photo is never paired with the old example.')
 cp=Path(args.config).resolve();c=json.loads(cp.read_text(encoding='utf-8-sig'))
 if not c.get('pair_verified'):raise ValueError('Confirm the same customer and body area, then set pair_verified=true.')
 def path(s):
  p=Path(s);return p if p.is_absolute() else (cp.parent/p).resolve()
 def photo(which,override):
  if override:return ImageOps.exif_transpose(Image.open(Path(override).resolve())).convert('RGB')
  if c.get(which):return ImageOps.exif_transpose(Image.open(path(c[which]))).convert('RGB')
  im=ImageOps.exif_transpose(Image.open(path(c['composite']))).convert('RGB')
  x,y,w,h=c[which+'_rect'];return im.crop((x,y,x+w,y+h))
 before=photo('before',args.before);after=photo('after',args.after)
 out=Path(args.output).resolve()
 if out.exists() and any(out.iterdir()):raise FileExistsError('Use a new empty output folder.')
 out.mkdir(parents=True,exist_ok=True)
 for fmt,height in [('story',1920),('portrait',1350),('square',1080)]:
  canvas=Image.new('RGB',(1080,height),CREAM);d=ImageDraw.Draw(canvas)
  top=850 if fmt=='story' else 180;bottom=40;gap=16;ph=(height-top-bottom-gap)//2
  title_y=570 if fmt=='story' else 43
  size=96
  while size>76 and font(size,600).getlength(c['title'])>720:size-=2
  if font(size,600).getlength(c['title'])>720:raise ValueError('Shorten the title to fit the safe area.')
  d.text((160,title_y),c['title'],font=font(size,600),fill=INK,anchor='lt')
  for i,(im,label) in enumerate([(before,'BEFORE  /  시술 전'),(after,'AFTER  /  시술 후')]):
   y=top+i*(ph+gap)
   if c.get('fit','cover')=='contain':
    box=Image.new('RGB',(1080,ph),CREAM);resized=ImageOps.contain(im,(1080,ph),Image.Resampling.LANCZOS);box.paste(resized,((1080-resized.width)//2,(ph-resized.height)//2))
   else:box=ImageOps.fit(im,(1080,ph),Image.Resampling.LANCZOS,centering=tuple(c.get(['before_center','after_center'][i],[.5,.5])))
   canvas.paste(box,(0,y));d=ImageDraw.Draw(canvas);d.rounded_rectangle((145,y+22,480,y+88),radius=6,fill=CREAM);d.text((160,y+38),label,font=font(28,500),fill=INK,anchor='lt')
  canvas.save(out/f'comparison-{fmt}.png')
 # Video and cover share the same source and small start logo.
 cfg={'layout':'minimal','input':str(out/'comparison-story.png'),'media_type':'image','title':[],'duration':c.get('duration',9),'speed':1.2,'fit':'contain','voice':str(path(c['voice'])) if c.get('voice') else None,'voice_speed':c.get('voice_speed',1.2),'captions':[]}
 config_out=out/'pair-video.local.json';config_out.write_text(json.dumps(cfg,ensure_ascii=False,indent=2),encoding='utf-8')
 command=[sys.executable,str(ROOT/'render.py'),'--config',str(config_out),'--output',str(out/'video')]
 if args.cover_only:command.append('--cover-only')
 subprocess.run(command,check=True)
 print(out)

if __name__=='__main__':main()
