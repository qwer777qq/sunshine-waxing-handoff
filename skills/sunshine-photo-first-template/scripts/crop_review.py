"""Make center-crop previews; these are simulations, not platform UI checks."""
from pathlib import Path
import argparse, subprocess
from PIL import Image, ImageDraw, ImageFont

CROPS = [('9-16',9,16), ('4-5',4,5), ('3-4',3,4), ('1-1',1,1)]

def crop_center(image, width, height):
    w,h=image.size
    crop_h=min(h, round(w*height/width)); crop_w=min(w, round(h*width/height))
    x=(w-crop_w)//2; y=(h-crop_h)//2
    return image.crop((x,y,x+crop_w,y+crop_h))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--video',type=Path,required=True);p.add_argument('--cover',type=Path,required=True)
    p.add_argument('--times',nargs='+',type=float,default=[0.5,4.0]);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();out=a.output.resolve()
    if out.exists() and any(out.iterdir()):raise FileExistsError('Choose a new empty output folder.')
    if not a.video.is_file() or not a.cover.is_file():raise FileNotFoundError('Video and cover must exist.')
    duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(a.video)],text=True).strip())
    if any(t<0 or t>=duration for t in a.times):raise ValueError('Each sample time must be inside video duration.')
    out.mkdir(parents=True,exist_ok=True)
    samples=[('cover',Image.open(a.cover).convert('RGB'))]
    for i,t in enumerate(a.times):
        frame=out/f'frame-{i}.png'
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-ss',str(t),'-i',str(a.video),'-frames:v','1','-y',str(frame)],check=True)
        samples.append((f'video {t:g}s',Image.open(frame).convert('RGB')))
    sheet=Image.new('RGB',(4*280,len(samples)*570),'#f5f0e8');draw=ImageDraw.Draw(sheet)
    for row,(name,source) in enumerate(samples):
        for col,(label,w,h) in enumerate(CROPS):
            cropped=crop_center(source,w,h);cropped.save(out/f'{row}-{label}.png')
            cropped.thumbnail((250,500),Image.Resampling.LANCZOS)
            x=col*280+15+(250-cropped.width)//2;y=row*570+42
            sheet.paste(cropped,(x,y));draw.text((col*280+15,row*570+12),f'{name}  {label}',fill='#51453c',font=ImageFont.load_default())
    sheet.save(out/'crop-review.jpg',quality=92)
    (out/'README.txt').write_text('Center crop simulations only. Not an actual platform UI, cover crop, safe zone, or publication check. Inspect every subtitle, important visual and platform preview.\n',encoding='utf8')
    print(out/'crop-review.jpg')

if __name__=='__main__': main()
