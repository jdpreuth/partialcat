import argparse
import string

global rulefile		# Array containing the contents of the passed in rule file
global wordlist		# Array containing the contents of the passed in wordlist
global output		# Array containing the genereated wordlist to be outputted

# Parse command line options and read in the rule and word lists
def parse_args():
	global rulefile, wordlist
	parser = argparse.ArgumentParser(description='Python utility to create special wordlist based on partial application of hashcat rules')
	parser.add_argument('rulefile', type=argparse.FileType('r'), help='file name of a hashcat rule file')
	parser.add_argument('wordlist', type=argparse.FileType('r'), help='file name of the wordlist')
	args = parser.parse_args()
	rulefile = args.rulefile.read().splitlines()
	wordlist = args.wordlist.read().splitlines()

# Function called for rule 's'. Replaces instances of one character with another
def funcS(words, check, replace):
	parsed = []
	for word in words:
		for i in range(1, word.count(check)+1):
			parsed.append(word.replace(check, replace, i))
	return parsed

# Main parsing function. Determines the rule to be applied and calls the matching rule functions.
# Populates global output array with the generated words
def parse(word, rule):
	parsed = [word]
	i = 0
	while i < len(rule):
		func = rule[i]
		i += 1
		if func == ':':
			parsed.append(word)
		elif func == 's':
			check = rule[i]
			i += 1
			replace = rule[i]
			i += 1
			parsed.extend(funcS(parsed, check, replace))
			print(parsed)
	parsed.pop(0)
	return parsed

def main():
	global output
	output = []

	# Parse input arguments and generate the wordlist
	parse_args()
	for word in wordlist:
		for rule in rulefile:
			output.extend(parse(word, rule))
	
	# Output the generated wordlist
	for word in output:
		print(word)

main()