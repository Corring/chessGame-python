from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import numpy as np


# determine which player's turn
def turn():
    check_for_winner();
    global times
    col = 0
    row = 0
    # player 1 turn
    if times % 2 == 0:
        for x in colList:
            for y in rowList:
                if player_list[row, col] != 1:
                    globals()[f"{x}_{y}_btn"]['state'] = DISABLED
                else:
                    globals()[f"{x}_{y}_btn"]['state'] = NORMAL
                row += 1
            row = 0
            col += 1
    # player 2 turn
    else:
        for x in colList:
            for y in rowList:
                if player_list[row, col] != 2:
                    globals()[f"{x}_{y}_btn"]['state'] = DISABLED
                else:
                    globals()[f"{x}_{y}_btn"]['state'] = NORMAL
                row += 1
            row = 0
            col += 1


def select(btn):
    global times, player_list, orgCol, orgRow, colList, rowList
    # determine which player's turn
    row = btn.grid_info()['row']  # Row of the button
    column = btn.grid_info()['column']  # column of the button
    print(f"now: {row}_{column}")
    if must_capture(row, column, times % 2):
        # capture and make opponent disappear
        if times % 2 == 0:
            globals()[f"{colList[mustCol]}_{rowList[mustRow]}"].set('X')
            player_list[mustRow, mustCol] = 1
            print(f"Change to X: {mustCol}_{mustRow}")
        else:
            globals()[f"{colList[mustCol]}_{rowList[mustRow]}"].set('O')
            player_list[mustRow, mustCol] = 2
            print(f"change to O :{mustCol}_{mustRow}")
        globals()[f"{colList[column]}_{rowList[row]}"].set(' ')
        player_list[row, column] = 0
        print(player_list)
        # continue move other pawn
    else:
        # highligt the button
        btn['bg'] = 'grey'
        # move pawn as the player like
        nextStep(btn, row, column)
        # make the allowable moved box to be clickable



def nextStep(btn, row, column):
    global times, colList, rowList
    if column < 7:
        if player_list[row, column + 1] == 0:
            globals()[f"{colList[column + 1]}_{rowList[row]}_btn"]['state'] = NORMAL
            globals()[f"{colList[column + 1]}_{rowList[row]}_btn"]['bg'] = 'yellow'
            globals()[f"{colList[column + 1]}_{rowList[row]}_btn"]['command'] = lambda: move(btn, globals()[
                f"{colList[column + 1]}_{rowList[row]}_btn"], row, column)
    if column > 0:
        if player_list[row, column - 1] == 0:
            globals()[f"{colList[column - 1]}_{rowList[row]}_btn"]['state'] = NORMAL
            globals()[f"{colList[column - 1]}_{rowList[row]}_btn"]['bg'] = 'yellow'
            globals()[f"{colList[column - 1]}_{rowList[row]}_btn"]['command'] = lambda: move(btn, globals()[
                f"{colList[column - 1]}_{rowList[row]}_btn"], row, column)
    if times % 2 == 0:
        if player_list[row-1,column] == 0:
            globals()[f"{colList[column]}_{rowList[row-1]}_btn"]['state'] = NORMAL
            globals()[f"{colList[column]}_{rowList[row-1]}_btn"]['bg'] = 'yellow'
            globals()[f"{colList[column]}_{rowList[row - 1]}_btn"]['command'] = lambda: move(btn, globals()[f"{colList[column]}_{rowList[row - 1]}_btn"], row, column)
    if times % 2 == 1:
        if player_list[row+1,column] == 0:
            globals()[f"{colList[column]}_{rowList[row+1]}_btn"]['state'] = NORMAL
            globals()[f"{colList[column]}_{rowList[row+1]}_btn"]['bg'] = 'yellow'
            globals()[f"{colList[column]}_{rowList[row + 1]}_btn"]['command'] = lambda: move(btn, globals()[f"{colList[column]}_{rowList[row + 1]}_btn"], row, column)


# move the pawn
def move(pre_btn, btn, prev_row, prev_col):
    global times, colList, rowList
    row = btn.grid_info()['row']  # Row of the button
    column = btn.grid_info()['column']  # column of the button
    # print(row, column)
    if (times % 2 == 0):
        player_list[row, column] = 1
        globals()[f"{colList[column]}_{rowList[row]}"].set('X')
    else:
        player_list[row, column] = 2
        globals()[f"{colList[column]}_{rowList[row]}"].set('O')
    player_list[prev_row, prev_col] = 0
    globals()[f"{colList[prev_col]}_{rowList[prev_row]}"].set('')
    print(player_list)
    # after move, check which player's turn
    times += 1
    for x in colList:
        for y in rowList:
            globals()[f"{x}_{y}_btn"]['bg'] = '#fff'
            globals()[f"{colList[column]}_{rowList[row]}_btn"]['command'] = lambda: select(
                globals()[f"{colList[column]}_{rowList[row]}_btn"])
    turn()


# determine whether pawn must capture or not
def must_capture(row, col, movingPlayer):
    global mustCol, mustRow
    if movingPlayer == 0:
        if col < 7 and player_list[row - 1, col + 1] == 2:
            mustCol = col + 1
            mustRow = row - 1
            print('must_capture')
            print(f"{mustRow}_{mustCol}")
            return True
        elif col > 1 and player_list[row - 1, col - 1] == 2:
            mustCol = col - 1
            mustRow = row - 1
            print(f"{mustRow}_{mustCol}")
            print('must_capture')
            return True
    else:
        if col > 1 and player_list[row + 1, col - 1] == 1:
            mustCol = col - 1
            mustRow = row + 1
            print('must_capture')
            return True
        elif col < 7 and player_list[row + 1, col + 1] == 1:
            mustCol = col + 1
            mustRow = row + 1
            print('must_capture')
            return True
    return False


# check who is the winner
def check_for_winner():
    global player_list
    # compare the winning condition
    for i in range(0,8):
        if player_list[0, i] == 1:
            messagebox.showinfo('winner', 'Player1 Win!')
        elif player_list[7, i] == 2:
            messagebox.showinfo('winner', 'Player2 Win!')



# main
window = Tk()
window.geometry("800x800")
window.resizable(True, True)
window.title("Ever Chess")

# times count how many times players drew
times = 0

# capture move
mustCol = 0
mustRow = 0
# orignal spot of the must moved pawn
orgCol = 0
orgRow = 0

# numpy matrix track players' pawns
player_list = np.zeros((8, 8))
player_list[6] = 1
player_list[1] = 2

# determine variable for each box
a_eight = StringVar()
a_eight_btn = Button(window, textvariable=a_eight, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(a_eight_btn))
a_seven = StringVar()
a_seven_btn = Button(window, textvariable=a_seven, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(a_seven_btn))
a_six = StringVar()
a_six_btn = Button(window, textvariable=a_six, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(a_six_btn))
a_five = StringVar()
a_five_btn = Button(window, textvariable=a_five, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(a_five_btn))
a_four = StringVar()
a_four_btn = Button(window, textvariable=a_four, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(a_four_btn))
a_three = StringVar()
a_three_btn = Button(window, textvariable=a_three, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(a_three_btn))
a_two = StringVar()
a_two_btn = Button(window, textvariable=a_two, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(a_two_btn))
a_one = StringVar()
a_one_btn = Button(window, textvariable=a_one, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(a_one_btn))
b_eight = StringVar()
b_eight_btn = Button(window, textvariable=b_eight, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(b_eight_btn))
b_seven = StringVar()
b_seven_btn = Button(window, textvariable=b_seven, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(b_seven_btn))
b_six = StringVar()
b_six_btn = Button(window, textvariable=b_six, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(b_six_btn))
b_five = StringVar()
b_five_btn = Button(window, textvariable=b_five, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(b_five_btn))
b_four = StringVar()
b_four_btn = Button(window, textvariable=b_four, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(b_four_btn))
b_three = StringVar()
b_three_btn = Button(window, textvariable=b_three, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(b_three_btn))
b_two = StringVar()
b_two_btn = Button(window, textvariable=b_two, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(b_two_btn))
b_one = StringVar()
b_one_btn = Button(window, textvariable=b_one, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(b_one_btn))
c_eight = StringVar()
c_eight_btn = Button(window, textvariable=c_eight, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(c_eight_btn))
c_seven = StringVar()
c_seven_btn = Button(window, textvariable=c_seven, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(c_seven_btn))
c_six = StringVar()
c_six_btn = Button(window, textvariable=c_six, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(c_six_btn))
c_five = StringVar()
c_five_btn = Button(window, textvariable=c_five, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(c_five_btn))
c_four = StringVar()
c_four_btn = Button(window, textvariable=c_four, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(c_four_btn))
c_three = StringVar()
c_three_btn = Button(window, textvariable=c_three, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(c_three_btn))
c_two = StringVar()
c_two_btn = Button(window, textvariable=c_two, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(c_two_btn))
c_one = StringVar()
c_one_btn = Button(window, textvariable=c_one, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(c_one_btn))
d_eight = StringVar()
d_eight_btn = Button(window, textvariable=d_eight, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(d_eight_btn))
d_seven = StringVar()
d_seven_btn = Button(window, textvariable=d_seven, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(d_seven_btn))
d_six = StringVar()
d_six_btn = Button(window, textvariable=d_six, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(d_six_btn))
d_five = StringVar()
d_five_btn = Button(window, textvariable=d_five, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(d_five_btn))
d_four = StringVar()
d_four_btn = Button(window, textvariable=d_four, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(d_four_btn))
d_three = StringVar()
d_three_btn = Button(window, textvariable=d_three, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(d_three_btn))
d_two = StringVar()
d_two_btn = Button(window, textvariable=d_two, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(d_two_btn))
d_one = StringVar()
d_one_btn = Button(window, textvariable=d_one, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(d_one_btn))
e_eight = StringVar()
e_eight_btn = Button(window, textvariable=e_eight, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(e_eight_btn))
e_seven = StringVar()
e_seven_btn = Button(window, textvariable=e_seven, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(e_seven_btn))
e_six = StringVar()
e_six_btn = Button(window, textvariable=e_six, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(e_six_btn))
e_five = StringVar()
e_five_btn = Button(window, textvariable=e_five, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(e_five_btn))
e_four = StringVar()
e_four_btn = Button(window, textvariable=e_four, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(e_four_btn))
e_three = StringVar()
e_three_btn = Button(window, textvariable=e_three, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(e_three_btn))
e_two = StringVar()
e_two_btn = Button(window, textvariable=e_two, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(e_two_btn))
e_one = StringVar()
e_one_btn = Button(window, textvariable=e_one, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(e_one_btn))
f_eight = StringVar()
f_eight_btn = Button(window, textvariable=f_eight, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(f_eight_btn))
f_seven = StringVar()
f_seven_btn = Button(window, textvariable=f_seven, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(f_seven_btn))
f_six = StringVar()
f_six_btn = Button(window, textvariable=f_six, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(f_six_btn))
f_five = StringVar()
f_five_btn = Button(window, textvariable=f_five, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(f_five_btn))
f_four = StringVar()
f_four_btn = Button(window, textvariable=f_four, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(f_four_btn))
f_three = StringVar()
f_three_btn = Button(window, textvariable=f_three, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(f_three_btn))
f_two = StringVar()
f_two_btn = Button(window, textvariable=f_two, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(f_two_btn))
f_one = StringVar()
f_one_btn = Button(window, textvariable=f_one, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(f_one_btn))
g_eight = StringVar()
g_eight_btn = Button(window, textvariable=g_eight, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(g_eight_btn))
g_seven = StringVar()
g_seven_btn = Button(window, textvariable=g_seven, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(g_seven_btn))
g_six = StringVar()
g_six_btn = Button(window, textvariable=g_six, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(g_six_btn))
g_five = StringVar()
g_five_btn = Button(window, textvariable=g_five, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(g_five_btn))
g_four = StringVar()
g_four_btn = Button(window, textvariable=g_four, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(g_four_btn))
g_three = StringVar()
g_three_btn = Button(window, textvariable=g_three, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(g_three_btn))
g_two = StringVar()
g_two_btn = Button(window, textvariable=g_two, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(g_two_btn))
g_one = StringVar()
g_one_btn = Button(window, textvariable=g_one, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(g_one_btn))
h_eight = StringVar()
h_eight_btn = Button(window, textvariable=h_eight, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(h_eight_btn))
h_seven = StringVar()
h_seven_btn = Button(window, textvariable=h_seven, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(h_seven_btn))
h_six = StringVar()
h_six_btn = Button(window, textvariable=h_six, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(h_six_btn))
h_five = StringVar()
h_five_btn = Button(window, textvariable=h_five, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(h_five_btn))
h_four = StringVar()
h_four_btn = Button(window, textvariable=h_four, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(h_four_btn))
h_three = StringVar()
h_three_btn = Button(window, textvariable=h_three, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(h_three_btn))
h_two = StringVar()
h_two_btn = Button(window, textvariable=h_two, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(h_two_btn))
h_one = StringVar()
h_one_btn = Button(window, textvariable=h_one, fg="black", width=10, height=5, bd=0, bg ="#fff",cursor="hand2", command=lambda: select(h_one_btn))

# generate chess gui
player1 = 'X'
player2 = 'O'
cur_row = 0
cur_col = 0
colList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
rowList = ['eight','seven','six','five','four','three','two','one']
for x in colList:
    for y in rowList:
        globals()[f"{x}_{y}_btn"].grid(row= cur_row, column= cur_col, padx=1, pady=1)
        # white (player 1) go first
        if (cur_row == 6):
            globals()[f"{x}_{y}"].set(player1)
            globals()[f"{x}_{y}_btn"]['state'] = NORMAL
        elif (cur_row == 1):
            globals()[f"{x}_{y}"].set(player2)
            globals()[f"{x}_{y}_btn"]['state'] = DISABLED
        else:
            globals()[f"{x}_{y}"].set('')
            globals()[f"{x}_{y}_btn"]['state'] = DISABLED
        cur_row += 1
    cur_row = 0
    cur_col += 1

window.mainloop()

