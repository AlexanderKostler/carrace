def count_words_and_distribution(file_path):
    word_count = {}  # Ein Dictionary, um die Wortzähler zu speichern
    total_word_count = 0  # Gesamtzahl der Wörter in der Datei

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Aufteilen der Zeile in Wörter
                words = line.split()
                for word in words:
                    # Entfernen von Satzzeichen
                    word_stripped = word.strip('.,!?":;()[]{}')
                    # Hinzufügen des Worts zum Dictionary oder Inkrementieren des Zählers
                    if word_stripped:
                        total_word_count += 1
                        # Hinzufügen des Worts und seiner ursprünglichen Schreibweise zum Dictionary
                        word_lower = word_stripped.lower()
                        if word_lower in word_count:
                            word_count[word_lower].append(word_stripped)
                        else:
                            word_count[word_lower] = [word_stripped]

    except FileNotFoundError:
        print(f'Die Datei {file_path} wurde nicht gefunden.')

    return word_count, total_word_count

# Dateipfad zur Textdatei angeben
file_path = 'testdatei_lang.txt'

while True:
    # Den Benutzer nach dem gesuchten Wort fragen
    target_word = input('Häufigkeitsverteilung berechnen, bitte Wort eingeben oder "exit" zum Beenden: ')

    if target_word.lower() == 'exit':
        break  # Die Schleife beenden, wenn der Benutzer "exit" eingibt

    # Wörter zählen und die Gesamtzahl der Wörter erhalten
    word_count, total_word_count = count_words_and_distribution(file_path)

    # Prüfen, ob das Zielwort im Dictionary vorhanden ist (nicht case-sensitive)
    target_word_lower = target_word.lower()
    if target_word_lower in word_count:
        occurrences = word_count[target_word_lower]
        print(f'Das Wort "{target_word}" kommt insgesamt {len(occurrences)} Mal vor (nicht case-sensitive).')

        # Anzeigen der Vorkommen und Schreibweisen (Groß- oder Kleinschreibung)
        for i, occurrence in enumerate(occurrences, start=1):
            original_case = "großgeschrieben" if occurrence.istitle() else "kleingeschrieben"
            print(f'Vorkommen {i}: "{occurrence}" ({original_case})')

            frequency_distribution = occurrences.count(occurrence) / total_word_count
            print(f'Häufigkeitsverteilung: {frequency_distribution:.4f}')
    else:
        print(f'Das Wort "{target_word}" wurde nicht gefunden (nicht case-sensitive).')
