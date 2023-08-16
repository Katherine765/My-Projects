wordlist = []
with open('wordle_words1.txt', 'r') as file:
    wordlist=[line.strip() for line in file.readlines()]

def main(word, wordlist):
	if not word in wordlist:
		print('Word not in wordlist.')
		return None 

	game=Game()

	while True:
		possible=[]
		for potential_guess in wordlist:
			if game.checkValidity(potential_guess):
				possible.append(potential_guess)

		game.generateData(possible)
		game.chooseBest(possible)

		print(game.topChoice)
		if game.actualCheck(word):
			break

	return game.tries


class Game():
	def __init__(self):
		self.frequency, self.placement = {}, {}
		self.wrong, self.somewhere = [], []
		self.know=[None for x in range(5)]
		self.check=None
		self.yellow={x:[] for x in range(5)}
		self.tries=0

		self.topChoice=None

	def checkValidity(self, potential_guess):
		guess_list=list(potential_guess)

		for x, letter in enumerate(guess_list):
			#No grays in word
			if letter in self.wrong:
				return False
			#No unmoved yellow
			if letter in self.yellow[x]:
				return False

		for x, letter in enumerate(self.somewhere):
        	#All yellows in word
			if not letter in guess_list:
				return False

		for x, letter in enumerate(self.know):
       		#All greens in word
			if not letter is None and not letter==guess_list[x]:
				return False

		return True


	def generateData(self, possible):
		self.frequency=[0 for x in range(26)]
		self.placement=[[0 for x in range(5)] for x in range(26)]
		for possible_guess in possible:
			guess_list=list(possible_guess)
			for x in range(5):
				letterNum=ord(possible_guess[x])-97
				#frequency counted once per word
				if x == possible_guess.find(guess_list[x]):
					self.frequency[letterNum] += 1
				(self.placement[letterNum])[x] += 1


	def chooseBest(self, possible):
		topRank=0
		for possible_guess in possible:
			rank=0
			guess_list=list(possible_guess)

			for x, letter in enumerate(guess_list):
				letterToNumber=ord(letter)-97
                #limits frequency points to 1 time per word
				if x == possible_guess.find(letter):
					rank += self.frequency[letterToNumber]
				rank += .55*(self.placement[letterToNumber])[x]
			#switch this sign to be very bad at wordle
			#(would also have to make rank start bigger)
			if rank>topRank:
				topRank=rank
				self.topChoice=possible_guess
		
		self.tries += 1

	def actualCheck(self, word):
		if word == self.topChoice:
			print('\nWin in %s tries!' %self.tries)
			return True

		guess_list=list(self.topChoice)
		for x, letter in enumerate(guess_list):
			#Green  
			if letter == word[x]:
				self.know[x]=letter
			#Yellow
			elif letter in word:
				self.somewhere.append(letter)
				self.yellow[x].append(letter)
			#Grey
			else:
				self.wrong.append(letter)

main('quick', wordlist)

'''
totalTries=0
for word in wordlist:
    totalTries += main(word,wordlist)

avg=totalTries/len(wordlist)
print(avg)
#average = 3.631965442764579
#if it chooses the worst possible guess each time, it gets it in 5.55377969762419
'''
