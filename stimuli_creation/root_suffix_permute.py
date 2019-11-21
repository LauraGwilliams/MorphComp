# make stimuli permutations

import numpy as np
import glob
import wave


# paths
root_dir = '/Users/lauragwilliams/Documents/experiments/brothelo'
file_dir = '%s/exp_design/stim_create/chunked' % (root_dir)
out_dir = '%s/exp_design/stim_create/combined' % (root_dir)

# define root path
f0 = '%s/%s.wav' % (file_dir, 'root1')

# define suffixes
suffix_dict = {'NN': ['ist', 'ade', 'ry'],
			   'VN': ['ize'],
			   'NV': ['ure', 'age', 'or'],
			   'VV': ['le'],
			   'AN': ['ic', 'ful', 'al'],
			   'NA': ['ence', 'tude'],
			   'AV': ['able', 'ent', 'ite']}

# helper functions
def wav_append(infiles, outfile):

	data= []
	for infile in infiles:
	    w = wave.open(infile, 'rb')
	    data.append( [w.getparams(), w.readframes(w.getnframes())] )
	    w.close()

	output = wave.open(outfile, 'wb')
	output.setparams(data[0][0])

	for data_n in range(len(infiles)):
		output.writeframes(data[data_n][1])
	output.close()

	pass

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

				f1 = '%s/%s_%s.wav' % (file_dir, seq1, s1)
				f2 = '%s/%s_%s.wav' % (file_dir, seq2, s2)
				f3 = '%s/%s_%s.wav' % (file_dir, seq3, s3)

				infiles = [f0, f1, f2, f3]
				outfile = '%s/%s_%s_%s_%s.wav' % (out_dir, 'root',
												 '_'.join([seq1, s1]),
												 '_'.join([seq2, s2]),
												 '_'.join([seq3, s3]))
				# wav_append(infiles, outfile)

				word_string = ''.join(['koss', s1, s2, s3]) #
				word_sequences.append(word_string)

				word_string = ''.join(['dag', s1, s2, s3]) #
				word_sequences.append(word_string)

				word_string = ''.join(['tok', s1, s2, s3]) #
				word_sequences.append(word_string)

# print(word_sequences)

# listen to them
import os
import random

random.shuffle(word_sequences)
for w in word_sequences[0:10]:
	print(w)
	os.system("say %s -r 120" % (w))

