from dataclasses import dataclass
import numpy as np
import ctypes
import time
from pynput import mouse
from table_helper import TableHelper
from typing import Optional

# Global variables
ENTROPY_POOL_SIZE = 32
ENTROPY_THRESHOLD = 512
entropy_pool = [0]*64
entrophy_pool_size = 0
entrophy_estimation = 0
mouse_listener: mouse.Listener = mouse.Listener()
dice_table: TableHelper
current_die: Optional['Die'] = None

PROCESS_PER_MONITOR_DPI_AWARE = 2
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

def on_move(x, y):
    if x != 0 and y != 0:
        t = time.perf_counter_ns()
        x = x & 0xF  # Keep only the 4 most significant bits
        y = y & 0xF  # Keep only the 4 most significant bits
        r = int(t) & 0xFF  # Keep only the 8 most significant bits
        entropy = ((x << 4) | y) ^ r  # e is 8 bits long and it's the new added entropy
        build_entropy(entropy)

def build_entropy(entropy: int):
    global entrophy_estimation, entropy_pool, entrophy_pool_size, current_die
    entrophy_pool_size %= ENTROPY_POOL_SIZE
    entropy_pool[entrophy_pool_size] ^= entropy

    entrophy_estimation += 1 # the code we're basing this on uses 2 here but I'm reducing it to 1 because it's pretty fast
    entrophy_pool_size += 1
    if entrophy_pool_size % 2 == 0 and current_die:
        current_die.value = get_rng(min=1, max=current_die.sides, use_entropy=False)
        dice_table.regenerate_table()
    if entrophy_estimation >= ENTROPY_THRESHOLD:
        mouse_listener.stop()
        # we need to reset this before we start a new roll
        entrophy_estimation = 0

def get_mouse_listener(new=False):
    global mouse_listener
    if new:
        mouse_listener.stop()
        mouse_listener = mouse.Listener(on_move=on_move)
    # try:
    #     mouse_listener.is_alive()
    #     print("reusing listener")
    # except Exception:
    #     mouse_listener = mouse.Listener(on_move=on_move)
    return mouse_listener

def get_rng(min: int = 1, max: int = 6, use_entropy: bool = True) -> int:
    if use_entropy:
        listener = get_mouse_listener(True)
        listener.start()
        mouse_listener.join()
        rng = np.random.default_rng(entropy_pool)
        return int(rng.integers(min, max+1))
    rng = np.random.default_rng()
    return int(rng.integers(min, max+1))

@dataclass
class Die:
    value: int
    sides: int
    locked: bool = False

@dataclass
class Dice:
    sides: int
    keep: int
    dice: list[Die]

    def roll(self, table: TableHelper):
        global dice_table, current_die
        dice_table = table
        for die in self.dice:
            if not die.locked:
                current_die = die
                generations_for_roll = get_rng(min=1, max=2, use_entropy=False)
                # print(f"rolling {generations_for_roll} times")
                for _ in range(generations_for_roll):
                    die.value = get_rng(min=1, max=self.sides)
        table.regenerate_table()