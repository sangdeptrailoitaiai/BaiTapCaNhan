import sys
import pygame
from PyQt5 import QtWidgets, uic
from algorithms import solve_with_algorithm

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

class PuzzleApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("puzzle_solver_gui.ui", self)
        self.startButton.clicked.connect(self.run_solver)
        self.algorithmComboBox.addItems([
            "BFS", "DFS", "Greedy", "Iterative", "IDDFS", "A*", "UCS", "SA", "Beam", "HC", "SHC", "SAHC", "AND_OR",
            "No_Observation", "Partial_Observation", "Genetic", "Backtracking", "ForwardTracking", "Stochastic_HC", "QLearning",
            "IDA*", "IDS"
        ])
        self.resultLabel.setText("Chọn thuật toán và nhấn 'Bắt đầu giải'")

    def run_solver(self):
        try:
            algo = self.algorithmComboBox.currentText()
            algo_lower = algo.lower()
            if algo_lower in ["qlearning","ida*"]:
                state = initial_state3
                algo_lower = algo.lower()
            if algo_lower in [ "stochastic_hc", "forwardtracking", "backtracking", "genetic", "ids"]:
                if isinstance(initial_state4[0], list):
                    state = [item for row in initial_state4 for item in row]
                else:
                    state = initial_state4
            elif algo_lower in ["partial_observation", "no_observation"]:
                if isinstance(initial_state4[0], list):
                    state = [item for row in initial_state4 for item in row]
                else:
                    state = initial_state4
            else:
                state = initial_state
            solution, cost, execution_time = solve_with_algorithm(state, goal_state, algo)
            if solution:
                result_text = f"Tìm thấy!\nChi phí: {cost}\nSố bước: {len(solution)-1}\nThời gian: {execution_time:.2f}s"
                self.resultLabel.setText(result_text)
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
