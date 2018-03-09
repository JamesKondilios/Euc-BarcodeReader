import zlib
import glob
import numpy as np
import zbarlight
from PIL import Image


files = glob.glob("/Users/jameskonda/Desktop/Genomics/EucBarcodeReader/TestPhotos/*.jpg")

for f in files:
    im = Image.open(f)
    code = zbarlight.scan_codes('qrcode', im)
    print(f + ": " + 'QR codes: %s' % code)
