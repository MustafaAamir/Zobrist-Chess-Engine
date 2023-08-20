import chess
import os

tranposition_table = {}

piece_values = {
  chess.PAWN: 1,
  chess.KNIGHT: 3, 
  chess.BISHOP: 3,
  chess.ROOK: 5,
  chess.QUEEN: 9,
  chess.KING: 1000
}

"""
For the time being, this only works for white. My intention was for it
to work for both colours, but I think my approach was flawed.
"""
target_squares = {
    chess.PAWN: [
        7, 7, 7, 7, 7, 7, 7, 7,
        5, 5, 5, 5, 5, 5, 5, 5,
        3, 3, 3, 4, 4, 3, 3, 3,
        3, 3, 3, 6, 6, 3, 3, 3, 
        4, 0, 3, 6, 6, 5, 3, 3,
        3, 4, 2, 5, 5, 2, 3, 3,
        2, 2, 2, 2, 2, 2, 2, 2,
        7, 7, 7, 7, 7, 7, 7, 7
    ],
    chess.KING: [
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0
    ],
    chess.KNIGHT: [
        0, 1, 1, 1, 1, 1, 1, 0,
        0, 2, 2, 2, 2, 2, 2, 0,
        0, 3, 4, 5, 5, 4, 3, 0, 
        0, 3, 4, 5, 5, 4, 4, 0,
        0, 4, 6, 6, 6, 6, 4, 0,
        0, 2, 6, 6, 6, 6, 2, 0,
        0, 0, 0, 4, 4, 0, 0, 0,
        0, 0, 2, 2, 2, 2, 0, 0
    ],
    chess.BISHOP: [
        2, 2, 2, 2, 2, 2, 2, 2,
        4, 4, 3, 3, 3, 3, 4, 5,
        2, 2, 2, 2, 2, 2, 2, 2,
        3, 6, 4, 6, 6, 4, 6, 3,
        6, 4, 6, 6, 6, 6, 4, 6, 
        5, 4, 5, 6, 6, 5, 4, 5, 
        6, 6, 6, 5, 5, 6, 6, 6,
        6, 6, 3, 3, 3, 3, 6, 6
    ],
    chess.ROOK: [
        6, 6, 6, 6, 6, 6, 6, 6,
        6, 6, 6, 6, 6, 6, 6, 6, 
        4, 4, 4, 4, 4, 4, 4, 4,
        3, 3, 3, 3, 3, 3, 3, 3,
        2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 5, 5, 5, 5, 5,
        2, 2, 2, 5, 5, 2, 2, 2,
        3, 2, 2, 6, 6, 3, 2, 3
    ],
    chess.QUEEN: [
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0
    ]
}

def save_moves_to_file(moves):
  with open("games.txt", "w") as file:
    for move in moves:
      file.write(move + " ")

def evaluate_board(board):
  evaluation = 0
  for square in chess.SQUARES:
    piece = board.piece_at(square)
    if piece is not None:
      # Did this because square values were prioritized over piece values
      if piece.color == chess.WHITE:
        value = piece_values[piece.piece_type] + (taget_squares[piece.piece_type][square ^ 56] / 10)
        evaluation += value
      else: 
        value = piece_values[piece.piece_type] + (taget_squares[piece.piece_type][square] / 10)
        evaluation -= value
  return evaluation


def minimax(board, depth, alpha, beta, maximizing):
  if depth == 0 or board.is_game_over():
    return evaluate_board(board)
  if maximizing:
    max_eval = -float("inf")
    for move in board.legal_moves:
      board.push(move)
      eval = minimax(board, depth - 1, alpha, beta, False)
      board.pop()
      max_eval = max(max_eval, eval)
      alpha = max(alpha, eval)
      if beta <= alpha:
        break
    return max_eval

  else:
    min_eval = float("inf")
    for move in board.legal_moves:
      board.push(move)
      eval = minimax(board, depth - 1, alpha, beta, True)
      board.pop()
      min_eval = min(min_eval, eval)
      beta = min(beta, eval)
      if beta <= alpha:
        break
    return min_eval

def best_move_finder(board, depth):
  best_move = None
  best_eval = -float('inf')

  for move in board.legal_moves:
    board.push(move)
    eval = minimax(board, depth - 1, -float("inf"), float("inf"), False)
    board.pop()

    if eval > best_eval:
      best_eval = eval
      best_move = move
      
  return best_move


def main():
  board = chess.Board()
  game_moves = []
  running = True
  while running and not board.is_game_over:
    if board.turn == chess.WHITE:
      print(board)
      print("White Engine's Turn")
      best_move = best_move_finder(board, depth=4)
      if best_move is None:
        break

      board.push(best_move)
      os.system("clear")
    else: # black
      print(board)  
      # Don't care about input validation
      user_move = input("Your Turn: ")
      board.push_san(user_move)
      os.system("clear") 
    game_moves.append(str(best_moves))

  print("Game Over")
  print("Result: ", board.result())
  save_moves_to_file(game_moves)


if __name__ == "__main__":
  main()
        
