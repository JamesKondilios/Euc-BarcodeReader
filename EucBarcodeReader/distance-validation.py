import zlib
import glob
import zbarlight
from PIL import Image
import exifread
from PIL.ExifTags import TAGS, GPSTAGS

# photos had to be exported from iphoto. File > export > Export Unmodified Original
#source activate barcode-reader
#/Users/jameskonda/Desktop/Genomics/EucBarcodeReader

def path_leaf(path):
    """ guaranteed filename from path; works on Win / OSX / *nix """
    head, tail = ntpath.split(path)
    return tail
print("HI")

files = glob.glob("/Users/jameskonda/Desktop/Genomics/EucBarcodeReader/TestPhotos/*.JPG")

for f in files:
    im = Image.open(f)
    codes = zbarlight.scan_codes('qrcode', im)
    code = codes[0].decode('utf8') if codes else 'unknown'
    print(f + ": " + 'QR codes: %s' % code)

    img = Image.open(f)
    info = img._getexif()

    decoded = dict((TAGS.get(key, key), value) for key, value in info.items())
    print(decoded.get('GPSInfo'))



# photos had to be exported from iphoto. File > export > Export Unmodified Original
#source activate barcode-reader
#/Users/jameskonda/Desktop/Genomics/EucBarcodeReader
