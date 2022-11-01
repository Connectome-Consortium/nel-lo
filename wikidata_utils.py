import spacy
from langdetect import detect


def get_entities(text, nlp, keep_nils=False):
    """
    Given an input text and pre-trained nlp model in the appropriate language, 
    links to wikidata identifiers for entities identified from text usage to be
    - FAC: facility/infrastructure (building, airport, road, etc)
    - GPE: geographic, e.g. country, city, state
    - LOC: location not defined by other categories, e.g. mountains, bodies of water.

    Parameters:
    - text: string of text from which to extract entities
    - nlp: pre-trained spacy model
    - keep_nils: parameter to determine whether entities without a corresponding wikidata entry
        are to be saved for further use in e.g. Pleiades extraction.
    Returns:
    - entities: dict where keys are wikidata URIs and values are the text under which they appear in the input text.
    The NIL key contains all unlinked entities.
    """
    entities = dict()
    
    doc = nlp(text)

    for ent in doc.ents:
        if ent.label_ in ['FAC', 'GPE', 'LOC']:
            if ent.kb_id_ != "NIL":
                uri = "https://www.wikidata.org/wiki/{}".format(ent.kb_id_)
                entities[uri] = ent.text
            elif keep_nils:
                if "NIL" not in entities:  # if key doesn't exist yet
                    entities["NIL"] = [ent.text]
                else:
                    entities["NIL"].append(ent.text)
    
    return entities
    