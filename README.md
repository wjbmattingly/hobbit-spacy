# Hobbit spaCy: A spaCy Pipeline for Middle Earth Data

![Hobbit spaCy](images/hobbitspacy.png)

Welcome to Hobbit spaCy, a custom Natural Language Processing pipeline built on top of the powerful [spaCy](https://spacy.io/) library. This pipeline is designed specifically for working with Middle Earth data, providing custom NER, tokenization, and other NLP tasks specifically tailored for texts from the world of J.R.R. Tolkien.

This is a work-in-progress that is currently being built as a teaching lesson at the  TAP Institute's Summer 2023 spaCy series.

## Features

* SpanRuler
* merge_spans (Custom Component): identifies overlapping spans that share the same label and merges them into a single span. For example Bilbo (Hobbit) Baggins (Hobbit) becomes Bilbo Baggins (Hobbit)
* identify_relations (Custom Component): identifies constructions such as Frodo son of Drogo

### Entities

#### People
* MAN
* HOBBIT
* DWARF
* ELF
* AINUR

#### Places
* CVT (City, Village, Town) -- this includes Bag End
* REALM -- Sometimes places fall under both CVT and Realm, such as Rivendell
* MOUNTAIN
* ROAD

#### Other
* WEAPON

### SpanRuler Labels

* RELATION (e.g. Frodo son of Drogo)

## Forthcoming Features

* Custom NER trained on Middle Earth Data

## Installation

You can install the Hobbit spaCy via pip:

```shell
pip install en-hobbit
```

## Usage

Here's a quick example of how to use Hobbit spaCy:

```
import spacy
from spacy import displacy

nlp = spacy.load("en_hobbit")

with open("texts/council.txt", "r") as f:
    text = f.read()
doc = nlp(text)
colors = {
    'HOBBIT': "#ADD8E6",   # Light blue
    'CVT': "#FFC0CB",   # Pink
    'REALM': "#FFFFE0",    # Light yellow
    'MAN': "#E6E6FA",      # Lavender
    'DWARF': "#98FB98",    # Pale green
    'ELF': "#FFE4B5",      # Moccasin
    'AINUR': "#FFDAB9",     # Peachpuff
    'RIVER': "#00FFFF",     # Aqua
    'MOUNTAIN': "#8B4513",  # SaddleBrown
    'ROAD': "#808080",      # Gray
    'RELATION': "#800080"   # Purple
}

options = {"ents": ['HOBBIT', 'CVT', 'REALM', 'MAN', 'DWARF', 'ELF', 'AINUR', "RIVER", "MOUNTAIN", "ROAD", "RELATION"], "colors": colors}
options["spans_key"] = "main"
displacy.render(doc, style="span", options=options)
```

Expected Output:

![Sample Output](images/sample.JPG)

## Documentation


## Contributing

We welcome contributions!

## License

Hobbit spaCy is released under the [MIT License](LICENSE).

## Contact

## Data Source

Source for the people can be found [here](https://github.com/juandes/lotr-names-classification)