# Implementação dos algoritimos Minimax, Negamax, 
# Minimax com poda e Negamax com poda no jogo da velha
# -----------------------------------------------------
# Autor: Marcio Antônio Rodrigues de Souza
# -----------------------------------------------------

from math import inf as infinity
import random

board = ["_","_","_"
        ,"_","_","_"
        ,"_","_","_"]

def win_state(board):
  win_state = [
    [board[0], board[1], board[2]],
    [board[3], board[4], board[5]],
    [board[6], board[7], board[8]],
    [board[0], board[3], board[6]],
    [board[1], board[4], board[7]],
    [board[2], board[5], board[8]],
    [board[0], board[4], board[8]],
    [board[2], board[4], board[6]]
  ]
  return win_state

def printBoard(board):
  print(" ", board[0], "|", board[1], "|", board[2], " ")
  print("-------------")
  print(" ", board[3], "|", board[4], "|", board[5], " ")
  print("-------------")
  print(" ", board[6], "|", board[7], "|", board[8], " ")
  print("\n")

def winner(board, player):
  if[player, player, player] in win_state(board):
    return True
  else:
    return False

def game_over(board):
  return winner(board, 'x') or winner(board, '0')

def jogadasPossiveis(board):
  listaDeCasasVazias = []
  for i, j in enumerate(board):
    if j == "_":
      listaDeCasasVazias.append(i)
  return listaDeCasasVazias

def avaliacao(state):
  if winner(state, '0'):
    score = 1
  elif winner(state, 'x'):
    score = -1
  else:
    score = 0
  return score

def avaliacaoNegamax(state, player):
  if (winner(state, '0') and player == '0') or (winner(state, 'x') and player == 'x'):
    score = 1
  elif (winner(state, 'x') and player == '0') or (winner(state, '0') and player == 'x'):
    score = -1
  else:
    score = 0
  return score

# Minimax
def miniMax(board, depth, player):
  if game_over(board) or depth == 0:
    score = [-1, avaliacao(board)]
    return score

  if player != "0":
    best = [-1, infinity]
    for move in jogadasPossiveis(board):
      board[move] = player
      score = miniMax(board, depth - 1, '0')
      board[move] = '_'
      if score[1] < best[1]:
        best[1] = score[1]
        best[0] = move
    return best

  else:
    best = [-1, -infinity]
    for move in jogadasPossiveis(board):
      board[move] = player
      score = miniMax(board, depth - 1, 'x')
      board[move] = '_'
      if score[1] > best[1]:
        best[1] = score[1]
        best[0] = move
    return best

# Minimax com poda
def miniMaxAB(board, depth, player, alpha, beta):
  if game_over(board) or depth == 0:
    score = [-1, avaliacao(board)]
    return score

  if player != "0":
    best = [-1, infinity]
    for move in jogadasPossiveis(board):
      board[move] = player
      score = miniMaxAB(board, depth - 1, '0', alpha, beta)
      board[move] = '_'
      if score[1] < best[1]:
        best[1] = score[1]
        best[0] = move
      alpha = max(best[1], alpha)
      if beta <= alpha:
        return
    return best

  else:
    best = [-1, -infinity]
    for move in jogadasPossiveis(board):
      board[move] = player
      score = miniMaxAB(board, depth - 1, 'x', alpha, beta)
      board[move] = '_'
      if score[1] > best[1]:
        best[1] = score[1]
        best[0] = move
      alpha = max(best[1], alpha)
      if beta <= alpha:
        return
    return best

# Negamax
def negaMax(board, depth, player):
  if game_over(board) or depth == 0:
    return [-1, avaliacaoNegamax(board, player)]

  best = [-1, -infinity]
  for move in jogadasPossiveis(board):
    board[move] = player
    if player == '0':
      score = negaMax(board, depth-1, 'x')
      score[1] = -score[1]
    if player == 'x':
      score = negaMax(board, depth-1, '0')
      score[1] = -score[1]
    board[move] = '_'

    if score[1] > best[1]:
      best[1] = score[1]
      best[0] = move
    
  return best

# Negamax com poda
def negaMaxAB(board, depth, player, alpha, beta):
  if game_over(board) or depth == 0:
    return [-1, avaliacaoNegamax(board, player)]

  best = [-1, -infinity]
  for move in jogadasPossiveis(board):
    board[move] = player
    if player == '0':
      score = negaMaxAB(board, depth-1, 'x', -beta, -alpha)
      score[1] = -score[1]
    if player == 'x':
      score = negaMaxAB(board, depth-1, '0', -beta, -alpha)
      score[1] = -score[1]
    board[move] = '_'

    if score[1] > best[1]:
      best[1] = score[1]
      best[0] = move
    alpha = max(alpha, best[1])
    if alpha >= beta:
      break
    
  return best

# Funções de jogada

# Humano
def human_turn(board):
  if game_over(board):
    return
  
  move = int(input("Escolha um número de  1 a 9:\n"))

  if move <= 9 and move >= 1:
    if board[move - 1] == "_":
      move -= 1
      board[move] = "x"
      printBoard(board)
      return
    else:
      print("Esta posição já está ocupada")
      move = -1
      human_turn(board)
  else:
    print("Caracetere irregular")
    move = -1
    human_turn(board)

# AI
def AI_move():
  ai_player = '0'
  depth = len(jogadasPossiveis(board))

  if game_over(board):
    return
    
  # move = miniMax(board, depth, ai_player)
  # move = negaMax(board, depth, ai_player)
  # move = miniMaxAB(board, depth, ai_player, -infinity, infinity)
  move = negaMaxAB(board, depth, ai_player, -infinity, infinity)
  if board[move[0]] == '_':
    board[move[0]] = ai_player
    
  printBoard(board)

# Inicialização do jogo
def main(board):
  while len(jogadasPossiveis(board)) > 0 and not game_over(board):
    human_turn(board)
    AI_move()

  if winner(board, "x"):
    print("Humano venceu!")
    return 0;
  elif winner(board, "0"):
    print("Inteligência artificial venceu!")
    return 0
  else:
    print("Empatou!")
    return 0

if __name__ == "__main__":
  while True:
    main(board)
    board = ["_","_","_",
            "_","_","_",
            "_","_","_",]
    again = input("Deseja jogar novamente? [s/n]\n")
    if again == "n":
      break