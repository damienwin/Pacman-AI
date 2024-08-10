import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import sys
import os
import pickle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))
from deep_nn import forward_propagation, deep_nn_model

X = np.load("datasets/signdigits/X.npy")
Y = np.load("datasets/signdigits/Y.npy")

# Split dataset into some training examples(15%) and shuffle data
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.15, random_state=42)

m_train = X_train.shape[0]
X_train_flat = X_train.reshape(m_train, -1).T

m_test = X_test.shape[0]
X_test_flat = X_test.reshape(m_test, -1).T

Y_train = Y_train.T
Y_test = Y_test.T

print(X_train_flat.shape)
print(Y_train.shape)
print(X_test_flat.shape)
print(Y_test.shape)

layer_dims = [4096, 1024, 256, 64, 10]
classification_method="multivariable"
num_iterations = 10000
learning_rate = 0.01
lambd = 0.05

parameters, _ = deep_nn_model(X_train_flat, Y_train, 
                              num_iterations=num_iterations, 
                              layer_dims=layer_dims, 
                              learning_rate=learning_rate, 
                              classification_method=classification_method, 
                              lambd=lambd)

def predict(X, parameters):
    AL, _ = forward_propagation(X, parameters, classification_type="multivariable")
    predictions = np.argmax(AL, axis=0)  
    return predictions

def calculate_accuracy(predictions, labels):
    labels = np.argmax(labels, axis=0)
    return np.mean(predictions == labels)

with open('model_parameters.pkl', 'wb') as f:
    pickle.dump(parameters, f)

train_predictions = predict(X_train_flat, parameters)
train_accuracy = calculate_accuracy(train_predictions, Y_train)
print(f"Training Accuracy: {train_accuracy * 100:.2f}%")

test_predictions = predict(X_test_flat, parameters)
test_accuracy = calculate_accuracy(test_predictions, Y_test)
print(f"Test Accuracy: {test_accuracy * 100:.2f}%")

def log_results(file_path, num_iterations, learning_rate, lambd, train_accuracy, test_accuracy):
    # Check if the file exists
    if not os.path.exists(file_path):
        # If the file doesn't exist, create it and add a header
        with open(file_path, 'w') as f:
            f.write(f"{'Iter':<8} {'Alpha':<8} {'Lambd':<8} {'Beta':<8} {'Train%':<10} {'Test%':<10}\n")
            f.close()
    
    # Append the results to the file
    with open(file_path, 'a') as f:
        f.write(f"{num_iterations:<8} {learning_rate:<8} {lambd:<8} {train_accuracy * 100:<10.2f} {test_accuracy * 100:<10.2f}\n")
        print("Successfully logged")

log_file_path = "tests/sign_numbers_test/training_log.txt"
log_results(log_file_path, num_iterations, learning_rate, lambd, train_accuracy, test_accuracy)