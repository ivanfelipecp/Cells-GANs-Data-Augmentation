import cv2
import os

def tif_2_png():
    formato = "png"
    dirr = "./Originales/"
    for infile in os.listdir(dirr):
        print("file : " + infile)
        if infile[-3:] == "tif":
            outfile = infile[:-3] + formato
            im = cv2.imread(dirr+infile,cv2.IMREAD_COLOR)
            print("new filename : " + outfile)
            out = im
            cv2.imwrite(dirr+outfile, out)

tif_2_png()