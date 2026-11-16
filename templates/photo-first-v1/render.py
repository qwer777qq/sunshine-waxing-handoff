"""Reusable local Reels/Shorts renderer. No cloud calls or publishing actions."""
from pathlib import Path
import argparse, json, math, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent
W,H,FPS = 1080,1920,30
CREAM,INK,RED = '#F5F0E8','#51453C','#B94B43'
FONT = ROOT/'fonts/NotoSansKR.ttf'
TONEMAP = 'zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=mobius:desat=0,zscale=t=bt709:m=bt709:r=tv'

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],encoding='utf-8'))

def run(args,cwd=None):
    p=subprocess.run(['ffmpeg','-hide_banner','-nostdin','-loglevel','error',*args],cwd=cwd,capture_output=True,text=True,encoding='utf-8',errors='replace')
    if p.returncode: raise RuntimeError(p.stderr[-5000:])

def font(size,weight=500):
    f=ImageFont.truetype(str(FONT),size)
    try:f.set_variation_by_axes([weight])
    except (OSError,ValueError):pass
    return f

def draw_lines(im,lines,x,y,size,color,weight=600,max_width=810):
    lines=lines if isinstance(lines,list) else [lines]
    if len(lines)>2:raise ValueError('Use at most two title lines.')
    while size>36 and max((font(size,weight).getlength(t) for t in lines),default=0)>max_width:size-=2
    if max((font(size,weight).getlength(t) for t in lines),default=0)>max_width:raise ValueError('Title too long; shorten it to fit the picture.')
    d=ImageDraw.Draw(im)
    for i,line in enumerate(lines):d.text((x,y+i*round(size*1.36)),line,font=font(size,weight),fill=color,anchor='lt')

def gradient(im,y,height,reverse=False):
    d=ImageDraw.Draw(im)
    for i in range(height):
        amount=(1-i/height) if reverse else i/height
        d.line((0,y+i,W,y+i),fill=(27,22,18,int(170*amount**1.4)))

def overlays(config,out):
    mode=config['layout']; title=config.get('title',[])
    title_im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(title_im)
    if mode=='full':
        gradient(title_im,0,620,True);draw_lines(title_im,title,64,300,72,'white')
    elif mode=='top-strip':
        draw_lines(title_im,title,64,240,62,INK)
    elif mode=='minimal':
        pass
    elif mode=='maternity':
        draw_lines(title_im,title,64,250,66,INK)
    else:raise ValueError('Unknown layout. Use full, top-strip, minimal or maternity.')
    title_im.save(out/'title-overlay.png')
    brand=Image.new('RGBA',(W,H));d=ImageDraw.Draw(brand)
    logo=ROOT/'../../designs/approved-20261116/website/assets/logo.webp'
    if logo.exists():
        im=Image.open(logo).convert('RGBA');im.thumbnail((62,62));brand.alpha_composite(im,(64,160))
    d.rounded_rectangle((142,164,635,216),radius=5,fill=CREAM)
    d.text((159,176),'SUNSHINE  /  WAXING',font=font(25),fill=INK,anchor='lt')
    brand.save(out/'brand-overlay.png')
    return title_im,brand

def ass_time(t):
    n=round(t*100);return f'{n//360000}:{n//6000%60:02d}:{n//100%60:02d}.{n%100:02d}'

def ass_escape(s):
    return s.replace('\\','\\\\').replace('{','\\{').replace('}','\\}').replace('\n','\\N')

def subtitles(config,out,duration):
    events=[];last_end=0
    for c in config.get('captions',[]):
        start,end=float(c['start']),float(c['end'])
        if not (0<=start<end<=duration+.02):raise ValueError('Caption time must be within the final output duration.')
        if start<last_end:raise ValueError('Caption overlap: use one idea at a time.')
        last_end=end;content=ass_escape(c['text'])
        if c.get('highlight'):
            key=ass_escape(c['highlight']);content=content.replace(key,r'{\c&H6174EE&}'+key+r'{\c&HFFFFFF&}')
        events.append(f'Dialogue: 0,{ass_time(start)},{ass_time(end)},Caption,,0,0,0,,{{\\fad(120,160)}}{content}')
    header='''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,Noto Sans KR,56,&H00FFFFFF,&H006174EE,&H00302018,&H80302018,-1,0,0,0,100,100,0,0,1,3,1,2,80,180,330,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    (out/'captions.ass').write_text(header+'\n'.join(events)+'\n',encoding='utf-8')

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--config',default=str(ROOT/'presets/01-fullscreen.json'))
    ap.add_argument('--input');ap.add_argument('--start',type=float);ap.add_argument('--duration',type=float)
    ap.add_argument('--crop',help='x,y,width,height in the display-oriented source')
    ap.add_argument('--voice',help='Already authorized voice file; raw speed unless voice_speed=1')
    ap.add_argument('--output',required=True);ap.add_argument('--cover-only',action='store_true')
    args=ap.parse_args()
    config_path=Path(args.config).resolve();c=json.loads(config_path.read_text(encoding='utf-8-sig'))
    def path(s):
        p=Path(s);return p.resolve() if p.is_absolute() else (config_path.parent/p).resolve()
    src=Path(args.input).resolve() if args.input else path(c['input'])
    if not src.is_file():raise FileNotFoundError(f'Input not found: {src}. Copy your media here or use --input.')
    if not FONT.is_file():raise FileNotFoundError('Bundled Noto Sans KR font is missing.')
    for tool in ('ffmpeg','ffprobe'):
        if not shutil.which(tool):raise FileNotFoundError(f'{tool} is not on PATH.')
    start=args.start if args.start is not None else float(c.get('start',0))
    duration=args.duration if args.duration is not None else float(c.get('duration',12))
    speed=float(c.get('speed',1.2));kind=c.get('media_type','video');crop=c.get('crop')
    if args.crop:crop=[int(v) for v in args.crop.split(',')]
    if not(0.5<=speed<=2 and 1<=duration<=180 and start>=0):raise ValueError('Check speed, duration and in-point.')
    metadata=probe(src);stream=next((s for s in metadata['streams'] if s['codec_type']=='video'),None)
    if not stream:raise ValueError('Source has no picture stream.')
    if kind=='video' and start+duration*speed>float(metadata['format']['duration'])+.05:raise ValueError('Selected range exceeds the source. Shorten duration or change start.')
    if crop and (len(crop)!=4 or min(crop)<0 or crop[2]<2 or crop[3]<2):raise ValueError('Crop must be x,y,width,height with positive size.')
    voice=Path(args.voice).resolve() if args.voice else (path(c['voice']) if c.get('voice') else None)
    voice_speed=float(c.get('voice_speed',1.2))
    if voice:
        if not voice.is_file():raise FileNotFoundError(str(voice))
        if not(.5<=voice_speed<=2):raise ValueError('voice_speed must be 0.5..2.')
        vd=float(probe(voice)['format']['duration'])/voice_speed
        if vd>duration+.05:raise ValueError(f'Voice lasts {vd:.2f}s after speed adjustment. Increase duration; do not cut the sentence.')
    out=Path(args.output).resolve()
    if out.exists() and any(out.iterdir()):raise FileExistsError('Use a new empty output folder to preserve prior renders.')
    out.mkdir(parents=True,exist_ok=True)
    title,brand=overlays(c,out);subtitles(c,out,duration)
    # A relative fonts directory avoids Windows drive-letter escaping in libass.
    (out/'fonts').mkdir();shutil.copy2(ROOT/'fonts/NotoSansKR-SemiBold.ttf',out/'fonts/NotoSansKR-SemiBold.ttf')
    if kind=='image':
        normalized=ImageOps.exif_transpose(Image.open(src)).convert('RGB');normalized.save(out/'normalized-input.png')
        inputs=['-loop','1','-framerate','30','-i',str(out/'normalized-input.png')]
    else:inputs=['-ss',str(start),'-t',str(duration*speed),'-i',str(src)]
    chain=[]
    if kind=='video':chain.append(f'setpts=(PTS-STARTPTS)/{speed}')
    if crop:chain.append('crop='+':'.join(str(v) for v in [crop[2],crop[3],crop[0],crop[1]]))
    if stream.get('color_transfer') in ('arib-std-b67','smpte2084'):chain.append(TONEMAP)
    mode=c['layout'];fit=c.get('fit','cover');box_h=H;box_y=0
    if mode=='top-strip':box_h=H-420;box_y=420
    if mode=='maternity':box_h=H-560;box_y=420
    if fit=='contain':
        chain.extend([f'scale={W}:{box_h}:force_original_aspect_ratio=decrease:force_divisible_by=2',f'pad={W}:{box_h}:(ow-iw)/2:(oh-ih)/2:color=0xF5F0E8'])
    else:chain.extend([f'scale={W}:{box_h}:force_original_aspect_ratio=increase:force_divisible_by=2',f'crop={W}:{box_h}'])
    if box_h!=H:chain.append(f'pad={W}:{H}:0:{box_y}:color=0xF5F0E8')
    chain+=['setsar=1','fps=30','format=yuv420p']
    base=','.join(chain)
    # Separate cover: same photo and typography, independent of overlay timing.
    run([*inputs,'-vf',base,'-frames:v','1','-y',str(out/'cover-base.png')])
    cover=Image.open(out/'cover-base.png').convert('RGBA');cover.alpha_composite(title);cover.alpha_composite(brand);cover.convert('RGB').save(out/'cover.png')
    c.update({'input':str(src),'start':start,'duration':duration,'speed':speed,'crop':crop,'voice':str(voice) if voice else None,'template_demo_without_voice':voice is None})
    (out/'render-settings.local.json').write_text(json.dumps(c,ensure_ascii=False,indent=2),encoding='utf-8')
    if args.cover_only:print(out/'cover.png');return
    for name in ('title-overlay.png','brand-overlay.png'):inputs+=['-loop','1','-framerate','30','-i',str(out/name)]
    if voice:inputs+=['-i',str(voice)]
    else:inputs+=['-f','lavfi','-i','anullsrc=r=48000:cl=stereo']
    hook=min(duration,float(c.get('hook_duration',2.8)));fade=min(.25,hook/2)
    graph=f'[0:v]{base}[base];[1:v]format=rgba,fade=t=out:st={hook-fade}:d={fade}:alpha=1[title];[2:v]format=rgba,fade=t=out:st=1.75:d=0.25:alpha=1[brand];[base][title]overlay=0:0:enable=lt(t\\,{hook}):shortest=1[v1];[v1][brand]overlay=0:0:enable=lt(t\\,2):shortest=1[v2];[v2]ass=filename=captions.ass:fontsdir=fonts,format=yuv420p[v]'
    if voice:graph+=f';[3:a]asetpts=PTS-STARTPTS,atempo={voice_speed},apad,atrim=duration={duration},afade=t=in:d=0.03,afade=t=out:st={duration-.12}:d=0.12[a]'
    else:graph+=f';[3:a]atrim=duration={duration}[a]'
    run([*inputs,'-filter_complex',graph,'-map','[v]','-map','[a]','-t',str(duration),'-c:v','libx264','-preset','fast','-crf','19','-c:a','aac','-b:a','160k','-ar','48000','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart','-y',str(out/'shorts.mp4')],cwd=out)
    result=probe(out/'shorts.mp4');(out/'probe.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(out/'shorts.mp4')

if __name__=='__main__':
    try:main()
    except (ValueError,FileNotFoundError,FileExistsError,RuntimeError) as e:print(f'ERROR: {e}',file=sys.stderr);sys.exit(1)
