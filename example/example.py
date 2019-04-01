from PIL import Image
import pytesseract as pyt
import sys

# Locate your tesseract executable
pyt.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Image path is included while running python files (from Terminal)
imagepath = sys.argv[1]

# Open image, get the width and height of the image
image = Image.open(imagepath)
width, height = image.size

# Simple image to string, the converted text is in english language.
text = pyt.image_to_string(image, lang='eng')

# Get data and normalize
data = pyt.image_to_data(image)
data = [i.replace("\t",";") for i in data.split("\n")]
data.pop(0)
out = []
for i in data:
    if ";-1;" in i:
        continue
    out.append(i)
data = out

# Information
print("The text is: ")
print(text)
print("Data: ")
print("\n".join(data))