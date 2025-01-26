import pandas as pd
from stemmer import stem

# Load CSV file
df = pd.read_csv('csv/top_subjects_per_word.csv', sep=',')


# Function to stem words and update occurrences
def stem_and_recount(row):
    stemmed_word = stem(row['Word'])
    row['Stemmed_Word'] = stemmed_word

    # Initialize a dictionary to hold total occurrences per stemmed word
    occurrences = {}

    # Recalculate occurrences after stemming
    for i in range(1, 4):
        subj_col = f'Subject{i}'
        occ_col = f'Subj{i}_Occurrences'

        # Add occurrences of the stemmed word
        occurrences[row[subj_col]] = occurrences.get(row[subj_col], 0) + row[occ_col]

    return pd.Series([stemmed_word, occurrences])


# Apply the function and store stemmed words and new occurrences
df[['Stemmed_Word', 'Recounted_Occurrences']] = df.apply(stem_and_recount, axis=1)

# Save the modified dataframe to a new CSV
df.to_csv('csv/stemmed_output.csv', index=False, sep=';')
