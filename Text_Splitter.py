class text_splitter:

    def split_text(text_input: str, length: int) -> list[str]:
        """
        Splits text into paragraphs based on the length n

        :param text_input: Text that should be split
        :param length: maximum length | cant be shorter than the longest word
        :return: Liste mit Teilstrings
        """

        split_text = []  # array for the paragraphs

        def get_closest_to_n(liste: list[int]) -> int:
            """
            smallest number that is the closest to length

            :param liste: List
            :return: smallest number that is the closest
            """
            if liste != [] and liste[0] <= length:  # Liste leer oder erste Zahl größer als n, keine Zahl größer als n
                index = int(len(liste) / 2)  # Mitte der Liste
                if liste[index] > length:  # Prüfen, ob die Zahl in der Mitte größer/kleiner ist als n
                    liste = liste[:index]  # Teil, der die gesuchte Zahl enthält, behalten
                else:
                    liste = liste[index:]  # Andere Seite speichern
                if len(liste) == 1:  # Gibt es nur 1 Element, dann gib dieses direkt zurück
                    return liste[0]  # Nächste Zahl an n zurückgeben
                else:
                    return get_closest_to_n(liste)  # Ansonsten weitermachen
            else:
                return length + 1  # Eine größere Zahl als n zurückgeben, da es irrelevant ist, welche

        def kmp(text, pattern) -> list[int]:
            """
            KMP ist ein Multi Pattern Matching-Algorithmus

            :param text: Text, der nach dem Pattern durchsucht wird
            :param pattern: der Größe nach sortierte Liste mit Positionen, an denen geordnet wird
            :return: Liste mit Positionen
            """

            poses = []
            # base case 1: pattern is empty
            if not pattern:
                print('The pattern occurs with shift 0')
                return [None]

            # base case 2: text is empty, or text's length is less than that of pattern's
            if not text or len(pattern) > len(text):
                print('Pattern not found')
                return None

            chars = list(pattern)

            # next[i] stores the index of the next best partial match
            next_match = [0] * (len(pattern) + 1)

            for i in range(1, len(pattern)):
                j = next_match[i + 1]

                while j > 0 and chars[j] is not chars[i]:
                    j = next_match[j]

                if j > 0 or chars[j] == chars[i]:
                    next_match[i + 1] = j + 1

            j = 0
            for i in range(len(text)):
                if j < len(pattern) and text[i] == pattern[j]:
                    j = j + 1
                    if j == len(pattern):
                        # print('Pattern occurs with shift', (i - j + 1))
                        poses.append(i - j + 1)
                elif j > 0:
                    j = next_match[j]
                    i = i - 1
            return poses

        def get_best_pos_of(eingabe: str, char: chr) -> int:
            """
            Findet aus einem Eingabe text das optimale Trennzeichen bei einer maximalen Zeichenlänge n aus slice_paragraph

            :param eingabe: Eingabetext, der getrennt werden soll
            :param char: Trennzeichen, nach dem gesucht werden soll
            :return: Position des besten Trennzeichens im Text
            """

            pos_list = kmp(eingabe, char)
            pos = get_closest_to_n(pos_list)
            if char != " " or pos == 0:
                pos += 1
            return pos

        def get_last_uppercase_pos(input_string: str) -> int:
            """
            Position des letzten großgeschriebenen Zeichens

            :param input_string: String, der durchsucht werden soll
            :return: Position des letzten Großbuchstabens
            """

            lang = len(input_string)  # Speichern der Länge des Input-Strings
            for i in range(lang - 1):
                if input_string[lang - i - 1].isupper():  # Prüft, ob das Zeichen ein Großbuchstabe ist
                    return lang - i - 1  # Gibt Position des Zeichens zurück
            return lang

        def slice_text(text_input_2, pos, liste):
            """
            Trennt den Text an entsprechender Position

            :param pos: Position des Trennzeichen
            :param text_input_2: Eingabetext, der aufgetrennt werden soll
            :param liste: Liste, zu der gekürzte Textabschnitte hinzugefügt werden
            :return: Liste mit Textabschnitten, gekürzter Eingabetext
            """

            liste.append(text_input_2[:pos])  # Fügt den Text bis zur Position des Trennzeichens zur Liste hinzu
            new_text_input = text_input_2[pos:]  # Entfernt den Teil vor der Trennposition vom Eingabetext
            assert (len(new_text_input) < len(text_input_2))  # Prüft, dass der neue Input kürzer als der vorherige Input ist
            return liste, new_text_input  # Rückgabe der bearbeiteten Liste und des gekürzten Eingabetexts

        while len(text_input) > length:  # Solange der Gesamttext länger als n ist, splitte ihn
            punkt_pos = get_best_pos_of(text_input, ".")  # Punkt als stärkstes Trennzeichen
            if punkt_pos <= length:  # Prüft, ob die Position des Punkts kleiner als n ist
                split_text, text_input = slice_text(text_input, punkt_pos, split_text)  # Trennt den Text am Punkt auf
            else:
                doppelpunkt_pos = get_best_pos_of(text_input, ":")  # Doppelpunkt als zweitstärkstes Trennzeichen
                if doppelpunkt_pos <= length:  # Prüft, ob die Position des Doppelpunkts kleiner als n ist
                    split_text, text_input = slice_text(text_input, doppelpunkt_pos, split_text)  # Trennt den Text am Doppelpunkt auf
                else:
                    semi_pos = get_best_pos_of(text_input, ";")  # Semikolon als drittstärkstes Trennzeichen
                    if semi_pos <= length:  # Prüft, ob die Position des Semikolons kleiner als n ist
                        split_text, text_input = slice_text(text_input, semi_pos, split_text)  # Trennt den Text am Semikolon auf
                    else:
                        kom_pos = get_best_pos_of(text_input, ";")  # Komma als viertstärkstes Trennzeichen
                        if kom_pos <= length:  # Prüft, ob die Position des Kommas kleiner als n ist
                            split_text, text_input = slice_text(text_input, kom_pos, split_text)  # Trennt den Text am Komma auf
                        else:
                            spa_pos = get_best_pos_of(text_input, " ")  # Leerzeichen als fünftstärkstes Trennzeichen
                            if spa_pos <= length:  # Prüft, ob die Position des Leerzeichens kleiner als n ist
                                split_text.append(text_input[:spa_pos])
                                if spa_pos == 0:  # Prüft, ob Text mit Leerzeichen beginnt
                                    split_text, text_input = slice_text(text_input,
                                                                        spa_pos + 1, split_text)  # Trennt den Text am Leerzeichen auf
                                else:
                                    split_text, text_input = slice_text(text_input,
                                                                        spa_pos, split_text)  # Trennt den Text am Leerzeichen auf
                            else:
                                trenn_pos = get_last_uppercase_pos(text_input[:length])  # Großbuchstabe als schwächstes Trennzeichen
                                split_text, text_input = slice_text(text_input,
                                                                    trenn_pos, split_text)  # Trennt den Text am Großbuchstaben auf

        split_text.append(text_input)  # Fügt den restlichen Text der Liste hinzu
        forbidden = ["", " ", None]  # Verbotene Listenelemente

        for elem in split_text:
            if elem in forbidden:  # Prüft, ob Listenelement verboten ist
                split_text.remove(elem)  # Entfernt Element aus der Liste
        return split_text  # Rückgabe der Liste mit Textabschnitten mit maximal n Zeichen

    def split_text_control(text_input: str, length: int):
        """
        Split text with lengthoutput returns the same as split_text but prints stuff
        :param length:
        :return:
        """
        output = text_splitter.split_text(text_input, length)
        for o in output:
            print(len(o),":",o)
        return output



