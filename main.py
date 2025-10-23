from fastapi import FastAPI
from fastapi.responses import FileResponse
import threading
import vlc  # using python-vlc for streaming
from pathlib import Path
import subprocess as subp

app = FastAPI()

# URL of the nature-sounds stream
STREAM_URL = "http://ec3.yesstreaming.net:3540/stream"
THIS_DIR = Path(__file__).parent


def command_result(cmd: str) -> str:
    return subp.run(cmd.split(), text=True, stdout=subp.PIPE).stdout.strip()


def get_bluetooth_device():
    return command_result("bluetoothctl devices Paired").split()[1]


state_lock = threading.Lock()
is_playing = False
player = vlc.MediaPlayer(STREAM_URL)
bluetooth_device = get_bluetooth_device()


def start_stream():
    player.play()


def stop_stream():
    player.stop()


# Serve static files
@app.get("/")
async def index() -> FileResponse:
    return FileResponse((THIS_DIR / "static/index.html"), media_type="text/html")


@app.get("/state")
async def get_state() -> bool:
    with state_lock:
        return is_playing


@app.post("/toggle")
async def toggle_playback() -> bool:
    global is_playing
    with state_lock:
        if is_playing:
            stop_stream()
            is_playing = False
        else:
            start_stream()
            is_playing = True
        return is_playing


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8100, reload=False)
