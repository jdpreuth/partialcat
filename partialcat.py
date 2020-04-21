#####################################
# Partialcat                        #
# Desc: Python wordlist creation    #
# tool based on hashcat rule engine #
# Author: Jon Preuth                #
#####################################

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

# Function called for rule 's'. Replaces instances of one character with another for all possible permutations of replacements in that word
# Input:
#	words: The list of words to which the rule should be applied
#	check: The character to be replaced
#	replace: The character to replace the checked character with
# Output: A list containing all possible permutations of a given substitution being applied
# EX: apple, sp6 -> a6ple, a66le
def substitution(words, check, replace):
	parsed = set([])
	sub = {check : replace}
	for word in words:
		parsed.add(word)
		parsed.update([''.join(letters) for letters in product(*({c, sub.get(c, c)} for c in word))])
	return parsed
 
# Function called for rule 'u'. Creates all possible uppercase combinations
# Input:
#	words: The list of words to apply the rule to
# Output: The list of words expanded to include all upper case character combinations
# EX: ate -> ate, atE, aTe, aTE, Ate, AtE, ATE
def uppercase(words):
	parsed = set([])
	for word in words:
		sub = {}
		for letter in word:
			sub.update({letter: letter.upper()})
		parsed.add(word)
		parsed.update([''.join(letters) for letters in product(*({c, sub.get(c, c)} for c in word))])
	return parsed

# Function called for rule 'c'. Capitalizes the first letter of each word in the inputted word list
# Input:
#	words: The list of words to apply the rule to
# Output: The list of words expanded to include the first letter capitlized
# EX: ate -> Ate
def capital(words):
	parsed = set([])
	for word in words:
		parsed.add(word.capitalize())
	return parsed

# Main parsing function. Determines the rule to be applied and calls the matching rule functions.
# Input:
#	word: The word to be processed
#	rule: The rule to be applied
# Output: A list of the iterative, partial application of a given rule to a word
def parse(word, rule):
	parsed = set([word])		# This seeds the list of words to be parsed. Removed as the final step.
	i = 0
	while i < len(rule):
		func = rule[i]
		i += 1
		if func == ':':
			pass # parsed.add(word)
		elif func == 's':
			check = rule[i]
			i += 1
			replace = rule[i]
			i += 1
			parsed.update(substitution(parsed, check, replace))
		elif func == 'u':
			parsed.update(uppercase(parsed))
		elif func == 'c':
			parsed.update(capital(parsed))
	#parsed.pop(0)	# Remove the seed value before returning
	#print(parsed)	Debug print statement to see each round of parsed words
	return parsed

def main():
	# Parse input arguments and generate the wordlist
	rulefile, wordlist = parse_args()
	output = set([])
	for word in wordlist:
		output.add(word)
		for rule in rulefile:
			output.update(parse(word, rule))
			#print(output)
	
	# Output the generated wordlist
	for word in output:
		print(word)

main()