
import requests
import time
import xml.etree.ElementTree as ET
from datetime import date, timedelta
import json
from collections import Counter
from pathlib import Path
from utils import read_embedded_dict, filter_dictionary, clean_text, str_tokenize_words, save_embedded_dict



#filepath = "datasets/arxiv-corpus/arxiv_cs_2021_2024.jsonl" #=962567
filepath = "datasets/arxiv-corpus/arxiv_cs_2015_2020.jsonl" #=469458


start_date = date(2015, 1, 1)
end_date = date(2020, 12, 31)


ns = {
    "oai": "http://www.openarchives.org/OAI/2.0/",
    "arxiv": "http://arxiv.org/OAI/arXiv/"
}


def main():

    base = "https://export.arxiv.org/oai2"

    current_date = start_date

    with open(filepath, "w", encoding="utf-8") as f:

        while current_date <= end_date:

            start_date = current_date
            current_date += timedelta(days=1)

            params = {
                "verb": "ListRecords",
                "set": "cs",
                "metadataPrefix": "arXiv",
                "from": start_date,
                "until": current_date,
            }

            print(f"...date: {start_date} >>")

            counter = 0

            while True:
                r = requests.get(base, params=params)
                root = ET.fromstring(r.text)

                # parse <record>...</record>
                rec_list = root.findall(".//oai:record", ns)
                for rec in rec_list:
                    counter += 1

                    title = rec.find(".//arxiv:title", ns)
                    abstract = rec.find(".//arxiv:abstract", ns)
                    categories = rec.find(".//arxiv:categories", ns)
                    doc_id = rec.find(".//arxiv:id", ns)
                    #if doc_id is not None:

                    #################

                    record = {
                        "title": title.text,
                        "description": abstract.text,
                        "date": str(start_date),
                        "terms": categories.text,
                        "ref": doc_id.text,
                    }
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")

                time.sleep(3.0)

                token = root.find(".//{http://www.openarchives.org/OAI/2.0/}resumptionToken")
                if token is None or token.text is None:
                    break
                params = {"verb": "ListRecords", "resumptionToken": token.text}

            f.flush()
            print(f"__date: {start_date} [{counter}] <<")


def statistic():
    counter = 0
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                counter += 1
    print(f"{filepath}: items={counter}")



def processing(dictionary: Counter):

    idx = 0
    with open("datasets/arxiv-corpus/arxiv_cs_2021_2024.jsonl", "r", encoding="utf-8") as f:

        for line in f:
            idx += 1
            item = json.loads(line)
            #print(item)

            question = item["title"]
            answer = item["description"]
            #print(f"{idx}::question: {question}\nanswer: {answer}")

            if idx % 1000 == 0:
                print(f"...items: {idx}")

            txt = clean_text(question + " " + answer)

            tokens = str_tokenize_words(txt)

            dictionary.update([ w for w in tokens if len(w) > 1 ])

    print(f"total items={idx}")


if __name__ == "__main__":
    #main()
    statistic()

    embedded_words = read_embedded_dict()

    dictionary = Counter()

    #processing(dictionary)


    dictionary = Counter(filter_dictionary(dictionary, embedded_words))

    if False:
        new_dict = dict()

        for word, count in dictionary.items():
            word = word.strip()
            if word not in embedded_words:
                if word.lower() in embedded_words:
                    embedded_words.add(word)
                    #print(f"added: [{word}]")
                else:
                    new_dict[word] = count

        dictionary = Counter(new_dict)
        save_embedded_dict(embedded_words)

        #####################################################

    if len(dictionary) > 0:

        print(f"Saved arxiv-json.sz={len(dictionary.items())}")

        with Path("data/arxiv-dictionary.json").open("w", encoding="utf-8") as f:
            json.dump(dictionary, f, indent=2)
        print(f"Saved json.sz={len(dictionary.items())}")

        most_common = dictionary.most_common()

        sorted_words = [word for word, _ in most_common]
        #sorted_words = sorted([word for word, _ in most_common])

        with Path("data/arxiv-dictionary.txt").open("w", encoding="utf-8") as f:
            for word in sorted_words:
                f.write(word + "\n")
