
import re
import json

file_path = "datasets/MaCoCu-uk-1.0.xml"
out_path = "datasets/MaCoCu-uk-1.0.jsonl"


lines = []

doc_open_re = re.compile(r'<doc\s+([^>]+)>')
attr_re = re.compile(r'(\w+)="([^"]*)"')

inside_doc = False
doc_lines = []
doc_attrs = {}

cntr = 0


with open(file_path, "r", encoding="utf-8", errors="ignore") as f, \
     open(out_path, "w", encoding="utf-8") as out:

    for line in f:
        line = line.rstrip("\n")
        stripped = line.strip()

        if stripped.startswith("<doc "):
            inside_doc = True
            doc_lines = []

            m = doc_open_re.match(stripped)
            doc_attrs = dict(attr_re.findall(m.group(1))) if m else {}
            continue

        if inside_doc:
            if stripped == "</doc>":
                full_text = " ".join(x for x in doc_lines if x).strip()

                s_id = doc_attrs.get("id")
                record = {
                    "id": s_id.replace("macocu.uk.", "") if s_id else "-1",
                    "title": doc_attrs.get("title"),
                    "url": doc_attrs.get("url"),
                    "domain": doc_attrs.get("domain"),
                    "crawl_date": doc_attrs.get("crawl_date"),
                    "text": full_text,
                }

                s = json.dumps(record, ensure_ascii=False)

                obj = json.loads(s)

                cntr += 1

                if cntr <= 10:
                    out.write(json.dumps(record, ensure_ascii=False) + "\n")
                else:
                    break

                inside_doc = False
                doc_lines = []
                doc_attrs = {}
            elif not stripped.startswith("<p ") and stripped != "</p>":
                doc_lines.append(stripped)


for i, line in enumerate(lines, 1):
    print(f"\n{i}: {line}")
