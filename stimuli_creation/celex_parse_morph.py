# leg5@nyu.edu
# extract morphemes from celex

# modules
import numpy as np
import pandas as pd
import re

# params
doc_name = 'eml'
col_names = ['IdNum', 'Head', 'Cob', 'MorphStatus', 'Lang', 'MorphCnt',
			 'NVAffComp', 'Der', 'Comp', 'DerComp', 'Def', 'Imm',
             'ImmSubCat', 'ImmSA', 'ImmAllo', 'ImmSubst', 'ImmOpac',
             'TransDer', 'ImmInfix', 'ImmRevers', 'FlatSA', 'StrucLab',
             'StrucAllo', 'StrucSubst', 'StrucOpac']

chosen_suffix_list = ['ize', 'ise', 'ure', 
			   'age', 'or', 'ist',
			   'ade', 'ry', 'ence', 
			   'tude', 'ent', 'ite', 
			   'ic', 'ful', 'al']

# paths
celex_path= '/Users/lauragwilliams/Documents/programming/corpora/celex/english/%s/%s.cd' % (doc_name, doc_name)

# load data as a pandas dataframe
df = pd.read_csv(celex_path, sep='\\', names=col_names)

# remove nans
idx = np.array(map(str, df['StrucLab'].values)) != 'nan'
df = df[idx]

# use regular expression to count the number of morphemes in each row
df['n_morph'] = np.array([len(re.findall('\[\w\]', row)) for row in df['StrucLab'].values])
df = df.query('n_morph > 1')

# check for words with particular sequences
# sequence = '\[N\|\w\.\].*\[V\|N\.\].*\[N\|V\.\]'
sequence = '\[N\|\N\.\].*\[N\|N\.\]'  # NN
sequence = '\[V\|\V\.\].*\[V\|V\.\]'  # VV
sequence = '\[V\|\N\.\].*\[N\|V\.\]'  # VN
sequence = '\[N\|\V\.\].*\[V\|N\.\]'  # NV
sequence = '\[N\|[NV]\.\].*\[N\|N\.\]'

min_reps = 1
count = 0
unique_suffixes = list()
for structure, label in df[['StrucLab', 'Head']].values:
	if len(re.findall(sequence, structure)) >= min_reps:
		count += 1
# 		print(structure, label)
# 		print('')
# print count


# init
suffix_strings = list()
transformations = list()
frequencies = list()
orders = list()
words = list()

for structure_string, string_freq, w in df[['StrucLab', 'Cob', 'Head']].values:

	# use regular expression to extract the suffix and its transformation
	suffixes = re.findall('\(\w+\)\[\w\|\w\.\]', structure_string)

	# skip if the word has a space (is a compound)
	# if ' ' in w:
	# 	continue

	# put the suffix and its function into the bins
	for si, suffix in enumerate(suffixes):

		# pull out the clean suffix and the clean trans
		s_string, trans = suffix.split('(')[1].split(')')

		# do not consider if the onset is not a vowel
		# if s_string[0] not in ['a', 'e', 'i', 'o', 'u', 'y']:
		# 	continue

		# skip if this example has been noted already
		# if s_string in suffix_strings and trans in transformations:
		# 	continue

		# otherwise, put in the bin
		suffix_strings.append(s_string)
		transformations.append(trans)
		frequencies.append(string_freq)
		orders.append(len(suffixes)-si)
		words.append(w)

suffix_df = pd.DataFrame()
suffix_df['suffix'] = np.array(suffix_strings)
suffix_df['trans'] = np.array(transformations)
suffix_df['freq'] = np.array(frequencies)
suffix_df['order'] = np.array(orders)
suffix_df['example_word'] = np.array(words)

# remove suffixes that occur in more than one transformation
picked_ratio = list()
mono_suffix = list()
ratio_suffixes = list()
for suff in np.unique(suffix_df['suffix']):

	# get info for this suffix
	suff_df = suffix_df.query("suffix == @suff")

	# if suff == 'ion':
	# 	print(suff_df)
	# 	0/0

	# remove counts that are zero
	suff_df = suff_df.query("freq > 0")
	if len(suff_df) == 0:
		continue

	# check whether the suffix occurs as a particular trans xN more than others
	suffix_trans_count = suff_df.groupby(['suffix', 'trans']).freq.sum()
	suff_counts = suffix_trans_count.as_matrix()

	# if it is a picked suffix, add to our list
	if suff in chosen_suffix_list:
		picked_ratio.append(suffix_trans_count)

	# find max value, and check it is x2 more than the rest
	ratio = 0  # use 2
	max_count = suff_counts.max()
	if max_count == 0:
		continue

	max_idx = np.argmax(suff_counts)
	suffix_list = [suffix_trans_count.keys()[ii][1] for ii in range(len(suff_counts))]
	most_freq_trans = suffix_list[max_idx]
	if sum(((float(max_count) / suff_counts) <= ratio)) > 1:
		continue

	# subset just the trans we want
	suff_df = suff_df.query("trans == @most_freq_trans")

	# count the number of unique words with this suffix
	suff_df['unique_count'] = len(suff_df)

	# get counts
	# trans_count = len(np.unique(suff_df['trans']))
	order_count = len(np.unique(suff_df['order']))
	if suff_df['order'].mean() > 1.1: #trans_count == 1 and 
		mono_suffix.append(suff)
		ratio_suffixes.append(suff_df)

	# if suff == 'ite':
	# 	print(suff_df)
	# 	0/0

kp_idx = np.isin(suffix_df['suffix'].values, mono_suffix)
# suffix_mono = suffix_df[kp_idx]
suffix_mono = pd.concat(ratio_suffixes)

# subset just the suffixes that do the trans we want
suffix_POS = suffix_mono.query("trans == '[N|A.]' or trans == '[A|N.]' or trans == '[N|N.]' or trans == '[A|A.]'")

# # count number of words the suffix is contained within
# # suffix_POS = suffix_mono[suffix_mono.trans.str.contains('\[B\|\w\.\]')]
# suffix_POS = suffix_mono[suffix_mono.trans.str.contains('\[N\|[AV]\.\]')]
# suffix_POS = suffix_mono[suffix_mono.trans.str.contains('\[[AVN]\|[AVN]\.\]')]
# suffix_POS = suffix_mono[suffix_mono.trans.str.contains('\[[A]\|[V]\.\]')]
# suffix_POS = suffix_mono.query("trans == '[V|*.]'")
suffix_counts = suffix_POS.groupby(['suffix', 'trans', 'unique_count']).freq.sum()
print(suffix_counts)
print(len(suffix_counts))
# suffix_POS.suffix.value_counts()


suffs = list()
transes = list()
count_tokens = list()
count_types = list()
example_words = list()

for suffix in suffix_df['suffix'].unique():
	# df for this suffix
	suff_dict = suffix_df.query("suffix == @suffix")['trans'].value_counts()

	# loop through each trans
	for trans in suff_dict.keys():
		suffs.append(suffix)
		transes.append(trans)
		count_types.append(suff_dict[trans]) # how many times this trans appears

		# get the token count multiplied by the freq of the words
		count_tokens.append(sum(suffix_df.query("trans == @trans")['freq'].values))
		example_words.append(suffix_df.query("trans == @trans and suffix == @suffix")['example_word'].values[0])

final_df = pd.DataFrame()
final_df['suffix'] = suffs
final_df['trans'] = transes
final_df['count_token'] = count_tokens
final_df['count_types'] = count_types
final_df['example_word'] = example_words

