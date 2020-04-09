import argparse
import string

global rulefile		# Array containing the contents of the passed in rule file
global wordlist		# Array containing the contents of the passed in wordlist

# Parse command line options and read in the rule and word lists
def parse_args():
	global rulefile, wordlist
	parser = argparse.ArgumentParser(description='Python utility to create special wordlist based on partial application of hashcat rules')
	parser.add_argument('rulefile', type=argparse.FileType('r'), help='file name of a hashcat rule file')
	parser.add_argument('wordlist', type=argparse.FileType('r'), help='file name of the wordlist')
	args = parser.parse_args()
	rulefile = args.rulefile.read().splitlines()
	wordlist = args.wordlist.read().splitlines()

def funcS(word, rule):
	check = rule[1]
	replace = rule[2]
	list = []
	for i in range(1, word.count(check)+1):
		list.append(word.replace(check, replace, i))
	return list

def parse(word, rule):
	print("Apply " + rule + " to " + word)
	func = rule[0]
	if func == ':':
		return word
	elif func == 's':
		return funcS(word, rule)
	return

def main():
	parse_args()
	for word in wordlist:
		for rule in rulefile:
			for result in parse(word, rule):
				print(result)

main()