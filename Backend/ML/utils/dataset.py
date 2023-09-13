import json
import os
import cv2
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from utils.pre_process_STSL import pre_process
from utils.pre_process_STSL import generate_tf_data
from typing import Tuple, List


class Dataset(object):
    """
    A class used to share common dataset functions and attributes.
    
    ...
    
    Attributes
    ----------
    
    Methods
    
    """

    def __init__(self, config_path='../config_STSL.json') -> None:
        self.config_path = config_path
        self.config = None
        self.X_train = None
        self.y_train = None
        self.X_val = None
        self.y_val = None
        self.X_test = None
        self.y_test = None
        self.class_names = None
        self.load_config()
        self.get_dataset()

    def load_config(self):
        with open(self.config_path) as json_data_file:
            self.config = json.load(json_data_file)

    def load_images_and_labels(self, dataset_path: str = 'Dataset_formatted',
                               val_size: float = 0.1, test_size: float = 0.1,
                               random_seed: int = 42) -> Tuple[Tuple[List[np.ndarray], List[int]],
    Tuple[List[np.ndarray], List[int]],
    Tuple[List[np.ndarray], List[int]]]:

        images = []
        labels = []

        # loops through all the files in the directory
        for filename in os.listdir(dataset_path):
            if filename.endswith(".png"):
                # reads the image using OpenCV
                image_path = os.path.join(dataset_path, filename)
                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

                # extracts label from the filename
                label = filename.split('_')[-1].split('.')[0]

                images.append(image)
                labels.append(label)

        # converts images and labels to numpy arrays
        images = np.array(images)
        labels = np.array(labels)

        # splits data into training and a temp set
        X_temp, X_test, y_temp, y_test = train_test_split(images, labels, test_size=test_size, random_state=random_seed)

        # splits temp set into training and validation sets
        X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=val_size / (1 - test_size),
                                                          random_state=random_seed)

        return (X_train, y_train), (X_val, y_val), (X_test, y_test)

    def get_dataset(self):
        # loads images and labels
        (self.X_train, self.y_train), (self.X_val, self.y_val), (
        self.X_test, self.y_test) = self.load_images_and_labels()
        # prepares the data
        self.X_train, self.y_train = pre_process(self.X_train, self.y_train)
        self.X_val, self.y_val = pre_process(self.X_val, self.y_val)
        self.X_test, self.y_test = pre_process(self.X_test, self.y_test)
        self.class_names = list(range(11))
        print("[INFO] Dataset loaded!")
        print()

    def get_tf_data(self) -> Tuple[tf.data.Dataset, tf.data.Dataset, tf.data.Dataset]:
        # creates TensorFlow datasets for training, validation, and testing data
        dataset_train, dataset_val, dataset_test = generate_tf_data(self.X_train, self.y_train, self.X_val, self.y_val,
                                                                    self.X_test, self.y_test, self.config['batch_size'])

        return dataset_train, dataset_val, dataset_test

    def print_ds_info(self):
        # print shapes
        print("Shapes of Datasets:")
        print(f"X_train: {self.X_train.shape}")
        print(f"y_train: {self.y_train.shape}")
        print(f"X_val: {self.X_val.shape}")
        print(f"y_val: {self.y_val.shape}")
        print(f"X_test: {self.X_test.shape}")
        print(f"y_test: {self.y_test.shape}")
        print()
        print()

        # collecting class distributions
        print("Class distribution:")
        datasets = {'train': self.y_train, 'val': self.y_val, 'test': self.y_test}
        distributions = {name: np.sum(dataset, axis=0) for name, dataset in datasets.items()}

        # printing class distributions as a table
        headers = ["Class"] + list(distributions.keys())
        table = [headers]
        for class_index in range(self.y_train.shape[1]):  # Using y_train as a reference for number of classes
            row = [f"Class {class_index}"]
            for dataset_name in distributions.keys():
                row.append(str(int(distributions[dataset_name][class_index])))
            table.append(row)

        # printing the table
        col_widths = [max(len(row[i]) for row in table) for i in range(len(table[0]))]
        row_format = " | ".join("{:<" + str(width) + "}" for width in col_widths)

        for row in table:
            print(row_format.format(*row))
