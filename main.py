import numpy as np
import time

sudokuBoard = None


def is_valid_guess(sudoku, x, y, guess):
	#check row and col
	for i in range(9):
		if sudoku[y][i] == guess or sudoku[i][x] == guess:
			return False
	box_x = (x // 3) * 3
	box_y = (y // 3) * 3

	#check for the element's own 3x3 grid, to see there is no repeats
	for i in range(3):
		for j in range(3):
			if sudoku[box_y + i][box_x + j] == guess: 
				return False

	return True

def get_possibilities(sudoku, x, y):
	possible_nums = []
	for i in range(1, 10):
		if is_valid_guess(sudoku, x, y, i):
			possible_nums.append(i)
	return possible_nums

def choose_max_row_col(arr, orientation):
	row_col = {}
	for elems in arr:
		direction = elems[orientation] #0 for columns, 1 for rows
		for options in elems[2]:
			if direction in row_col:
				if options not in row_col[direction]:
					row_col[direction].append(options)
			else:
				row_col[direction] = [options]
			
	max_len = 0
	out = None

	for keys in row_col:
		if len(row_col[keys]) > max_len:
			max_len = len(row_col[keys])
			out = keys
	return out

def get_min(arr):
	min_idx = 0
	for idx, elems in enumerate(arr):
		if len(elems[2]) < len(arr[min_idx][2]):
			min_idx = idx
	return arr[min_idx]

def find_empty_spots(sudoku):
	possibilities = []
	for y in range(9):
		for x in range(9):
			if sudoku[y][x] == 0:
				all_possibilities = get_possibilities(sudoku, x, y)
				if len(all_possibilities) == 1:
					return [x, y, all_possibilities]
				possibilities.append([x, y, all_possibilities])

	if len(possibilities) == 0: 
		return False

	max_len = len(get_min(possibilities)[2])
	to_maximize = list(filter(lambda x: len(x[2]) == max_len, possibilities))

	if len(to_maximize[0][2]) == 0:
		return to_maximize[0]	# if the algorithm gets stuck and has no possible options to continue, return this to the backtrack 
								# function as it will return false, causing the function to backtrack
	max_row = choose_max_row_col(to_maximize, 1)
	maximized_row = list(filter(lambda x: x[1] == max_row, to_maximize))

	max_col = choose_max_row_col(to_maximize, 0)
	maximized_col = list(filter(lambda x: x[0] == max_col, maximized_row))

	if len(maximized_col) == 0:
		return get_min(maximized_row)
	return get_min(maximized_col)

def backTrack(sudoku, possibilities):
	global sudokuBoard
	if not find_empty_spots(sudoku):
		sudokuBoard = np.copy(sudoku)
		return True
	x, y = possibilities[0], possibilities[1]
	for guesses in possibilities[2]:
		sudoku[y][x] = guesses
		if backTrack(sudoku, find_empty_spots(sudoku)):
			return True
	sudoku[y][x] = 0
	return False

def sudoku_solver(sudoku):
	begin = time.process_time()
	if backTrack(sudoku.tolist(), find_empty_spots(sudoku)):
		print(f"This sudoku took {time.process_time() - begin}s to complete")
		return sudokuBoard
	print(f"This sudoku took {time.process_time() - begin}s to complete")
	return np.ones((9,9)) * -1

sudoku = np.array([
 [0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0]])
print(sudoku_solver(sudoku))
