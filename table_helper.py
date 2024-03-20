import itertools
# import curses
# import os
# from prettytable import PrettyTable
from typing import TYPE_CHECKING
from rich.table import Table
from rich.live import Live

if TYPE_CHECKING:
    from dice import Dice

class TableHelper():
    def __init__(self, dice_groups: list['Dice'], live: Live):
        self.dice_groups = dice_groups
        self.live = live
        self.regenerate_table()
        # self.table.align = "c"
        # self.table.padding_width = 1

    def regenerate_table(self):
        self.table = Table()
        self.headers = self._build_headers()
        rows = self._build_rows_by_column(self.dice_groups)
        # rows.insert(0, self.headers) # type: ignore
        # self.table.clear_rows()
        for row in rows:
            values = [str(val) for val in row]
            self.table.add_row(*values)
        # # Clear the terminal
        # os.system('cls' if os.name == 'nt' else 'clear')
        # # Print the updated table
        # print(self.table)
        # self.stdscr.clear()
        # self.stdscr.addstr(str(self.table))
        # self.stdscr.refresh()
        self.live.update(self.table)

    def get_table(self) -> Table:
        return self.table

    def _build_headers(self) -> list[str]:
        headers = []
        for i, dice_group in enumerate(self.dice_groups):
            if i+1 == len(self.dice_groups):
                headers += [f"d{dice_group.sides}", "roll", f"k{dice_group.keep}", "Total", "Keep Total"]
            else:
                headers += [f"d{dice_group.sides}", "roll", f"k{dice_group.keep}"]
        for column in headers:
            self.table.add_column(column)
        return headers
    
    def get_sum_of_keep(self, rolls: list[int], keep: int) -> int:
        temp_roles = rolls.copy()
        temp_roles.sort(reverse=True)
        # print(temp_roles[:keep])
        # print(sum(temp_roles[:keep]))
        return sum(temp_roles[:keep])
    
    def _build_rows_by_column(self, dice_groups: list['Dice']) -> list[list[int|str]]:
        columns = []
        # keep_column = []
        combined_totals = 0
        combined_keeps = 0
        largest_group = max([len(dice_group.dice) for dice_group in dice_groups])
        for i, dice_group in enumerate(dice_groups):
            column_die_num: list[int|str] = [i for i in range(1, len(dice_group.dice)+1)]
            column_die_num += [""] * (largest_group - len(column_die_num))
            column_die_num.append("Total")

            column_die_value: list[int] = [die.value for die in dice_group.dice]
            column_die_value += [0] * (largest_group - len(column_die_value))
            
            keep_sum = self.get_sum_of_keep(column_die_value, dice_group.keep)
            keep_column = ["-" for _ in range(largest_group)]
            combined_keeps += keep_sum
            keep_column.append(keep_sum) # type: ignore

            column_die_sum = sum(column_die_value)
            column_die_value.append(column_die_sum)

            # if i == 1:
            #     print(f"column_die_value: {column_die_value}")
            combined_totals += column_die_sum
            column_die_value = [die_val if die_val != 0 else '' for die_val in column_die_value] # type: ignore
            # if i == 1:
            #     print(f"column_die_value: {column_die_value}")
            columns.append(column_die_num)
            columns.append(column_die_value)
            columns.append(keep_column)
        columns.append([combined_totals])
        columns.append([combined_keeps])
        # Transpose columns to rows
        # print("columns: ")
        # print(columns)
        rows = list(map(list, itertools.zip_longest(*columns, fillvalue='')))
        # print("rows: ")
        # print(rows)
        return rows


    def save_table(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self.table))
