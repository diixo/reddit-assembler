
from utils import clean_text, filter_dictionary


if __name__ == "__main__":

    txt = "   Hello!   "
    print(clean_text(txt))

    txt = "Wow  ou  yeah! ![gif](giphy|abc123)"
    print(clean_text(txt))

    txt = text = "It is funny good_day! ![gif](giphy|60rNlHSC6PoBy6KtHn)    Very funny!"
    print(clean_text(text))

    text = "Wow  ouh  yeah! ![gif](giphy|123abc)  Looks..here: [example](https://link.com) and here more https://google.com"
    print(clean_text(text))

    text = "I can&#39;t believe it! This is &quot;awesome&quot; &amp; hilarious &gt; all expectations."
    print(clean_text(text))

###############################


    word_counts = {
        "hello": 5,
        "world": 3,
        "привет": 4,
        "123abc": 2,
        "hello-world": 1,
        "good_day": 6,
        "John's": 4,
        "mañana": 2,
        "cool-guy99": 7,
        ".start": 3,
        "mid.dle": 2,
        "end.": 1,
        "...": 1,           # ❌ remove
        "bonus+": 4,
        "extra++": 2,
        "flag#": 1,
        "code###": 2,
        "mix+#": 3,
        ".123": 1,          # ❌ remove
        ".123++": 2,        # ❌ remove
        "42": 3,            # ❌ remove
        "456++": 2,         # ❌ remove
        "123..456": 2,      # ❌ remove
        ".com":     5,
    }

    word_counts = filter_dictionary(word_counts)

    print(word_counts)
