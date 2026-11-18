"""Install the portable Sunshine skill from a GitHub clone or extracted ZIP."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,shutil,sys

ROOT=Path(__file__).resolve().parent
NAME='sunshine-photo-first-template'

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--dest',type=Path,help='Parent skills directory; default CODEX_HOME/skills or ~/.codex/skills')
 args=parser.parse_args()
 parent=(args.dest if args.dest else Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex')))/'skills').expanduser().resolve()
 target=parent/NAME
 if target.exists():raise FileExistsError(f'Existing skill preserved: {target}. Choose a new --dest, or back up and remove the old version yourself.')
 required=[ROOT/'skills'/NAME/'SKILL.md',ROOT/'templates/photo-first-v1/fonts/NotoSansKR.ttf',ROOT/'templates/photo-first-v1/fonts/NotoSansKR-SemiBold.ttf',ROOT/'designs/approved-20261116/website/assets/before-after.webp']
 missing=[str(p.relative_to(ROOT)) for p in required if not p.is_file()]
 if missing:raise FileNotFoundError('Download the entire repository ZIP first; missing: '+', '.join(missing))
 parent.mkdir(parents=True,exist_ok=True)
 ignored=shutil.ignore_patterns('__pycache__','*.pyc','*.local.json','*.log')
 shutil.copytree(ROOT/'skills'/NAME,target,ignore=ignored)
 kit=target/'assets/toolkit'
 shutil.copytree(ROOT/'templates/photo-first-v1',kit/'templates/photo-first-v1',ignore=ignored)
 shutil.copytree(ROOT/'templates/shorts-covers-v1',kit/'templates/shorts-covers-v1',ignore=ignored)
 shutil.copytree(ROOT/'designs/approved-20261116',kit/'designs/approved-20261116',ignore=ignored)
 shutil.copy2(ROOT/'CURRENT_DESIGN.md',kit/'CURRENT_DESIGN.md')
 shutil.copy2(ROOT/'BENCHMARK_TEMPLATE.md',kit/'BENCHMARK_TEMPLATE.md')
 manifest={'name':NAME,'version':'2026-11-16','self_contained':True,'source':'https://github.com/qwer777qq/sunshine-waxing-handoff','render_sha256':hashlib.sha256((kit/'templates/photo-first-v1/render.py').read_bytes()).hexdigest()}
 (target/'installation.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 print(f'Installed: {target}\nCheck: python "{target / "scripts/run.py"}" --check\nInvoke in Codex: ${NAME}')

if __name__=='__main__':
 try:main()
 except (FileExistsError,FileNotFoundError) as error:print(error,file=sys.stderr);sys.exit(1)
