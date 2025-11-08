from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path
import asyncio
import subprocess
from collections.abc import Iterable

app = FastAPI()

PROJECT_PATH = Path(__file__).parent.parent.parent
MEDIA_PATH = PROJECT_PATH / "media"


class Player:
    def __init__(self, files: Iterable[Path]):
        self.files = list(files)
        if not self.files:
            raise ValueError("empty file list")
        self._current = 0
        self._task = None
        self._proc = None
        self._playing = False

    async def _loop(self):
        self._current = 0
        while self._playing:
            if self._current >= len(self.files):
                self._current = 0

            file = self.files[self._current]
            self._proc = await asyncio.create_subprocess_exec(
                "mpg123",
                "-q",
                "-k",
                "100",
                file,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            await self._proc.wait()
            self._current += 1

    async def play(self):
        if self.is_playing:
            await self.stop()
        self._playing = True
        self._task = asyncio.create_task(self._loop())

    async def stop(self):
        self._playing = False
        if self.is_playing:
            self._proc.terminate()

    @property
    def is_playing(self) -> bool:
        return bool(self._proc and self._proc.returncode is None)


player = Player(MEDIA_PATH.glob("*.mp3"))


@app.get("/")
async def index() -> HTMLResponse:
    with open(PROJECT_PATH / "static/index.html", encoding="utf-8") as f:
        return HTMLResponse(f.read())


@app.get("/state")
async def get_state() -> bool:
    return player.is_playing


@app.post("/toggle")
async def toggle_playback() -> bool:
    if player.is_playing:
        await player.stop()
        return False
    else:
        await player.play()
        return True


def main():
    import uvicorn

    uvicorn.run("ambient_player.main:app", host="0.0.0.0", port=8100, reload=False)


if __name__ == "__main__":
    main()
