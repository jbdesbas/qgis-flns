import copy
import re

# Strings to keep in short names
linking_words = (
    " ",
    "-",
    "et",
    "en",
    "dit",
    "le",
    "la",
    "les",
    "l'",
    "lès",
    "en",
    "sur",
    "du",
    "de",
    "des",
    "d'",
    "sous",
    "aux",
    "à",
    "au",
    "aux",
)

adjectives_and_numbers = (
    "Grand",
    "Grande",
    "Grands",
    "Grandes",
    "Petit",
    "Petits",
    "Petite",
    "Petites",
    "Haute",
    "Hautes",
    "Hauts",
    "Haut",
    "Basse",
    "Basses",
    "Bas",
    "Vieux",
    "Vieille",
    "Vieilles",
    "Neuf",
    "Neufs",
    "Neuve",
    "Neuves",
    "Jeune",
    "Jeunes",
    "Gros",
    "Grosse",
    "Grosses",
    "Beau",
    "Beaux",
    "Belle",
    "Belles",
    "Un",
    "Deux",
    "Trois",
    "Quatre",
    "Cinq",
    "Six",
    "Sept",
    "Treize",
    "Vingt",
    "Cent",
    "Mille",
    "Entre",
)

other_parts_to_keep = ("Notre",)

# Strings to abbreviate in short names
parts_to_cut = {
    "saint": "St",
    "sainte": "Ste",
    "saints": "Sts",
    "saintes": "Stes",
    "arrondissement": "arr.",
    "sur":"ˢ/",
    "sous":"ˢ/ₛ"
}


class NameProcessor:
    """
    Class that generates the complete, short and very short name of a locality.

    :param original_name: The original name of the city
    :type original_name: str
    """

    def __init__(self, original_name):
        """Constructor method"""
        self.original_name = original_name

    def preprocess_name(self):
        """Returns the complete name prepared from the original name.

        This method removes multiple spaces, spaces after apostrophes and parentheses with their content.

        :return: The complete name.
        :rtype: str
        """

        complete_name = " ".join(self.original_name.split())
        complete_name = complete_name.replace("' ", "'")
        complete_name = complete_name.split("(")[0].strip()

        return complete_name

    def cut_name(self, name_to_cut):
        """Returns the complete name divided into parts.

        This method splits the complete name with these separators : " - ", " -", "- ", " ", "-".

        :param name_to_cut: The name to cut is the complete name genrated by the preprocess_name() method.
        :type name_to_cut: str
        :return: A list which contain every single words and spaces in the name
        :rtype: list
        """

        name_parts = []

        # TODO: enlever les trois premières lignes ?
        if " - " in name_to_cut:
            name_parts = name_to_cut.split(" - ")
        elif " -" in name_to_cut:
            name_parts = name_to_cut.split(" -")
        elif "- " in name_to_cut:
            name_parts = name_to_cut.split("- ")
        else:
            name_parts = re.split("( |-)", name_to_cut)

        return name_parts

    def get_short_name(self):
        """Returns the short name of the locality.

        This method uses preprocess_name() and cut_name() methods before shortening the name.
        Then, if the name do not contain '-' or 'arrondissement', the short name is the same as the original name.
        Else, the method applies the following rules :
        - The first word of the name is kept.
        - keys of parts_to_cut are replaced by their values
        - If the name begin with 'St' or a similar word, the following word is kept in its
        entirety.
        - The words in linking_words, adjectives_and_numbers, other_parts_to_keep are kept in
        their entirety.
        - When the word is the first in a sequence of words separated by dashes and this word
        is part of the parts to keep, the next word is kept.
        - Words containing "d'" or "l'" are abbreviated : "d'Allier" -> "d'A."
        - All of the other words are abbreviated with the first letter and a period.


        :return: The short name.
        :rtype: str
        """

        short_name_parts = []
        complete_name = self.preprocess_name()
        complete_name_parts = self.cut_name(complete_name)

        # Parts do not contain '-' ou 'Arrondissement'
        if (
            "-" not in complete_name_parts
            and "Arrondissement" not in complete_name_parts
        ):
            short_name_parts = copy.copy(complete_name_parts)

        # Parts contain '-' ou 'Arrondissement'
        else:
            # Indicators used to guide the processing of the following words
            seen_first_dash = False
            seen_second_dash = False
            begin_with_saint = False
            keep_next_word = False

            # Processing of each word
            for i in range(len(complete_name_parts)):
                part = complete_name_parts[i]

                if part.lower() in parts_to_cut.keys():
                    # Remplacement of the part, contained in keys of parts_to_cut, with its value
                    short_name_parts.append(parts_to_cut[part.lower()])
                    if i == 0 and part.lower() != "arrondissement":
                        begin_with_saint = True
                elif i == 0:
                    short_name_parts.append(part)
                elif part in linking_words:
                    short_name_parts.append(part)
                elif part.upper().lower() == part:
                    # Keep the part if it is all lower case
                    short_name_parts.append(part)
                elif part in other_parts_to_keep:
                    short_name_parts.append(part)
                elif keep_next_word:
                    short_name_parts.append(part)
                    keep_next_word = False
                elif part.upper().lower()[0:2] in ("l'", "d'"):
                    short_name_parts.append("{0}.".format(part[0:3]))
                elif seen_first_dash and not begin_with_saint:
                    short_name_parts.append("{0}.".format(part[0]))
                elif seen_second_dash:
                    short_name_parts.append("{0}.".format(part[0]))
                else:
                    short_name_parts.append(part)

                if (
                    part in (adjectives_and_numbers or other_parts_to_keep)
                    and not seen_first_dash
                ):
                    keep_next_word = True

                if part == "-":
                    if seen_first_dash:
                        seen_second_dash = True
                    else:
                        seen_first_dash = True

        short_name = "".join(short_name_parts)

        return short_name

    def get_very_short_name(self):
        """Returns the very short name of the locality.

        This method uses get_short_name(), cut_name() methods and it copies the short name
        before very shortening the name.
        The short name is scrolled from the right to the left :
        The word of the name is deleted if :
        - it is '.'
        - it is a word in linking_words
        - it is an abbreviated word
        The word is kept if :
        - it is the first word of the name
        - if the name begin with 'St', it keeps the following word too
        - the name contain 'arr.' then name of the city and number of district are kept

        :return: The very short name
        :rtype: str
        """
        very_short_name_parts = []

        short_name = self.get_short_name()
        short_name_parts = self.cut_name(short_name)

        very_short_name_parts = copy.copy(short_name_parts)

        last_part_removed = True

        # Processing of each word of short_name
        for i in range(len(short_name_parts) - 1, -1, -1):
            part = short_name_parts[i]

            # On supprime la dernière partie si elle contient un '.', si elle fait partie de linking_words,
            if not last_part_removed:
                # if the last part has not been deleted, end of processing
                pass
            elif "." in part:
                # delete the last part if it contains '.'
                very_short_name_parts.pop()
            elif part in linking_words:
                # delete the last part if it is contained in linking_words
                very_short_name_parts.pop()
            elif part != " " and part.upper().lower() == part and not part[0].isdigit():
                very_short_name_parts.pop()
            elif part in parts_to_cut.values():
                # delete the last part if it is contained in values of parts_to_cut
                very_short_name_parts.pop()
            elif part in other_parts_to_keep:
                # delete the last part if it is contained in other_parts_to_keep
                very_short_name_parts.pop()
            else:
                last_part_removed = False

        very_short_name = "".join(very_short_name_parts)

        return very_short_name
