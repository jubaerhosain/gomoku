import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtWidgets import QGridLayout, QDesktopWidget, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QTimer

from gomoku import Gomoku, Point


class GomokuBoard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.board_width = 800
        self.board_height = 500
        self.timer = QTimer()
        self.timer.timeout.connect(self.ai_move)
        self.game = Gomoku()
        self.current_player = 'X'
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Gomoku Game")
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.createGrid())
        main_layout.addWidget(self.createRightPanel())
        main_widget.setLayout(main_layout)
        # Calculate the center position
        screen_geometry = QDesktopWidget().screenGeometry()
        x = (screen_geometry.width() - self.board_width) // 2
        y = (screen_geometry.height() - self.board_height) // 2
        self.setGeometry(x, y, self.board_width, self.board_height)
        # Set the fixed size of the main window
        self.setFixedSize(self.board_width, self.board_height)

    def createGrid(self):
        grid_widget = QWidget()
        grid_layout = QGridLayout()
        grid_layout.setVerticalSpacing(5)
        grid_layout.setHorizontalSpacing(5)
        grid_layout.setAlignment(Qt.AlignCenter)
        self.buttons = []
        for row in range(10):
            row_buttons = []
            for col in range(10):
                button = QPushButton()
                button.setFixedSize(40, 40)
                button.position = Point(row, col)
                button.clicked.connect(self.buttonClicked)
                button.setStyleSheet(
                    "QPushButton { border-radius: 20px; background-color: grey; }")
                row_buttons.append(button)
                grid_layout.addWidget(button, row, col)
            self.buttons.append(row_buttons)
        grid_widget.setLayout(grid_layout)
        return grid_widget

    def createRightPanel(self):
        right_widget = QWidget()
        new_game_button = QPushButton("New Game")
        self.current_player_label = QPushButton("Your Move")
        self.current_player_label.setDisabled(True)
        your_color = QPushButton("You: Green")
        your_color.setDisabled(True)
        ai_color = QPushButton("AI: Red")
        ai_color.setDisabled(True)
        
        button_height = 40
        button_width = 200
        new_game_button.setFixedSize(button_width, button_height)
        self.current_player_label.setFixedSize(button_width, button_height)
        your_color.setFixedSize(button_width, button_height)
        ai_color.setFixedSize(button_width, button_height)
        new_game_button.setStyleSheet(
            "QPushButton { background-color: #4CAF50; color: white; font-size: 18px; text-align: center; }"
            "QPushButton:hover { background-color: #45a049; }"
        )
        self.current_player_label.setStyleSheet(
            "QPushButton { background-color: #2196F3; color: white; font-size: 18px; text-align: center; }"
        )
        your_color.setStyleSheet(
            "QPushButton { background-color: green; color: white; font-size: 18px; text-align: center; }"
        )
        ai_color.setStyleSheet(
            "QPushButton { background-color: red; color: white; font-size: 18px; text-align: center; }"
        )
        new_game_button.clicked.connect(self.newGame)
        right_layout = QVBoxLayout()
        right_layout.addWidget(new_game_button)
        right_layout.addWidget(self.current_player_label)
        right_layout.addWidget(your_color)
        right_layout.addWidget(ai_color)
        right_layout.setSpacing(10)
        right_layout.setAlignment(Qt.AlignHCenter)
        right_widget.setLayout(right_layout)
        return right_widget

    def buttonClicked(self):
        if self.current_player != 'X':
            return

        sender = self.sender()
        x, y = sender.position.x, sender.position.y
        if not self.game.is_valid_move(x, y):
            return

        sender.setStyleSheet(
            f"border-radius: 20px; background-color: green;")
        self.game.make_move(x, y, self.game.PLAYER_MARKER)

        if self.game.is_won(self.game.PLAYER_MARKER):
            self.current_player_label.setText("You Won!!")
            self.game_ended()
            return
        
        if self.game.is_draw():
            self.current_player_label.setText("Game is draw!!")
            self.game_ended()
            return

        self.current_player = 'O'
        self.current_player_label.setText("AI is moving...")

        self.timer.start(1000)

    def newGame(self):
        for i in range(10):
            for j in range(10):
                self.buttons[i][j].setStyleSheet(
                    "QPushButton { border-radius: 20px; background-color: grey; }")
                self.buttons[i][j].setEnabled(True)

        self.current_player = 'X'
        self.current_player_label.setText("Your Move")
        self.game.reset_game()

    def ai_move(self):
        self.timer.stop()
        pos = self.game.get_ai_move()
        self.buttons[pos.x][pos.y].setStyleSheet(
            f"border-radius: 20px; background-color: red;")
        self.game.make_move(pos.x, pos.y, self.game.AI_MARKER)

        if self.game.is_won(self.game.AI_MARKER):
            self.current_player_label.setText("AI Won!!")
            self.game_ended()
            return
        
        if self.game.is_draw():
            self.current_player_label.setText("Game is draw!!")
            self.game_ended()
            return

        self.current_player = 'X'
        self.current_player_label.setText("Your Move")

    def game_ended(self):
        for i in range(self.game.board_size):
            for j in range(self.game.board_size):
                self.buttons[i][j].setDisabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GomokuBoard()
    window.show()
    sys.exit(app.exec_())
