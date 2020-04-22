#####################################
# Partialcat                        #
# Desc: Python wordlist creation    #
# tool based on hashcat rule engine #
# Author: Jon Preuth                #
#####################################

import argparse
import string
from itertools import product

# Optional flags
global IGNORE
global OUTPUT

# Parse command line options and read in the rule and word lists
# Output: The rulefile and wordlist as arrays
def parse_args():
	global IGNORE, OUTPUT
	parser = argparse.ArgumentParser(description='Python utility to create special wordlist based on partial application of hashcat rules')
	parser.add_argument('rulefile', type=argparse.FileType('r'), help='file name of a hashcat rule file')
	parser.add_argument('wordlist', type=argparse.FileType('r'), help='file name of the wordlist')
	parser.add_argument('-i', '--ignore', action="store_true", help='ignore unsupported rules')
	parser.add_argument('-o', '--output', help='file name to write the output to')
	args = parser.parse_args()
	rulefile = args.rulefile.read().splitlines()
	wordlist = args.wordlist.read().splitlines()
	IGNORE = args.ignore
	OUTPUT = args.output

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

# Function called for rule 'l'. Creates all possible lowercase combinations
# Input:
#	words: The list of words to apply the rule to
# Output: The list of words expanded to include all lowercase character combinations
# EX: ATE -> ate, atE, aTe, aTE, Ate, AtE, ATE
def lowercase(words):
	parsed = set([])
	for word in words:
		sub = {}
		for letter in word:
			sub.update({letter: letter.lower()})
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

# Function called for rule 't'. Toggles case of each character of each word in the inputted word list in all permutations
# Input:
#	words: The list of words to apply the rule to
# Output: The list of words expanded to include all toggled case combinations
# EX: aTe -> ate, atE, aTe, aTE, Ate, AtE, ATE
def toggle(words):
	parsed = set([])
	for word in words:
		sub = {}
		for letter in word:
			sub.update({letter: letter.swapcase()})
		parsed.add(word)
		parsed.update([''.join(letters) for letters in product(*({c, sub.get(c, c)} for c in word))])
	return parsed

# Function called for rule 'TN'. Toggles case of characters at position N
# Input:
#	words: The list of words to apply the rule to
#	position: The Nth place to toggle the character. 0 indexed
# Output: The list of words expanded to include the toggled cases
# EX: aTe, bad, T3 -> aTE, baD
def toggleN(words, N):
	parsed = set([])
	for word in words:		
		parsed.add(word[:N] + word[N].swapcase() + word[(N+1):])
	return parsed

# Function called for rule 'r'. Reverses each word in the inputted word list
# Input:
#	words: The list of words to apply the rule to
# Output: The list of words reversed
# EX: ate -> eta
def reverse(words):
	parsed = set([])
	for word in words:
		parsed.add(word[::-1])
	return parsed

# Function called for rule 'd'. Duplicates each word in the inputted word list
# Input:
#	words: The list of words to apply the rule to
# Output: The list of words duplicated
# EX: ate -> ateate
def duplicate(words):
	parsed = set([])
	for word in words:
		parsed.add(word + word)
	return parsed

# Function called for rule 'pN'. Append duplicated word N times
# Input:
#	words: The list of words to apply the rule to
# Output: The list of words duplicated N times
# EX: ate, p2 -> ateateate
def duplicateN(words, N):
	parsed = set([])
	for word in words:
		dup = word
		for i in range(0, N):
			dup = dup + word
		parsed.add(dup)
	return parsed

# Function called for rule 'f'. Duplicates each word in the inputted word list reversed
# Input:
#	words: The list of words to apply the rule to
# Output: The list of words duplicated in reverse
# EX: ate -> ateeta
def reflect(words):
	parsed = set([])
	for word in words:
		parsed.add(word + word[::-1])
	return parsed

# Function called for rule '$X'. Appends character X to the end of each word
# Input:
#	words: The list of words to apply the rule to
#	char: The character to be appended
# Output: The list of words with the chars appended
# EX: ate, $X -> ateX
def append(words, char):
	parsed = set([])
	for word in words:
		parsed.add(word + char)
	return parsed

# Function called for rule '^X'. Preprends character X to the beginning of each word
# Input:
#	words: The list of words to apply the rule to
#	char: The character to be preprended
# Output: The list of words with the chars prepended
# EX: ate, ^X -> Xate
def prepend(words, char):
	parsed = set([])
	for word in words:
		parsed.add(char + word)
	return parsed

# Function called for rule '['. Truncates characters from the left.
# Input:
#	words: The list of words to apply the rule to
# Output: The list of words with all left truncations of the word
# EX: ate-> ate, te, e
def trunLeft(words):
	parsed = set([])
	for word in words:
		for i in range(1, len(word)):
			parsed.add(word[i:])
	return parsed

# Function called for rule ']'. Truncates characters from the right.
# Input:
#	words: The list of words to apply the rule to
# Output: The list of words with all right truncations of the word
# EX: ate-> ate, at, a
def trunRight(words):
	parsed = set([])
	for word in words:
		for i in range(len(word), 0, -1):
			parsed.add(word[:i])
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
			pass
		elif func == 'l':
			parsed.update(lowercase(parsed))
		elif func == 'u':
			parsed.update(uppercase(parsed))
		elif func == 'c':
			parsed.update(capital(parsed))
		elif func == 't':
			parsed.update(toggle(parsed))
		elif func == 'T':
			N = rule[i]
			i += 1
			parsed.update(toggleN(parsed, int(N)))
		elif func == 'r':
			parsed.update(reverse(parsed))
		elif func == 'd':
			parsed.update(duplicate(parsed))
		elif func == 'p':
			N = rule[i]
			i += 1
			parsed.update(duplicateN(parsed, int(N)))
		elif func == 'f':
			parsed.update(reflect(parsed))
		elif func == '$':
			char = rule[i]
			i += 1
			parsed.update(append(parsed, char))
		elif func == '^':
			char = rule[i]
			i += 1
			parsed.update(prepend(parsed, char))
		elif func == '[':
			parsed.update(trunLeft(parsed))
		elif func == ']':
			parsed.update(trunRight(parsed))
		elif func == 's':
			check = rule[i]
			i += 1
			replace = rule[i]
			i += 1
			parsed.update(substitution(parsed, check, replace))
		else:		# Function isn't currently supported or incorrect rule. Error and exit
			if not IGNORE:
				print("Rule { " + func + " } isn't supported. Run with the -i flag to simply ignore unsupported rules")
				exit()	
	return parsed

def main():
	global IGNORE, OUTPUT
	# Parse input arguments and generate the wordlist
	rulefile, wordlist = parse_args()
	output = set([])
	for word in wordlist:
		output.add(word)
		for rule in rulefile:
			output.update(parse(word, rule))
	
	# Output the generated wordlist
	if not OUTPUT:
		for word in output:
			print(word)
	else:
		with open(OUTPUT, 'w') as file:
			for word in output:
				print(word)
				file.write(word + '\n')

main()