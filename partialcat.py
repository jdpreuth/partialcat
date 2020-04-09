import argparse
import string

# Parse command line options and read in the rule and word lists
# Output: The rulefile and wordlist as arrays
def parse_args():
	#global rulefile, wordlist
	parser = argparse.ArgumentParser(description='Python utility to create special wordlist based on partial application of hashcat rules')
	parser.add_argument('rulefile', type=argparse.FileType('r'), help='file name of a hashcat rule file')
	parser.add_argument('wordlist', type=argparse.FileType('r'), help='file name of the wordlist')
	args = parser.parse_args()
	rulefile = args.rulefile.read().splitlines()
	wordlist = args.wordlist.read().splitlines()
	return rulefile, wordlist

# Function called for rule 's'. Replaces instances of one character with another in a partial, iterative fashion
# Input:
#	words: The list of words to which the rule should be applied
#	check: The character to be replaced
#	replace: The character to replace the checked character with
# Output: The list created by partially applying the given rule to the inputted word list
def funcS(words, check, replace):
	parsed = []
	for word in words:
		for i in range(1, word.count(check)+1):
			parsed.append(word.replace(check, replace, i))
	return parsed

# Main parsing function. Determines the rule to be applied and calls the matching rule functions.
# Input:
#	word: The word to be processed
#	rule: The rule to be applied
# Output: A list of the iterative, partial application of a given rule to a word
def parse(word, rule):
	parsed = [word]		# This seeds the list of words to be parsed. Removed as the final step.
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
	parsed.pop(0)	# Remove the seed value before returning
	#print(parsed)	Debug print statement to see each round of parsed words
	return parsed

def main():
	# Parse input arguments and generate the wordlist
	rulefile, wordlist = parse_args()
	output = []
	for word in wordlist:
		for rule in rulefile:
			output.extend(parse(word, rule))
	
	# Output the generated wordlist
	for word in output:
		print(word)

main()