import argparse

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

def main():
	parse_args()
	print(rulefile)
	print(wordlist)

main()