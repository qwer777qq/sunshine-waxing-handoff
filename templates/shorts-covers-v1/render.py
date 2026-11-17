"""Render reusable text/shape/photo layouts as PNG, WebP and editable SVG."""
import argparse, base64, html, io, json
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
CREAM, INK, MUTED = '#F5F0E8', '#51453C', '#9C806B'
W, H = 1080, 1920

def font(size, weight=600):
    f = ImageFont.truetype(str(ROOT/'../photo-first-v1/fonts/NotoSansKR.ttf'), size)
    f.set_variation_by_axes([weight])
    return f

class Layout:
    def __init__(self):
        self.image = Image.new('RGB', (W,H), CREAM)
        self.svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',f'<rect width="{W}" height="{H}" fill="{CREAM}"/>']
    def rect(self,x,y,w,h,color):
        ImageDraw.Draw(self.image).rectangle((x,y,x+w,y+h), fill=color)
        self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"/>')
    def text(self,lines,x,y,size=80,color=INK,weight=600,max_width=720):
        if isinstance(lines,str): lines=[lines]
        if len(lines)>2: raise ValueError('Use one or two short title lines.')
        min_size=76 if size>=90 else 26
        while size>min_size and max((font(size,weight).getlength(t) for t in lines),default=0)>max_width: size-=2
        if max((font(size,weight).getlength(t) for t in lines),default=0)>max_width: raise ValueError('Shorten the title.')
        for i,s in enumerate(lines):
            yy=y+i*round(size*1.3)
            ImageDraw.Draw(self.image).text((x,yy),s,font=font(size,weight),fill=color,anchor='lt')
            self.svg.append(f'<text data-name="교체할 문구" x="{x}" y="{yy}" dominant-baseline="text-before-edge" font-family="Noto Sans KR" font-size="{size}" font-weight="{weight}" fill="{color}">{html.escape(s)}</text>')
    def photo(self,src,x,y,w,h,center=(.5,.5),contain=False):
        if contain:
            im=ImageOps.contain(src,(w,h),Image.Resampling.LANCZOS)
            x+=(w-im.width)//2;y+=(h-im.height)//2;w,h=im.size
        else: im=ImageOps.fit(src,(w,h),Image.Resampling.LANCZOS,centering=tuple(center))
        self.image.paste(im,(x,y)); data=io.BytesIO();im.save(data,format='JPEG',quality=95)
        self.svg.append(f'<image data-name="교체할 실제 사진" x="{x}" y="{y}" width="{w}" height="{h}" href="data:image/jpeg;base64,{base64.b64encode(data.getvalue()).decode()}"/>')
    def shade(self):
        layer=Image.new('RGBA',(W,1000));d=ImageDraw.Draw(layer)
        for y in range(1000): d.line((0,y,W,y),fill=(30,23,18,int(175*(1-y/1000)**1.4)))
        self.image.paste(layer,(0,0),layer)
        self.svg.append('<defs><linearGradient id="shade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1e1712" stop-opacity=".63"/><stop offset="1" stop-color="#1e1712" stop-opacity="0"/></linearGradient></defs><rect width="1080" height="1000" fill="url(#shade)"/>')
    def brand(self,y=100,color=INK): self.text('SUNSHINE  /  WAXING',160,y,28,color,500)
    def save(self,out,id):
        self.image.save(out/f'{id}.png');self.image.save(out/f'{id}.webp',quality=92)
        (out/f'{id}.svg').write_text('\n'.join(self.svg+['</svg>']),encoding='utf-8')

def build(c,base):
    p=Path(c['photo']);p=p if p.is_absolute() else base/p
    source=ImageOps.exif_transpose(Image.open(p)).convert('RGB');a=Layout();mode=c['layout'];center=c.get('center',[.5,.5])
    if mode=='full':
        a.photo(source,0,0,W,H,center);a.shade();a.brand(470,'#FFFFFF');a.text(c['title'],160,570,96,'#FFFFFF');a.text(c['label'],160,825,27,'#FFFFFF',400)
    elif mode=='header':
        a.photo(source,0,900,W,H-900,center);a.brand(470);a.text(c['title'],160,570,96)
    elif mode=='label':
        a.photo(source,0,0,W,H,center);a.rect(145,480,750,340,CREAM);a.text(c['label'],160,500,24,MUTED,400,700);a.text(c['title'],160,570,96,INK,600,700)
    elif mode=='maternity':
        a.brand(470);a.text(c['label'],160,525,28,MUTED,400);a.text(c['title'],160,570,96)
        a.photo(source,0,880,W,1000,contain=True);a.text(c.get('footer',''),160,840,28,INK,400)
    elif mode=='pair':
        if not c.get('pair_verified'): raise ValueError('Verify the before/after pair and set pair_verified=true.')
        a.brand(470);a.text(c['title'],160,570,96)
        for key,y,label in [('before',850,'BEFORE  /  시술 전'),('after',1370,'AFTER  /  시술 후')]:
            if c.get(key):
                fp=Path(c[key]);fp=fp if fp.is_absolute() else base/fp
                im=ImageOps.exif_transpose(Image.open(fp)).convert('RGB')
            else:
                x,yy,w,h=c[key+'_rect'];im=source.crop((x,yy,x+w,yy+h))
            a.photo(im,0,y,W,520,c.get(key+'_center',[.5,.5]));a.rect(145,y+22,310,62,CREAM);a.text(label,160,y+37,26,INK,500)
    else: raise ValueError(f'Unknown layout: {mode}')
    return a

def main():
    p=argparse.ArgumentParser();p.add_argument('--config',default=str(ROOT/'presets.json'));p.add_argument('--output',required=True);args=p.parse_args()
    config=Path(args.config).resolve();out=Path(args.output).resolve()
    if out.exists() and any(out.iterdir()): raise FileExistsError('Use a new empty output folder to preserve previous designs.')
    out.mkdir(parents=True,exist_ok=True);entries=json.loads(config.read_text(encoding='utf-8-sig'))
    overview=Image.new('RGB',(1600,740),CREAM);d=ImageDraw.Draw(overview)
    for i,c in enumerate(entries):
        if c.get('before') and not c.get('after') or c.get('after') and not c.get('before'): raise ValueError('Replace both before and after photos together.')
        a=build(c,config.parent);a.save(out,c['id']);tile=a.image.resize((288,512),Image.Resampling.LANCZOS);x=20+i*316
        overview.paste(tile,(x,112));d.text((x,656),f"{c['id']}  {c['name']}",font=font(23,500),fill=INK,anchor='lt')
    d.text((20,28),'SUNSHINE / SHORTS COVER COLLECTION',font=font(30,500),fill=INK,anchor='lt');overview.save(out/'overview.jpg',quality=94)
    print(f'{len(entries)} covers: 1080x1920 PNG / WebP / editable SVG -> {out}')

if __name__=='__main__':main()
