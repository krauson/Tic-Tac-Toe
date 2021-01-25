#upload 50
def print_board(board):
    
    temp_board = board.copy()
    
    i = 0
    while i < len(temp_board):
    
        temp_board[i] = "  ".join(temp_board[i])
        i += 1
    
    temp_board = "\n".join(temp_board)
    
    print(temp_board)
    
    return

def is_cell_empty(places , board):


    if board[places[0]][places[1]] != '-':
        print(f"Cell ({places[0]}, {places[1]}) is taken, use other")
        print_board(board)
        return False

    else:
        return True


def places_are_valid(places):


    line_num = places[0]
    column_num = places[1]

    # places are between 0 - 2

    if (0 > line_num) or 2 < line_num:
        print(f"Invalid line chosen ({line_num}).")
        return False

    if (0 > column_num) or 2 < column_num:
        print(f"Invalid column chosen ({column_num}).")
        print(places)
        return False

    return True


def convert_to_int_list(param_str):


    num_list = param_str.split()

    i = 0
    while i < len(num_list):

        num_list[i] = int(num_list[i])
        i += 1

    return num_list

def make_turn(player_char,board):

    places = input(f"Player '{player_char}' Please choose a cell:")

#   convert to list of ints
    places = convert_to_int_list(places)

    print(places)

    if places_are_valid(places) and is_cell_empty(places , board):

        board[places[0]][places[1]] = player_char
        print_board(board)
        return  board

    else:
        return make_turn(player_char, board)


def check_board(board):


        i = 0
        while i < len(board):

            if board[i][0] == board[i][1] == board[i][2] and board[i][0] != '-':
                return board[i][0]
            i += 1

        # checking if there is win in one of the columns

        i = 0
        while i < len(board):

            if board[0][i] == board[1][i] == board[2][i] and board[0][i] != '-':
                return board[0][i]
            i += 1

        # checking if there is win in one of the crosses

        if board[0][0] == board[1][1] == board[2][2] and board[1][1] != '-':
            return board[0][0]

        elif board[0][2] == board[1][1] == board[2][0] and board[1][1] != '-':
            return board[0][2]

        else:
            return ''


def tic_tac_toe():


    moves_counter = 0

    board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]

    player_char = 'O'
    
    print_board(board)

    while check_board(board) == '' and moves_counter < 9:

        if moves_counter % 2 == 0:

            player_char = 'O'

        else:

            player_char = 'X'

        board = make_turn(player_char, board)

        moves_counter += 1


    if check_board(board) == '':
        print("It's a tie!")

    else:
        print(f"The winner is: {player_char}")

    answer = input("press y if you want to play another game: ")

    if answer == "y":
        tic_tac_toe()

    else:
        print("Goodbye! I hope you enjoyed:)")
        return


tic_tac_toe()