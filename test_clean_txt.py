
from main import clean_text


if __name__ == "__main__":

    txt = "   Hello!   "
    print(clean_text(txt))

    txt = "Wow  ou  yeah! ![gif](giphy|abc123)"
    print(clean_text(txt))

    txt = text = "It is funny! ![gif](giphy|60rNlHSC6PoBy6KtHn)    Very funny!"
    print(clean_text(text))

    text = "Wow  ouh  yeah! ![gif](giphy|123abc)  Looks  here: [example](https://link.com) and here more https://google.com"
    print(clean_text(text))
