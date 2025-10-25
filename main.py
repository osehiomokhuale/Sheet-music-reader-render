from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import uuid
import shutil
from pathlib import Path
from omr import run_audiveris
from music_processing import musicxml_to_wav

app = FastAPI()
WORKDIR = Path("./data")
WORKDIR.mkdir(exist_ok=True)

@app.post('/upload')
async def upload(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.png','.jpg','.jpeg')):
        raise HTTPException(status_code=400, detail="Image must be PNG/JPG/JPEG")
    uid = uuid.uuid4().hex
    img_path = WORKDIR / f"{uid}.jpg"
    with img_path.open('wb') as f:
        shutil.copyfileobj(file.file, f)
    try:
        musicxml_path = run_audiveris(str(img_path), output_dir=str(WORKDIR))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OMR failed: {e}")
    wav_path = WORKDIR / f"{uid}.wav"
    musicxml_to_wav(musicxml_path, wav_out=str(wav_path))
    return {"id": uid, "audio_url": f"/play/{uid}"}

@app.get('/play/{uid}')
async def play(uid: str):
    wav = WORKDIR / f"{uid}.wav"
    if not wav.exists():
        raise HTTPException(status_code=404, detail="Audio not found")
    return FileResponse(path=str(wav), media_type='audio/wav', filename=wav.name)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
