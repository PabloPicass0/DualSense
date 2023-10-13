# Introduction

This is the repository to the report "Exploratory Study on Complex Gesture Recognition for an iPad-based Tactile Sign Language Tutoring System" that is submitted in partial fulfillment of the  requirements for the MSc degree in Computing of Imperial College London.


# What's contained in this project

The repository is structured into front end (DualSense) and back end (Backend).

## DualSense

The front end is implemented in Swift. The directory contains the scripts for the app as well as a "MenuView" file that serves as landing page when the app is opened, and the directories "Parametric" and "ML" which contain the code for the recognition views. The recognition views are brought together in the menu view so that the user can select them and start performing gestures. Note that for the parametric recogniser each sign requires its own view. This is because for the parametric recogniser, depending on the sign, a different recognition function is called that is tied to the respective Bezier curve template. For the ML approach, the model is trained on all signs and hence only one view is required.
 

## Backend

The back end is implemented in python and consists out of a flask application designed to catch and respond to front end requests. The directory contains a few individual python files as well as two subdirectories. The individual python files consist out of the endpoint script that contains all the code related to the flask application and "extraction", "parameterisation", and "recognition", which provide functions to fit and match Bezier curves. The subdirectories are "ML" and "Parametric". The latter contains a subdirectory for each sign with the code to fit the respective curve(s), the raw data that was used to fit the curve(s), and the fitted curve template. The former contains all the code for the machine learning approach, including the saved model and dataset. Please note that code related to the model architecture heavily builds on https://github.com/EscVM/Efficient-CapsNet/blob/main/README.md. This is also declared in a NOTICE file within the directory. A notebook is included "model_training" to let you train and test a model yourself (GPU recommended; ensure the packages in requirements.txt are installed).

## Run the application

1. Run the endpoint
2. Ensure the frontend targets the correct IP address (update the baseURL variable in GlobalConstants.swift)
3. Run the build within Xcode --> Xcode provides a Content View to test the application without an iPad
4. Enjoy!
