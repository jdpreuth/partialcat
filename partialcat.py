import argparse
import string
from itertools import product

# Parse command line options and read in the rule and word lists
# Output: The rulefile and wordlist as arrays
def parse_args():
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
# EX: apple, sp6 -> a6ple, a66le
def substitution(words, check, replace):
	parsed = []
	sub = {check: replace}
	for word in words:
		parsed.extend([''.join(letters) for letters in product(*({c, sub.get(c, c)} for c in word))])
	return parsed
 
# Function called for rule 'u'. Creates all possible uppercase combinations
# Note: Far from optimized. Produces many duplicates. Run output through sort | uniq to minimize
# Input:
#	words: The list of words to apply the rule to
# Output: The list of words expanded to include all upper case character combinations
# EX: ate -> ate, atE, aTe, aTE, Ate, AtE, ATE
def uppercase(words):
	parsed = []
	for word in words:
		toggles = []
		toggles.append(word)
		for i in range(0, len(word)):
			permutations = []
			for toggle in toggles:
				permutations.append(toggle)
				permutations.append(toggle[:i] + toggle[i].upper() + toggle[(i+1):])
			toggles.extend(permutations)
		parsed.extend(toggles)
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
			parsed.extend(substitution(parsed, check, replace))
		elif func == 'u':
			parsed.extend(uppercase(parsed))
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