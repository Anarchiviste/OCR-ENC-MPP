# OCR utilisant Tesseract.
"""
/!\ Attention /!\

Ce programme demande des chemins d'accès à des fichiers, et demande d'enregistrer des nouveaux fichiers pour les  réutiliser.
Pour pouvoir utiliser ce code, il faut changer les chemins des documents directement dans le code, 
les lignes à modifier avant de lancer le code sont signalées par un commentaire #PATH.
"""

# Installation des librairies
!pip install pdf2image
!sudo apt-get install poppler-utils
!pip install pytesseract
import pytesseract
import cv2
from PIL import Image
import re

# Convertir le pdf en .jpg
from pdf2image import convert_from_path
print("Attendez que le fichier soit importé.")
file = convert_from_path('/chemin/du/pdf.pdf') #PATH
for i in range(len(file)):
  # sauvegarde en .jpg
  print("Progré: " + str(round(i/len(file) * 100)) + "%")
  file [i].save('page'+ str(i+1) +'.jpg', 'JPEG')
print("Conversion réussi !")

# Chargement des .jpg ainsi créés dans une variable image_file
from matplotlib import pyplot as plt
image_file = "/content/page1.jpg" #PATH

# Définir la fonction display pour vérifier que nous avons l'image dans une bonne qualité
def display(im_path):
    dpi = 80
    im_data = plt.imread(im_path)

    height, width  = im_data.shape[:2]

    # What size does the figure need to be in inches to fit the image?
    figsize = width / float(dpi), height / float(dpi)

    # Create a figure of the right size with one axes that takes up the full figure
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])

    # Hide spines, ticks, etc.
    ax.axis('off')

    # Display the image.
    ax.imshow(im_data, cmap='gray')

    plt.show()

display(image_file)

# Chargement de l'image dans la variable img
img = cv2.imread(image_file)

# Définition de la fonction de grayscale
def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Passage du .jpg dans la fonction greyscale + chargement dans variable gray_image
gray_image = grayscale(img)
cv2.imwrite("content/sample_data/gray.jpg", gray_image) #PATH

# Sauvegarde de l'image monochrome en .jpg
cv2.imwrite("/content/sample_data/gray.jpg", gray_image) #PATH

# Vérification visuel de l'image monochrome
plt.imshow(gray_image, cmap='gray')
plt.axis('off')
plt.show()

# Définition de la fonction de binarisation
def binarization(gray_image, threshold=225):
    _, im_bw = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)
    return im_bw

# Binarisation de gray_image, sauvegarde dans binary_image et sous forme de .jpg
binary_image = binarization(gray_image)
cv2.imwrite("/content/sample_data/binary_image.jpg", binary_image) #PATH

# OCRisation
img_tes = "/content/sample_data/binary_image.jpg" #PATH
img = Image.open(img_tes)
plt.imshow(img, cmap='gray')
plt.axis('off')
plt.show()

ocr_result = pytesseract.image_to_string(img)
print (ocr_result)

#création d'un .txt de sortie
output_path = "/content/ocr_output.txt" #PATH
with open(output_path, "w") as text_file: 
    text_file.write(ocr_result)

print(f"OCR result saved to: {output_path}")

#définition de la fonction de nettoyage
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
# Impression du texte nettoyé
texte_nettoye = nettoyer_texte_ocr(ocr_result)
print("Texte nettoyé :\n", texte_nettoye)

#création d'un .txt de sortie du texte nettoyé
output_path = "/content/regex_output.txt" #PATH
with open(output_path, "w") as text_file:
    text_file.write(texte_nettoye)

print(f"texte nettoyé resultat sauvegardé à: {output_path}")
