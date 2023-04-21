import numpy as np
from matplotlib import pyplot as plt
from random import randint, shuffle


class InvalidWeightsException(Exception):
    pass


class InvalidNetworkInputException(Exception):
    pass


class HopfieldNetwork(object):
    def __init__(self, num_inputs):
        self._num_inputs = num_inputs
        self._weights = np.random.uniform(-1.0, 1.0, (num_inputs, num_inputs))

    def set_weights(self, weights):
        """Update the weights array"""
        if weights.shape != (self._num_inputs, self._num_inputs):
            raise InvalidWeightsException()

        self._weights = weights

    def get_weights(self):
        """Return the weights array"""
        return self._weights

    def calculate_neuron_output(self, neuron, input_pattern):
        """Calculate the output of the given neuron"""
        num_neurons = len(input_pattern)

        s = 0.0

        for j in range(num_neurons):
            s += self._weights[neuron][j] * input_pattern[j]

        return 1.0 if s > 0.0 else -1.0

    def run_once(self, update_list, input_pattern):
        """Iterate over every neuron and update it's output"""
        result = input_pattern.copy()

        changed = False
        for neuron in update_list:
            neuron_output = self.calculate_neuron_output(neuron, result)

            if neuron_output != result[neuron]:
                result[neuron] = neuron_output
                changed = True

        return changed, result

    def run(self, input_pattern, max_iterations=10):
        """Run the network using the input data until the output state doesn't change
        or a maximum number of iteration has been reached."""
        iteration_count = 0

        result = input_pattern.copy()

        update_list = []
        for i in range(self._num_inputs):
            update_list.append(i)

        while True:
            # update_list = range(self._num_inputs)

            shuffle(update_list)

            changed, result = self.run_once(update_list, result)

            if not changed or iteration_count == max_iterations:
                return result

def calculate_weight(i, j, patterns):
    """Calculate the weight between the given neurons"""
    num_patterns = len(patterns)

    s = 0.0
    for mu in range(num_patterns):
        s += patterns[mu][i] * patterns[mu][j]

    w = (1.0 / float(num_patterns)) * s

    return w


def calculate_neuron_weights(neuron_index, input_patterns):
    """Calculate the weights for the given neuron"""
    num_patterns = len(input_patterns)
    num_neurons = len(input_patterns[0])

    weights = np.zeros(num_neurons)

    for j in range(num_neurons):
        if neuron_index == j: continue
        weights[j] = calculate_weight(neuron_index, j, input_patterns)

    return weights


def hebbian_training(network, input_patterns):
    """Train a network using the Hebbian learning rule"""
    n = len(input_patterns)

    num_neurons = len(input_patterns[0])

    weights = np.zeros((num_neurons, num_neurons))

    for i in range(num_neurons):
        weights[i] = calculate_neuron_weights(i, input_patterns)

    network.set_weights(weights)
