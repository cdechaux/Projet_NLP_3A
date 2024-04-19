import yaml
import re
import unicodedata
import string


def load_labels(file_path: str) -> dict:
    """
    Load labels from a YAML file.

    Args:
        file_path (str): The path to the YAML file.

    Returns:
        -tokens (dict): The loaded labels.
        -list_tags (list): List des tags
        -noms_tags (dict): Names of tags
    """
    with open(file_path, "r") as file:
        tokens = yaml.safe_load(file)

    list_tags = []
    for nom, valeurs in tokens.items():
        list_tags.append(valeurs["start"])

    noms_tags = {}
    for tag in list_tags:
        nom_tag_p = None
        for nom, valeurs in tokens.items():
            if valeurs["start"] == tag:
                nom_tag_p = nom
        noms_tags.update({tag: nom_tag_p})

    return tokens, list_tags, noms_tags


def clean_text(text, list_tags):
    """removing special characters and tags except those in list_tags, and normalizing text

    Args:
        -text (str): text to clean
        -list_tags (list): list of tags to keep

    Returns:
        str: clean and normalize
    """
    clean_text = re.sub(r"[^\w\s" + re.escape("".join(list_tags)) + "]", "", text)
    normalized_text = "".join(
        c
        for c in unicodedata.normalize("NFD", clean_text)
        if unicodedata.category(c) != "Mn"
    )
    return normalized_text


def load_lines(data: dict) -> list:
    """Split text by line

    Args:
        data (dict): Dictionary to split

    Returns:
        data_lines: list of all lines in data
    """
    data_lines = []
    for key, value in data.items():
        liste_elements = value.split("\n")
        data_lines.append(liste_elements)
    data_lines = [element for sous_liste in data_lines for element in sous_liste]
    return data_lines


def fill_tag_dictionary(data_lines, list_tags, pattern):
    """
    Fill the dictionary with words corresponding to each tag.

    Args:
    - data_lines: A list of strings containing the data lines.
    - list_tags: A list of tags.
    - pattern: Pattern to split

    Returns:
    - data_dict: A dictionary containing lists of words corresponding to each tag.
    """

    # Initialize an empty dictionary to store the data
    data_dict = {tag: [] for tag in list_tags}

    # Iterate through each line in the data
    for sublist in data_lines:
        # Initialize a dictionary to track whether a tag has been found in the current line
        comptes_dict = {tag: 0 for tag in list_tags}

        # Split the line into words using the regular expression pattern
        for word in re.split(pattern, sublist):
            # Check if the word starts with any of the tags
            for tag in list_tags:
                if word.startswith(tag):
                    # If a tag is found, mark it as found in the comptes_dict and add the word to the corresponding tag list
                    comptes_dict[tag] = 1
                    data_dict[tag].append(word[1:])

        # Add empty strings for tags that were not found in the line
        for tag in list_tags:
            if comptes_dict[tag] == 0:
                data_dict[tag].append("")

    return data_dict

def check_empty(row):
    """Function to check if one column is filled and the other empty

    Args:
        row : row of dataframe

    Returns:
        bool : False il both are empty or full 
    """
    if row["surname"] != "" and row["surname_household"] == "":
        return True
    elif row["surname"] == "" and row["surname_household"] != "":
        return True
    else:
        return False  


def check_both_not_empty(row):
    """Function to check if two columns are empty

    Args:
        row : row of dataframe

    Returns:
        bool : True if both are not empty
    """
    if row["surname"] != "" and row["surname_household"] != "":
        return True
    else:
        return False

# Définir une fonction pour fusionner les colonnes
def fusionner_colonnes(colonne1, colonne2):
    """ Merge two columns for one row

    Args:
        colonne1 (str): first column to merge
        colonne2 (str): second column to merge

    Returns:
        str
    """
    if colonne1 != "":
        return colonne1
    elif colonne2 != "":
        return colonne2
    else:
        return ""


def longueur_chaine(chaine):
    return len(str(chaine))


def nombre_mots(chaine):
    return len(str(chaine).split())


def nombre_caracteres_speciaux(chaine):
    return sum(c.isdigit() or c in string.punctuation for c in str(chaine))


def nombre_lettres(chaine):
    return sum(c.isalpha() for c in str(chaine))


def nombre_voyelles(chaine):
    return sum(c.lower() in "aeiou" for c in str(chaine))


def nombre_consonnes(chaine):
    return sum(c.isalpha() and c.lower() not in "aeiou" for c in str(chaine))

