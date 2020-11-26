import numpy as np
import scipy.special


def relu(matrix):
    matrix[matrix < 0] = 0


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
        output = np.array(input)

        for weight in self.weights:
            output = output @ weight
            relu(output)

        return scipy.special.softmax(output, axis=-1)

    def set_weights(self, weights):
        self.weights = weights
