import re
from collections import Counter
import pandas as pd

df = pd.read_csv('csv/subject_info.csv')

# scraped_data = ' '.join(df['podmienky'].fillna('') + ' ' + df['vysledky'].fillna('') + ' ' + df['osnova'].fillna(''))
scraped_data = ' '.join(df['vysledky'].fillna('') + ' ' + df['osnova'].fillna(''))
# scraped_data = ' '.join(df['osnova'].fillna(''))

slovak_stopwords = [
    'a', 'aby', 'aj', 'ak', 'ale', 'alebo', 'ani', 'ako', 'asi', 'ba', 'bez',
    'by', 'bol', 'bola', 'boli', 'bude', 'cez', 'čo', 'do', 'ešte', 'ho', 'ja',
    'je', 'ju', 'k', 'kam', 'keď', 'kde', 'lebo', 'len', 'ma', 'má', 'málo',
    'mi', 'my', 'na', 'nad', 'ne', 'než', 'nich', 'nie', 'o', 'od', 'po', 'pod',
    'pre', 'pri', 's', 'so', 'som', 'sa', 'si', 'ste', 'sme', 'ten', 'to', 'tu',
    'tvoj', 'u', 'v', 'za', 'z', 'že', 'čo', 'kým'
]

def clean_and_tokenize(text):
    text = re.sub(r'[^a-zA-ZáäčďéíľĺňóôŕšťúýžÁÄČĎÉÍĽĹŇÓÔŔŠŤÚÝŽ\s]', '', text.lower())
    words = text.split()
    words = [word for word in words if word not in slovak_stopwords]
    return words

words = clean_and_tokenize(scraped_data)

word_freq = Counter(words)
most_common_words = word_freq.most_common(1000)

df_common_words = pd.DataFrame(most_common_words, columns=['Word', 'Frequency'])

df_common_words.to_csv('common_words.csv', index=False)

corpus = [word for word, freq in most_common_words]

print(most_common_words)
print(corpus)
