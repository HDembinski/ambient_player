from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import threading
import vlc  # using python-vlc for streaming
from pathlib import Path

app = FastAPI()

# URL of the nature-sounds stream
STREAM_URL = "http://ec3.yesstreaming.net:3540/stream"
THIS_PATH = Path(__file__).parent
MEDIA_PATH = THIS_PATH / "media"


state_lock = threading.Lock()
player = vlc.MediaListPlayer()
player.set_playback_mode(vlc.PlaybackMode.loop)
media_list = vlc.MediaList()
for p in MEDIA_PATH.glob("*.mp3"):
    media_list.add_media(p)
player.set_media_list(media_list)


# Serve static files
@app.get("/")
async def index() -> HTMLResponse:
    with open(THIS_PATH / "static/index.html", encoding="utf-8") as f:
        return HTMLResponse(f.read())


@app.get("/state")
async def get_state() -> bool:
    with state_lock:
        return player.is_playing()


@app.post("/toggle")
async def toggle_playback() -> bool:
    with state_lock:
        if player.is_playing():
            player.pause()
            return False
        else:
            player.play()
            return True


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8100, reload=False)
