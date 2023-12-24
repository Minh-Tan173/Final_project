import pygame
from time import sleep

# Biến toàn cục
h_Max = 1 # Trạng thái Max
c_Min = -1 # Trạng thái Min
Draw = 0 # Trạng thái khi hoà game

# Khởi tạo màn hình game
pygame.init()
width = 720
height = 720
screen_size = (width, height) # (x,y)
screen = pygame.display.set_mode(screen_size) # Khởi tạo cửa sổ game, dài 800 pixel, rộng 720 pixel
gui_font = pygame.font.Font(r"C:\Users\admin\OneDrive\Máy tính\final exam\font\Agbalumo-Regular.ttf", 23) # (font path, font size)


class Button():
    def __init__(self, text, image, image_Pressed, Position, width, height, scale, elevation):
        # Top rectangle
        self.image = pygame.transform.scale(image, (width * scale, height * scale)) # Biến self.image nhận image được scale lại theo tỉ lệ scale biết trước
        self.image_rect = self.image.get_rect() # tạo một collider hình chữ nhật kích thước bằng image để tương tác với image
        self.image_rect.topleft = (Position) # Xác định toạ độ của collider hình chữ nhật
        self.Position = Position # Toạ độ mà image sẽ được vẽ
        
        # Bottom rectangle
        self.image_Pressed = pygame.transform.scale(image_Pressed, (width * scale, height * scale))
        
        # text
        self.text = gui_font.render(text, True, "#FFFFFF") # custom chữ trên bề mặt button, 3 tham số truyền vào gồm text, Có khử răng cưa chữ hay không (True), màu chữ (màu trắng)
        self.text_rect = self.text.get_rect(center = self.image_rect.center) # vị trí đặt văn bản đã render ở trên (tâm collider)
        
        # core attributes
        self.Clicked = False # Kiểm tra xem đã nhấn chuột hay chưa
        self.elevation = elevation
        self.dynamic_elevaton = elevation
        self.original_image_center = self.image_rect.center # Toạ độ tâm nguyên bản
        
    
    def draw(self):
        if self.Clicked == False: # Nếu chưa nhấn thì vẽ lên màn hình button
            screen.blit(self.image, self.Position) # Vẽ image ra màn hình game
        else: # nếu Clicked == True tức là đã nhấn lên button thì vẽ lên màn hình button_presssed
            screen.blit(self.image_Pressed, self.Position)
        
        # Elevation text logic
        self.coordinates = list(self.text_rect.center)
        self.coordinates[1] = self.original_image_center[1] - self.dynamic_elevaton
        self.text_rect.center = self.coordinates
        screen.blit(self.text, self.text_rect) # Vẽ chữ lên trên image
        
        # pygame.draw.rect(screen, (255, 0, 0), self.image_rect, 2) # Hiển thị collider xung quanh button image
        # pygame.draw.rect(screen, (255, 0, 0), self.text_rect, 2) # Hiển thị collider xung quanh text image
    
    def IsCollider(self):
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos() # lấy toạ độ của con trỏ chuột theo thời gian thực
        
        # Check if the mouse pointer over the image
        if self.image_rect.collidepoint(mouse_pos): # Kiểm tra xem con trỏ chuột có đang nằm (tiếp xúc) với collider hay chưa
            self.mouse_button = pygame.mouse.get_pressed() # Trả về trạng thái của chuột, bình thường là [false, false, false] với index = 0 là trạng thái chuột trái, i = 1 là trạng thái con lăn chuột, i = 2 là trạng thái chuột phải, nếu nhấn nút nào thì giá trị sẽ trả về True tương ứng
            
            if self.mouse_button[0] and self.Clicked == False: # Nếu nhấn chuột trái và nhấn chuột trái được một lần
                self.dynamic_elevaton = 0
                self.Clicked = True # Đã nhấn   
                self.action = True # Khởi tạo hành động 
                return self.action
            
            if not self.mouse_button[0]: # Nếu chưa nhấn chuột trái lần nào
                self.dynamic_elevaton = self.elevation
                self.Clicked = False # Chưa nhấn

class TicTacToe_game():
    def __init__(self):
        # Size board
        self.WidthBoard = 600
        self.HeightBoard = 600
        self.SizeBoard = (self.WidthBoard, self.HeightBoard)
        
        # Position board
        self.X_pos = 40
        self.Y_pos = 60
        self.pos = (self.X_pos, self.Y_pos)
        
        self.DrawBoard()
        
    def DrawBoard(self):
        pygame.draw.rect(screen, "#FFFFFF", (self.pos, self.SizeBoard), width = 10)
        pygame.display.update()
        

def main():
    menu()

    
def menu():
    # Load Background
    background = pygame.image.load(r"C:\Users\admin\OneDrive\Máy tính\final exam\asset\background.png")
    test = pygame.image.load(r"C:\Users\admin\OneDrive\Máy tính\final exam\asset\353613432_948536942905927_6475526066104574156_n (1).jpg")
    
    # Load Icon and Title game
    icon = pygame.image.load(r"C:\Users\admin\OneDrive\Máy tính\final exam\asset\icon.png").convert_alpha()
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Cờ caro")
    
    # Load button 
    button = pygame.image.load(r"C:\Users\admin\OneDrive\Máy tính\final exam\asset\button.png").convert_alpha() # load ảnh button (image)
    button_pressed = pygame.image.load(r"C:\Users\admin\OneDrive\Máy tính\final exam\asset\buttonPressed.png").convert_alpha()
    width_button = button.get_width() # Nhận chiều dài của button image
    height_button = button.get_height() # Nhận chiều dài của button image
    menu_text = ["Start game", "Quit game"] # Các loại button xuất hiện ở menu
    
    # Type of button
    start_pos = (50, 360) # Toạ độ nút Start
    start_button = Button(menu_text[0], button, button_pressed, start_pos, width_button, height_button, 0.3, 4)
    
    quit_pos = (350, 360) # Toạ độ nút Quit
    quit_button = Button(menu_text[1], button, button_pressed, quit_pos, width_button, height_button, 0.3, 4)
    
    # Vòng lặp trạng thái game
    Running = True
    Start_Game = True
    while Running:
        for event in pygame.event.get(): # Lần lượt lặp qua các sự kiện trong game (từ trước cho đến khi gọi hàm)
            if event.type == pygame.QUIT: # Nếu phát hiện sự kiện QUIT (người dùng đóng cửa sổ) thì mới ngừng chạy chương trình
                Running = False
                
        screen.blit(background, (-300,0)) # Vẽ background lên màn hình, toạ độ vẽ là (-300,0)
        
        # Kiểm tra trạng thái màn hình game (Gồm màn hình game và màn hình menu)
        start_button.draw() # Vẽ start button lên màn hình
        start_button.IsCollider()
        if start_button.IsCollider(): # Nếu click vào start button thì:
            print("Start")
                
        quit_button.draw() # vẽ quit button lên màn hình
        if quit_button.IsCollider(): # Nếu nhấn vào button Quit game thì kết thúc game ngay lập tức
            print("Quit!")
            Running = False
        
        pygame.display.flip() # Thủ tục cần thiết sau khi vẽ lên màn hình, cập nhật lại toàn bộ màn hình
        
    

if __name__ == "__main__":
    main()
            