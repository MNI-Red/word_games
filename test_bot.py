import string
from collections import defaultdict
min_word_length = 4
root_value = ""
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

def make_tree_from_list(word_list, root):
	word = ""
	first = True
	for x in word_list:
		if len(x) >= min_word_length:
			# print(x)
			if first:
				add_word(word, root, checks = False)
				first = False
			add_word(x, root)
			# print(x)
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

def count_even_paths(node):
	num_even_paths = 0
	for i in node.paths:
		if i%2==0:
			num_even_paths += node.paths[i]
	return num_even_paths

def count_odd_paths(node):
	num_odd_paths = 0
	for i in node.paths:
		if i%2!=0:
			num_odd_paths += node.paths[i]
	return num_odd_paths

def pick_next_letter(node):
	child_address = [node.children[i] for i in node.children]
	even_paths_by_node = {}
	for i in node.children:
		even_paths_by_node[i] = count_odd_paths(node.children[i]) - count_even_paths(node.children[i])
		# even_paths_by_node[i] = count_even_paths(node.children[i]) - count_odd_paths(node.children[i])
	even_paths_by_node = sorted(even_paths_by_node.items(), key=lambda x: x[1], reverse=True)
	# print(even_paths_by_node)
	return node.children[even_paths_by_node[0][0]]

def bot_move(new_string, root):
	start = traverse_tree_to_start(new_string, root)
	# start.print_info()
	current = pick_next_letter(start)
	
	# if len(start.children) == 1:
	# 	current = start.children[list(start.children.keys())[0]]
	# 	# end = start.children[list(start.children.keys())[0]]
	# else:
	# 	current = pick_next_letter(start)
		# end = bsf(root, start)
		# if not end:
		# 	end = start.children[list(start.children.keys())[0]]
	# end.print_info()
	# current = end
	# word_by_letters = [current.value]
	# while current != start:
	# 	current = current.parent_node
	# 	word_by_letters.insert(0, current.value)
	
	# print(word_by_letters)
	# next_letter = word_by_letters[1]
	# current = start.children[next_letter]
	# if len(start.children) is 1:
	# 	next_letter = end.value
	# else:
	# 	next_letter = word_by_letters[-2]

	return current.value

def traverse_tree_to_start(word, root):
	current = root
	for i in word:
		# print(current.children, i)
		current = current.children[i]
	return current

def get_starting_order():
	answer = ""
	while answer != "y" and answer != "n":
		answer = input("Would you like the human to go first: [y/n]\n")
	return True if answer == "y" else False

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

#def play_ghost(legal_words, root):
	# 	letter_choices = [i for i in alphabet]
	# 	current_word = get_letter(letter_choices)
	# 	print("\nHuman's turn: \n" + str(current_word))
	# 	human = False
	# 	current_node = root
	# 	while len(current_word) < min_word_length or current_word not in legal_words:
	# 		print(current)
	# 		letter_choices = list(current_node.children.keys())
	# 		if human:
	# 			added_letter = get_letter(letter_choices)
	# 			print("\nHuman's turn: ")
	# 		else:
	# 			added_letter, current_node = play(current_word[-1], current_node)
	# 			print("\nBot's turn: ")
	# 		current_word = current_word + added_letter
	# 		human = not human
	# 		print(current_word)
	# 		# print()
	# 		# print(current_word)
	# 	print("Final Word: " + str(current_word) + "\nWinner Human: " + str(human))

def play_ghost(legal_words, root, human = False):
	current_word = ""
	current_node = root
	# # if human:
	# letter_choices = [i for i in alphabet]
	# current_word = get_letter(letter_choices)
	# print("\nHuman's turn: \n")
	# # else:
	# # 	added_letter, current_node = bot_move(current_word, current_node)
	# # 	print("\nBot's turn: ")
	# # human = not human
	# print(current_word)
	
	while len(current_word) < min_word_length or current_word not in legal_words:
		letter_choices = list(current_node.children)
		if human:
			added_letter = get_letter(letter_choices)
			print("\nHuman's turn: ")
		else:
			added_letter = bot_move(current_word, root)
			print("\nBot's turn: ")
		current_word = current_word + added_letter
		current_node = current_node.children[added_letter]
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

def print_tree(root, path = []):
	if root is None:
		return
	path.append(root.value)
	if root.children is None: 
		print(path)

	for i in root.children:
		print_tree(root.children[i], path)

def sort_scrabble(scrabble, short):
	with open(scrabble, "r") as scr:
		with open(short, "w") as sho:
			for i in scr:
				if len(i[:-1].lower()) >= min_word_length:
					sho.write(i.lower())

def initialize_bot(word_file):
	# sort_scrabble("scrabble.txt", "new_scrabble.txt")
	legal_words_list = get_words(word_file)
	root = Node(None, root_value, 0)
	tree = make_tree(word_file, root)
	return legal_words_list, root, tree

def play(current_game_state, word_list):
	play_ghost(legal_words_list, tree, get_starting_order()) 

legal_words_list, root, tree = initialize_bot("scrabble.txt")
# print_tree(tree)
# print(legal_words_list)

# legal_words_list = get_words(word_file)
# root = Node(None, root_value, 0)
# tree = make_tree(word_file, root)

play_ghost(legal_words_list, tree, get_starting_order())
# play_ghost(legal_words_list, tree)
# tree.print_info()
print()

# print_branch(tree, "zeal")


# tree = make_word_tree(word_list)
# print(tree.get_children())
# play_ghost(word_list)