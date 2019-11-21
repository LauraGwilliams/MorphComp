# leg5@nyu.edu
# save wav files of stimuli

# modules
import wave
import glob

# paths
root_dir = '/Users/lauragwilliams/Documents/experiments/brothelo'
file_dir = '%s/exp_design/stim_create/chunked' % (root_dir)
out_dir = '%s/exp_design/stim_create/combined' % (root_dir)

# define root path
f0 = '%s/%s.wav' % (file_dir, 'root1')

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


f1 = '%s/%s_%s.wav' % (file_dir, seq1, s1)
f2 = '%s/%s_%s.wav' % (file_dir, seq2, s2)
f3 = '%s/%s_%s.wav' % (file_dir, seq3, s3)

infiles = [f0, f1, f2, f3]
outfile = '%s/%s_%s_%s_%s.wav' % (out_dir, 'root',
								 '_'.join([seq1, s1]),
								 '_'.join([seq2, s2]),
								 '_'.join([seq3, s3]))


# print(word_sequences)

# listen to them
import os
import random

random.shuffle(word_sequences)
for w in word_sequences[0:10]:
	print(w)
	os.system("say %s -r 120" % (w))