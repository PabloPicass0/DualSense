# Introduction

This is the repository to the report "Exploratory Study on Complex Gesture Recognition for an iPad-based Tactile Sign Language Tutoring System" that is submitted in partial fulfillment of the  requirements for the MSc degree in Computing of Imperial College London.


# What's contained in this project

The repository is structured into front end (DualSense) and back end (Backend).

## DualSense
 

## Backend

The back end is written in python and consists out of a flask application designed to catch and respond to front end requests. The directory contains a few individual python files as well as 
two subdirectories. The individual python files consist out of the endpoint script that contains all the code related to the flask application and "extraction", "parameterisation", and 
"recognition", which provide functions to fit and match Bezier curves. The subdirectories are "ML" and "Parametric". The latter contains a subdirectory for each sign with the code to fit 
the respective curve(s), the raw data that was used to fit the curve(s), and the curve template(s) itself. The former contains all the code for the machine learning approach, including the 
saved model and dataset. Please note that code related to the model architecture heavily builds on https://github.com/EscVM/Efficient-CapsNet/blob/main/README.md. This is also declared in a 
NOTICE file within the directory.
