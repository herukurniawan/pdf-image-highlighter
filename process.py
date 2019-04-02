from PIL import Image
import pytesseract as pyt
from textdistance import hamming
import sys

# Locate your tesseract executable
pyt.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

class pdf2bbox:

    lang = 'eng'
    config = '--psm 6 --oem 1'
    threshold = 1
    page = 0

    def __init__(self, ipath):

        # Update properties
        self.result = []

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

        # read text
        self.txt = self.read()

        # All terms properties in data is converted to bounding box
        #self.data = [self.data2bbox(i) for i in self.data]


    def filterdata(self):
        result = []
        out = []
        prev = 0
        for i in self.data:
            if not i.split(";")[11]:
                continue
            now = int(i.split(";")[4])-1
            if now != prev:
                prev = now
                result.append(out)
                out = []
            out.append(i)
        result.append(out)
        self.data = result

    def data2bbox(self,data):
        data = data.split(";")
        term = dict()
        term['pageWidth'] = self.width
        term['pageHeight'] = self.height
        term['pageNumber'] = self.page
        term['left'] = int(data[6])
        term['top'] = int(data[7])
        term['right'] = self.width - (int(data[6]) + int(data[8]))
        term['bottom'] = self.height - (int(data[7]) + int(data[9]))
        term['text'] = data[11]
        return term

    def read(self):
        txts = []
        for i in self.data:
            cnt = len(i)
            txt = ""
            for j in i:
                txt2 = j.split(";")[11]
                if not txt:
                    txt = txt2
                else:
                    txt = txt + " " + txt2
            txts.append(txt)
        return txts

    def search(self,term):
        cterm = len(term.split(" "))
        for i in range(len(self.txt)):
            token = self.txt[i].split(" ")
            for j in range(len(token)-cterm+1):
                k = j+cterm
                terms = " ".join(token[j:k])
                distance = hamming(term,terms)
                if distance <= self.threshold:
                    start = self.data[i][j]
                    stop = self.data[i][k-1]
                    result = self.extract_bbox(start,stop)
                    result['text'] = terms
                    self.result.append(result)

    def extract_bbox(self,start,stop):
        result = self.data2bbox(start)
        if start != stop:
            stop = stop.split(";")
            result['right'] = self.width - (int(stop[6]) + int(stop[8]))
            result['bottom'] = self.height - (int(stop[7]) + int(stop[9]))
        return(result)

soe = "aspammer@website.com is spam"
image_path = [sys.argv[1]]
cnt = 1
result = []
for i in image_path:
    pdfb = pdf2bbox(i)
    pdfb.page = cnt
    pdfb.search(soe)
    result += pdfb.result
    cnt = cnt + 1
print(result)