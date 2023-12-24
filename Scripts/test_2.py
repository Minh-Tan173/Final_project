import copy
import sys
import pygame
from math import inf as infinity

# Screen infor
WIDTH = 720
HEIGHT = 720    

# Board infor
WidthBoard = 600
HeightBoard = 600
LineSize = 5
columnBoard = 4
rowBoard = 4
board_position = (60, 60)
color = "#FFFFFF"
SQSIZE = WidthBoard // 4
Dist_SaB = board_position[0] # distance between top left of screen and top left of board

# Text infor
pygame.font.init()
NameGame_font = pygame.font.Font(r"C:\Users\admin\OneDrive\Máy tính\final exam\font\Agbalumo-Regular.ttf", 50) # Tên game hiển thị ở menu
fig_font = pygame.font.Font(r"C:\Users\admin\OneDrive\Máy tính\final exam\font\LithosPro-Black.ttf", 120) # Kích thước X, O
FinalState_font = pygame.font.Font(r"C:\Users\admin\OneDrive\Máy tính\final exam\font\Agbalumo-Regular.ttf", 50)
gui_font = pygame.font.Font(r"C:\Users\admin\OneDrive\Máy tính\final exam\font\Agbalumo-Regular.ttf", 23)

# --- PYGAME SETUP ---

pygame.init()

    # Load icon and title game 
pygame.display.set_caption("Tic tac toe")
icon = pygame.image.load(r"C:\Users\admin\OneDrive\Máy tính\final exam\asset\icon.png")
pygame.display.set_icon(icon)

    # Load background
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
background = pygame.image.load(r"C:\Users\admin\OneDrive\Máy tính\final exam\asset\background.png").convert_alpha()
screen.blit(background, (-300, 0))
    
    # Load button 
button = pygame.image.load(r"C:\Users\admin\OneDrive\Máy tính\final exam\asset\button.png").convert_alpha() # load ảnh button (image)
button_pressed = pygame.image.load(r"C:\Users\admin\OneDrive\Máy tính\final exam\asset\buttonPressed.png").convert_alpha()
width_button = button.get_width() # Nhận chiều dài của button image
height_button = button.get_height() # Nhận chiều dài của button image
Button_text = ["Start game", "Quit game", "Reset game"] # Các loại button xuất hiện ở menu


class Board:
    def __init__(self):
        self.squares = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
        ]

        self.marked_sqrs = 0 # biến marked_sqrs lưu trữ số lượng những ô đã được chọn

    def final_state(self, show = False, board_pos = board_position):
        '''
        return 0 if there is no win yet
        return 1 if player 1 wins
        return -1 if player -1 wins
        '''
        line_color = None
        line_width = 5

        # Chiến thắng theo hàng:
        for row in self.squares:
            row_index = self.squares.index(row) # index của row trong squares
            if row[0] == row[1] == row[2] == row[3] and not row[0] == 0:
                if show:
                    if row[0] == 1: # Đại diện cho người chiến thắng là human
                        line_color = "#944df5"
                    elif row[0] == -1: # Đại diện cho người chiến thắng là computer
                        line_color = "#f6fad0"
                    
                    start_pos = (board_pos[0], row_index * SQSIZE + Dist_SaB + SQSIZE//2)
                    end_pos = (WIDTH -  Dist_SaB, row_index * SQSIZE + Dist_SaB + SQSIZE//2)
                    pygame.draw.line(screen, line_color, start_pos, end_pos, line_width)
                
                return self.squares[row_index][0] # Trả về trạng thái chiến thắng, 1 nếu là human, -1 nếu là computer
        
        # Chiến thắng theo cột:
        col_0 = [] # Lưu trữ giá trị cột 1 trong square
        col_1 = [] # Lưu trữ giá trị cột 2 trong square
        col_2 = [] # Lưu trữ giá trị cột 3 trong square
        
        for row in self.squares:
            col_0.append(row[0])
            col_1.append(row[1])
            col_2.append(row[2])
        
        column = [col_0, col_1, col_2] # Lưu trị giá trị từng cột trong square
        for col in column:
            if col[0] == col[1] == col[2] == col[3] and not col[0] == 0:
                if show:
                    if col[0] == 1: # Đại diện cho người chiến thắng là human
                        line_color = "#944df5"
                    elif col[0] == -1: # Đại diện cho người chiến thắng là computer
                        line_color = "#f6fad0"

                    start_pos = (column.index(col) * SQSIZE + SQSIZE//2 + Dist_SaB, board_pos[1])
                    end_pos = (column.index(col) * SQSIZE + SQSIZE//2 + Dist_SaB, HEIGHT - Dist_SaB)
                    pygame.draw.line(screen, line_color, start_pos, end_pos, line_width)
                
                return col[0]
        
        # Chiến thắng theo hàng chéo
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] == self.squares[3][3] and not self.squares[0][0] == 0:
            if show:
                if col[0] == 1: # Đại diện cho người chiến thắng là human
                    line_color = "#944df5"
                elif col[0] == -1: # Đại diện cho người chiến thắng là computer
                    line_color = "#f6fad0"
            
                start_pos = (board_pos)
                end_pos = (WIDTH - Dist_SaB, HEIGHT - Dist_SaB)
                pygame.draw.line(screen, line_color, start_pos, end_pos, line_width)
            
            return self.squares[0][0]
        
        if self.squares[0][3] == self.squares[1][2] == self.squares[2][1] == self.squares[3][0] and not self.squares[0][3] == 0:
            if show:
                if col[0] == 1: # Đại diện cho người chiến thắng là human
                    line_color = "#944df5"
                elif col[0] == -1: # Đại diện cho người chiến thắng là computer
                    line_color = "#f6fad0"
            
                start_pos = (WIDTH - Dist_SaB, board_pos[1])
                end_pos = (board_pos[0], HEIGHT - Dist_SaB)
                pygame.draw.line(screen, line_color, start_pos, end_pos, line_width)
            
            return self.squares[0][2]           

        # Chưa chiến thắng
        return 0

    def mark_sqr(self, row, col, player): # Nhập lựa chọn vào squares
        self.squares[row][col] = player
        self.marked_sqrs += 1 # Số lượng ô được chọn tăng thêm 1

    def Is_empty(self, row, col): # Kiểm tra xem ô lựa chọn còn trống hay không, nếu còn trống trả về True
        if self.squares[row][col] == 0:
            return True
        
        return False

    def get_empty_sqrs(self): # Nhận toàn bộ ô trống còn lại
        empty_sqrs = []
        for index_row, row in enumerate(self.squares):
            for index_column, column in enumerate(self.squares):
                if self.squares[index_row][index_column] == 0:
                    empty_sqrs.append([index_row, index_column]) # Kiểm tra xem board còn những ô trống nào, nếu ô nào còn trống thì gán toạ độ [hàng, cột] của nó vào list empty_sprite
        
        return empty_sqrs

    def isFull(self):
        return self.marked_sqrs == 16 # Nếu số lượng ô được chọn == 9 (toàn bộ các ô đã được chọn) thì trả về True

    def isempty(self):
        return self.marked_sqrs == 0 # Nếu chưa ô nào được chọn thì trả về True


class AI:

    def __init__(self, level = 1, player=-1):
        self.level = level
        self.player = player

    def minimax(self, board,depth,  maximizing):
        
        # terminal case
        case = board.final_state()

        # player 1 wins
        if case == 1:
            return 1, None # eval, move

        # player 2 wins
        if case == -1:
            return -1, None # Trả về best_move = None vì trạng thái game đã kết thúc, không tiếp tục chơi được

        # draw
        elif board.isFull():
            return 0, None
        
        if depth == 0:
            return 0, None

        if maximizing: # người chơi cực đại hoá
            max_value = -infinity
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                value = self.minimax(temp_board, depth - 1, False)[0]
                if value > max_value:
                    max_value = value
                    best_move = (row, col)

            return max_value, best_move

        elif not maximizing: # người chơi cực tiểu hoá
            min_value = infinity
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                value = self.minimax(temp_board, depth - 1, True)[0]
                if value < min_value:
                    min_value = value
                    best_move = (row, col)

            return min_value, best_move

    def eval(self, main_board):
        eval, move = self.minimax(main_board, 6,  False)
        print(f"AI has chosen to mark the square in pos {move} with an eval of: {eval}")

        return move # row, col


class Button: 
    def __init__(self, text, image, image_Pressed, Position, width, height, scale, elevation):
        # Top left rect
        self.image = pygame.transform.scale(image, (width * scale, height * scale)) # Biến self.image nhận image được scale lại theo tỉ lệ scale biết trước
        self.image_rect = self.image.get_rect() # tạo một collider hình chữ nhật kích thước bằng image để tương tác với image
        self.image_rect.topleft = (Position) # Xác định toạ độ của collider hình chữ nhật
        self.Position = Position # Toạ độ mà image sẽ được vẽ
                
        # text
        self.text = gui_font.render(text, True, "#FFFFFF") # custom chữ trên bề mặt button, 3 tham số truyền vào gồm text, Có khử răng cưa chữ hay không (True), màu chữ (màu trắng)
        self.text_rect = self.text.get_rect(center = self.image_rect.center) # vị trí đặt văn bản đã render ở trên (tâm collider)
        
        # Core attributes
        self.Clicked = False
        
    def draw(self):        
        screen.blit(self.image, self.Position)
        screen.blit(self.text, self.text_rect) # Vẽ chữ lên trên image
        
    def IsCollider(self):
        self.action = False
        
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos() # lấy toạ độ của con trỏ chuột theo thời gian thực
        
        # Check if the mouse pointer over the image
        if self.image_rect.collidepoint(mouse_pos): # Kiểm tra xem con trỏ chuột có đang nằm (tiếp xúc) với collider hay chưa
            self.mouse_button = pygame.mouse.get_pressed() # Trả về trạng thái của chuột, bình thường là [false, false, false] với index = 0 là trạng thái chuột trái, i = 1 là trạng thái con lăn chuột, i = 2 là trạng thái chuột phải, nếu nhấn nút nào thì giá trị sẽ trả về True tương ứng
            if self.mouse_button[0] == True and self.Clicked == False: # Nếu nhấn chuột trái và nhấn chuột trái được một lần
                self.Clicked = True # Đã nhấn  
                print(self.Clicked)
                self.action = True # Khởi tạo hành động
                
                return self.action
        
        if pygame.mouse.get_pressed()[0] == False: # Nếu chưa nhấn chuột trái lần nào
            self.Clicked = False # Chưa nhấn
        

class Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1   #1-cross  #2-circles
        self.running = True

        # Text fig
        self.X_fig = fig_font.render("X", True, "#944df5")
        self.O_fig = fig_font.render("O", True, "#f6fad0")
        
    # -- DRAW --
    def draw_Menu(self):
        # Load name game
        self.NameGame = NameGame_font.render("TIC TAC TOE", True, "#F5F5F5")
        
        # Load button
        start_pos = (50, 360) # Toạ độ nút Start
        start_button = Button(Button_text[0], button, button_pressed, start_pos, width_button, height_button, 0.3, 4)
        
        quit_pos = (350, 360) # Toạ độ nút Quit
        quit_button = Button(Button_text[1], button, button_pressed, quit_pos, width_button, height_button, 0.3, 4)
        
        # --DRAW--
        screen.blit(self.NameGame, (60,100))
        
        # Start button
        start_button.draw()
        if start_button.IsCollider():
            main(MenuRunning = False)
        
        # Quit button
        quit_button.draw()
        if quit_button.IsCollider():
            pygame.quit()
            sys.exit()
    
    def draw_FinalNotification(self, FinalText, GameState):
        # Notification rect infor:
        self.width_Rect = 300 + 50
        self.Height_Rect = 300
        self.pos_Rect = (((WIDTH - self.Height_Rect) // 2), ((WIDTH - self.Height_Rect) // 2) - 50)  
        self.color_rect = "#00FFFF"
        
        # Final text notification
        if GameState == 1:
            self.FinalText = FinalState_font.render(FinalText, True, "#FFFFFF") # Nếu người chơi thắng thì in chữ màu trắng
        elif GameState == -1:
            self.FinalText = FinalState_font.render(FinalText, True, "#FF0033") # Nếu computer thắng thì in chữ màu đỏ
        elif GameState == 0:
            self.FinalText = FinalState_font.render(FinalText, True, "#00EE00") # Nếu draw thì in chữ màu xanh lá
        
        self.pos_Text = (self.pos_Rect[0] + 55, self.pos_Rect[1] + 20)
        
        # Type of button
        quit_pos = (self.pos_Rect[0] + 70, self.pos_Rect[1] + 250)
        quit_button = Button(Button_text[1], button, button_pressed, quit_pos, width_button, height_button, 0.2, 4)
        
        reset_pos = (self.pos_Rect[0] + 70, self.pos_Rect[1] + 200)
        reset_button = Button(Button_text[2], button, button_pressed, reset_pos, width_button, height_button, 0.2, 4)
                
        # Bảng trạng thái
        pygame.draw.rect(screen, self.color_rect, (self.pos_Rect, (self.Height_Rect, self.width_Rect)), border_radius = 10)
        screen.blit(self.FinalText, self.pos_Text)
        
        # Draw button
        reset_button.draw()
        if reset_button.IsCollider():
            self.ResetGame() # Cập nhật lại chỉ số game về ban đầu
            main(MenuRunning = False) # Đệ quy lại hàm main (chạy lại hàm main từ đầu sau khi nhấn vào Reset game)
        
        quit_button.draw()
        if quit_button.IsCollider():
            pygame.quit()
            sys.exit()
       

    def DrawBoard(self,  WidthBoard, HeightBoard, LineSize, column, row, position, color):
        # Board infor
        self.WidthBoard = WidthBoard
        self.HeightBoard = HeightBoard
        self.SizeBoard = (self.WidthBoard, self.HeightBoard)
        self.LineSize = LineSize
        self.column = column
        self.row = row
        self.position = position
        self.color = color
        
        
        # Draw board
        pygame.draw.rect(screen, self.color, (self.position, self.SizeBoard), width = self.LineSize,  border_radius = 20)
        
        for i in range(1, 4):
            Vline_pos = [(i * SQSIZE + Dist_SaB, self.position[1]), (i * SQSIZE + Dist_SaB, HEIGHT - Dist_SaB)]
            pygame.draw.line(screen, self.color, Vline_pos[0], Vline_pos[1], width=self.LineSize)
        
        Vline2_pos = [(SQSIZE*2 + Dist_SaB, self.position[1]), (SQSIZE*2 + Dist_SaB, HEIGHT - Dist_SaB)]
        pygame.draw.line(screen, self.color, Vline2_pos[0], Vline2_pos[1], width= self.LineSize)
        
        # Horizon line
        for i in range(1, 4):
            Hline_pos = [(self.position[0], i * SQSIZE + Dist_SaB), (WIDTH - Dist_SaB, i * SQSIZE + Dist_SaB)]
            pygame.draw.line(screen, self.color, Hline_pos[0], Hline_pos[1], width=self.LineSize)    
    

    def draw_fig(self, collumn, row):
        if self.player == 1: # Nếu là lượt của người chơi
            self.center_x = (collumn * SQSIZE + SQSIZE//2 + self.position[0], row * SQSIZE + SQSIZE//2 + self.position[1]) # Toạ độ tâm của ô trống click chuột vào
            self.Sprite_Pos_x = (self.center_x[0] - SQSIZE//2, self.center_x[1] - SQSIZE//2) # Toạ độ cột, hàng (toạ độ Top_Left) của ô trống click chuột vào
            self.TopRect_x = pygame.Rect(self.Sprite_Pos_x, (SQSIZE, SQSIZE)) # Tạo một object kiểu Rect - 1 colider lấy kích thước toạ độ ứng với ô trống click vào
            self.text_rect_x = self.X_fig.get_rect(center = self.TopRect_x.center) # Cập nhật lại toạ độ tâm của Text_fig
            screen.blit(self.X_fig, self.text_rect_x)  
        
        elif self.player == -1: # Nếu là lượt của computer
            self.center_o = (collumn * SQSIZE + SQSIZE//2 + self.position[0], row * SQSIZE + SQSIZE//2 + self.position[1]) # Toạ độ tâm của ô trống click chuột vào
            self.Sprite_Pos_o = (self.center_o[0] - SQSIZE//2, self.center_o[1] - SQSIZE//2) # Toạ độ cột, hàng (toạ độ Top_Left) của ô trống click chuột vào
            self.TopRect_o = pygame.Rect(self.Sprite_Pos_o, (SQSIZE, SQSIZE)) # Tạo một object kiểu Rect - 1 colider lấy kích thước toạ độ ứng với ô trống click vào
            self.text_rect_o = self.X_fig.get_rect(center = self.TopRect_o.center) # Cập nhật lại toạ độ tâm của Text_fig
            screen.blit(self.O_fig, self.text_rect_o) 

    # --- OTHER METHODS ---

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(col, row)
        self.next_turn()

    def next_turn(self):
        self.player = self.player * (-1)
        
    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isFull()
    
    def ResetGame(self):
        # Đặt lại trạng thái game bằng cách tạo mới các đối tượng cần thiết
        self.board = Board()
        self.ai = AI()
        self.player = 1
        self.running = True

        # Đặt lại màn hình
        screen.blit(background, (-300, 0))
        self.DrawBoard(WidthBoard, HeightBoard, LineSize, columnBoard, rowBoard, board_position, color)

        # Cập nhật màn hình
        pygame.display.update()
                    

def main(MenuRunning = True):
    # --- Game objects ---
    game = Game()    
    board = game.board # Biến board là object của class Board
    ai = game.ai # Biến ai là object của class AI
    
    FinalText, GameState = None, None

    if MenuRunning:
        running = True
        while running:
            for event in pygame.event.get():
    
                # quit event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            game.draw_Menu()
        
            pygame.display.update()
    
    else:
        screen.blit(background, (-300, 0))
        game.DrawBoard(WidthBoard, HeightBoard, LineSize, columnBoard, rowBoard, board_position, color)

        # --- Game loop ---
        while True:
            for event in pygame.event.get():
                # quit event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # click event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    Clicked_pos = event.pos
                    row = (Clicked_pos[1] - 60) // SQSIZE
                    col = (Clicked_pos[0] - 60) // SQSIZE
                    if board_position[0] <= Clicked_pos[0] <= (HEIGHT - board_position[0]):
                        if board_position[1] <= Clicked_pos[1] <= (WIDTH - board_position[1]):
                            # human mark sqr
                            if board.Is_empty(row, col) and game.running:
                                game.make_move(row, col)

                                if game.isover():
                                    # Trạng thái cuối cùng của game
                                    if board.isFull():
                                        FinalText = "Draw!"
                                        GameState = 0
                                        game.running = False
                                    else:
                                        if board.final_state(show=True) == 1:
                                            FinalText = "You win"
                                            GameState = 1
                                            game.running = False

            # AI initial call
            if game.player == ai.player and game.running:

                # update the screen
                pygame.display.update()

                # eval
                row, col = ai.eval(board)
                game.make_move(row, col)

                if game.isover():
                    if board.isFull():
                        FinalText = "Draw!"
                        GameState = 0
                        game.running = False
                    else:
                        if board.final_state(show=True) == -1:
                            FinalText = "You lose!"
                            GameState = -1
                            game.running = False

            # Bảng thông báo sau khi kết thúc game
            if game.running == False:
                game.draw_FinalNotification(FinalText=FinalText, GameState=GameState)

            pygame.display.update()

if __name__ == "__main__":
    main()
