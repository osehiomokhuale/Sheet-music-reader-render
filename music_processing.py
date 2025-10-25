from music21 import converter, midi
import subprocess
from pathlib import Path

SOUNDFONT_PATH = "/usr/share/sounds/sf2/FluidR3_GM.sf2"  # update to your .sf2 path

def musicxml_to_wav(musicxml_path: str, wav_out: str) -> str:
    p = converter.parse(musicxml_path)
    midi_fp = Path(wav_out).with_suffix('.mid')
    mf = midi.translate.streamToMidiFile(p)
    mf.open(str(midi_fp), 'wb')
    mf.write()
    mf.close()
    wav_fp = Path(wav_out)
    cmd = [
        'fluidsynth',
        '-ni',
        SOUNDFONT_PATH,
        str(midi_fp),
        '-F',
        str(wav_fp),
        '-r', '44100'
    ]
    subprocess.run(cmd, check=True)
    return str(wav_fp)
