import string
from collections import defaultdict
min_word_length = 4
alphabet = string.ascii_lowercase

class Node():
	

	def add_children(self, child):
		self.children[child.value] = child

	def __init__(self, parent, value_in, distance_in):
		self.parent_node = parent
		self.value = value_in
		self.distance_from_root = distance_in
		self.children = {}
		self.paths = defaultdict(lambda: 0)

	def print_info(self, with_children_vals = False):
		if with_children_vals:
			print("Value: " + str(self.value) + "\nChildren Keys: " + str(self.children.keys()) + "\nChildren Vals: " + str(self.children.values()) +
			"\nDistance from root: " + str(self.distance_from_root) + "\nPaths Available: " + str(dict(self.paths)) + "\n")

		print("Value: " + str(self.value) + "\nChildren Keys: " + str(self.children.keys()) +"\nDistance from root: " 
			+ str(self.distance_from_root) + "\nPaths Available: " + str(dict(self.paths)) + "\n")

def get_words(file):
	words = []
	with open(file, "r") as f:
		for line in f:
			words.append(line[:-1].lower())
	return words

def make_tree(file, root):
	with open(file, "r") as f:
		word = ""
		while len(word) < 4:
			word = next(f)[:-1].lower()
		add_word(word, root, checks = False)
		for word in f:
			to_add = word[:-1].lower()
			if len(to_add) >= min_word_length:
				# print(to_add)
				add_word(to_add, root)
				# print(to_add)
	return root

# def add_first(word, root):
	# parent = root
	# # parent.print_info()
	# stack = []
	# for i in word:
	# 	# parent.print_info()
	# 	added = add_leaf(parent, i)
	# 	# print("Parent Info")
	# 	# parent.print_info()
	# 	# print()
	# 	parent = added
	# 	# print(parent.children.values())
	# 	stack.append(parent)

	# last = stack.pop()
	# length = 1
	# while(stack):
	# 	current = stack.pop()
	# 	current.paths[length] += 1
	# 	length += 1

def add_word(word, root, checks = True):
	parent = root
	stack = []
	created_node = True
	for i in word:
		if checks:
			if not created_node and not parent.children:
				# print("exited, no children, is a word")
				return
			if i in parent.children:
				created_node = False
				stack.append(parent)
				parent = parent.children[i]
				continue

		added = add_leaf(parent, i)
		# print("added leaf: " + added.value)
		parent = added
		stack.append(parent)
		created_node = True

	last = stack.pop()
	length = 1
	while(stack):
		current = stack.pop()
		current.paths[length] += 1
		length += 1
	root.paths[length] += 1

def add_leaf(parent, value):
	leaf = Node(parent, value, parent.distance_from_root + 1)
	# print("leaf")
	# leaf.print_info()
	# print()
	parent.add_children(leaf)
	return leaf


def bsf(root, start):
	queue = []
	queue.append(start)
	visited = [start]
	while queue:
		current = queue.pop(0)
		# print(queue)
		# print("Start: " + str(start) + "Current: " + str(current))
		distance = start.distance_from_root - current.distance_from_root
		if not current.children and distance%2 == 0 and current.distance_from_root >= min_word_length:
			return current
		for key in current.children:
			if current.children[key] not in visited:
				queue.append(current.children[key])
				visited.append(current.children[key])

def play(new_letter, root):
	start = traverse_tree_to_start(new_letter, root)
	# start.print_info()
	if len(start.children) is 1:
		end = start.children[list(start.children.keys())[0]]
	else:
		end = bsf(root, start)
	# end.print_info()
	current = end.parent_node
	path = [current.value]
	while current is not start:
		current = current.parent_node
		path.append(current.value)
	
	# print(path)

	if len(start.children) is 1:
		next_letter = end.value
	else:
		next_letter = path[-2]
	current = start.children[next_letter]

	return next_letter, current

def traverse_tree_to_start(letter, root):
	parent = root
	parent = parent.children[letter]
	return parent

def get_letter(valid_letters):
	print("\nValid Letters: " + str(valid_letters))
	letter_in = input("Enter a letter: ")
	while letter_in not in valid_letters:
		letter_in = input("Enter a letter: ")
	return letter_in

def if_over(word):
	if word in scrabble_words:
		return True
	return False

def play_ghost(legal_words, root):
	letter_choices = [i for i in alphabet]
	current_word = get_letter(letter_choices)
	print("\nHuman's turn: \n" + str(current_word))
	human = False
	current_node = root
	while len(current_word) < min_word_length or current_word not in legal_words:
		letter_choices = list(current_node.children.keys())
		if human:
			added_letter = get_letter(letter_choices)
			print("\nHuman's turn: ")
		else:
			added_letter, current_node = play(current_word[-1], current_node)
			print("\nBot's turn: ")
		current_word = current_word + added_letter
		human = not human
		print(current_word)
		# print()
		# print(current_word)
	print("Final Word: " + str(current_word) + "\nWinner Human: " + str(human))

def print_branch(root, letters):
	while root.children and letters:
		root.print_info()
		root = root.children[letters[0]]
		letters = letters [1:]
	root.print_info()

def sort_scrabble(scrabble, short):
	with open(scrabble, "r") as scr:
		with open(short, "w") as sho:
			for i in scr:
				if len(i[:-1].lower()) >= min_word_length:
					sho.write(i.lower())

# sort_scrabble("scrabble.txt", "new_scrabble.txt")
legal_words_list = get_words("scrabble.txt")
root = Node(None, " ", 0)
tree = make_tree("scrabble.txt", root)


# print(legal_words_list)

play_ghost(legal_words_list, tree)
# tree.print_info()
print()

# print_branch(tree, "zeal")


# tree = make_word_tree(word_list)
# print(tree.get_children())
# play_ghost(word_list)
