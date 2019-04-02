from PIL import Image
import pytesseract as pyt
import sys

# Locate your tesseract executable
pyt.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

class pdf2bbox:

    lang = 'eng'
    config = '--psm 6 --oem 1'

    def __init__(self, ipath):
        # Image path is included while running python files (from Terminal)
        imagepath = ipath

        # Open image, get the width and height of the image
        self.image = Image.open(imagepath)

        # Get image width and height
        self.width, self.height = self.image.size
        
        # Simple image to string, the converted text in english language.
        self.text = pyt.image_to_string(self.image, lang=self.lang, config=self.config)

        # Convert image to data
        data = pyt.image_to_data(self.image, lang='eng', config='--psm 6 --oem 1')

        # Data normalize
        self.data = [i.replace("\t",";") for i in data.split("\n")]

        # Get header and exclude it from the data
        self.header = self.data.pop(0)

        # Discard empty data
        self.filterdata()

        # All terms properties in data is converted to bounding box
        self.data = [self.data2bbox(i) for i in self.data]


    def filterdata(self):
        out = []
        for i in self.data:
            if not i.split(";")[11]:
                continue
            out.append(i)
        self.data = out

    def data2bbox(self,data):
        data = data.split(";")

        term = dict()
        term['pageWidth'] = self.width
        term['pageHeight'] = self.height
        term['pageNumber'] = int(data[1])
        term['left'] = int(data[6])
        term['top'] = int(data[7])
        term['right'] = self.width - (int(data[6]) + int(data[8]))
        term['bottom'] = self.height - (int(data[7]) + int(data[9]))
        return term

image_path = sys.argv[1]
pdfb = pdf2bbox(image_path)
print(pdfb.header)
print(pdfb.width, pdfb.height)
print(pdfb.data)