import argparse
from dataclasses import dataclass
import json
import time
from typing import cast
from dice import Dice, Die, get_mouse_listener
from table_helper import TableHelper
from rich.live import Live
import yaml

# region get_roll_result_old
# def get_roll_result_old(dice_sides: int):
#     # Calculate the number of bytes needed to represent the dice sides
#     needed_bits = len(bin(dice_sides)[2:])
#     # Convert the entropy pool to bytes
#     entropy_bytes = ''
#     for item in entropy_pool:
#         entropy_bytes += f"{item:08b}"
#     hash_bin = entropy_bytes
#     # print(f"hash_bin: {hash_bin}")
#     print(f"len(hash_bin): {len(hash_bin)}")
#     for i in range(needed_bits, len(hash_bin)):
#         roll = int(hash_bin[i-needed_bits:i], 2)
#         print(f"hash_bin: {hash_bin[i-needed_bits:i]}\troll: {roll}")
#         if roll <= dice_sides and roll > 0:
#             return roll
#     return 0
# endregion

def write_dice_to_file(dice_list):
    dice_data = [{'sides': d.sides, 'keep': d.keep, 'dice': [{'1_value': v.value, '2_locked': v.locked} for v in d.dice]} for d in dice_list]
    with open('dice.yaml', 'w') as file:
        yaml.dump(dice_data, file)

def load_dice_from_file():
    with open('dice.yaml', 'r') as file:
        dice_data = yaml.safe_load(file)
    dice_list = [Dice(d['sides'], d['keep'], [Die(v['1_value'], d['sides'], v['2_locked']) for v in d['dice']]) for d in dice_data]
    return dice_list


def main(dice_list: list[Dice]):
    # build some initial entropy
    listener = get_mouse_listener(True)
    listener.start()
    print("Move mouse to prepare entropy")
    listener.join()
    print("Ready to go!")
    time.sleep(1)
    
    with Live(refresh_per_second=15) as live:
        table = TableHelper(dice_list, live)
        # roll each group of dice
        for dice in dice_list:
            dice.roll(table)
        
    write_dice_to_file(dice_list)


if __name__ == '__main__':
    print("Lets roll some dice!")

    @dataclass
    class ProgramArgs:
        use_json: bool
        dice: list[str]
    
    parser = argparse.ArgumentParser(description="Dice roller")
    parser.add_argument('-i', '--use-json', action='store_true', help='Use dice.json for input instead of dice arguments')
    parser.add_argument('dice', type=str, nargs='*', help='Dice to roll, format: <number>d<sides>[,<keep>][,<group_copies>]')
    args = cast(ProgramArgs, parser.parse_args())

    dice_list = []
    if args.use_json:
        dice_list = load_dice_from_file()
    else:
        for dice_arg in args.dice:
            dice_args = dice_arg.split(',')
            number, sides = map(int,dice_args[0].split('d'))
            # number = int(dice_args[1]) if len(dice_args) > 1 else 1
            keep = int(dice_args[1]) if len(dice_args) > 1 else number
            group_copies = int(dice_args[2]) if len(dice_args) > 2 else 1
            for _ in range(group_copies):
                dice_list.append(Dice(sides, keep, [Die(0, sides, False) for _ in range(number)]))
    main(dice_list)