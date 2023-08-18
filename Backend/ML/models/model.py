import numpy as np
import tensorflow as tf
from utils.tools import get_callbacks, marginLoss
from utils.dataset import Dataset
from models import efficient_capsnet_graph_STSL
import os
import json
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import pandas as pd
from utils.visualisation import plotWrongImages


class Model(object):
    """
    A class used to share common model functions and attributes.
    
    ...
    
    Attributes
    ----------
    mode: str
        model modality (Ex. 'test')
    config_path: str
        path configuration file
    verbose: bool
    
    Methods
    -------
    load_config():
        load configuration file
    load_graph_weights():
        load network weights
    predict(dataset_test):
        use the model to predict dataset_test
    evaluate(X_test, y_test):
        compute accuracy and test error with the given dataset (X_test, y_test)
    save_graph_weights():
        save model weights
    """

    def __init__(self, mode='test', config_path='config_STSL.json', verbose=True):
        self.model = None
        self.mode = mode
        self.config_path = config_path
        self.config = None
        self.verbose = verbose
        self.load_config()


    def load_config(self):
        """
        Load config file
        """
        with open(self.config_path) as json_data_file:
            self.config = json.load(json_data_file)
    

    def load_graph_weights(self):
        print(f"Attempting to load weights from: {self.model_path}")
        try:
            self.model.load_weights(self.model_path)
        except Exception as e:
            print("[ERRROR] Graph Weights not found")
            
        
    def predict(self, dataset_test):
        return self.model.predict(dataset_test)
    


    def evaluate(self, X_test, y_test):
        print('-'*30 + f'{"STSL"} Evaluation' + '-'*30)

        # calculate accuracy
        y_pred, X_gen =  self.model.predict(X_test)
        acc = np.sum(np.argmax(y_pred, 1) == np.argmax(y_test, 1))/y_test.shape[0]

        test_error = 1 - acc
        print('Test acc:', acc)
        print(f"Test error [%]: {(test_error):.4%}")
    
        print(f"N° misclassified images: {int(test_error*len(y_test))} out of {len(y_test)}")

        # convert predicted probabilities to class labels
        y_pred_class = np.argmax(y_pred, axis=1)
        y_true_class = np.argmax(y_test, axis=1)

        # directly print the classification report
        print("\nClassification Report:")
        print(classification_report(y_true_class, y_pred_class))

        # create label mappings for confusion matrix plotting
        label_mapping = {'CH': 0, 'G': 1, 'H': 2, 'J': 3, 'LL': 4, 'Ñ': 5, 'RR': 6, 'V': 7, 'W': 8, 'Z': 9, 'Y': 10}
        combined_labels = [f"{v} [{k}]" for k, v in label_mapping.items()]

        # plot the confusion matrix
        matrix = confusion_matrix(y_true_class, y_pred_class)
        plt.figure(figsize=(10, 6))
        sns.heatmap(matrix, annot=True, fmt="d", linewidths=.5, cmap="Blues", xticklabels=combined_labels, yticklabels=combined_labels)
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.title('Confusion Matrix')
        plt.savefig("Confusion Matrix.png")
        plt.show()


    def save_graph_weights(self):
        self.model.save_weights(self.model_path)


    def save_full_model(self, save_path):
        try:
            self.model.save(save_path)
            if self.verbose:
                print(f"Model saved successfully to {save_path}")
        except Exception as e:
            print(f"[ERROR] Failed to save the model. Reason: {e}")




class EfficientCapsNet(Model):
    """
    A class used to manage an Efficiet-CapsNet model. 'mode' define the particular architecure and modality of the 
    generated network.
    
    ...
    
    Attributes
    ----------
    mode: str
        model modality (Ex. 'test')
    config_path: str
        path configuration file
    custom_path: str
        custom weights path
    verbose: bool
    
    Methods
    -------
    load_graph():
        load the network graph for the MNIST model
    train(dataset, initial_epoch)
        train the constructed network with a given dataset. All train hyperparameters are defined in the configuration file

    """
    def __init__(self, mode='test', config_path='config_STSL.json', custom_path=None, verbose=True):
        Model.__init__(self, mode, config_path, verbose)
        if custom_path != None:
            self.model_path = custom_path
        else:
            self.model_path = os.path.join(self.config['saved_model_dir'], f"efficient_capsnet_STSL.h5")
        # self.model_path_new_train = os.path.join(self.config['saved_model_dir'], f"efficient_capsnet_STSL_new_train.h5")
        self.tb_path = os.path.join(self.config['tb_log_save_dir'], f"efficient_capsnet_STSL")
        self.load_graph()
    

    def load_graph(self):
        self.model = efficient_capsnet_graph_STSL.build_graph(self.config['STSL_INPUT_SHAPE'], self.mode, self.verbose)
        
            
    def train(self, dataset=None, initial_epoch=0):
        callbacks = get_callbacks(self.tb_path, self.model_path, self.config['lr_dec'], self.config['lr'])

        if dataset == None:
            dataset = Dataset(self.config_path)
        dataset_train, dataset_val, _ = dataset.get_tf_data()    

        self.model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=self.config['lr']),
            loss=[marginLoss, 'mse'],
            loss_weights=[1., self.config['lmd_gen']],
            metrics={'Efficient_CapsNet': 'accuracy'})
        steps=None

        print('-'*30 + f'{"EfficientCapsNet"} train' + '-'*30)

        history = self.model.fit(dataset_train,
          epochs=self.config[f'epochs'], steps_per_epoch=steps,
          validation_data=(dataset_val), batch_size=self.config['batch_size'], initial_epoch=initial_epoch,
          callbacks=callbacks)
        
        return history
