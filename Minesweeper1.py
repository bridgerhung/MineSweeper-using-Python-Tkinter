import tkinter as tk
import random
from tkinter import messagebox
import sys
import time  # Add this import
from tkinter import simpledialog  # Add this import

def generateRandomBoard(rows, col, num_mines):
    # Generate a board with the specified number of mines
    board = [['E' for _ in range(col)] for _ in range(rows)]
    mines_placed = 0
    while mines_placed < num_mines:
        i = random.randint(0, rows - 1)
        j = random.randint(0, col - 1)
        if board[i][j] == 'E':
            board[i][j] = 'M'
            mines_placed += 1
    return [board, num_mines]


def numberMineBoard(board):
    vis = [["0" for _ in range(len(board[0]))] for _ in range(len(board))]
    numberOfRows = len(board)
    numberOfColumns = len(board[0])
    for i in range(0, numberOfRows):
        for j in range(0, numberOfColumns):
            if board[i][j] == "M":
                vis[i][j] = "M"
                for drow in range(-1, 2):
                    for dcol in range(-1, 2):
                        nrow = i + drow
                        ncol = j + dcol
                        if nrow >= 0 and nrow < numberOfRows and ncol >= 0 and ncol < numberOfColumns:
                            if board[nrow][ncol] == "M":
                                continue
                            tmp = int(vis[nrow][ncol]) + 1
                            vis[nrow][ncol] = str(tmp)

    return vis


def dfs(row, col, board, actualBoard, vis, buttons):
    vis[row][col] = 1
    board[row][col] = "B"
    buttons.add(len(board[0]) * row + col)
    for drow in range(-1, 2):
        for dcol in range(-1, 2):
            nrow = row + drow
            ncol = col + dcol
            if nrow >= 0 and nrow < len(board) and ncol >= 0 and ncol < len(board[0]) and not vis[nrow][ncol]:
                if actualBoard[nrow][ncol] == "0":
                    dfs(nrow, ncol, board, actualBoard, vis, buttons)
                else:
                    board[nrow][ncol] = actualBoard[nrow][ncol]
                    buttons.add(len(board[0]) * nrow + ncol)


def checkSpaces(mineCount, board, actualBoard, buttons):
    cnt = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 'E':
                cnt += 1
    if cnt == mineCount:
        for i in range(len(board)):
            for j in range(len(board[0])):
                val = i*len(board[0]) + j
                if actualBoard[i][j] == 'M':
                    buttons[val].config(text="", bg="#76EEC6", state=tk.DISABLED, borderwidth=1,)
        return True
    return False


def markMinesAtEnd(board, actualBoard, buttons,disabledbuttons):
    for i in range(len(board)):
        for j in range(len(board[0])):
            val = i*len(board[0]) + j
            color = "red"
            if actualBoard[i][j] == 'M':
                if val in disabledbuttons:
                    color = "#E3CF57"
                    disabledbuttons.remove(val)
                label_text = actualBoard[i][j]  # Get the text from the label
                buttons[val].config(text=label_text,
                                                 bg=color, state=tk.DISABLED, borderwidth=1,)
    for i in disabledbuttons:
        buttons[i].config(text="X", bg="#C1CDCD", state=tk.DISABLED, borderwidth=1,)

def playerClicks(crow, ccol, board, actualBoard, vis, mineCount, buttons, buttonsClear, disabledbuttons):
    if actualBoard[crow][ccol] == "M":
        markMinesAtEnd(board, actualBoard, buttons,disabledbuttons)
        return "Lost"
    elif actualBoard[crow][ccol] != "0":
        board[crow][ccol] = actualBoard[crow][ccol]
    else:
        dfs(crow, ccol, board, actualBoard, vis, buttonsClear)
    if checkSpaces(mineCount, board, actualBoard, buttons):
        return "Win"

    return "Cont"


def create_board(board, actualBoard, coordinates, vis, buttonsclear, mineCount, dimensions):
    n = len(board)  # Number of rows
    m = len(board[0])  # Number of columns
    dimOfRow = dimensions[0][0]
    dimOfCol = dimensions[0][1]
    disabledbuttons = []

    def close():
        print("Closing, Thanks for Playing!")
        root.destroy()
        sys.exit()
    
    def handle_left_click(value, buttons):
        # Handle left mouse button click (reveal logic)
        if value == -1:  # Check if the "New Board" button is pressed
            root.destroy()  # Close the current main window
            backToMainMenu()  # Return to main menu for new settings
        
        button = buttons[value]
        row = coordinates[value][0]
        col = coordinates[value][1]

        if value not in disabledbuttons:
            # Check if button 1 is clicked
            if playerClicks(row, col, board, actualBoard, vis, mineCount,  buttons, buttonsclear, disabledbuttons) == "Lost":
                # Display a pop-up dialog with "Yes" and "No" buttons
                response = messagebox.askyesno(
                    "Game Over", " You Lost\n Do you want to replay?", icon='warning')
                if response:  # If "Yes" is clicked
                    root.destroy()  # Close the current main window
                    details = generateRandomBoard(dimOfRow, dimOfCol)
                    newboard = details[0]
                    newmineCount = details[1]
                    create_board(makeGameboard(newboard), numberMineBoard(newboard), makeCoordinates(
                        newboard), makeVisited(newboard), buttonsclear, newmineCount, dimensions)  # Create a new board
                else:
                    close()
            elif playerClicks(row, col, board, actualBoard, vis, mineCount,  buttons, buttonsclear,disabledbuttons) == 'Win':
                buttonlabel = actualBoard[row][col]
                button.config(text=buttonlabel, bg="lightblue",
                            state=tk.DISABLED, borderwidth=1,)
                response = messagebox.askyesno(
                    "You Won!", " You Cleared all the mines\n Do you want to replay?", icon='info')
                if response:  # If "Yes" is clicked
                    root.destroy()  # Close the current main window
                    details = generateRandomBoard(dimOfRow, dimOfCol)
                    newboard = details[0]
                    newmineCount = details[1]
                    create_board(makeGameboard(newboard), numberMineBoard(newboard), makeCoordinates(
                        newboard), makeVisited(newboard), buttonsclear, newmineCount, dimensions)  # Create a new board
                else:
                    close()

            else:
                playerClicks(row, col, board, actualBoard, vis,
                            mineCount,  buttons, buttonsclear,disabledbuttons)
                buttonlabel = actualBoard[row][col]
                button.config(text=buttonlabel, bg="lightblue",
                            state=tk.DISABLED, borderwidth=1,)  # Disable the button
                for button_index in buttonsclear:
                    label_text = actualBoard[coordinates[button_index]
                                            [0]][coordinates[button_index][1]]
                    if label_text == "0":
                        label_text = " "
                    buttons[button_index].config(
                        text=label_text, bg="lightblue", state=tk.DISABLED, borderwidth=1,)
                buttonsclear.clear()

    def handle_right_click(value, buttons):
        # Handle right mouse button click (flag logic)
        button = buttons[value]
        row = coordinates[value][0]
        col = coordinates[value][1]
        buttonlabel = actualBoard[row][col]
        if value not in disabledbuttons:
            button.config(text='F', fg="red",  borderwidth=1,)
            disabledbuttons.append(value)
        else:
            button.config(text=" ", fg="red",  borderwidth=1,)
            disabledbuttons.remove(value)
    
    def closeExisting():
        root.destroy()
        backToMainMenu()

    # Create a new main window
    root = tk.Tk()
    root.title("Minesweeper")

    # Create a label widget
    label = tk.Label(root, text="")
    label.grid(row=0, column=0, columnspan=m)
    # Create multiple buttons with fixed size and unique values
    buttons = []
    colors = ["#F0FFFF", "#C1CDCD"]
    start = 0
    for i in range(n):
        for j in range(m):
            value = i * m + j
            cbg = colors[start]
            button = tk.Button(
            root,
            text=f" ",
            width=4,  # Adjust the width as needed
            height=2,  # Adjust the height as needed
            borderwidth=1,
            bg=cbg  # Adjust the background color as needed
            )
            button.bind("<Button-1>",lambda event, value=value: handle_left_click(value, buttons))
            button.bind("<Button-3>", lambda event, value=value: handle_right_click(value, buttons))
            buttons.append(button)
            button.grid(row=i+1, column=j, padx=0, pady=0)
            start = not start
        if m % 2 == 0:
            colors = colors[::-1]
    # Add a "New Board" button

    new_board_button = tk.Button(root, text="New Board")
    new_board_button.bind("<Button-1>",lambda event, value=value: handle_left_click(-1, buttons))
    new_board_button.grid(row=n+1, columnspan=m+1,  padx=10, pady=10)
    # Create the additional button
    additional_button = tk.Button(root, text="Main Menu", command= lambda: closeExisting())
    additional_button.grid(row=n+3, column=0, columnspan=m, padx=10, pady=5)

    start_time = time.time()
    timer_label = tk.Label(root, text="Time: 0")
    timer_label.grid(row=0, column=0, columnspan=m)

    def update_timer():
        elapsed_time = int(time.time() - start_time)
        if elapsed_time <= 999:
            timer_label.config(text=f"Time: {elapsed_time}")
            root.after(1000, update_timer)

    update_timer()

    root.protocol("WM_DELETE_WINDOW", close)
    # Start the Tkinter event loop
    root.mainloop()

# Create the initial board

def makeCoordinates(board):
    coordinates = {}
    for i in range(len(board)):
        for j in range(len(board[0])):
            coordinates[i*len(board[0]) + j] = (i, j)
    return coordinates


def makeVisited(board):
    vis = [[0 for _ in range(len(board[0]))] for _ in range(len(board))]
    return vis


def makeGameboard(board):
    gameboard = [['E' for _ in range(len(board[0]))]
                 for _ in range(len(board))]
    return gameboard

def backToMainMenu():
    dimensions = []
    def left_click(value):
        # Prompt user for custom width, height, and number of mines
        width = simpledialog.askinteger("寬度", "請輸入遊戲寬度 (5-35):", minvalue=5, maxvalue=35)
        height = simpledialog.askinteger("高度", "請輸入遊戲高度 (5-35):", minvalue=5, maxvalue=35)
        max_mines = width * height - 1
        num_mines = simpledialog.askinteger("地雷數", f"請輸入地雷數量 (1-{max_mines}):", minvalue=1, maxvalue=max_mines)
        dimensions.append([height, width, num_mines])
        root.destroy()
    
    def on_closing():
    # This function will be called when the window is closed
        root.destroy()
        sys.exit()

    # Create the main application window
    root = tk.Tk()
    root.title("Minesweeper")

    # Set window size
    window_width = 400
    window_height = 200
    root.geometry(f"{window_width}x{window_height}")

    # Place the window in the center of the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"+{x}+{y}")

    # Create buttons for easy, medium, and hard
    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)

    easy_button = tk.Button(button_frame, text="Easy",
                            padx=20, pady=10, command=lambda: left_click(1))
    medium_button = tk.Button(
        button_frame, text="Medium", padx=20, pady=10, command=lambda: left_click(2))
    hard_button = tk.Button(button_frame, text="Hard",
                            padx=20, pady=10, command=lambda: left_click(3))

    easy_button.grid(row=0, column=0, padx=10)
    medium_button.grid(row=0, column=1, padx=10)
    hard_button.grid(row=0, column=2, padx=10)

    # Create instruction label with "i" symbol (info)
    instruction_label = tk.Label(
        root, text="Instructions: \nLeft-click to choose difficulty \n\n i) Left-click to reveal \nii) Right-click to flag (F) \niii) Beaware of the Mines! (M)")
    instruction_label.pack()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    # Start the Tkinter event loop
    root.mainloop()

    details = generateRandomBoard(dimensions[0][0], dimensions[0][1], dimensions[0][2])
    board = details[0]
    mineCount = dimensions[0][2]

    
    buttonsclear = set()
    create_board(makeGameboard(board), numberMineBoard(board), makeCoordinates(
        board), makeVisited(board), buttonsclear, mineCount, dimensions)


backToMainMenu()
