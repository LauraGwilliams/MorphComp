# non-word root selection
# leg5@nyu.edu

import pandas as pd

# paths
git_root = '/Users/lauragwilliams/Documents/experiments/brothelo/MorphComp'
input_fname = '%s/stimuli_creation/corpus_input_files/NonWord.csv' % (git_root)
output_fname = '%s/stimuli_creation/parsed_output/parsed_roots.csv' % (git_root)

# load data
df = pd.read_csv(input_fname)

# not nan or #
not_nan_idx = np.array(map(str, df['Word'].values)) != 'nan'
df = df[not_nan_idx]
not_nan_idx = np.array(map(str, df['BG_Mean'].values)) != '#'
df = df[not_nan_idx]

# mean accuracy as a non-word
df = df.query("NWI_Mean_Accuracy > 0.7 and NWI_Mean_Accuracy < 0.9").reset_index()
df['BG_Mean'] = np.array([float(val.replace(',','')) for val in df['BG_Mean'].values])
df = df.query("BG_Mean > 1000").reset_index()

# ending in a certain string
vowel_cons = ['am', 'em', 'im', 'om', 'um', 'ym',
			  'an', 'en', 'in', 'on', 'un', 'yn']
m_idx = np.array([np.isin(string[-2:], vowel_cons) for string in df['Word'].values])
df = df[m_idx]

# but not ending in:
m_idx = np.array([string[-3:] != 'ion' for string in df['Word'].values])
df = df[m_idx]

m_idx = np.array([string[-3:] != 'ian' for string in df['Word'].values])
df = df[m_idx]

m_idx = np.array([string[-3:] != 'ain' for string in df['Word'].values])
df = df[m_idx]

m_idx = np.array([string[-2:] != 'on' for string in df['Word'].values])
df = df[m_idx]

m_idx = np.array([string[-2:] != 'en' for string in df['Word'].values])
df = df[m_idx]

# take words of different lengths
df.to_csv(output_fname)

# df_short_words = df.query("Length < 5")['Word'].values
# df_mid_words = df.query("Length >= 5 and Length < 7")['Word'].values
# df_long_words = df.query("Length >= 7 and Length < 9")['Word'].values
