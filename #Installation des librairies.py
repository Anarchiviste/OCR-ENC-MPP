#Installation des librairies
!pip install pdf2image
!sudo apt-get install poppler-utils
!pip install pytesseract
import pytesseract
import cv2
from PIL import Image

#Convertir le pdf en .jpg
from pdf2image import convert_from_path
print("Please Wait while the file is being loaded.")
file = convert_from_path('/le_chemin_du_pdf.pdf')
for i in range(len(file)):
  # sauvegarde en .jpg
  print("Progress: " + str(round(i/len(file) * 100)) + "%")
  file [i].save('page'+ str(i+1) +'.jpg', 'JPEG')
print("Conversion Successful")

#Chargement des .jpg ainsi créés dans une variable image_file
from matplotlib import pyplot as plt
image_file = "/page1.jpg"

#définir la fonction display pour vérifier que nous avons l'image dans une bonne qualité
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

#chargement de l'image dans la variable img
img = cv2.imread(image_file)

#Définition de la fonction de grayscale
def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#Passage du .jpg dans la fonction greyscale + chargement dans variable gray_image
gray_image = grayscale(img)
cv2.imwrite("/gray.jpg", gray_image)

# Sauvegarde de l'image monochrome en .jpg
cv2.imwrite("/gray.jpg", gray_image)

# vérification visuel de l'image monochrome
plt.imshow(gray_image, cmap='gray')
plt.axis('off')
plt.show()

#Définition de la fonction de binarisation
def binarization(gray_image, threshold=128):
    _, im_bw = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)
    return im_bw

#Binarisation de gray_image, sauvegarde dans binary_image et sous forme de .jpg
binary_image = binarization(gray_image)
cv2.imwrite("/binary_image.jpg", binary_image)

#OCRisation
img_tes = "/binary_image.jpg"
img = Image.open(img_tes)
plt.imshow(img, cmap='gray')
plt.axis('off')
plt.show()

ocr_result = pytesseract.image_to_string(img)
print (ocr_result)

#création d'un .txt de sortie
output_path = "/ocr_output.txt"
with open(output_path, "w") as text_file:
    text_file.write(ocr_result)

print(f"OCR result saved to: {output_path}")
