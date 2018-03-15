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

    lat = [float(x) / float(y) for x, y in decoded['GPSInfo'][2]]
    lat = lat[0] + lat[1] / 60
    lon = [float(x) / float(y) for x, y in decoded['GPSInfo'][4]]
    lon = lon[0] + lon[1] / 60
    alt = float(decoded['GPSInfo'][6][0]) / float(decoded['GPSInfo'][6][1])

    if decoded['GPSInfo'][1] == "S":
        lat *= -1
    if decoded['GPSInfo'][3] == "W":
        lon *= -1

    print(lat,lon,alt)



# photos had to be exported from iphoto. File > export > Export Unmodified Original
#source activate barcode-reader
#/Users/jameskonda/Desktop/Genomics/EucBarcodeReader

# Iphone GPS data is a little bit off :/
