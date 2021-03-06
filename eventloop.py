import asyncio
import time


coroutines: list = []


class LoopEnd(Exception):
    """Loop end exception."""
    pass


async def sleep(tics: int = 1):
    """Sleep for <<tics>> times."""
    for _ in range(tics):
        await asyncio.sleep(0)


def add_coroutine(coroutine):
    """Add coroutine to coroutines list."""
    coroutines.append(coroutine)


def loop_forever(windows_for_refresh: list):
    """Loop until at least one coroutine can work."""
    if not coroutines:
        raise Exception("No coroutines for start")

    index: int = 0
    while coroutines:
        if index >= len(coroutines):
            index = 0
        coroutine = coroutines[index]
        try:
            coroutine.send(None)
            index += 1
        except StopIteration:
            coroutines.remove(coroutine)
        except LoopEnd:
            coroutines.clear()
            break
        for canvas in windows_for_refresh:
            canvas.refresh()
        time.sleep(0.01)
