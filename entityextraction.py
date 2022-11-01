import spacy
from langdetect import detect
from os import listdir
import json
import argostranslate.package, argostranslate.translate
from bs4 import BeautifulSoup
import wikidata_utils
import pleiades_utils


PLEIADES = True  # if pleiades extraction is to be used after wikidata, set this to true

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


def extract_from_rescs(inpath, outpath):
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

                language = detect(cleaned_abstract)
                if language == 'de':
                    nlp = nlp_de
                elif language == 'fr':
                    nlp = nlp_fr
                elif language == 'it':
                    nlp = nlp_it
                else:
                    nlp = nlp_en

                entities = wikidata_utils.get_entities(cleaned_abstract, nlp)

                if len(entities) > 0:
                    node["entities"] = [(entities[key], key) for key in entities]

            if node["@type"] == "schema:Place" and "schema:name" in node.keys():
                place_entities = wikidata_utils.get_entities(node["schema:name"], nlp)
                if len(place_entities) > 0:
                    node["entities"] = [(place_entities[key], key) for key in place_entities]

        with open(outpath + f, 'w') as f_write:
            json.dump(doc, f_write)


def extract_from_dasch(inpath, outpath):
    for f in listdir(inpath):
        with open(inpath + f, 'r') as f_load:
            output = []
            doc = f_load.read()

            language = detect(doc)
            if language == 'de':
                nlp = nlp_de
            elif language == 'fr':
                nlp = nlp_fr
            elif language == 'it':
                nlp = nlp_it
            else:
                nlp = nlp_en

            entities = wikidata_utils.get_entities(doc, nlp, PLEIADES)

            # wikidata entities
            if len(entities) > 0:
                output += [f'{entities[key]} {key}\n' for key in entities if key != "NIL"]

            # pleiades entities
            if "NIL" in entities:
                for entity in entities["NIL"]:
                    candidates = pleiades_utils.get_pleiades_results(entity)
                    if len(candidates) > 0:
                        output.append(f'Pleiades query: {entity}\n')
                        for cand in candidates:
                            output.append(f'{cand["title"]} {cand["uri"]}\n')

        print(output)

        with open(outpath + f, 'w') as f_write:
            f_write.writelines(output)


def extract_from_limc(infile, outfile):
    nlp = nlp_en
    with open(infile, 'r') as f_load:
        doc = json.load(f_load)
    for node in doc["nodes"]:
            text = node["labels"]["en"]
            entities = wikidata_utils.get_entities(text, nlp, PLEIADES)

            # wikidata entities
            if len(entities) > 0:
                print(entities)
                node["entities"] = [(entities[key], key) for key in entities if key != "NIL"]

            # pleiades entities
            candidates = pleiades_utils.get_pleiades_results(node["labels"]["en"])
            if len(candidates) > 0:
                node["pleiades"] = candidates
    with open(outfile, 'w') as f_write:
        json.dump(doc, f_write)

def sample_historic_text():
    text = """
    Alexander the Great founded the city in 332 BCE after the start of his Persian campaign; it was to be the capital of his new Egyptian dominion and a naval base that would control the Mediterranean. The choice of the site that included the ancient settlement of Rhakotis (which dates to 1500 BCE) was determined by the abundance of water from Lake Maryūṭ, then fed by a spur of the Canopic Nile, and by the good anchorage provided offshore by the island of Pharos.

    After Alexander left Egypt his viceroy, Cleomenes, continued the creation of Alexandria. With the breakup of the empire upon Alexander’s death in 323 BCE, control of the city passed to his viceroy, Ptolemy I Soter, who founded the dynasty that took his name. The early Ptolemies successfully blended the religions of ancient Greece and Egypt in the cult of Serapis ( Sarapis ) and presided over Alexandria’s golden age. Alexandria profited from the demise of Phoenician power after Alexander sacked Tyre (332 BCE) and from Rome’s growing trade with the East via the Nile ANC-LOC and the canal that then linked it with the Red Sea ANC-LOC . Indeed, Alexandria became, within a century of its founding, one of the Mediterranean’s largest cities and a centre of Greek scholarship and science. Such scholars as Euclid, Archimedes, Plotinus the philosopher, and Ptolemy and Eratosthenes the geographers studied at the Mouseion, the great research institute founded in the beginning of the 3rd century BCE by the Ptolemies that included the city’s famed library. The ancient library housed numerous texts, the majority of them in Greek; a “daughter library” was established at the temple of Serapis about 235 BCE. The library itself was later destroyed in the civil war that occurred under the Roman emperor Aurelian in the late 3rd century CE, while the subsidiary branch was destroyed in 391 CE (see Alexandria, Library of).

    Alexandria was also home to a populous Jewish colony and was a major centre of Jewish learning; the translation of the Old Testament from Hebrew to Greek, the Septuagint, was produced there. Many other ethnic and religious groups were represented in the city, and Alexandria was the scene of much interethnic strife during this period.

    Roman and Byzantine periods
    The decline of the Ptolemies in the 2nd and 1st centuries BCE was matched by the rise of Rome. Alexandria played a major part in the intrigues that led to the establishment of imperial Rome.
    """
    nlp = nlp_en
    entities = wikidata_utils.get_entities(text, nlp, PLEIADES)
    print(entities)

    if "NIL" in entities:
        for entity in entities["NIL"]:
            candidates = pleiades_utils.get_pleiades_results(entity)


if __name__ == "__main__":
    #inpath = "filmwochenschau/"
    #outpath = "fws_entities/"
    #extract_from_rescs(inpath, outpath)

    inpath = "nello/"
    outpath = "nello/"
    extract_from_dasch(inpath, outpath)

    #infile = "OrtsdatenLIMC.json"
    #outfile = "LIMC_results.json"
    #extract_from_limc(infile, outfile)

    #sample_historic_text()