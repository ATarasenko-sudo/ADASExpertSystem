import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from hmmlearn import hmm

class HiddenMarkovModel:
    def __init__(self):
        self.states = ["state1", "state2", "state3"]
        self.n_states = len(self.states)
        self.observations = ["state1", "state2", "state3"]
        self.n_observations = len(self.observations)
        self.start_probability = np.array([0.6, 0.3, 0.1])
        self.transition_probability = np.array([[0.5, 0.4, 0.1],
                                   [0.1, 0.5, 0.4],
                                   [0.1, 0.4, 0.5]])

        self.emission_probability = np.array([[0.7, 0.2, 0.1],
                                 [0.4, 0.4, 0.2],
                                 [0.2, 0.4, 0.4]])

        self.model = hmm.CategoricalHMM(n_components=self.n_states)
        
    def fit(self):
        self.model.startprob_ = self.start_probability
        self.model.transmat_ = self.transition_probability
        self.model.emissionprob_ = self.emission_probability
        
    def predict(self, observations_sequence):
        return self.model.predict(observations_sequence)
    
    def plot_results(self, observations_sequence, hidden_states):
        sns.set_style("darkgrid")
        plt.plot(observations_sequence, '-', label="observations_sequence")
        plt.plot(hidden_states, '-o', label="Hidden State")
        plt.legend()
        plt.show()



# # Create an instance of the HiddenMarkovModel class
# hmm_model = HiddenMarkovModel()

# # Fit the model
# hmm_model.fit()

# # Define the sequence of observations
# observations_sequence = np.array([0, 0, 0, 0, 1, 1, 2, 2, 2]).reshape(-1, 1)

# # Predict the most likely hidden states
# hidden_states = hmm_model.predict(observations_sequence)
# print("Most likely hidden states:", hidden_states)

# # Plot the results
# hmm_model.plot_results(observations_sequence, hidden_states)
