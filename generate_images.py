import Augmentor
import os
import csv

NEW_DIRECTORY = "/data"
NEW_IMAGE_DIRECTORY = "/images"
NEW_GT_DIRECTORY = "/gt"

CSV_IMAGES_NAME = "images.csv"
CSV_GT_NAME = "gt.csv"

# Data augmentation of the images and their gt
def data_augmentation(path, save_path, size, samples, ground_truth=None):
    p = Augmentor.Pipeline(path,save_path)
    if ground_truth != None:
        p.ground_truth(ground_truth)
    p.crop_random(probability=1, percentage_area=0.8)
    p.flip_left_right(probability=0.3)
    p.flip_top_bottom(probability=0.4)
    p.resize(probability=1.0, width=size[0], height=size[1])
    p.sample(samples)

# Change the name of the images
def change_names(path,gt=True):
    # Get the files
    files = os.listdir(path)
    # Variables
    files.sort()
    size = len(files)
    i = 1

    # Rename the files
    if gt:
        half = size//2
        reals, gts = files[:half], files[half:]
        for r, g in zip(reals,gts):
            os.rename(os.path.join(path, r), os.path.join(path, "image_{}.png".format(i)))
            os.rename(os.path.join(path, g), os.path.join(path, "gt_{}.png".format(i)))
            i += 1
    else:
        for f in files:
            os.rename(os.path.join(path, r), os.path.join(path, "image_{}.png".format(i)))
            i += 1

def move_images(path, path_images, path_gt):
    os.makedirs(path_images)
    os.makedirs(path_gt)

    files = os.listdir(path)
    files.sort()
    size = len(files)
    half = size//2
    gts, reals = files[:half], files[half:]

    for g, r in zip(gts, reals):
        os.rename(os.path.join(path, g), os.path.join(path_gt, g))
        os.rename(os.path.join(path, r), os.path.join(path_images, r))
    
    os.rename(path_images, path+NEW_IMAGE_DIRECTORY)
    os.rename(path_gt, path+NEW_GT_DIRECTORY)

def create_csv(path, directory, name):
    files = os.listdir(path)
    files.sort()
    actual_path = os.getcwd()

    with open(name, 'w') as csvfile:
        fieldnames = ['image', 'class']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in files:
            writer.writerow({"image":i,"class":"1"})

# Actual directory
dirr = os.getcwd()
# Path of the images
real = dirr + "/Originales"
# Path of the GT images
gt = dirr+"/GT"
# New path to save the generated images
path = dirr+NEW_DIRECTORY

# 
new_images_path = dirr+NEW_IMAGE_DIRECTORY
new_gt_path = dirr+NEW_GT_DIRECTORY

# Functions

# Generates images
data_augmentation(real, path,(256,256), 10, gt)

# Changes the name
change_names(path)

# Move the images
move_images(path, new_images_path, new_gt_path)

# Creates CSV
create_csv(path+NEW_IMAGE_DIRECTORY, NEW_IMAGE_DIRECTORY, CSV_IMAGES_NAME)
create_csv(path+NEW_GT_DIRECTORY, NEW_GT_DIRECTORY,CSV_GT_NAME)