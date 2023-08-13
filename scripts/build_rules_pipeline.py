import spacy
import pandas as pd
from spacy.language import Language
from spacy.tokens import Span
from components import *
import argparse

def make_patterns(filename, label):
    with open(filename, "r") as f:
        data = f.read().splitlines()
    return [{"pattern": d, "label": label} for d in data]

def main(version):
    print(f"Building Hobbit spaCy Rules-Based Pipeline for version: {version}")
    cities = pd.read_csv("./assets/cities.csv")
    cvt = cities.city.tolist()
    with open("./assets/fps.txt", "r") as f:
        fps = f.read().splitlines()
    url = "https://raw.githubusercontent.com/juandes/lotr-names-classification/master/characters_data.csv"
    df = pd.read_csv(url)
    df['name'] = df['name'].str.replace("Sackville-...", "Sackville").str.replace("Sackvil...", "Sackville")

    names_df = pd.read_csv("./assets/names.csv")
    df = pd.concat([df, names_df]).reset_index(drop=True)

    nlp = spacy.blank("en")

    ruler = nlp.add_pipe("span_ruler", config={"spans_key": "main"})
    # relation_ruler = nlp.add_pipe("span_ruler", name="reelation_ruler", config={"spans_key": "relation"})
    patterns = []
    for idx, row in df.iterrows():
        name = row["name"]
        race = row["race"]
        tokens = []
        for i, token in enumerate(name.split()):
            if token[0].isupper() and len(token) > 2 and token.lower() not in fps:
                tokens.append({"TEXT": token, "OP": "*"})
        if tokens:
            patterns.append({"pattern": tokens, "label": race.upper()})

    patterns = patterns+make_patterns("./assets/realm.txt", "REALM")
    patterns = patterns+make_patterns("./assets/mountain.txt", "MOUNTAIN")
    patterns = patterns+make_patterns("./assets/river.txt", "RIVER")
    patterns = patterns+make_patterns("./assets/road.txt", "ROAD")
    patterns = patterns+make_patterns("./assets/weapon.txt", "WEAPON")

    for city in cvt:
        patterns.append({"pattern": city, "label": "CVT"})
    races = df.race.unique()
    races = [race.upper() for race in races]


    ruler.add_patterns(patterns)
    # relation_ruler.add_patterns(span_patterns)
    nlp.add_pipe("merge_spans")
    nlp.add_pipe("find_relations")
    nlp.meta["lang"] = "en"
    nlp.meta["name"] = "hobbit"
    nlp.meta["version"] = version
    nlp.meta["author"] = "W.J.B. Mattingly"
    nlp.meta["description"] = "This is a spaCy package for working with Middle Earth Data."
    nlp.meta["license"] = "MIT"
    nlp.meta["url"] = "https://github.com/wjbmattingly/hobbit-spacy"
    
    
    nlp.to_disk("./hobbit-spacy")
    print("Pipeline Saved to ./hobbit-spacy")

def __init__(version):
    main(version)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to process Middle Earth Data.")
    parser.add_argument("version", type=str, help="Version of the spaCy package.")
    
    args = parser.parse_args()
    __init__(args.version)