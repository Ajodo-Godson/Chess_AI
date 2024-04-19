import sys
import chess
import chess.svg
import chess.pgn
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QPushButton, QLabel, QSpinBox, QComboBox
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMouseEvent
from evaluation import *
from ai import *
import time
book_path = 'Resources/gm2600.bin'
#book_path = 'Resources/gm2001.bin'
class ChessGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.ai_color = None  # AI color is not set initially
        self.initUI()
        
        QTimer.singleShot(100, self.prompt_ai_color_selection)  # Prompt for AI color after the UI initializes


    def initUI(self):
        self.setGeometry(100, 100, 520, 520)
        self.setWindowTitle('Chess AI')
        self.board = chess.Board()
        self.svgWidget = QSvgWidget(parent=self)
        self.svgWidget.setGeometry(10, 10, 500, 500)
        self.square_size = self.svgWidget.geometry().width() // 8

        self.pgnButton = QPushButton('Generate PGN & Show FEN', self)
        self.pgnButton.clicked.connect(self.generate_pgn_and_show_fen)
        self.pgnButton.move(520, 200)  

        #Select depth to play: 
        self.depthLabel = QLabel('Select Depth to Play', self)
        self.depthLabel.move(520, 30)
        self.depthComboBox = QComboBox(self)
        self.depthComboBox.addItems([str(i) for i in range(1, 11)])  # Adding depth options 1 to 10
        self.depthComboBox.setFixedSize(100, 30)
        self.depthComboBox.move(520, 50)

        # Select AI color
        self.move_from_square = None
        self.legal_moves = []
        self.whiteButton = QPushButton('AI Plays White', self)
        self.whiteButton.clicked.connect(lambda: self.set_ai_color(chess.WHITE))
        self.whiteButton.move(520, 100)  
        
        self.blackButton = QPushButton('AI Plays Black', self)
        self.blackButton.clicked.connect(lambda: self.set_ai_color(chess.BLACK))
        self.blackButton.move(520, 150)  
        self.update_board()
      
        # Resign Button
        self.resignButton = QPushButton('Resign', self)
        self.resignButton.clicked.connect(self.handle_resign)
        self.resignButton.move(520, 250)  

        # Claim Draw Button
        self.claimDrawButton = QPushButton('Claim Draw', self)
        self.claimDrawButton.clicked.connect(self.handle_claim_draw)
        self.claimDrawButton.move(520, 300)  

        #Counter
        self.movesLabel = QLabel('Moves: 0', self)
        self.movesLabel.setFixedSize(200, 30)  # Width of 200 pixels and height of 30 pixels
        self.movesLabel.move(520, 350)  # Position next to other controls
        
        self.timeLabel = QLabel('Time: 0.0s', self)
        self.timeLabel.setFixedSize(200, 30)  # Width of 200 pixels and height of 30 pixels
        self.timeLabel.move(520, 400)  # Position next to other controls
        

    def generate_pgn_and_show_fen(self):
        pgn_string = self.generate_pgn_from_moves()
        QMessageBox.information(self, "Current FEN", f"Current FEN: {self.board.fen()}\n\nPGN:\n{pgn_string}")

    def generate_pgn_from_moves(self):
        game = chess.pgn.Game()
        game.headers["Event"] = "Casual Game"
        game.headers["White"] = "Player1" if self.ai_color == chess.BLACK else "AI"
        game.headers["Black"] = "AI" if self.ai_color == chess.BLACK else "Player1"
        game.headers["Result"] = self.board.result()
        
        # Use a temporary board to validate and play through the moves
        temp_board = chess.Board()
        node = game

        # Iterate through the move_stack to add the moves to the PGN game
        for move in self.board.move_stack:
            # Ensure the move is legal in the current board state
            if move in temp_board.legal_moves:
                temp_board.push(move)
                node = node.add_variation(move)
            else:
                print(f"Illegal move {move} in position {temp_board.fen()}")
                break  # Break on illegal move

        # Convert the game object to a PGN string
        exporter = chess.pgn.StringExporter(headers=True, variations=True, comments=False)
        pgn_string = game.accept(exporter)
        return pgn_string

    def prompt_ai_color_selection(self):
        """Prompt the user to select the AI's color at startup."""
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Select AI Color")
        msgBox.setText("Which color should the AI play?")
        whiteButton = msgBox.addButton("White", QMessageBox.AcceptRole)
        blackButton = msgBox.addButton("Black", QMessageBox.AcceptRole)
        msgBox.exec()

        if msgBox.clickedButton() == whiteButton:
            self.set_ai_color(chess.WHITE)
            
        elif msgBox.clickedButton() == blackButton:
            self.set_ai_color(chess.BLACK)


    def update_board(self, highlight_moves=None):
        if highlight_moves is None:
            highlight_moves = []
        # Flip the board view based on AI's color
        board_flipped = self.ai_color == chess.WHITE
        board_svg = chess.svg.board(board=self.board, size=500,
                                    lastmove=self.board.peek() if self.board.move_stack else None,
                                    squares=highlight_moves, flipped=board_flipped).encode('UTF-8')
        self.svgWidget.load(board_svg)
        self.display_game_over_message()  # Check and display if the game
    
    def mousePressEvent(self, event: QMouseEvent):
        try:
            if event.button() == Qt.LeftButton:
                # Calculate click position taking board flip into account
                if self.ai_color == chess.WHITE:  # If board is flipped
                    x = 7 - ((event.x() - self.svgWidget.x()) // self.square_size)
                    y = (event.y() - self.svgWidget.y()) // self.square_size
                else:  # Board is not flipped
                    x = (event.x() - self.svgWidget.x()) // self.square_size
                    y = 7 - ((event.y() - self.svgWidget.y()) // self.square_size)
                    
                square = chess.square(x, y)

                if self.move_from_square is None:
                    self.move_from_square = square
                    self.legal_moves = [move.to_square for move in self.board.legal_moves if move.from_square == square]
                    self.update_board(highlight_moves=self.legal_moves)
                else:
                    piece = self.board.piece_at(self.move_from_square)
                    if piece and piece.piece_type == chess.PAWN and chess.square_rank(square) in (0, 7):
                        promotion = chess.QUEEN
                    else:
                        promotion = None

                    move = chess.Move(self.move_from_square, square, promotion=promotion)
                    if move in self.board.legal_moves:
                        self.board.push(move)
                        self.update_board()
                        self.move_from_square = None
                        self.legal_moves = []
                        QTimer.singleShot(100, self.ai_move)  # AI moves after a short delay
                    else:
                        self.move_from_square = None
                        self.legal_moves = []
                        self.update_board()  # Deselect if the move is not valid
        except Exception as e:
            print(f"Error in mousePressEvent: {e}")



    def handle_resign(self):
        if self.board.turn == chess.WHITE:
            winner = "Black"
        else:
            winner = "White"
        QMessageBox.information(self, "Game Over", f"{winner} wins by resignation")
        # Reset the board
        self.board.reset()
        self.update_board()  

    def handle_claim_draw(self):
        
        QMessageBox.information(self, "Game Over", "Draw claimed")
        # Reset the board 
        self.board.reset()
        self.update_board()

    def display_game_over_message(self):
        if self.board.is_checkmate():
            winner = "Black wins by checkmate" if self.board.turn == chess.WHITE else "White wins by checkmate"
            QMessageBox.information(self, "Game Over", winner)
        elif self.board.is_stalemate():
            QMessageBox.information(self, "Game Over", "Stalemate")
        elif self.board.is_insufficient_material():
            QMessageBox.information(self, "Game Over", "Draw due to insufficient material")
        elif self.board.can_claim_draw():
            QMessageBox.information(self, "Game Over", "Draw can be claimed")
        elif self.board.is_seventyfive_moves():
            QMessageBox.information(self, "Game Over", "Draw by 75-move rule")
        elif self.board.is_fivefold_repetition():
            QMessageBox.information(self, "Game Over", "Draw by fivefold repetition")
        elif self.board.is_variant_draw():
            QMessageBox.information(self, "Game Over", "Draw by variant-specific reason")
    
    def set_ai_color(self, color):
        """Sets the AI's color and triggers a move if it's AI's turn."""
        self.ai_color = color
        if self.board.turn == self.ai_color:
            QTimer.singleShot(100, self.ai_move)  #

    
    def iterative_deepening_search(self, max_depth):
        best_move = None
        is_maximising_player = self.ai_color == chess.WHITE  # True if AI is white, False if black
        for depth in range(1, max_depth + 1):
            current_best_move = minimax_root(depth, self.board)
            if current_best_move:
                best_move = current_best_move
            else:
                break  # If no move found at this depth, unlikely to find in deeper.
        return best_move
    

    def ai_move(self):
        global debug_info
        debug_info["nodes"] = 0  # Reset node count at the start of a new move calculation

        if not self.board.is_game_over():
            start_time = time.time()
            # Get the selected depth from the Qcombobox
            selected_depth = int(self.depthComboBox.currentText())

            # First, try to get a book move
            book_move = get_book_move(self.board, book_path)
            if book_move:
                self.board.push(book_move)
                move_used = book_move
                print("Book move used:", book_move)
                move_source = "Book"
            else:
                # If no book move available, calculate the move using AI
                move = self.iterative_deepening_search(max_depth=selected_depth)
                if move:
                    self.board.push(move)
                    move_used = move
                    print("AI calculated move:", move)
                    move_source = "AI"
                else:
                    print("No move selected by AI.")
                    move_used = None

            elapsed_time = time.time() - start_time
            debug_info["time"] = elapsed_time  # Store elapsed time in debug_info

            # Update GUI labels with metrics from debug_info
            self.movesLabel.setText(f"Moves: {debug_info['nodes']} (Source: {move_source})")
            self.timeLabel.setText(f"Time: {elapsed_time:.2f}s")

            self.update_board()
            self.display_game_over_message()
        else:
            print("Game over detected.")


def get_book_move(board, book_path):
    try:
        with chess.polyglot.open_reader(book_path) as reader:
            book_moves = reader.find_all(board)
            bookky = [entry for entry in book_moves]
            if bookky:
                max_move = max(bookky, key=lambda entry: entry.weight).move
            
                return max_move
            else:
                return None
    except Exception as e:
        print(f"Error reading the book: {str(e)}")
    return None




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChessGUI()
    ex.show()
    sys.exit(app.exec_())