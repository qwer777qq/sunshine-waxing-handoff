from pathlib import Path
import json, subprocess, sys

HERE = Path(__file__).resolve().parent
conf = json.loads((HERE / 'template.json').read_text(encoding='utf-8'))
def run(args):
    subprocess.run(args, cwd=HERE, check=True)
def stamp(seconds):
    return f'{int(seconds)//3600}:{int(seconds)//60%60:02d}:{seconds%60:05.2f}'
def ev(start, end, style, text, anim=''):
    return f'Dialogue: 0,{stamp(start)},{stamp(end)},{style},,0,0,0,,{{{anim}}}{text}\n'

speed = conf['speed']
header = '''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Main,Pretendard,96,&H00FFFFFF,&H00FFFFFF,&H00251C19,&H90000000,-1,0,0,0,100,100,0,0,1,3.5,1.5,2,100,165,360,1
Style: Badge,Pretendard,66,&H00FFFFFF,&H00FFFFFF,&H00251C19,&H90000000,-1,0,0,0,100,100,0,0,1,3,1,7,90,90,190,1
Style: Small,Pretendard,34,&H00FFFFFF,&H00FFFFFF,&H00251C19,&H90000000,-1,0,0,0,100,100,0,0,1,2,1,7,90,90,285,1
Style: Hook,Pretendard ExtraBold,100,&H00FFFFFF,&H00FFFFFF,&H00251C19,&H80000000,-1,0,0,0,100,100,0,0,1,4,2,8,90,150,210,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
ass=header
ass+=ev(0,2.5/speed,'Hook',conf['hook'],r'\fad(80,130)\fscx96\fscy96\t(0,220,\fscx100\fscy100)')
for s in conf['captions']:
    animation=r'\fad(90,130)\fscx97\fscy97\t(0,220,\fscx100\fscy100)'
    # Red accent is supplied as ASS markup in the editable configuration.
    ass+=ev(s['start']/speed,s['end']/speed,'Main',s['text'],animation)
for s in conf['labels']:
    animation=r'\fad(120,120)'
    if s.get('after'):
        animation+=r'\c&H004A7BC3&\fscx92\fscy92\t(0,260,\fscx100\fscy100)'
    ass+=ev(max(s['start'],2.6)/speed,s['end']/speed,'Badge',s['text'],animation)
ass+=ev(2.6/speed,conf['duration']/speed,'Small','실제 전후 사진',r'\fad(100,100)')
(HERE/'template.ass').write_text(ass,encoding='utf-8-sig')

before=Path(conf['before']);after=Path(conf['after']);logo=Path(conf['logo']);audio=Path(conf['audio'])
split=conf['split'];duration=conf['duration']
vf=(f'[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,trim=duration={split},setpts=(PTS-STARTPTS)/{speed}[b];'
    f'[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,trim=duration={duration-split},setpts=(PTS-STARTPTS)/{speed}[a];'
    '[b][a]concat=n=2:v=1:a=0[base];'
    '[2:v]crop=980:330:100:690,scale=270:-2,format=rgba[logo];'
    '[base][logo]overlay=70:65:enable=\'lt(t,1.6)\',ass=template.ass:fontsdir=fonts,format=yuv420p[v]')
cmd=['ffmpeg','-y','-hide_banner','-loglevel','error','-loop','1','-framerate','30','-i',str(before),'-loop','1','-framerate','30','-i',str(after),'-loop','1','-framerate','30','-i',str(logo),'-i',str(audio),'-filter_complex',vf,'-map','[v]','-map','3:a','-af',f'atempo={speed},apad','-t',str(duration/speed),'-c:v','libx264','-preset','veryfast','-crf','19','-threads','4','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',str(HERE/'선샤인_숏츠_고급주황_v2.mp4')]
run(cmd)
cover_ass=header+ev(0,3,'Hook',conf['hook'],r'\pos(540,210)')
(HERE/'cover.ass').write_text(cover_ass,encoding='utf-8-sig')
cover_filter='[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1[base];[1:v]crop=980:330:100:690,scale=270:-2,format=rgba[l];[base][l]overlay=70:65,ass=cover.ass:fontsdir=fonts[v]'
run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(before),'-i',str(logo),'-filter_complex',cover_filter,'-map','[v]','-frames:v','1','-q:v','2',str(HERE/'썸네일_두줄.jpg')])
print('Preview created:', HERE/'선샤인_숏츠_고급주황_v2.mp4')
