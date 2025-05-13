import sys
import pygame
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from algorithms import solve_with_algorithm
import random
from collections import defaultdict

def generate_random_puzzle():
    # Tạo một puzzle ngẫu nhiên có thể giải được
    numbers = list(range(9))  # [0,1,2,3,4,5,6,7,8]
    random.shuffle(numbers)
    
    # Kiểm tra xem puzzle có thể giải được không
    inversions = 0
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] != 0 and numbers[j] != 0 and numbers[i] > numbers[j]:
                inversions += 1
    
    # Nếu số nghịch đảo là lẻ, puzzle không thể giải được
    # Trong trường hợp đó, ta đổi chỗ hai số khác 0 để tạo puzzle có thể giải được
    if inversions % 2 == 1:
        # Tìm hai số khác 0 để đổi chỗ
        non_zero = [i for i in range(len(numbers)) if numbers[i] != 0]
        if len(non_zero) >= 2:
            i, j = random.sample(non_zero, 2)
            numbers[i], numbers[j] = numbers[j], numbers[i]
    
    return numbers

initial_state = [2,6,5,
                 0,8,7,
                 4,3,1]

goal_state = [1, 2, 3,
              4, 5, 6,
              7, 8, 0]

initial_state2 = [1, 2, 3,
                 4, 5, 6,
                 0, 7, 8]

initial_state3 = [1, 2, 3,
                4, 5, 6,
                7, 0, 8]

initial_state4 = [
    [1, 2, 3],
    [5, 0, 6],
    [4, 7, 8]
]

def show_solution_with_pygame(solution, cost, execution_time):
    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    font = pygame.font.Font(None, 72)  
    move_font = pygame.font.Font(None, 36)  
    info_font = pygame.font.Font(None, 48)  # Font mới cho thông tin
    clock = pygame.time.Clock()
    
    cell_size = 120  
    board_size = cell_size * 3
    start_x = 50  
    start_y = (800 - board_size) // 2
    
    moves = []
    for i in range(len(solution)-1):
        current = solution[i]
        next_state = solution[i+1]
        empty_pos = current.index(0)
        next_empty = next_state.index(0)
        diff = next_empty - empty_pos
        if diff == 1: moves.append("Right")
        elif diff == -1: moves.append("Left")
        elif diff == 3: moves.append("Down")
        elif diff == -3: moves.append("Up")
    
    for state_idx, state in enumerate(solution):
        screen.fill((255, 255, 255))
        
        # Vẽ bảng puzzle
        for i in range(3):
            for j in range(3):
                val = state[i * 3 + j]
                x = start_x + j * cell_size
                y = start_y + i * cell_size
                
                if val == 0:
                    pygame.draw.rect(screen, (255, 0, 0), (x, y, cell_size, cell_size))  
                else:
                    pygame.draw.rect(screen, (255, 255, 255), (x, y, cell_size, cell_size)) 
                
                pygame.draw.rect(screen, (0, 0, 0), (x, y, cell_size, cell_size), 3) 
                if val != 0:
                    text = font.render(str(val), True, (0, 0, 0))
                    text_rect = text.get_rect(center=(x + cell_size//2, y + cell_size//2))
                    screen.blit(text, text_rect)
        
        # Hiển thị thông tin thời gian và chi phí
        info_x = start_x + board_size + 30
        info_y = start_y - 100  # Vị trí phía trên bảng puzzle
        
        # Hiển thị thời gian
        time_text = f"Time: {execution_time:.2f}s"
        time_surface = info_font.render(time_text, True, (0, 0, 0))
        screen.blit(time_surface, (info_x, info_y))
        
        # Hiển thị chi phí
        cost_text = f"Cost: {cost}"
        cost_surface = info_font.render(cost_text, True, (0, 0, 0))
        screen.blit(cost_surface, (info_x, info_y + 50))
        
        # Hiển thị số bước
        steps_text = f"Steps: {state_idx}/{len(solution)-1}"
        steps_surface = info_font.render(steps_text, True, (0, 0, 0))
        screen.blit(steps_surface, (info_x, info_y + 100))
        
        # Hiển thị các bước di chuyển
        move_x = start_x + board_size + 30 
        move_y = start_y + board_size//2  
        
        header = move_font.render("Moves:", True, (0, 0, 0))
        screen.blit(header, (move_x, move_y - 50))
        
        move_text = ", ".join(moves[:state_idx+1])
        text = move_font.render(move_text, True, (0, 0, 0))

        max_width = 1000 - move_x - 50 
        if text.get_width() > max_width:
            words = moves[:state_idx+1]
            lines = []
            current_line = []
            current_width = 0

            for idx, word in enumerate(words):
                word_text = move_font.render(word, True, (0, 0, 0))
                add_width = word_text.get_width()
                if current_line:
                    add_width += move_font.render(", ", True, (0, 0, 0)).get_width()
                if current_width + add_width < max_width:
                    current_line.append(word)
                    current_width += add_width
                else:
                    lines.append(", ".join(current_line))
                    current_line = [word]
                    current_width = word_text.get_width()
            if current_line:
                lines.append(", ".join(current_line))

            for i, line in enumerate(lines):
                text = move_font.render(line, True, (0, 0, 0))
                screen.blit(text, (move_x, move_y + i * 40))
        else:
            screen.blit(text, (move_x, move_y))
        
        pygame.display.flip()
        pygame.time.delay(300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        clock.tick(30) 
    
    pygame.quit()

class AlgorithmInfo:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.results = defaultdict(list)  # {algorithm_name: [(time, cost), ...]}
    
    def add_result(self, algorithm, time, cost):
        self.results[algorithm].append((time, cost))
    
    def get_average_time(self, algorithm):
        times = [t for t, _ in self.results[algorithm]]
        return sum(times) / len(times) if times else 0
    
    def get_average_cost(self, algorithm):
        costs = [c for _, c in self.results[algorithm]]
        return sum(costs) / len(costs) if costs else 0

class InfoDialog(QtWidgets.QDialog):
    def __init__(self, algorithm_info, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thông tin thuật toán")
        self.setMinimumSize(400, 300)
        
        layout = QtWidgets.QVBoxLayout(self)
        
        # Tạo bảng
        table = QtWidgets.QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Thuật toán", "Số lần chạy", "Thời gian TB (s)", "Chi phí TB"])
        
        # Thêm dữ liệu
        algorithms = sorted(algorithm_info.results.keys())
        table.setRowCount(len(algorithms))
        
        for i, algo in enumerate(algorithms):
            results = algorithm_info.results[algo]
            if results:
                avg_time = algorithm_info.get_average_time(algo)
                avg_cost = algorithm_info.get_average_cost(algo)
                
                table.setItem(i, 0, QtWidgets.QTableWidgetItem(algo))
                table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(len(results))))
                table.setItem(i, 2, QtWidgets.QTableWidgetItem(f"{avg_time:.3f}"))
                table.setItem(i, 3, QtWidgets.QTableWidgetItem(f"{avg_cost:.1f}"))
        
        table.resizeColumnsToContents()
        layout.addWidget(table)
        
        # Nút đóng
        close_button = QtWidgets.QPushButton("Đóng")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

class PuzzleApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("puzzle_solver_gui.ui", self)
        
        # Tạo widget chính và layout
        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QtWidgets.QVBoxLayout(main_widget)
        
        # Layout cho phần trên (nút tạo mới và hiển thị ma trận)
        top_layout = QtWidgets.QHBoxLayout()
        
        # Nút tạo puzzle mới
        self.newPuzzleButton = QtWidgets.QPushButton("Tạo Puzzle Mới")
        self.newPuzzleButton.setMinimumWidth(150)
        self.newPuzzleButton.clicked.connect(self.generate_new_puzzle)
        top_layout.addWidget(self.newPuzzleButton)
        
        # Nút thông tin
        self.infoButton = QtWidgets.QPushButton("Thông tin")
        self.infoButton.setMinimumWidth(150)
        self.infoButton.clicked.connect(self.show_info)
        top_layout.addWidget(self.infoButton)
        
        # Label hiển thị ma trận
        self.matrixLabel = QtWidgets.QLabel()
        self.matrixLabel.setWordWrap(True)
        self.matrixLabel.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.matrixLabel.setStyleSheet("QLabel { padding: 10px; }")
        top_layout.addWidget(self.matrixLabel)
        
        # Thêm top layout vào main layout
        main_layout.addLayout(top_layout)
        
        # Layout cho phần chọn thuật toán
        algo_layout = QtWidgets.QHBoxLayout()
        algo_label = QtWidgets.QLabel("Chọn thuật toán:")
        self.algorithmComboBox = QtWidgets.QComboBox()
        self.algorithmComboBox.addItems([
            "BFS", "DFS", "Greedy", "Iterative", "IDDFS", "A*", "UCS", "SA", "Beam", "HC", "SHC", "SAHC", "AND_OR",
            "No_Observation", "Partial_Observation", "Genetic", "Backtracking", "ForwardTracking", "Stochastic_HC", "QLearning",
            "IDA*", "IDS", "Random_HC", "Min_Conflicts"
        ])
        algo_layout.addWidget(algo_label)
        algo_layout.addWidget(self.algorithmComboBox)
        main_layout.addLayout(algo_layout)
        
        # Nút bắt đầu giải
        self.startButton = QtWidgets.QPushButton("Bắt đầu giải")
        self.startButton.clicked.connect(self.run_solver)
        main_layout.addWidget(self.startButton)
        
        # Label hiển thị kết quả
        self.resultLabel = QtWidgets.QLabel()
        self.resultLabel.setWordWrap(True)
        self.resultLabel.setAlignment(Qt.AlignCenter)
        self.resultLabel.setStyleSheet("QLabel { padding: 10px; }")
        main_layout.addWidget(self.resultLabel)
        
        # Thiết lập kích thước cửa sổ tối thiểu
        self.setMinimumSize(600, 400)
        
        # Khởi tạo trạng thái ban đầu và thông tin thuật toán
        self.current_state = initial_state
        self.algorithm_info = AlgorithmInfo()
        self.update_matrix_display(initial_state)
        self.resultLabel.setText("Chọn thuật toán và nhấn 'Bắt đầu giải'")

    def generate_new_puzzle(self):
        self.current_state = generate_random_puzzle()
        self.update_matrix_display(self.current_state)
        self.resultLabel.setText("Đã tạo puzzle mới. Chọn thuật toán và nhấn 'Bắt đầu giải'")
        # Reset thông tin thuật toán khi tạo puzzle mới
        self.algorithm_info.reset()

    def update_matrix_display(self, state):
        matrix_str = "Ma trận hiện tại:\n"
        for i in range(0, 9, 3):
            row = state[i:i+3]
            matrix_str += " ".join(str(x) for x in row) + "\n"
        self.matrixLabel.setText(matrix_str)

    def show_info(self):
        dialog = InfoDialog(self.algorithm_info, self)
        dialog.exec_()

    def run_solver(self):
        try:
            algo = self.algorithmComboBox.currentText()
            algo_lower = algo.lower()
            
            # Xác định trạng thái ban đầu dựa trên thuật toán
            if algo_lower in ["qlearning", "q-learning"]:
                state = initial_state3
            elif algo_lower in ["partial_observation", "no_observation"]:
                if isinstance(initial_state4[0], list):
                    state = [item for row in initial_state4 for item in row]
                else:
                    state = initial_state4
            elif algo_lower in ["stochastic_hc", "forwardtracking", "backtracking", "genetic", "ids"]:
                if isinstance(initial_state4[0], list):
                    state = [item for row in initial_state4 for item in row]
                else:
                    state = initial_state4
            else:
                state = self.current_state

            solution, cost, execution_time = solve_with_algorithm(state, goal_state, algo)
            if solution:
                result_text = f"Tìm thấy!\nChi phí: {cost}\nSố bước: {len(solution)-1}\nThời gian: {execution_time:.2f}s"
                self.resultLabel.setText(result_text)
                # Lưu thông tin thuật toán
                self.algorithm_info.add_result(algo, execution_time, cost)
                show_solution_with_pygame(solution, cost, execution_time)
            else:
                self.resultLabel.setText("Không tìm thấy lời giải.")
        except Exception as e:
            self.resultLabel.setText(f"Lỗi: {str(e)}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PuzzleApp()
    window.show()
    sys.exit(app.exec_())
