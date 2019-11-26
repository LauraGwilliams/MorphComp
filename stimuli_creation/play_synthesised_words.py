# leg5@nyu.edu
# synthesise and play word candidates

# modules
import pandas as pd
import os
import random

# paths
git_root = '/Users/lauragwilliams/Documents/experiments/brothelo/MorphComp'
input_fname = '%s/stimuli_creation/parsed_output/word_candidates.csv' % (git_root)
input_fname = '%s/stimuli_creation/parsed_output/picked_roots.csv' % (git_root)


suffixes = ['ist', 'ade', 'ry', 'ize', 'ure', 'age', 'or',
			'ic', 'ful', 'al', 'ence', 'tude', 'able', 'ent',
			'ite']

# params
speech_rate = 120

# load word candidates
word_list = pd.read_csv(input_fname)['root']

# listen to them
# random.shuffle(word_list)
for ii, w in enumerate(['charlotan']):
	for suffix in suffixes:
		complex_word = w+suffix
		print(ii, complex_word)
		os.system("say %s -r %s" % (complex_word, speech_rate))
		raw_input("Press Enter to continue...")

