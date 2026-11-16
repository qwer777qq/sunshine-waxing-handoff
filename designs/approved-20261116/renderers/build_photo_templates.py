"""Photo-first layouts. Sources are genuine brand photos; no skin/body retouching."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
from functools import lru_cache
import base64, io, html, json

ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[1]
OUT=ROOT/'website/assets'
EDIT=ROOT/'editable-svg'
EDIT.mkdir(exist_ok=True)
SOURCES={'nape':OUT/'nape.webp','leg':OUT/'leg.jpg','shop':OUT/'interior.webp','maternity':OUT/'maternity-place.jpg'}
CREAM='#F5F0E8'; INK='#51453C'; MUTED='#9C806B'
@lru_cache(None)
def font(size,weight=400,serif=False):
 source=ROOT/'fonts/NotoSerifKR.ttf' if serif else REPO/'templates/photo-first-v1/fonts/NotoSansKR.ttf'
 f=ImageFont.truetype(str(source),size);f.set_variation_by_axes([weight]);return f

class Art:
 def __init__(self,h):
  self.h=h;self.im=Image.new('RGB',(1080,h),CREAM)
  self.svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="{h}" viewBox="0 0 1080 {h}">',f'<rect width="1080" height="{h}" fill="{CREAM}"/>']
 def rect(self,x,y,w,h,c):
  ImageDraw.Draw(self.im).rectangle((x,y,x+w,y+h),fill=c);self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}"/>')
 def text(self,s,x,y,size=40,color=INK,weight=400,serif=False):
  d=ImageDraw.Draw(self.im);f=font(size,weight,serif)
  for i,line in enumerate(s.split('\n')):
   yy=y+i*round(size*1.34);d.text((x,yy),line,font=f,fill=color,anchor='lt')
   self.svg.append(f'<text data-name="교체할 문구" x="{x}" y="{yy}" dominant-baseline="text-before-edge" font-family="Noto {"Serif" if serif else "Sans"} KR" font-size="{size}" font-weight="{weight}" fill="{color}">{html.escape(line)}</text>')
 def photo(self,key,x,y,w,h,contain=False,center=(.5,.5)):
  src=Image.open(SOURCES[key]).convert('RGB')
  if contain:
   im=ImageOps.contain(src,(w,h),Image.Resampling.LANCZOS);x+=(w-im.width)//2;y+=(h-im.height)//2;w,h=im.size
  else:im=ImageOps.fit(src,(w,h),Image.Resampling.LANCZOS,centering=center)
  self.im.paste(im,(x,y));b=io.BytesIO();im.save(b,format='JPEG',quality=95)
  self.svg.append(f'<image data-name="교체할 실제 사진" x="{x}" y="{y}" width="{w}" height="{h}" href="data:image/jpeg;base64,{base64.b64encode(b.getvalue()).decode()}"/>')
 def gradient(self,y,h,reverse=False):
  layer=Image.new('RGBA',(1080,h));d=ImageDraw.Draw(layer)
  for v in range(h):
   p=(1-v/h) if reverse else v/h;d.line((0,v,1080,v),fill=(30,23,18,int(170*p**1.4)))
  self.im.paste(layer,(0,y),layer)
  gid=f'g{y}';self.svg.append(f'<defs><linearGradient id="{gid}" x2="0" y2="1"><stop offset="0" stop-color="#1e1712" stop-opacity="{.67 if reverse else 0}"/><stop offset="1" stop-color="#1e1712" stop-opacity="{0 if reverse else .67}"/></linearGradient></defs><rect x="0" y="{y}" width="1080" height="{h}" fill="url(#{gid})"/>')
 def brand(self,y,color=INK):self.text('SUNSHINE  /  WAXING',62,y,25,color,500)
 def save(self,id,fmt):
  name=f'{id:02d}-{fmt}';self.im.save(OUT/(name+'.png'));self.im.save(OUT/(name+'.webp'),quality=93)
  (EDIT/(name+'.svg')).write_text('\n'.join(self.svg+['</svg>']),encoding='utf-8')

def build(id,h):
 a=Art(h);safe=230 if h==1920 else 55
 if id==13:
  a.photo('nape',0,0,1080,h,center=(.5,.65));a.gradient(0,470,True)
  a.brand(safe,'#FFFFFF');a.text('올림머리 전,\n뒷목부터 깔끔하게',62,safe+58,62,'#FFFFFF',600)
 elif id==14:
  foot=180;a.photo('nape',0,0,1080,h-foot,center=(.5,.65));a.rect(0,h-foot,1080,foot,CREAM)
  a.text('Nape Waxing',55,h-foot+25,32,MUTED,400,True);a.text('올림머리의 마무리, 뒷목 라인',55,h-foot+82,44,INK,500)
 elif id==15:
  a.photo('leg',0,0,1080,h);a.gradient(0,490,True);a.brand(safe,'#FFFFFF')
  a.text('다리 왁싱,\n시술 장면 그대로',62,safe+58,62,'#FFFFFF',600)
 elif id==16:
  a.photo('leg',0,0,1080,h-160);a.rect(0,h-160,1080,160,CREAM)
  a.text('Leg Waxing',55,h-132,30,MUTED,400,True);a.text('매끈한 라인을 위한 다리 왁싱',55,h-78,42,INK,500)
 elif id==17:
  m=26;a.photo('nape',m,m,1080-2*m,h-2*m,center=(.5,.65));a.rect(50,safe,510,134,CREAM)
  a.text('SUNSHINE WAXING',73,safe+15,21,MUTED);a.text('뒷목 라인 기록',73,safe+59,45,INK,500)
 elif id==18:
  a.photo('shop',0,0,1080,h);a.gradient(h-550,550)
  a.text('Your private moment.',60,h-360,44,'#FFFFFF',400,True);a.text('선샤인에서 만나요',60,h-265,62,'#FFFFFF',500);a.brand(h-130,'#FFFFFF')
 elif id==19:
  bar=150;a.photo('nape',0,bar,1080,h-bar,center=(.5,.65));a.brand(28);a.text('뒷목 왁싱 · 실제 시술 기록',62,77,42,INK,500)
 elif id==20:
  a.photo('leg',0,0,1080,h);a.rect(56,safe,385,57,CREAM);a.text('SUNSHINE  /  LEG WAXING',74,safe+13,22,INK,500)
 else:
  # A square branded original is kept intact, including its existing lettering.
  if id==21:
   a.brand(42);a.text('임산부 왁싱',58,104,66,INK,500)
   a.photo('maternity',0,215,1080,h-280,contain=True);a.text('예비맘을 위한 예약 상담',58,h-53,28,MUTED)
  elif id==22:
   a.photo('maternity',0,0,1080,h-185,contain=True);a.rect(0,h-185,1080,185,CREAM)
   a.text('Maternity Waxing',58,h-157,32,MUTED,400,True);a.text('예비맘, 선샤인에서 만나요',58,h-96,46,INK,500)
  elif id==23:
   a.rect(0,0,1080,h,'#ECE1D7');a.text('Maternity',54,40,60,INK,400,True);a.text('임산부 왁싱 · 예약 전 상담',54,127,34,MUTED)
   a.photo('maternity',24,205,1032,h-285,contain=True);a.brand(h-53)
  elif id==24:
   a.photo('maternity',0,0,1080,h-154,contain=True);a.rect(0,h-154,1080,154,INK)
   a.text('임산부 왁싱, 궁금한 점부터',54,h-125,44,CREAM,500);a.text('SUNSHINE WAXING  /  네이버 예약 상담',54,h-58,25,CREAM)
 return a

if __name__=='__main__':
 ids=list(range(13,21))+(list(range(21,25)) if SOURCES['maternity'].exists() else [])
 for fmt,h in {'portrait':1350,'story':1920,'square':1080}.items():
  for id in ids:build(id,h).save(id,fmt)
 sheet=Image.new('RGB',(1440,((len(ids)+3)//4)*480+30),CREAM);d=ImageDraw.Draw(sheet)
 for j,id in enumerate(ids):
  im=Image.open(OUT/f'{id:02d}-portrait.webp');im.thumbnail((330,413));x=20+(j%4)*355;y=20+(j//4)*480;sheet.paste(im,(x,y));d.text((x,y+425),f'{id:02d} / SUNSHINE',font=font(22),fill=INK)
 sheet.save(ROOT/'overview.jpg',quality=95)
 print(f'Created {len(ids)} photo-first families, {len(ids)*3} layouts.')
