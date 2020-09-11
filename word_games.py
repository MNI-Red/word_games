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

	def print_info(self):
		print("Value: " + str(self.value) + "\nChildren keys: " + str(self.children) + "\nDistance from root: " + str(self.distance_from_root))


def get_words(file, root):
	with open(file, "r") as f:
		add_word(next(f)[:-1].lower(), root, checks = True)
		for word in f:
			to_add = word[:-1].lower()
			add_word(to_add, root)

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

def add_word(word, root, checks = False):
	parent = root
	stack = []
	for i in word:
		if not checks:
			if not parent.children:
				print("exited, no children, is a word")
				return
			if i in parent.children:
				stack.append(parent)
				parent = parent.children[i]
				continue

		added = add_leaf(parent, i)
		parent = added
		stack.append(parent)

	last = stack.pop()
	length = 1
	while(stack):
		current = stack.pop()
		current.paths[length] += 1
		length += 1

def add_leaf(parent, value):
	leaf = Node(parent, value, parent.distance_from_root + 1)
	print("leaf")
	leaf.print_info()
	print()
	parent.add_children(leaf)
	return leaf

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

root = Node(None, " ", 0)
tree = get_words("small_scrabble.txt", root)
print(len(tree.children))
print(tree.children.keys())
# tree = make_word_tree(word_list)
# print(tree.get_children())
# play_ghost(word_list)
