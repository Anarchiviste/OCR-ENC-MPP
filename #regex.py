import re

# Définition de la fonction de nettoyage
def nettoyer_texte_ocr(texte):
    # Correction des substitutions fréquentes
    corrections = {
        r'\b0(?=\w)': 'O',   # 0 au début d’un mot → O
        r'(?<=\w)0\b': 'O',   # 0 à la fin d’un mot → O
        r'\b1(?=\w)': 'l',   # 1 au début d’un mot → l
        r'(?<=\w)1\b': 'l',   # 1 à la fin d’un mot → l
        r'\b5(?=\w)': 'S',   # 5 au début d’un mot → S
    }

    for pattern, replacement in corrections.items():
        texte = re.sub(pattern, replacement, texte)

    # Suppression des caractères non imprimables
    texte = re.sub(r'[\x00-\x1F\x7F]', '', texte)

    # Suppression des espaces multiples
    texte = re.sub(r'[ \t]+', ' ', texte)

    # Suppression des lignes vides
    texte = re.sub(r'\n\s*\n', '\n', texte)

    # Nettoyage de caractères parasites
    texte = re.sub(r'[^\w\s.,;:!?\'\"()\[\]{}\-]', '', texte)

    # Suppression des espaces avant les ponctuations
    texte = re.sub(r'\s+([.,;:!?])', r'\1', texte)

    return texte.strip()

texte_nettoye = nettoyer_texte_ocr(ocr_result)
print("Texte nettoyé :\n", texte_nettoye)

# Création d'un .txt de sortie
output_path = "/content/regex_output.txt"
with open(output_path, "w") as text_file:
    text_file.write(texte_nettoye)

print(f"texte nettoyé resultat sauvegardé à: {output_path}")
