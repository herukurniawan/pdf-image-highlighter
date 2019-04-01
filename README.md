# PDF-Image Highlighter
I am making a highlighter for a group of image in a PDF file. It is a long journey.

### Prerequisites
* Install Google tesseract in your PC. Follow the installation tutorial [here](https://github.com/tesseract-ocr/tesseract/wiki#installation). I am using `tesseract` with configuration `--psm 3 --oem 1` (**LSTM model** and made for **small text detection**). To install `tesseract` in Ubuntu machine:
````
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
````
* Python 3.x.
* You will need to install `pillow` for PIL.
````
pip install pillow
````
* Install `pytesseract`.
````
pip install pytesseract
````
* You need to install `pdf2image` for pdf to image converter.
````
pip install pdf2image
````
### Example

I made some example! I placed my example files in `example` directory. First, change your active directory to `example`.
````
cd example
````

After that, run this command:
````
# python example.py <image_file>
python example.py textimage2.png
````

You will get the result (*shortened version*):

![Example Image](example/textimage2.png)

````
The text extraction result is: 
Attn: Pearlene Then
Sub-BU: Technology Department - PUBO9
To: Public Utilities Board
Accounts Payable Section, Finance Department,
...

Data: 
5;1;1;1;1;1;6;22;35;13;93;Attn:
5;1;1;1;1;2;49;22;68;13;92;Pearlene
5;1;1;1;1;3;122;22;39;13;96;Then
5;1;1;1;2;1;7;43;64;13;90;Sub-BU:
...
````