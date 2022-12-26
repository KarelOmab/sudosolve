from PIL import Image

import pytesseract


src_img = '/Users/karelomab/empty_6.png'

# If you don't have tesseract executable in your PATH, include the following:
#pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

# Simple image to string
#print(pytesseract.image_to_string(Image.open(src_img), config = '--psm 7 outputbase digits'))

for i in range(1, 13):
    try: print(pytesseract.image_to_string(Image.open(src_img), config = '--psm {} outputbase digits'.format(i)))
    except : print("ex")
