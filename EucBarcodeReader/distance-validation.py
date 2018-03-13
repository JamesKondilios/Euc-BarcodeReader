import zlib
import glob
import zbarlight
from PIL import Image
import piexif as pe
import exifread


files = glob.glob("/Users/jameskonda/Desktop/Genomics/EucBarcodeReader/TestPhotos/*.jpg")

for f in files:
    im = Image.open(f)
    codes = zbarlight.scan_codes('qrcode', im)
    code = codes[0].decode('utf8') if codes else 'unknown'
    print(f + ": " + 'QR codes: %s' % code)
    tags = exifread.process_file(open(str(f), 'rb')) # none of this works
    geo = {i:tags[i] for i in tags.keys() if i.startswith('GPS')} # this does not works

    print(geo) # returns only empty brackets - look into

    


#im = Image.open(f)

#exif_dict = pe.load("/Users/jameskonda/Desktop/Genomics/EucBarcodeReader/TestPhotos/1m.jpg")
#exif_dict = pe.load(im)
#print(exif_dict)


#source activate barcode-reader
#/Users/jameskonda/Desktop/Genomics/EucBarcodeReader
