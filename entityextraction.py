import spacy
from langdetect import detect
from os import listdir
import json
import argostranslate.package, argostranslate.translate
from bs4 import BeautifulSoup


# installed_languages = argostranslate.translate.get_installed_languages()
nlp_en = spacy.load('entitylinker2/nlp')
print('LOADED MODEL: English')
nlp_de = spacy.load('entitylinker_de/nlp')
print('LOADED MODEL: German')
nlp_fr = spacy.load('entitylinker_fr/nlp')
print('LOADED MODEL: French')
nlp_it = spacy.load('entitylinker_it/nlp')
print('LOADED MODEL: Italian')



def clean_text(abstract):
    return BeautifulSoup(abstract, "lxml").text


def translate_text(abstract):
    from_code = detect(abstract)
    to_code = 'en'
    from_lang = list(filter(lambda x: x.code == from_code, installed_languages))[0]
    to_lang = list(filter(lambda x: x.code == to_code, installed_languages))[0]
    translation = from_lang.get_translation(to_lang)
    translated_abstract = translation.translate(abstract)
    return translated_abstract


def get_entities(abstract):
    entities = set()
    doc = nlp(abstract)
    for ent in doc.ents:
        if ent.label_ in ['FAC', 'GPE', 'LOC']:
            if ent.kb_id_ != "NIL":
                uri = "https://www.wikidata.org/wiki/{}".format(ent.kb_id_)
            else:
                uri = "NIL"
            entities.add((ent.text, uri))
    return entities


def get_entities_multiling(text):
    entities = dict()

    language = detect(text)
    if language == 'de':
        nlp = nlp_de
    elif language == 'fr':
        nlp = nlp_fr
    elif language == 'it':
        nlp = nlp_it
    else:
        nlp = nlp_en
    
    doc = nlp(text)

    for ent in doc.ents:
        if ent.label_ in ['FAC', 'GPE', 'LOC']:
            if ent.kb_id_ != "NIL":
                uri = "https://www.wikidata.org/wiki/{}".format(ent.kb_id_)
                entities[uri] = ent.text
    
    return entities

def main(inpath, outpath):
    counter = 0
    for f in listdir(inpath):
        if counter % 1000 == 0:
            print("{} files processed, starting {}".format(counter, f))
        counter += 1

        with open(inpath + f, 'r') as f_load:
            doc = json.load(f_load)
        for node in doc["@graph"]:
            if "schema:abstract" in node.keys():
                # title + abstract
                raw_abstract = node["schema:name"] + "\n" + node["schema:abstract"]
                cleaned_abstract = clean_text(raw_abstract)
                entities = get_entities_multiling(cleaned_abstract)
                if len(entities) > 0:
                    node["entities"] = [(entities[key], key) for key in entities]

            if node["@type"] == "schema:Place" and "schema:name" in node.keys():
                place_entities = get_entities_multiling(node["schema:name"])
                if len(place_entities) > 0:
                    node["entities"] = [(place_entities[key], key) for key in place_entities]

        with open(outpath + f, 'w') as f_write:
            json.dump(doc, f_write)


if __name__ == "__main__":
    inpath = "filmwochenschau/"
    outpath = "fws_entities/"
    main(inpath, outpath)
