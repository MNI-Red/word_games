import string
min_word_length = 4
alphabet = string.ascii_lowercase

class Node():
	children = []
	def add_children(self, child):
		self.children.append(child)

	def get_value(self):
		return self.value

	def get_parent(self):
		return self.parent_node

	def get_children(self):
		return self.children

	def __init__(self, parent, value_in):
		self.parent_node = parent
		self.value = value_in

def get_words(file):
	scrabble_words = []
	with open(file, "r") as f:
		for word in f:
			scrabble_words.append(word[:-1].lower())
	# print(scrabble_words)
	return scrabble_words

def get_letter():
	return input("Enter a letter: ")

def if_over(word):
	if word in scrabble_words:
		return True
	return False

def play_ghost(words):
	current = get_letter()
	while len(current) < min_word_length or current not in words:
		current = current + get_letter()
	print(current)

def make_word_tree(legal_words):
	root = Node(None, " ")
	for i in alphabet:
		root.add_children(Node(root, i))

	# print("Children: " +str(root.get_children()))
	for x in root.get_children():
		# print(x)
		add_possible_next_letter(x, legal_words)
	return root

def add_possible_next_letter(node, legal_words):
	# print("Node: " + str(node))
	base = node.get_value()
	for i in alphabet:
		if base+i in legal_words:
			node.add_children(Node(node, base+i))


word_list = get_words("scrabble.txt")
tree = make_word_tree(word_list)
print(tree.get_children())
# play_ghost(word_list)
