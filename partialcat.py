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

def parse(word, rule):
	func = rule[0]
	if func == ':':
		return word
	else if func == 's':
		check = rule[1]
		replace = rule[2]
	return #string.replace(word, check, replace)

def main():
	parse_args()
	for word in wordlist:
		for rule in rulefile:
			print(parse(word, rule))

main()