from math import inf as infinity
from random import choice
import platform
import time
from os import system


def evaluate(state): # Đánh giá trạng thái hiện tại của game
    if wins(state, COMP):
        value = +1 # Trả về 1 nếu người chơi win
    elif wins(state, HUMAN):
        value = -1 # Trả về -1 nếu máy tính win
    else:
        value = 0 # Trả về 0 nếu không thắng không thua (hoà game hoặc game chưa kết thúc)

    return value


def wins(state, player): # Kiểm tra các điều kiện để thắng
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False


def game_over(state): # Kết thúc game, kiểm tra xem người thắng là Player hay Computer
    return wins(state, HUMAN) or wins(state, COMP) # Trả về True nếu Player hoặc Computer win


def empty_cells(state): # Gán tất cả các ô trống vào một list (mỗi ô trống được thể hiện bằng 1 toạ độ cụ thể)
    """
    Each empty cell will be added into cells' list
    :param state: the state of the current board
    :return: a list of empty cells
    """
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0: # Nếu cell == 0 tức ô đó còn trống
                cells.append([x, y]) # thêm toạ độ của ô trống đó vào list cells tạo trước

    return cells


def valid_move(x, y): # Kiểm tra xem ô lựa chọn vào có phải là ô trống không, nếu có trả về True, nếu không trả về False
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def set_move(x, y, player):
    if valid_move(x, y): # Nếu (x,y) hợp lệ (ô đó còn trống)
        board[x][y] = player # Gán giá trị toạ độ tương ứng của list board với player hiện tại (có thể là X hoặc O)
        return True
    else:
        return False


def minimax(state, depth, player):
    if depth == 0 or game_over(state): # Kiểm tra trạng thái của game, nếu không còn ô trống hoặc kết thúc game thì trả về kết quả game
        value = evaluate(state)
        return [0, 0, value]
    
    if player == HUMAN: # Tương ứng với Max
        best = [-1, -1, -infinity] # gán với giá trị nhỏ nhất có thể, đảm bảo rằng tìm được giá trị nào cũng sẽ lớn hơn giá trị này
        for cell in empty_cells(state): # Duyệt qua từng ô trống
            x, y = cell[0], cell[1] # gán x,y tức toạ độ tương ứng của ô trống đang duyệt ở vòng lặp đó
            state[x][y] = player # state[x][y] = 1
            value = minimax(state, depth - 1, -player)
            state[x][y] = 0
            value[0], value[1] = x, y
            if value[2] > best[2]:
                best = value 
        
    elif player == COMP: # Tương ứng với Min
        best = [-1, -1, +infinity] # gán với giá trị lớn nhất có thể, đảm bảo rằng tìm được giá trị nào cũng sẽ nhỏ hơn giá trị này
        for cell in empty_cells(state): # Duyệt qua từng ô trống
            x, y = cell[0], cell[1] # gán x,y tức toạ độ tương ứng của ô trống đang duyệt ở vòng lặp đó
            state[x][y] = player # state[x][y] = -1
            value = minimax(state, depth - 1, -player)
            state[x][y] = 0
            value[0], value[1] = x, y
            if value[2] < best[2]:
                best = value  

    return best


def clean():
    """
    Clears the console
    """
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def render(state, c_choice, h_choice):
    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


def ai_turn(c_choice, h_choice):
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board): # Kiểm tra trạng thái của game, nếu không còn ô trống hoặc kết thúc game thì kết thúc lượt
        return

    clean()
    print(f'Computer turn [{c_choice}]')
    render(board, c_choice, h_choice)

    if len(empty_cells(board)) == 9: # Bảng còn đầy đủ ô trống, dành cho khi lượt đầu tiên là của Computer 
        x = choice([0, 1, 2]) # Chọn một toạ độ x tuỳ ý
        y = choice([0, 1, 2]) # Chọn một toạ độ y tuỳ ý
    else: # Bảng không còn đủ 9 ô trống (xay ra khi Computer không đi lượt đầu tiên hoặc trong quá trình chơi)
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]

    set_move(x, y, COMP)


def human_turn(c_choice, h_choice):
    # Từ điển cho các bước di chuyển hợp lệ
    move = 0
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    clean()
    print(f"Human turn [{h_choice}]")
    render(board, c_choice, h_choice)

    while not 1 <= move <= 9:
        try:
            move = int(input("Select (1..9): ")) # Nhập lựa chọn
            coordinates = moves[move] # Xác định toạ độ ô ứng với lựa chọn
            can_move = set_move(coordinates[0], coordinates[1], HUMAN)

            if not can_move:
                print("Bad move")
                move = 0
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')


def main():
    global HUMAN, COMP, board
    HUMAN = +1 # Max
    COMP = -1 # Min
    board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    ]
    """
    Main function that calls all functions
    """
    clean() # Làm sạch màn hình terminal
    h_choice = ''  # X or O
    c_choice = ''  # X or O
    first = ''  # if human is the first

    # Human chooses X or O to play
    while h_choice != 'O' and h_choice != 'X': # Khi h_choice khác O và X (người chơi chưa nhập lựa chọn hoặc lựa chọn không đúng)
        try:
            print()
            h_choice = input('Choose X or O\nChosen: ').strip().upper()
        except (EOFError, KeyboardInterrupt): # người dùng nhập ctrl+d và ctrl+c (2 lựa chọn phổ biến khi muốn ngắn chương trình đang chạy ngay)
            print('Bye')
            exit()
        except (KeyError, ValueError): # người dùng nhập sai key và value
            print('Bad choice')

    # Setting computer's choice
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    # Human may starts first
    clean()
    while first != 'Y' and first != 'N': # Kiểm tra xem người dùng có nhập đúng yêu cầu không, nếu không thì nhập lại hoặc báo lỗi nếu có lỗi xảy ra
        try:
            first = input('First to start?[y/n]: ').strip().upper() # Hỏi xem có người chơi muốn đi trước hay đi sau
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Vòng lặp sự kiện game
    while len(empty_cells(board)) > 0 and not game_over(board): # Khi game vẫn còn ô trống hoặc game chưa kết thúc
        if first == "N":
            ai_turn(c_choice, h_choice)
            first = ''
        elif first == "Y":
            human_turn(c_choice, h_choice) # Lượt Player
            ai_turn(c_choice, h_choice) # Lượt Computer

    # Game over message
    if wins(board, HUMAN):
        clean()
        print(f'Human turn [{h_choice}]')
        render(board, c_choice, h_choice)
        print('YOU WIN!')
    elif wins(board, COMP):
        clean()
        print(f'Computer turn [{c_choice}]')
        render(board, c_choice, h_choice)
        print('YOU LOSE!')
    else:
        clean()
        render(board, c_choice, h_choice)
        print('DRAW!')

    exit()


if __name__ == '__main__':
    main()
