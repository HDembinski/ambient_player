import pytest
import asyncio
from pathlib import Path

from ambient_player.main import Player


TEST_MP3 = (Path(__file__).parent.parent / "media").glob("*.mp3")


@pytest.mark.anyio
async def test_player_play_and_stop():
    player = Player(TEST_MP3)

    assert not player.is_playing

    await player.play()
    await asyncio.sleep(3)  # allow player loop to start

    assert player.is_playing

    await player.stop()
    assert not player.is_playing
    assert player._current == 0

    await player.play()
    await asyncio.sleep(3)  # allow player loop to start

    assert player.is_playing

    await player.stop()
    assert not player.is_playing
