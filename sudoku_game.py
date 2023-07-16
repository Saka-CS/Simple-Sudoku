import collections
from random import randrange
import random
import copy
import time


def clear():
    print("\n" * 20)


class COLOR:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def make_sudoku(remove):
    sudoku = [['.', '.', '.', '.', '.', '.', '.', '.', '.'],
              ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
              ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
              ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
              ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
              ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
              ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
              ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
              ['.', '.', '.', '.', '.', '.', '.', '.', '.']]

    while True:
        row_dict = collections.defaultdict(set)
        col_dict = collections.defaultdict(set)
        box_dict = collections.defaultdict(set)

        for row in range(9):
            for col in range(9):
                if sudoku[row][col] != '.':
                    row_dict[row].add(sudoku[row][col])
                    col_dict[col].add(sudoku[row][col])
                    box_dict[(row // 3, col // 3)].add(sudoku[row][col])

        minimum = 10
        minimum_location = [10, 10]
        minimum_arr = []

        for row in range(9):
            for col in range(9):
                counter = 0
                possible_arr = []
                if sudoku[row][col] == '.':
                    for num in range(1, 10):
                        if num not in row_dict[row] and num not in col_dict[col] and\
                                num not in box_dict[(row // 3, col // 3)]:
                            counter += 1
                            possible_arr.append(num)
                    if counter < minimum:
                        minimum = counter
                        minimum_location = [row, col]
                        minimum_arr = copy.deepcopy(possible_arr)
                    elif counter == minimum and random.randint(0, 100) > 95:
                        minimum_location = [row, col]
                        minimum_arr = copy.deepcopy(possible_arr)

        if not minimum_arr:
            for row in range(9):
                for col in range(9):
                    if sudoku[row][col] == '.':
                        return False
            break
        sudoku[minimum_location[0]][minimum_location[1]] = random.choice(minimum_arr)

    sudoku = valid_sudoku(sudoku, remove)
    return sudoku


def valid_sudoku(sudoku, remove):
    location = [i for i in range(81)]
    og_remove = remove
    remove = randrange(remove - 3, remove + 3)

    while remove:
        if not location:
            return make_sudoku(og_remove)
        p = random.choice(location)
        temp_number = sudoku[p // 9][p % 9]
        sudoku[p // 9][p % 9] = '.'

        row_dict = collections.defaultdict(set)
        col_dict = collections.defaultdict(set)
        box_dict = collections.defaultdict(set)

        for row in range(9):
            for col in range(9):
                if sudoku[row][col] != '.':
                    row_dict[row].add(sudoku[row][col])
                    col_dict[col].add(sudoku[row][col])
                    box_dict[(row // 3, col // 3)].add(sudoku[row][col])

        maximum = 1
        for row in range(9):
            for col in range(9):
                counter = 0
                if sudoku[row][col] == '.':
                    for num in range(1, 10):
                        if num not in row_dict[row] and num not in col_dict[col] and\
                                num not in box_dict[(row // 3, col // 3)]:
                            counter += 1
                    if counter > maximum:
                        maximum = counter

        if maximum > 1:
            sudoku[p // 9][p % 9] = temp_number
        else:
            remove -= 1
        location.pop(location.index(p))

    return sudoku


def display(sudoku, y, x):
    clear()

    print(end="    ")
    for i in range(9):
        print(COLOR.BLUE + str(i + 1) + COLOR.END, end="   ")
    print()
    print("  +-----------+-----------+-----------+")

    for r, row in enumerate(sudoku):
        print(COLOR.GREEN + str(r + 1) + COLOR.END, end="   ")
        print("\b\b|", end=" ")
        for c, col in enumerate(row):
            if r + 1 == y and c + 1 == x:
                print(COLOR.RED + str(col) + COLOR.END, end="   ")
            else:
                print(col, end="   ")
            if (c + 1) % 3 == 0:
                print("\b\b|", end=" ")
        print()
        if (r + 1) % 3 == 0:
            print("  +-----------+-----------+-----------+")


def validation(sudoku):
    row_dict = collections.defaultdict(set)
    col_dict = collections.defaultdict(set)
    box_dict = collections.defaultdict(set)
    counter = 0

    for row in range(9):
        for col in range(9):
            if sudoku[row][col] != '.':
                counter += 1
                if sudoku[row][col] in row_dict[row] or sudoku[row][col] in col_dict[col] or\
                        sudoku[row][col] in box_dict[(row // 3, col // 3)]:
                    return False
                row_dict[row].add(sudoku[row][col])
                col_dict[col].add(sudoku[row][col])
                box_dict[(row // 3, col // 3)].add(sudoku[row][col])
    if counter == 81:
        return "Victory"
    return True


def play(dif):
    if dif == "1":
        sudoku = make_sudoku(15)
        while not sudoku:
            sudoku = make_sudoku(15)
    elif dif == "2":
        sudoku = make_sudoku(25)
        while not sudoku:
            sudoku = make_sudoku(25)
    else:
        sudoku = make_sudoku(35)
        while not sudoku:
            sudoku = make_sudoku(35)
    mistake = 0
    game_time1 = time.time()

    while True:
        display(sudoku, -1, -1)

        y, x = input("\t\tEnter the y and x position or (-1) to exit: ").split(" ", 2)

        if y == "-1" or x == "-1":
            break
        if not x.isnumeric() or not y.isnumeric():
            continue

        x = int(x)
        y = int(y)

        if x < 1 or x > 9 or y < 1 or y > 9 or sudoku[y - 1][x - 1] != '.':
            continue

        display(sudoku, y, x)

        change_number = input("\t\tEnter the new number or (-1) to return: ")

        if not change_number.isnumeric():
            continue

        change_number = int(change_number)
        if change_number > 9 or change_number < 1:
            continue

        sudoku[y - 1][x - 1] = change_number

        game_state = validation(sudoku)

        if game_state == "Victory":
            clear()
            game_time2 = time.time()
            print(f"\n\n\t\tVictory is mine\n\t\tYour score is", int(1000000 / ((game_time2 - game_time1) * mistake)) if mistake != 0 else int(1000000 / (game_time2 - game_time1)))
            break
        elif not game_state:
            mistake += 1
            sudoku[y - 1][x - 1] = '.'


while True:
    print("\n\t\t\tSakamoto Sudoku Game TM")
    print("\n\t\t1- Play")
    print("\n\t\t2- Quit")

    option = input("\n\n\t\t\tEnter your option: ")

    if option == '1':
        clear()
        print("\n\t\t\tChoose the difficulty")
        print("\n\t\t1- Easy")
        print("\n\t\t2- Normal")
        print("\n\t\t3- Hard")
        print("\n\t\t4- Return to menu")

        difficulty = input("\n\n\t\t\tEnter your option: ")

        if difficulty == '1' or difficulty == '2' or difficulty == '3':
            play(difficulty)
        else:
            clear()
            continue

    elif option == '2':
        clear()
        print("\n\n\t\t\tThanks For Playing <3")
        break
    else:
        clear()
        print("\t\tEnter a valid option")
