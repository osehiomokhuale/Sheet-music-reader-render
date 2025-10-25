import subprocess
from pathlib import Path

AUDIVERIS_CMD = "audiveris"  # ensure audiveris is installed and on PATH

def run_audiveris(image_path: str, output_dir: str) -> str:
    out_dir = Path(output_dir)
    cmd = [AUDIVERIS_CMD, '-batch', '-export', image_path]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"Audiveris failed: {p.stderr}\n{p.stdout}")
    mp = Path(image_path)
    candidates = list(mp.parent.glob('*.musicxml')) + list(mp.parent.glob('*.xml'))
    if not candidates:
        candidates = list(out_dir.glob('**/*.musicxml'))
    if not candidates:
        raise FileNotFoundError('No MusicXML produced by Audiveris')
    musicxml = max(candidates, key=lambda p: p.stat().st_mtime)
    return str(musicxml)
