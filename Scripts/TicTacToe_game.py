import pygame
from os import system
from math import inf as infinity
import random
import copy

def main():
    pygame.init()
    
    # Load screen game
    width_screen = 720
    height_screen = 720
    global screen
    screen = pygame.display.set_mode((width_screen, height_screen))
    
    # Load background
    background = pygame.image.load(r"C:\Users\admin\OneDrive\Máy tính\final exam\asset\background.png").convert_alpha()
    
    # Text infor
    global fig_font
    fig_font = pygame.font.Font(r"C:\Users\admin\OneDrive\Máy tính\final exam\font\LithosPro-Black.otf", 150)
    
    # Board infor
    WidthBoard = 600
    HeightBoard = 600
    LineSize = 5
    column = 3
    row = 3
    board_position = (60, 60)
    color = "#FFFFFF"
    
    global SquareSize
    SquareSize = WidthBoard // row # Kích thước một cạnh ô vuông trong board
    
    # Background
    screen.blit(background, (-300, 0))
    
    # Vẽ bảng lên màn hình vào tạo bảng tương ứng trên terminal
    game = TicTacToe_game(WidthBoard, HeightBoard, LineSize, column, row, board_position, color)
    game.DrawBoard() # Vẽ bảng lên màn hình
    T_Board = game.GameBoard # Tạo bảng tương ứng trên terminal
    
    # Ai object
    ai_turn = game.Ai
    
    # Human object
    player_turn = None
    
    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Human turn    
            if event.type == pygame.MOUSEBUTTONDOWN: # Nếu phát hiện sự kiện người dùng nhấn chuột
                # print(event.pos)
                ClickedPosition = event.pos # Gán biến ClickedPosition với toạ độ nhấn chuột hiện tại, ứng với (x,y) tức (toạ độ cột, toạ độ hàng)
                col_pos = (ClickedPosition[0] - 60) // SquareSize # Chuyển đổi toạ độ y pixel tương ứng thành vị trí cột trong board
                row_pos = (ClickedPosition[1] - 60) // SquareSize # Chuyển đổi toạ độ x pixel tương ứng thành vị trí hàng trong board 
    
                if board_position[0] <= ClickedPosition[0] <= (height_screen - board_position[0]): # Nếu click chuột trong toạ độ cột 60 <= toạ độ cột chuột <= (720-60)
                    if board_position[1] <= ClickedPosition[1] <= (width_screen - board_position[1]): # Nếu click chuột trong toạ độ 60 <= toạ độ hàng chuột <= (720-60)
                        if T_Board.IsEmpty(row_pos, col_pos): # Nếu ô click vào còn trống
                            system("cls")
                            T_Board.mark_choice(row_pos, col_pos, game.player) # Nhập lựa chọn vào terminal board
                            game.draw_fig(col_pos, row_pos) # Hiện thị lựa chọn trên game screen
                            game.next_turn() # Tới lượt tiếp theo
                            print(T_Board)
            
            if game.player == -1: # Khi self.player == -1
                system("cls")
                pygame.display.update()
                depth = len(T_Board.Get_EmptySprite()) # khởi tạo độ sâu thuật toán (tương ứng với số lượng ô trống còn lại)
                if not T_Board.IsFull():
                    row_pos, col_pos = ai_turn.eval(T_Board)
                    T_Board.mark_choice(row_pos, col_pos, game.player)
                    game.draw_fig(col_pos, row_pos)
                    game.next_turn()

            pygame.display.update()


class Board:
    def __init__(self):
        self.TerminalBoard = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        ]
    
    def mark_choice(self, row, column, player): # Nhập lựa chọn của người chơi
        self.TerminalBoard[row][column] = player # Thay thế ô hiện tại bằng giá trị đại diện cho người chơi
        
    def IsEmpty(self, row, column): # Kiểm tra xem ô click vào còn trống hay không
        if self.TerminalBoard[row][column] == 0:
            return True
        
    def Get_EmptySprite(self):
        empty_sprite = []
        for index_row, row in enumerate(self.TerminalBoard):
            for index_column, column in enumerate(self.TerminalBoard):
                if self.TerminalBoard[index_row][index_column] == 0:
                    empty_sprite.append([index_row, index_column]) # Kiểm tra xem board còn những ô trống nào, nếu ô nào còn trống thì gán toạ độ [hàng, cột] của nó vào list empty_sprite

        return empty_sprite
    
    def IsFull(self): # Nếu bảng không còn ô nào trống thì trả về True
        depth = len(self.Get_EmptySprite())
        if depth == 0:
            return True
    
    def Final_State(self): # Kiểm tra điều kiện chiến thắng
        """ 
        return 1 if human win
        return 0 if not win yet or draw
        return -1 if computer win
        """
        self.column0 = [] # Biến column lưu trữ giá trị cột 0 trong bảng
        self.column1 = [] # Biến column lưu trữ giá trị cột 1 trong bảng
        self.column2 = [] # Biến column lưu trữ giá trị cột 2 trong bảng
        
        # Chiến thắng theo hàng:
        for row in self.TerminalBoard: # Duyệt qua từng hàng của bảng
            if self.TerminalBoard[0] == self.TerminalBoard[1] == self.TerminalBoard[2] and not self.TerminalBoard == 0:
                return self.TerminalBoard
        
        # Chiến thắng theo cột:
        for row in self.TerminalBoard: # tìm giá trí nằm ở từng cột 0,1,2
            self.column0.append(row[0])
            self.column1.append(row[1])
            self.column2.append(row[2])
        if self.column0[0] == self.column0[1] == self.column0[2] and not self.column0[0] == 0:
            return self.column0[0]
        elif self.column1[0] == self.column1[1] == self.column1[2] and not self.column1[0] == 0:
            return self.column1[0]
        elif self.column2[0] == self.column2[1] == self.column2[2] and not self.column2[0] == 0:
            return self.column2[2]
        
        # Chiến thắng theo đường chéo
        if self.TerminalBoard[0][0] == self.TerminalBoard[1][1] == self.TerminalBoard[2][2] and not self.TerminalBoard == 0:
            return self.TerminalBoard[0][0]
        if self.TerminalBoard[2][2] == self.TerminalBoard[1][1] == self.TerminalBoard[2][0] and not self.TerminalBoard == 0:
            return self.TerminalBoard[2][2]
        
        return 0
        
    def __str__(self):
        text_line1 = f"[{self.TerminalBoard[0][0]}, {self.TerminalBoard[0][1]}, {self.TerminalBoard[0][2]}]"
        text_line2 = f"[{self.TerminalBoard[1][0]}, {self.TerminalBoard[1][1]}, {self.TerminalBoard[1][2]}]"
        text_line3 = f"[{self.TerminalBoard[2][0]}, {self.TerminalBoard[2][1]}, {self.TerminalBoard[2][2]}]"
        
        return f"{text_line1}\n{text_line2}\n{text_line3}"
  
  
class AI_turn:
    def __init__(self, level=1, player=-1):
        self.level = level
        self.player = player

    # --- RANDOM ---

    def minimax(self, board, maximizing):
        
        # terminal case
        case = board.final_state()

        # player 1 wins
        if case == 1:
            return 1, None # eval, move

        # player 2 wins
        if case == -1:
            return -1, None

        # draw
        elif board.Isfull():
            return 0, None

        if maximizing:# Người chơi cực đại
            max_eval = - infinity
            best_move = None
            empty_sqrs = board.Get_EmptySprite()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing: # Người chơi cực tiểu
            min_eval = infinity
            best_move = None
            empty_sqrs = board.Get_EmptySprite()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board) # tạo 1 bản sao độc lập của terminal board
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move
            
    def eval(self, main_board):
        eval, move = self.minimax(main_board)
        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')
            
        return move # row, col

            
class TicTacToe_game:
    def __init__(self, WidthBoard, HeightBoard, LineSize, column, row, position, color):
        # Board infor
        self.WidthBoard = WidthBoard
        self.HeightBoard = HeightBoard
        self.SizeBoard = (self.WidthBoard, self.HeightBoard)
        self.LineSize = LineSize
        self.column = column
        self.row = row
        self.position = position
        self.color = color
        
        # Terminal board
        self.GameBoard = Board()
        self.player = 1 # Người chơi
               
        # Text_Fig
        self.X_fig = fig_font.render("X", True, "#944df5")
        self.O_fig = fig_font.render("O", True, "#f6fad0")
        
        # Ai player
        self.Ai = AI_turn()
        
    def DrawBoard(self):
        pygame.draw.rect(screen, self.color, (self.position, self.SizeBoard), width = self.LineSize,  border_radius = 20)
        
        # Vertical line   
        pygame.draw.line(screen, self.color, (260, 60), (260, 660), width= self.LineSize)
        pygame.draw.line(screen, self.color, (460, 60), (460, 660), width= self.LineSize)
        
        # Horizon line
        pygame.draw.line(screen, self.color, (60, 260), (660, 260), width= self.LineSize)
        pygame.draw.line(screen, self.color, (60, 460), (660, 460), width= self.LineSize)

    def draw_fig(self, collumn, row):
        if self.player == 1: # Nếu là lượt của người chơi
            self.center_x = (collumn * SquareSize + SquareSize//2 + self.position[0], row * SquareSize + SquareSize//2 + self.position[1]) # Toạ độ tâm của ô trống click chuột vào
            self.Sprite_Pos_x = (self.center_x[0] - SquareSize//2, self.center_x[1] - SquareSize//2) # Toạ độ cột, hàng (toạ độ Top_Left) của ô trống click chuột vào
            self.TopRect_x = pygame.Rect(self.Sprite_Pos_x, (SquareSize, SquareSize)) # Tạo một object kiểu Rect - 1 colider lấy kích thước toạ độ ứng với ô trống click vào
            self.text_rect_x = self.X_fig.get_rect(center = self.TopRect_x.center) # Cập nhật lại toạ độ tâm của Text_fig
            screen.blit(self.X_fig, self.text_rect_x)  
        
        elif self.player == -1: # Nếu là lượt của computer
            self.center_o = (collumn * SquareSize + SquareSize//2 + self.position[0], row * SquareSize + SquareSize//2 + self.position[1]) # Toạ độ tâm của ô trống click chuột vào
            self.Sprite_Pos_o = (self.center_o[0] - SquareSize//2, self.center_o[1] - SquareSize//2) # Toạ độ cột, hàng (toạ độ Top_Left) của ô trống click chuột vào
            self.TopRect_o = pygame.Rect(self.Sprite_Pos_o, (SquareSize, SquareSize)) # Tạo một object kiểu Rect - 1 colider lấy kích thước toạ độ ứng với ô trống click vào
            self.text_rect_o = self.X_fig.get_rect(center = self.TopRect_o.center) # Cập nhật lại toạ độ tâm của Text_fig
            screen.blit(self.O_fig, self.text_rect_o) 
        
    def next_turn(self):
        self.player = self.player*(-1)
        
        

if __name__ == "__main__":
    main()