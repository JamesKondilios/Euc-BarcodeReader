import zlib
import glob
import zbarlight
import PIL
from PIL import Image
import exifread
from PIL.ExifTags import TAGS, GPSTAGS
import os
import csv
import shutil

# photos had to be exported from iphoto. File > export > Export Unmodified Original
#source activate barcode-reader
#/Users/jameskonda/Desktop/Genomics/EucBarcodeReader


files = glob.glob("/Users/jameskonda/Desktop/Genomics/EucBarcodeReader/TestPhotos/*.JPG")


def GetFiles(dirPath):
    files = glob.glob("/Users/jameskonda/Desktop/Genomics/EucBarcodeReader/TestPhotos/*.JPG")
    return files


def GetQRCode(image):
    codes = zbarlight.scan_codes('qrcode', image)
    if codes:
        code = codes[0].decode('utf8')
        return code
    else:
        code = "unknown"

        # flag for `unknown` folder



# {
#     1: 'N', # latitude ref
#     2: ((51, 1), (3154, 100), (0, 1)), # latitude, rational degrees, mins, secs
#     3: 'W', # longitude ref
#     4: ((0, 1), (755, 100), (0, 1)), # longitude rational degrees, mins, secs
#     5: 0, # altitude ref: 0 = above sea level, 1 = below sea level
#     6: (25241, 397), # altitude, expressed as a rational number
#     7: ((12, 1), (16, 1), (3247, 100)), # UTC timestamp, rational H, M, S
#     16: 'T', # image direction when captured, T = true, M = magnetic
#     17: (145423, 418) # image direction in degrees, rational
# }


def GetLatLonAlt(image):
    exifdata = img._getexif()
    decoded = dict((TAGS.get(key, key), value) for key, value in exifdata.items())
    if decoded.get('GPSInfo'):
        lat = [float(x) / float(y) for x, y in decoded['GPSInfo'][2]] # pull out latitude
        lat = lat[0] + lat[1] / 60
        if decoded['GPSInfo'][1] == "S": # correction for location relative to equator
            lat *= -1
        lon = [float(x) / float(y) for x, y in decoded['GPSInfo'][4]] # pull out longditude
        lon = lon[0] + lon[1] / 60
        if decoded['GPSInfo'][3] == "W": # corection for location relative to g'wch
            lon *= -1
        alt = float(decoded['GPSInfo'][6][0]) / float(decoded['GPSInfo'][6][1])
        return [lat,lon,alt]
    else:
        # flag for unknown gps data folder
        return


def GetMetaData(image):
    exifdata = image._getexif()
    decoded = dict((TAGS.get(key, key), value) for key, value in exifdata.items())
    date, time = decoded['DateTimeOriginal'].split(" ")
    return date, time



def MakeGoodDataDirectory(feildID):
    '''If QR code can be read, and GPS data is all good, make directory:
    /processed/<FieldID>/'''
    # add some sort of assert statement here to check the above condition.
    path = '/Users/jameskonda/Desktop/Genomics/EucBarcodeReader/processed'+'/'+str(feildID)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def MakeBadDataDirectory(filename):



for f in files:
    image = Image.open(f)
    GetMetaData(image)
    feildID = GetQRCode(image)
    path = MakeGoodDataDirectory(feildID)
    shutil.copy2(f, path)










        # READING IN CSV:
# reader = csv.reader(open('metadata/EucMetadata.csv', "rb"))
#     for rows in reader:
#         k = rows[0]
#         v = rows[1]
#         mydict[k] = v


# put
# photos had to be exported from iphoto. File > export > Export Unmodified Original
#source activate barcode-reader
#/Users/jameskonda/Desktop/Genomics/EucBarcodeReader

# Iphone GPS data is a little bit off :/
