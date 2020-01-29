import argparse

global rulefile, wordlist

def parse_args():
	global rulefile, wordlist
	parser = argparse.ArgumentParser(description='Python utility to create special wordlist based on partial application of hashcat rules')
	parser.add_argument('rulefile', type=argparse.FileType('r'), help='file name of a hashcat rule file')
	parser.add_argument('wordlist', type=argparse.FileType('r'), help='file name of the wordlist')
	args = parser.parse_args()
	rulefile = args.rulefile
	wordlist = args.wordlist

def main():
	parse_args()
	print(rulefile)
	print(wordlist)

main()