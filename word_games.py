min_word_length = 4
scrabble_words = []
with open("scrabble.txt", "r") as f:
	for word in f:
		scrabble_words.append(word[:-1].lower())
# print(scrabble_words)

def get_letter():
	return input("Enter a letter: ")

def if_over(word):
	if word in scrabble_words:
		return True
	return False

def play_ghost():
	current = get_letter()
	while len(current) < min_word_length or current not in scrabble_words:
		current = current + get_letter()
	print(current)

play_ghost()
