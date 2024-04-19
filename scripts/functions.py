import yaml


def load_labels(file_path: str) -> dict:
    """
    Load labels from a YAML file.

    Args:
        file_path (str): The path to the YAML file.

    Returns:
        tokens (dict): The loaded labels.
        list_tags (list): List des tags
        noms_tags (dict): Names of tags
    """
    with open(file_path, 'r') as file:
        tokens = yaml.safe_load(file)

    list_tags = []
    for nom, valeurs in tokens.items():
        list_tags.append(valeurs['start'])

    noms_tags = {}
    for tag in list_tags:
        nom_tag_p = None
        for nom, valeurs in tokens.items():
            if valeurs['start'] == tag:
                nom_tag_p = nom
        noms_tags.update({tag: nom_tag_p})

    return tokens, list_tags, noms_tags


def clean_text(text):
    """ removing special characters and tags except those in list_tags, and normalizing

    Args:
        text (str): text to clean

    Returns:
        str: clean and normalize 
    """
    clean_text = re.sub(r'[^\w\s' + re.escape(''.join(list_tags)) + ']', '', text)
    normalized_text = ''.join(c for c in unicodedata.normalize('NFD', clean_text) if unicodedata.category(c) != 'Mn')
    return normalized_text