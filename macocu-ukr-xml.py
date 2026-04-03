import re
import json

file_path = "datasets/MaCoCu-uk-1.0.xml"
out_path = "datasets/MaCoCu-uk-1.0.jsonl"

LIMIT = 10


def main():

    lines = []

    doc_open_re = re.compile(r'<doc\s+([^>]+)>')
    attr_re = re.compile(r'(\w+)="([^"]*)"')

    inside_doc = False
    doc_lines = []
    doc_attrs = {}
    p_attrs = {}


    cntr = 0

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f, \
        open(out_path, "w", encoding="utf-8") as out:

        for line in f:
            line = line.rstrip("\n")
            stripped = line.strip()

            if stripped.startswith("<doc "):
                inside_doc = True
                doc_lines = []
                p_attrs = {}

                m = doc_open_re.match(stripped)
                doc_attrs = dict(attr_re.findall(m.group(1))) if m else {}
                continue

            if inside_doc:
                if stripped.startswith("<p "):
                    p_attrs = dict(attr_re.findall(stripped))

                    #print(p_attrs)

                    #print(p_attrs.get("quality"))    # good
                    #print(p_attrs.get("lm_score"))   # 0.712
                    #print(p_attrs.get("sensitive"))  # no

                    continue

                if stripped == "</doc>":
                    full_text = " ".join(x for x in doc_lines if x).strip()

                    s_id = doc_attrs.get("id")
                    p_id = p_attrs.get("id")

                    record = {
                        "id": s_id.replace("macocu.uk.", "") if s_id else "-1",
                        "title": doc_attrs.get("title"),
                        "text": full_text,
                        "url": doc_attrs.get("url"),
                        #"domain": doc_attrs.get("domain"),
                        "crawl_date": doc_attrs.get("crawl_date"),

                        "lm_score": float(p_attrs["lm_score"]) if p_attrs.get("lm_score") else None,
                        "quality": p_attrs.get("quality"),
                        "sensitive": p_attrs.get("sensitive"),
                        #"lang": p_attrs.get("lang"),
                    }

                    s = json.dumps(record, ensure_ascii=False)

                    obj = json.loads(s)
                    out.write(json.dumps(record, ensure_ascii=False) + "\n")

                    if LIMIT != 0:
                        lines.append(s)

                    cntr += 1
                    if (cntr >= LIMIT) and (LIMIT > 0):
                        break

                    if cntr % 1000 == 0:
                        print(f"...on: {cntr} examples")

                    inside_doc = False
                    doc_lines = []
                    doc_attrs = {}
                    p_attrs = {}

                elif stripped != "</p>":
                    doc_lines.append(stripped)


    for i, line in enumerate(lines, 1):
        print(f"\n{i}: {line}")


if __name__ == "__main__":
    main()
