import numpy as np
import scipy.special


def relu(matrix):
    matrix[matrix < 0] = 0
    return matrix


class NeuralNetwork:
    def __init__(self, layer1=4, layer2=6, layer3=3):
        '''
        Tworzy gęstą sieć neuronową o rozmiarach warst
        podanych jako layer1, layer2, layer3
        '''
        self.input_size = layer1
        self.hidden_layer_size = layer2
        self.output_size = layer3

        weights1 = np.random.random((layer1, layer2))
        weights2 = np.random.random((layer2, layer3))
        self.weights = [weights1, weights2]

    def __call__(self, input):
        '''
        Użycie sieci neuronowej poprzez podanie sygnału wejściowego
        '''
        weights1, weights2 = self.weights
        output = np.array(input)

        output = relu(output @ weights1)
        output = scipy.special.softmax(output @ weights2, axis=-1)

        return output

    def set_weights(self, weights):
        '''
        Przypisanie wag sieci neuronowej
        '''
        self.weights = weights

    def get_weights(self):
        '''
        Zwrócenie wag sieci neuronowej
        '''
        return self.weights
