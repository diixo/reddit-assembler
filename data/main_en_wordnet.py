
import nltk
from nltk.corpus import wordnet as wn


nltk.download('wordnet')


english_words = set()

for synset in wn.all_synsets():
    for lemma in synset.lemmas():
        txt = lemma.name().replace("_", " ")
        english_words.add(txt)

with open("data/nltk_english_wordnet_words.txt", "w", encoding="utf-8") as f:
    for word in sorted(english_words):
        f.write(word + "\n")

print(f"Saved: {len(english_words)} words into: wordnet_english_words.txt")

