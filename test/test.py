# Test Harness for WordBrain puzzles

from os import sys, path

ADDED_WORDS = ['tv', 'haystack', 'crab', 'scooter', 'snowman', 'elk', 'chimney', 'cabin', 'biscuit', 'mince']
ADVANCED = False

# Solution from: http://stackoverflow.com/questions/11536764/how-to-fix-attempted-relative-import-in-non-package-even-with-init-py
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from src import solver

test_vals = [\
			([4], 'oavl', 2, ['oval']), \
			([4,5], 'imclaraen', 3, ['nail', 'cream']), \
			([4,6,6], 'raweebtlmturtins', 4, ['turtle', 'timber', 'swan'])\
			### INSERT MORE TESTS HERE ###
			]

for test_tuple in test_vals:
	if not test_tuple[3] in solver.main(ADVANCED, ADDED_WORDS, test_tuple[0], test_tuple[2], test_tuple[1], False):
		print "FAILURE: ", test_tuple	

