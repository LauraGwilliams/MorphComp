# leg5@nyu.edu
# make stimuli permutations

import numpy as np
import pandas as pd

# paths
git_root = '/Users/lauragwilliams/Documents/experiments/brothelo/MorphComp'
input_fname = '%s/stimuli_creation/parsed_output/picked_roots-annotated.csv' % (git_root)
output_fname = '%s/stimuli_creation/parsed_output/word_candidates.csv' % (git_root)

# load roots
root_df = pd.read_csv(input_fname)
root_df = root_df.query("accept == 1")
roots = root_df['root'].values

# define suffixes
suffix_dict = {'NN': ['ist', 'ade', 'ry'],
			   'VN': ['ize'],
			   'NV': ['ure', 'age', 'or'],
			   # 'VV': ['le'],
			   'AN': ['ic', 'ful', 'al'],
			   'NA': ['ence', 'tude'],
			   'AV': ['able', 'ent', 'ite']}

# create sequences
trans = suffix_dict.keys()
sequences = list()
for s1 in trans:

	# find possible 2nd pos suffixes
	s2s = np.array(trans)[[t[1] == s1[0] for t in trans]]

	for s2 in s2s:
		# find possible 3rd pos suffixes
		s3s = np.array(trans)[[t[1] == s2[0] for t in trans]]

		for s3 in s3s:
			# add the 3 sequences to the bin
			sequences.append([s1, s2, s3])

# loop through sequences and build words
file_sequences = np.zeros([len(sequences), 3])
word_sequences = list()
root_list = list()
s1s = list()
s2s = list()
s3s = list()
all_sequences = list()
t1s = list()
t2s = list()
t3s = list()

all_infiles = list()
for sequence in sequences:

	seq1 = sequence[0]
	seq2 = sequence[1]
	seq3 = sequence[2]

	if seq1 == seq2 or seq2 == seq3:
		continue

	infiles = list()
	for s1 in suffix_dict[seq1]:
		for s2 in suffix_dict[seq2]:
			for s3 in suffix_dict[seq3]:

				if s1 == s2 or s2 == s3 or s1 == s3:
					continue

				if s1 == 'ic' and s2 == 'ence' or s2 == 'ic' and s3 == 'ence':
					continue
				if s1 == 'ic' and s2 == 'ite' or s2 == 'ic' and s3 == 'ite':
					continue
				if s1 == 'dom' or s2 == 'dom':
					continue

				# add suffixes to root, and add to bin
				for root, nsyll in root_df[['root', 'nsyll']].values:
					if nsyll == 1:
						word_string = ''.join([root, s1, s2, s3])
						s1s.append(s1)
						s2s.append(s2)
						s3s.append(s3)
						t1s.append(seq1)
						t2s.append(seq2)
						t3s.append(seq3)

					if nsyll == 2:
						word_string = ''.join([root, s1, s2])
						s1s.append(s1)
						s2s.append(s2)
						s3s.append('')
						t1s.append(seq1)
						t2s.append(seq2)
						t3s.append('')

					if nsyll == 3:
						word_string = ''.join([root, s1])
						s1s.append(s1)
						s2s.append('')
						s3s.append('')
						t1s.append(seq1)
						t2s.append('')
						t3s.append('')

					word_sequences.append(word_string)
					root_list.append(root)
					all_sequences.append('_'.join(sequence))

# save results
df = pd.DataFrame()
df['words'] = np.array(word_sequences)
df['roots'] = np.array(root_list)
df['s1'] = np.array(s1s)
df['s2'] = np.array(s2s)
df['s3'] = np.array(s3s)
df['sequence'] = np.array(all_sequences)
df['t1'] = np.array(t1s)
df['t2'] = np.array(t2s)
df['t3'] = np.array(t3s)
df.to_csv(output_fname)
