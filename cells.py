import pandas as pd
import numpy as np
import cv2
import os

import torch
import torch.nn as nn
from torch.autograd import Variable
from torchvision import transforms
from torch.utils.data.dataset import Dataset

class CellsDataset(Dataset):
    def __init__(self, csv_path, root_dir, transform=None):
        """
        Args:
            csv_path (string): path to csv file
            img_path (string): path to the folder where images are
            transform: pytorch transforms for transforms and tensor conversion
        """
        # Directory with images
        self.root_dir = root_dir
        # Transforms
        self.to_tensor = transforms.ToTensor()
        # Read the csv file
        self.data_info = pd.read_csv(csv_path, header=0)
        # First column contains the image paths
        self.image_arr = np.asarray(self.data_info.iloc[:, 0])
        # Second column is the labels
        self.label_arr = np.asarray(self.data_info.iloc[:, 1])
        # Calculate len
        self.data_len = len(self.data_info.index)

    def __len__(self):
        return self.data_len

    def __getitem__(self, index):
        # Get image name from the pandas df
        single_image_name = os.path.join(os.path.join(self.root_dir,self.image_arr[index]))
        # Open image in gray scale
        img_as_img = np.array(cv2.imread(single_image_name, 0))
        # 2d to 3d array: 256x256 -> 1x256x256
        img_as_img = img_as_img.reshape(img_as_img.shape[0], img_as_img.shape[1],1)

        # Transform image to tensor
        img_as_tensor = self.to_tensor(img_as_img)
        # Get label(class) of the image based on the cropped pandas column
        single_image_label = self.label_arr[index]

        return (img_as_tensor, single_image_label)

"""
# Upload the dataset
dataset = CellsDataset("./images.csv","./data/images")

# Data loader
data_loader = torch.utils.data.DataLoader(dataset=dataset,
                                        batch_size=10,
                                        shuffle=True)

for i, (img, label) in enumerate(data_loader):
    # Todo
"""