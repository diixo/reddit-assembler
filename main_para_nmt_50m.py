
def main():

    file_path = "datasets/para-nmt-50m/para-nmt-50m.txt"

    with open(file_path, "r", encoding="utf-8") as f:
        for i in range(20):
            line = f.readline().strip()
            source, target, score = line.split("\t")
            score = float(score)
            if score > 0.8:
                print(f"Source: {source}")
                print(f"Target: {target}")
                print(f"BLEU: {score}")
                print("---")


if __name__ == "__main__":
    main()
