# FWS Analyse Runde 2

## Kantonskürzel
* https://memobase.ch/record/bar-001-SFW_0071-1 ZH korrekt
* https://memobase.ch/record/bar-001-SFW_0316-2 NE richtig und falsch (mehrfach vorhanden)
* https://memobase.ch/record/bar-001-SFW_0394-2 SG korrekt
* https://memobase.ch/record/bar-001-SFW_1311-3 FR falsch - nicht mehr Frankreich aber Freiburg i.Br.
Folgerung: Verbesserung. Immer noch Amiguität bei Kürzeln, aber häufiger korrekte Treffer.
Frage: Kantonskürzel die als Ort identifiziert wurden per default auf Kantone verlinken statt das Modell disambigieren zu lassen? Für CH Anwendungen vermutlich okay, skaliert aber nicht global.

## Fehlerhafte Verlinkungen
* https://memobase.ch/record/bar-001-SFW_0984-2 besser
* https://memobase.ch/record/bar-001-SFW_0984-2 besser
* https://memobase.ch/record/bar-001-CJS_0083-3_d besser
* https://memobase.ch/record/bar-001-SFW_1220-4 besser
Folgerung: deutliche Verbesserung; komplett random Entitäten werden nicht mehr verlinkt (vermutlich durch Verbesserung der sprachspezifischen Modelle, die Uebersetzungsfehler eliminieren)

## Div
* Nachnamen als Orte: https://memobase.ch/record/bar-001-SFW_1220-4 weiterhin fehlerhaft (Maréchal Montgomery vs Montgomery AL)
* Freiburg i.Br. vs i.Ue. https://memobase.ch/record/bar-001-SFW_1036-1 weiterhin schwierig. In anderen Sprachen besser, da dort nicht "Freiburg" geschrieben steht.
* Bindestriche weiterhin schwierig: hier trennt der Tokenizer nicht. Biel-Bienne hingegen verlinkt auf Biel; hier auch https://www.wikidata.org/wiki/Q1034 "also known as" bekannt.
* https://memobase.ch/record/bar-001-CGS_0741-2 Schule existiert nicht auf Wikidata und wird auch nicht verlinkt.

## DH Feedback
* https://memobase.ch/de/object/bar-001-SFW_0679-1
{('Paris', 'Q90'), ('Molotow', 'Q132899'), ('Schukow', 'Q124617'), ('Frankreichs', 'Q71084'), ('Genf-Cointrin', 'Q289972'), ('Eisenhower', 'Q9916'), ('Ehrenkompanie', 'Q1300017'), ('GE', 'Q230'), ('Genf', 'Q71'), ('Frankreichs', 'Q70972'), ('Palais des Nations', 'Q594846'), ('Amerikas', 'Q30'), ('GE', 'Q54173'), ('Eden', 'Q301637'), ('Schweiz', 'Q39'), ('Europa', 'Q46'), ('Bulganin', 'Q48093')}
* * Genève-Cointrin identifiziert
* * Palais des Nations: gefunden
* * einige Orte verpasst (UK)
* * Frankreichs falsch
* * trotz Filter auf Orte werden teilweise Personen verlinkt. Hier könnte noch mit Abfragen an Wikidata gearbeitet werden, die beispielweise Entities entfernen, deren instance of property (P31) human (Q5) ist.

## Title, spatial coverage
* Titel stellt keine Probleme dar und wurde mit aufgenommen in die Liste der Entities zu den Abstracts
* Aufnahmeort + räumliche Abdeckung ist nicht in allen Fällen funktional, das ist auch zu erwarten, da die Methoden für location extraction von Fliesstexten gemacht sind.
