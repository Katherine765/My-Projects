BLANK='.' ; PLAYER1='X' ; PLAYER2='O'
wins = ['012','345','678','036','147','258','048','246']

class TTT():
	def __init__(self):
		self.spaces=[BLANK for x in range(9)]
		self.player=PLAYER1

	def drawBoard(self):
		print()
		for x in range(0,9,3):
			print(f'{self.spaces[x]}{self.spaces[x+1]}{self.spaces[x+2]}  {x+1}{x+2}{x+3}')
			
	def getMove(self):
		move=input(f'Player {self.player}\'s move:   ')
		while True:
			if move in [str(x) for x in range(1,10)]:
				if self.spaces[int(move)-1] == BLANK:
					break
			move=input(f'Invalid move. Player {self.player}\'s move:   ')
			
		self.spaces[int(move)-1]=self.player

	def checkBoard(self):
		for win in wins:
			winList=[int(x) for x in win]
			if self.spaces[winList[0]] == self.spaces[winList[1]] == self.spaces[winList[2]] == self.player:
				return True

		if not BLANK in self.spaces:
			return 'tie'

		return False

	def switchPlayer(self):
		if self.player==PLAYER1:
			self.player=PLAYER2
		else:
			self.player=PLAYER1

def main():
	ttt=TTT()

	while True:
		ttt.drawBoard()
		ttt.getMove()
		result=ttt.checkBoard()
		if result:
			break
		ttt.switchPlayer()

	#so you can actually see the win
	ttt.drawBoard()
	if result == 'tie':
		print('Tie game.')
	elif result:
		print(f'Player {ttt.player} wins!')

main()