import tensorflow as tf
from tensorflow import Tensor
from typing import Tuple
import numpy as np


def pre_process(images: np.ndarray, labels: np.ndarray, num_classes: int = 11) -> Tuple[np.ndarray, np.ndarray]:
    # mapping of characters to integers, e.g., if 'J' corresponds to the class 10
    label_mapping = {'CH': 0, 'G': 1, 'H': 2, 'J': 3, 'LL': 4, 'Ñ': 5, 'RR': 6, 'V': 7, 'W': 8, 'Z': 9, 'Y': 10}

    # converts string labels to integers
    integer_labels = [label_mapping[label] for label in labels]

    # normalizes the images to [0, 1] range by dividing by 255
    normalised_images = (images / 255.0)[..., None].astype('float32')

    # one-hot encodes the labels
    one_hot_labels = tf.keras.utils.to_categorical(integer_labels, num_classes=num_classes)

    return normalised_images, one_hot_labels


def generator(image: Tensor, label: Tensor) -> Tuple[Tuple[Tensor, Tensor], Tuple[Tensor, Tensor]]:
    return (image, label), (label, image)


def generate_tf_data(X_train: np.ndarray, y_train: np.ndarray, X_val: np.ndarray, y_val: np.ndarray, X_test: np.ndarray,
                     y_test: np.ndarray, batch_size: int) -> Tuple[tf.data.Dataset, tf.data.Dataset, tf.data.Dataset]:
    # prepares training data
    dataset_train = tf.data.Dataset.from_tensor_slices((X_train, y_train))
    dataset_train = dataset_train.shuffle(buffer_size=len(X_train))
    # tensorflow chooses the optimal number of parallel calls to process data
    dataset_train = dataset_train.map(generator, num_parallel_calls=tf.data.AUTOTUNE)
    dataset_train = dataset_train.batch(batch_size)
    # tensorflow prefetches an optimal number of batches
    dataset_train = dataset_train.prefetch(tf.data.AUTOTUNE)

    # prepares validation data
    dataset_val = tf.data.Dataset.from_tensor_slices((X_val, y_val))
    dataset_val = dataset_val.cache()
    dataset_val = dataset_val.map(generator, num_parallel_calls=tf.data.AUTOTUNE)
    dataset_val = dataset_val.batch(batch_size)
    dataset_val = dataset_val.prefetch(tf.data.AUTOTUNE)

    # prepares testing data
    dataset_test = tf.data.Dataset.from_tensor_slices((X_test, y_test))
    dataset_test = dataset_test.cache()
    dataset_test = dataset_test.map(generator, num_parallel_calls=tf.data.AUTOTUNE)
    dataset_test = dataset_test.batch(batch_size)
    dataset_test = dataset_test.prefetch(tf.data.AUTOTUNE)

    return dataset_train, dataset_val, dataset_test
