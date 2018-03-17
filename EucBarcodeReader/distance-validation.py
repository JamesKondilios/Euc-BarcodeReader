#!/usr/bin/env python3
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
from sys import stdin, stdout, stderr
from tqdm import tqdm
from docopt import docopt

# photos had to be exported from iphoto. File > export > Export Unmodified Original
#source activate barcode-reader
#/Users/jameskonda/Desktop/Genomics/EucBarcodeReader

def get_args():
    CLI= """
    USAGE:
        imgproc.py [options] -o OUTDIR INPUT_IMAGE ...

    OPTIONS:
        -o OUTDIR   Output directory (creates subdirectories under here)
        -a          Ask if we can't automatically get some data (NOT IMPLEMENTED)
    """
    opts = docopt(CLI)
    return {"inputs": opts["INPUT_IMAGE"],
            "output_dir": opts["-o"],
            "ask": opts["-a"]}


def GetQRCode(image):
    codes = zbarlight.scan_codes('qrcode', image)
    if codes:
        return codes[0].decode('utf8')
    else:
        return "unknown"

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
    exifdata = image._getexif()
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
        return lat,lon,alt
    return "", "", ""

def GetExifData(image):
    exifdata = image._getexif()
    decoded = dict((TAGS.get(key, key), value) for key, value in exifdata.items())
    datetime = decoded['DateTimeOriginal']
    gps = GetLatLonAlt(image)
    return datetime, gps


def OpenMetaData(filename):
    metadata={}
    with open(filename, mode='r') as infile:
        reader = csv.reader(infile)
        header = next(reader)
        for row in reader:
            id = row[7]
            metadata[id] = list(row)
    return header, metadata

def MoveTo(source, destdir):
    from os.path import exists, basename, join, splitext
    destfile = join(destdir, basename(source))
    if not exists(destdir):
        os.makedirs(destdir)
    while exists(destfile):
        print("WARNING:", destfile, "exists, appending _2 to name", file=stderr)
        file, ext = splitext(destfile)
        destfile = file + "_2" + ext
    shutil.copy2(source, destfile)


# def MoveToNoExif(fieldID, filename):
#     ''' If QR code can be read but metadata is missing, make directory
#     /processed/no-metadata/<fieldID>/ and copy image to this location'''
#     # add some sort of assert statement here to check the above condition.
#     path = '/Users/jameskonda/Desktop/Genomics/EucBarcodeReader/processed/no-metadata/' + str(fieldID)
#     if not os.path.exists(path):
#         os.makedirs(path)
#     shutil.copy2(filename, path)


header, metadata = OpenMetaData('/Users/jameskonda/Desktop/Genomics/EucBarcodeReader/metadata/EucMetadata.csv')
options = get_args()
out = options["output_dir"]
if not os.path.isdir(out):
    os.makedirs(out)
csv_out = out + "/annotated_metadata.csv"
if not os.path.exists(csv_out):
    with open(csv_out, "w") as fh:
        print(*header, "EXIF_datetime", "EXIF_GPS_lat", "EXIF_GPS_long", "EXIF_GPS_elev", file=fh, sep="\t")

for f in tqdm(options["inputs"]):
    try:
        image = Image.open(f)
    except Exception as exc:
        print("ERROR:", str(exc), file=stderr)
        MoveTo(f, out + "/unknown")
        continue

    fieldID = GetQRCode(image)
    if not fieldID:
        MoveTo(f, out + "/unknown")
        continue

    Sample_metadata = metadata.get(fieldID)
    if Sample_metadata:
        MoveTo(f, out + "/all-good/" + fieldID)
    else:
        MoveTo(f, out + "/no-metadata/" + fieldID)
        Sample_metadata = ["" for _ in header]

    datetime, gps = GetExifData(image)
    with open(csv_out, "a")  as fh:
        print(*Sample_metadata, datetime, *gps, file=fh, sep="\t")


 p./distance-validation.py -o kdm Test1Photos/*
        # READING IN CSV:
# reader = csv.reader(open('metadata/EucMetadata.csv', "rb"))
#     for rows in reader:
#         k = rows[0]
#         v = rows[1]
#         metadata[k] = v


# put
# photos had to be exported from iphoto. File > export > Export Unmodified Original
#source activate barcode-reader
#/Users/jameskonda/Desktop/Genomics/EucBarcodeReader

# Iphone GPS data is a little bit off :/
