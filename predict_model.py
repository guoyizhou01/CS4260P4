import numpy as np
import joblib
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def weights_to_prediction(input):
    input_data = np.array([input])
    # Loading model parameters from the text file
    parameters_file_path = 'model_parameters.txt'  # Update with the correct path
    model_parameters = {}
    with open(parameters_file_path, 'r') as file:
        for line in file:
            key, value = line.split(":")
            model_parameters[key] = np.array(eval(value))

    # Extracting the weights and biases
    weights_input_hidden = model_parameters["weights_input_hidden"]
    bias_hidden = model_parameters["bias_hidden"]
    weights_hidden_output = model_parameters["weights_hidden_output"]
    bias_output = model_parameters["bias_output"]

    # Prediction function
    def predict(input_data):
        # Forward pass
        hidden_layer_input = np.dot(input_data, weights_input_hidden) + bias_hidden
        hidden_layer_output = sigmoid(hidden_layer_input)
        output_layer_input = np.dot(hidden_layer_output, weights_hidden_output) + bias_output
        predicted_output = sigmoid(output_layer_input)
        return predicted_output


    # Load the StandardScaler
    scaler_file_path = 'scaler.pkl'  # Update with the correct path
    scaler = joblib.load(scaler_file_path)

    # Standardize the input data
    input_data_standardized = scaler.transform(input_data)

    # Now use input_data_standardized for prediction
    predicted_output = predict(input_data_standardized)
    # print("Predicted Output:", predicted_output[0][0])
    return predicted_output[0][0]

if __name__ == '__main__':
    # Example prediction
      # Update with the actual input data
    weights_to_prediction([9, 10, 9, 4, 10, 5, 10, 5, 10, 5])