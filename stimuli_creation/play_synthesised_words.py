# leg5@nyu.edu
# synthesise and play word candidates

# modules
import pandas as pd
import os
import random

# paths
git_root = '/Users/lauragwilliams/Documents/experiments/brothelo/MorphComp'
input_fname = '%s/stimuli_creation/parsed_output/word_candidates.csv' % (git_root)

# params
speech_rate = 120

# load word candidates
word_list = pd.read_csv(input_fname)['words']

# listen to them
random.shuffle(word_list)
for w in word_list[0:10]:
	print(w)
	os.system("say %s -r %s" % (w, speech_rate))