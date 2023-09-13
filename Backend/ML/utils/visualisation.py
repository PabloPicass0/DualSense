import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import widgets
import pandas as pd
import matplotlib.patches as patches


class AffineVisualizer(object):
    # only MNIST
    def __init__(self, model, X, y, hist=True):
        self.min_value = - 0.30
        self.max_value = + 0.30
        self.step = 0.05
        self.sliders = {str(i): widgets.FloatSlider(min=self.min_value, max=self.max_value, step=self.step) for i in
                        range(16)}
        self.text = widgets.IntText()
        self.sliders['index'] = self.text
        self.model = model
        self.X = X
        self.y = y
        self.hist = hist

    def affineTransform(self, **info):

        index = abs(int(info['index']))
        tmp = np.zeros([1, 10, 16])

        for d in range(16):
            tmp[:, :, d] = info[str(d)]

        y_pred, X_gen = self.model.predict([self.X[index:index + 1], self.y[index:index + 1], tmp])

        if self.hist:
            fig, ax = plt.subplots(1, 3, figsize=(15, 3))
        else:
            fig, ax = plt.subplots(1, 2, figsize=(12, 12))
        ax[0].imshow(self.X[index, ..., 0], cmap='gray')
        ax[0].set_title('Input Digit')
        ax[1].imshow(X_gen[0, ..., 0], cmap='gray')
        ax[1].set_title('Output Generator')
        if self.hist:
            ax[2].set_title('Output Caps Length')
            ax[2].bar(range(10), y_pred[0])
        plt.show()

    def on_button_clicked(self, k):
        for i in range(16):
            self.sliders[str(i)].value = 0

    def start(self):
        button = widgets.Button(description="Reset")
        button.on_click(self.on_button_clicked)

        main = widgets.HBox([self.text, button])
        u1 = widgets.HBox([self.sliders[str(i)] for i in range(0, 4)])
        u2 = widgets.HBox([self.sliders[str(i)] for i in range(4, 8)])
        u3 = widgets.HBox([self.sliders[str(i)] for i in range(8, 12)])
        u4 = widgets.HBox([self.sliders[str(i)] for i in range(12, 16)])

        out = widgets.interactive_output(self.affineTransform, self.sliders)

        display(main, u1, u2, u3, u4, out)


def plotHistory(history):
    """
    Plot the loss and accuracy curves for training and validation 
    """
    pd.DataFrame(history.history).plot(figsize=(8, 5), y=list(history.history.keys())[0:-1:2])
    plt.grid(True)
    plt.show()


def plotImages(X_batch, y_batch, n_img, class_names):
    max_c = 5  # max images per row

    if n_img <= max_c:
        r = 1
        c = n_img
    else:
        r = int(np.ceil(n_img / max_c))
        c = max_c

    fig, axes = plt.subplots(r, c, figsize=(15, 15))
    axes = axes.flatten()
    for img_batch, label_batch, ax in zip(X_batch, y_batch, axes):
        ax.imshow(img_batch, cmap='gray')
        ax.grid()
        ax.set_title('Class: {}'.format(class_names[np.argmax(label_batch)]))
    plt.tight_layout()
    plt.show()


def plotWrongImages(X_test, y_test, y_pred, n_img, class_names):
    max_c = 5  # max images per row

    indices = np.where(np.argmax(y_pred, -1) != np.argmax(y_test, -1))[0]  # indices of wrong images

    if n_img <= max_c:
        r = 1
        c = n_img
    else:
        r = int(np.ceil(n_img / max_c))
        c = max_c

    fig, axes = plt.subplots(r, c, figsize=(20, 20))
    axes = axes.flatten()
    for index, ax in zip(indices, axes):
        ax.imshow(X_test[index, :, :, 0], cmap='gray')
        ax.set_axis_off()

        # Add a black rectangle patch
        rect = patches.Rectangle((0, 0), X_test.shape[2] - 1, X_test.shape[1] - 1, linewidth=1, edgecolor='black',
                                 facecolor='none')
        ax.add_patch(rect)

        ax.set_title('Class: {} ({:.3f}) \nPred [1]: {} ({:.3f}) \nPred [2]: {} ({:.3f})'.format(
            class_names[np.argmax(y_test[index])], y_pred[index][np.argmax(y_test[index])],
            class_names[np.argmax(y_pred[index])], np.max(y_pred[index]),
            class_names[np.argsort(y_pred[index], axis=0)[-2]], y_pred[index][np.argsort(y_pred[index], axis=0)[-2]]),
                     color='black', fontsize=14)
    plt.tight_layout()
    plt.show()


def plotWrongImagesWithCharts(X_test, y_test, y_pred, reconstructed_images, n_img, class_names):
    max_c = 5  # max images per row
    indices = np.where(np.argmax(y_pred, -1) != np.argmax(y_test, -1))[0]  # indices of wrong images

    if n_img <= max_c:
        r = 3
        c = n_img
    else:
        r = int(np.ceil(n_img / max_c)) * 3
        c = max_c

    fig = plt.figure(figsize=(20, 30))

    fig, axes = plt.subplots(r, c, figsize=(10, 10))
    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.2, hspace=0.1)
    axes = axes.flatten()

    for i, index in enumerate(indices[:n_img]):
        # Plot misclassified images
        ax = axes[i]
        ax.imshow(X_test[index, :, :, 0], cmap='gray')
        ax.axis('off')
        rect = patches.Rectangle((0, 0), X_test.shape[2] - 1, X_test.shape[1] - 1, linewidth=1, edgecolor='black',
                                 facecolor='none')
        ax.add_patch(rect)

        ax.set_title('Class: {} ({:.3f}) \nPred [1]: {} ({:.3f}) \nPred [2]: {} ({:.3f})'.format(
            class_names[np.argmax(y_test[index])], y_pred[index][np.argmax(y_test[index])],
            class_names[np.argmax(y_pred[index])], np.max(y_pred[index]),
            class_names[np.argsort(y_pred[index], axis=0)[-2]], y_pred[index][np.argsort(y_pred[index], axis=0)[-2]]
        ), color='black', fontsize=14)

        # Plot capsule lengths as bar chart
        ax = axes[i + c]
        lengths = y_pred[index]
        ax.bar(range(len(class_names)), lengths,
               color=['g' if i == np.argmax(y_test[index]) else 'r' for i in range(len(class_names))])
        ax.set_xticks([0, 5, 10])
        ax.set_yticks([0, 0.25, 0.5, 0.75])
        ax.axis(True)

        # Plot reconstructed images
        ax = axes[i + 2 * c]
        ax.imshow(reconstructed_images[index, :, :, 0], cmap='gray')
        ax.axis('off')
        rect = patches.Rectangle((0, 0), reconstructed_images.shape[2] - 1, reconstructed_images.shape[1] - 1,
                                 linewidth=1, edgecolor='black', facecolor='none')
        ax.add_patch(rect)

    plt.show()
