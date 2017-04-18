import os
from PIL import Image

def compress_PIL(infile, times):
    baseName, e = os.path.splitext(infile)
    try:
        f, e = os.path.splitext(infile)
        f = (baseName + str("compress"))
        outfile = f + ".jpg"
        #open previously generated file
        compImg = Image.open(infile)
        #compress file at 50% of previous quality
        compImg.save(outfile, "JPEG", quality=50)
        infile = outfile
    except IOError:
        print("Cannot convert", infile)
        

if __name__ == '__main__':
    infile = str(input("Filename to compress: "))
    compress_PIL(infile, 1)