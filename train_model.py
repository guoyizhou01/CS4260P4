import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

# Load and preprocess the dataset
file_path = 'data_medium.txt'  # Update with the correct path
data = pd.read_csv(file_path, delimiter='\t', encoding='utf-8').values
X = data[:, 1:]  # Features
y = data[:, 0].reshape(-1, 1)  # Target

# Normalizing the input data
scaler = StandardScaler()
X_normalized = scaler.fit_transform(X)

# Neural network configuration
n_inputs = X.shape[1]
n_hidden_enhanced = 10  # Increased number of neurons in the hidden layer
n_outputs = 1

# Initialize weights and biases
weights_input_hidden_enhanced = np.random.rand(n_inputs, n_hidden_enhanced)
bias_hidden_enhanced = np.random.rand(n_hidden_enhanced)
weights_hidden_output_enhanced = np.random.rand(n_hidden_enhanced, n_outputs)
bias_output_enhanced = np.random.rand(n_outputs)

# Training function
def train_enhanced(X, y, epochs, learning_rate):
    global weights_input_hidden_enhanced, weights_hidden_output_enhanced, bias_hidden_enhanced, bias_output_enhanced

    for epoch in range(epochs):
        # Forward pass
        hidden_layer_input = np.dot(X, weights_input_hidden_enhanced) + bias_hidden_enhanced
        hidden_layer_output = sigmoid(hidden_layer_input)
        output_layer_input = np.dot(hidden_layer_output, weights_hidden_output_enhanced) + bias_output_enhanced
        y_pred = sigmoid(output_layer_input)

        # Backward pass
        error_output = y - y_pred
        d_weights_hidden_output = np.dot(hidden_layer_output.T, error_output * sigmoid_derivative(y_pred))
        error_hidden = np.dot(error_output * sigmoid_derivative(y_pred), weights_hidden_output_enhanced.T)
        d_weights_input_hidden = np.dot(X.T, error_hidden * sigmoid_derivative(hidden_layer_output))

        # Update weights and biases
        weights_hidden_output_enhanced += learning_rate * d_weights_hidden_output
        weights_input_hidden_enhanced += learning_rate * d_weights_input_hidden
        bias_output_enhanced += learning_rate * np.sum(error_output * sigmoid_derivative(y_pred), axis=0)
        bias_hidden_enhanced += learning_rate * np.sum(error_hidden * sigmoid_derivative(hidden_layer_output), axis=0)

# Retrain the model
train_enhanced(X_normalized, y, epochs=10000, learning_rate=0.005)

# Saving the model parameters to a text file
model_parameters = {
    "weights_input_hidden": weights_input_hidden_enhanced.tolist(),
    "bias_hidden": bias_hidden_enhanced.tolist(),
    "weights_hidden_output": weights_hidden_output_enhanced.tolist(),
    "bias_output": bias_output_enhanced.tolist()
}

parameters_file_path = 'model_parameters.txt'  # Update with the correct path
with open(parameters_file_path, 'w') as file:
    for key, value in model_parameters.items():
        file.write(key + ":" + str(value) + "\n")
scaler_file_path = 'scaler.pkl'  # Update with the correct path
joblib.dump(scaler, scaler_file_path)