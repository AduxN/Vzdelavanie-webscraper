import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer

# Load the relevant words CSV with the 'Relevant' column
relevant_words_df = pd.read_csv('relevant_words.csv', sep=";")

# Filter the relevant words
relevant_words = relevant_words_df[relevant_words_df['Relevant'] == 'y']['Word'].tolist()

# Load the subject_info.csv
subject_info_df = pd.read_csv('subject_info.csv')

# Combine the text fields for each subject (you can adjust these columns if needed)
subject_texts = subject_info_df['vysledky'].fillna('') + ' ' + subject_info_df['osnova'].fillna('')


# Clean and tokenize the text (remove special characters, lowercase)
def clean_text(text):
    text = re.sub(r'[^a-zA-ZáäčďéíľĺňóôŕšťúýžÁÄČĎÉÍĽĹŇÓÔŔŠŤÚÝŽ\s]', '', text.lower())
    return text


# Clean the subject texts
cleaned_subject_texts = subject_texts.apply(clean_text)

# Create a CountVectorizer using the filtered relevant words
vectorizer = CountVectorizer(vocabulary=relevant_words)

# Transform the cleaned texts into the DTM (rows are subjects, columns are word counts)
dtm = vectorizer.fit_transform(cleaned_subject_texts)

# Convert the DTM into a DataFrame for easier handling
dtm_df = pd.DataFrame(dtm.toarray(), columns=vectorizer.get_feature_names_out(), index=subject_info_df['code'])

dtm_df = dtm_df.drop_duplicates()

# Save the DTM to a CSV file
dtm_df.to_csv('document_term_matrix.csv', index=True, header=True)

print("Document-Term Matrix saved to 'document_term_matrix.csv'")

# Create an empty list to store the results
top_subjects_per_word = []

# Iterate over each word (column) in the DTM matrix
for word in dtm_df.columns:
    # Sort subjects by the occurrences of the current word (in descending order)
    top_subjects = dtm_df[word].sort_values(ascending=False).head(3)

    # Extract the top 3 subjects and their occurrences
    subject1, subj1_count = top_subjects.index[0], top_subjects.iloc[0]
    subject2, subj2_count = top_subjects.index[1], top_subjects.iloc[1] if len(top_subjects) > 1 else ('', 0)
    subject3, subj3_count = top_subjects.index[2], top_subjects.iloc[2] if len(top_subjects) > 2 else ('', 0)

    # Append the word and the top 3 subjects with their occurrences to the results list
    top_subjects_per_word.append([word, subject1, subj1_count, subject2, subj2_count, subject3, subj3_count])

# Convert the results list to a DataFrame
top_words_df = pd.DataFrame(top_subjects_per_word, columns=[
    'Word', 'Subject1', 'Subj1_Occurrences', 'Subject2', 'Subj2_Occurrences', 'Subject3', 'Subj3_Occurrences'
])

# Save the results to a CSV file
top_words_df.to_csv('top_subjects_per_word.csv', index=False)

print("Top 3 subjects per word saved to 'top_subjects_per_word.csv'")

# top_words_df = pd.read_csv('top_subjects_per_word_dynamic.csv')

# Replace subject codes with "-" where the corresponding occurrence is 0
top_words_df.loc[top_words_df['Subj1_Occurrences'] == 0, 'Subject1'] = '-'
top_words_df.loc[top_words_df['Subj2_Occurrences'] == 0, 'Subject2'] = '-'
top_words_df.loc[top_words_df['Subj3_Occurrences'] == 0, 'Subject3'] = '-'

# Save the updated DataFrame back to a new CSV file
top_words_df.to_csv('top_subjects_per_word_final.csv', index=False)
