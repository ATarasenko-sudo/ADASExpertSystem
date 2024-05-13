import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import math

from metricCalculator import *
from ExpertDB import *

class FuzzyLogicController:
    def __init__(self, membership_func):
        self.membership_func =  membership_func

        # Определение нечетких переменных входа
        self.amplitudeOfSteer = ctrl.Antecedent(np.arange(-1, self.membership_func[0,2][1], 1), 'amplitudeOfSteer')
        self.amplitudeOfAcc = ctrl.Antecedent(np.arange(-1, self.membership_func[1,2][1], 1), 'amplitudeOfAcc')
        self.LDV = ctrl.Antecedent(np.arange(-1, self.membership_func[3,2][1], 1), 'LDV')
       
        # Определение нечеткой переменной выхода
        self.DriverState = ctrl.Consequent(np.arange(-0.1, 4, 1), 'DriverState')

        # Определение функций принадлежности
        self.amplitudeOfSteer['low'] = fuzz.trimf(self.amplitudeOfSteer.universe, [self.membership_func[0,0][0]-1,(self.membership_func[0,0][0] + self.membership_func[0,0][1])/2, self.membership_func[0,0][1]])
        self.amplitudeOfSteer['medium'] = fuzz.trimf(self.amplitudeOfSteer.universe, [self.membership_func[0,1][0]-1, (self.membership_func[0,1][0] + self.membership_func[0,1][1])/2, self.membership_func[0,1][1]])
        self.amplitudeOfSteer['hard'] = fuzz.trimf(self.amplitudeOfSteer.universe, [self.membership_func[0,2][0]-1, (self.membership_func[0,2][0] + self.membership_func[0,2][1])/2, self.membership_func[0,2][1]])

        self.amplitudeOfAcc['low'] = fuzz.trimf(self.amplitudeOfAcc.universe, [self.membership_func[1,0][0]-1, (self.membership_func[1,0][0] + self.membership_func[1,0][1])/2, self.membership_func[1,0][1]])
        self.amplitudeOfAcc['medium'] = fuzz.trimf(self.amplitudeOfAcc.universe, [self.membership_func[1,1][0]-1, (self.membership_func[1,1][0] + self.membership_func[1,1][1])/2, self.membership_func[1,1][1]])
        self.amplitudeOfAcc['hard'] = fuzz.trimf(self.amplitudeOfAcc.universe, [self.membership_func[1,2][0]-1, (self.membership_func[1,2][0] + self.membership_func[1,2][1])/2, self.membership_func[1,2][1]])

        self.LDV['low'] = fuzz.trimf(self.LDV.universe, [self.membership_func[3,0][0]-1, (self.membership_func[3,0][0] + self.membership_func[3,0][1])/2, self.membership_func[3,0][1]])
        self.LDV['medium'] = fuzz.trimf(self.LDV.universe, [self.membership_func[3,1][0]-1, (self.membership_func[3,1][0] + self.membership_func[3,1][1])/2, self.membership_func[3,1][1]])
        self.LDV['hard'] = fuzz.trimf(self.LDV.universe, [self.membership_func[3,2][0]-1, (self.membership_func[3,2][0] + self.membership_func[3,2][1])/2, self.membership_func[3,2][1]])


        self.DriverState['medium'] = fuzz.trimf(self.DriverState.universe, [1,2,2.5])
        self.DriverState['hard'] = fuzz.trimf(self.DriverState.universe, [2,3,4])
        self.DriverState['low'] = fuzz.trimf(self.DriverState.universe, [-0.1,1,1.5])
        # Определение правил
        rules = [
            ctrl.Rule(self.LDV['low'] & self.amplitudeOfSteer['low'] & self.amplitudeOfAcc['low'], self.DriverState['low']),
            ctrl.Rule(self.LDV['medium'] & self.amplitudeOfSteer['low'] & self.amplitudeOfAcc['low'], self.DriverState['low']),
            ctrl.Rule(self.LDV['hard'] & self.amplitudeOfSteer['low'] & self.amplitudeOfAcc['low'], self.DriverState['medium']),
            ctrl.Rule(self.LDV['low'] & self.amplitudeOfSteer['medium'] & self.amplitudeOfAcc['low'], self.DriverState['low']),
            ctrl.Rule(self.LDV['medium'] & self.amplitudeOfSteer['medium'] & self.amplitudeOfAcc['low'], self.DriverState['medium']),
            ctrl.Rule(self.LDV['hard'] & self.amplitudeOfSteer['medium'] & self.amplitudeOfAcc['low'], self.DriverState['medium']),
            ctrl.Rule(self.LDV['low'] & self.amplitudeOfSteer['hard'] & self.amplitudeOfAcc['low'], self.DriverState['medium']),
            ctrl.Rule(self.LDV['medium'] & self.amplitudeOfSteer['hard'] & self.amplitudeOfAcc['low'], self.DriverState['hard']),
            ctrl.Rule(self.LDV['hard'] & self.amplitudeOfSteer['hard'] & self.amplitudeOfAcc['low'], self.DriverState['hard']),
            ctrl.Rule(self.LDV['low'] & self.amplitudeOfSteer['low'] & self.amplitudeOfAcc['medium'], self.DriverState['low']),
            ctrl.Rule(self.LDV['medium'] & self.amplitudeOfSteer['low'] & self.amplitudeOfAcc['medium'], self.DriverState['medium']),
            ctrl.Rule(self.LDV['hard'] & self.amplitudeOfSteer['low'] & self.amplitudeOfAcc['medium'], self.DriverState['hard']),
            ctrl.Rule(self.LDV['low'] & self.amplitudeOfSteer['medium'] & self.amplitudeOfAcc['medium'], self.DriverState['low']),
            ctrl.Rule(self.LDV['medium'] & self.amplitudeOfSteer['medium'] & self.amplitudeOfAcc['medium'], self.DriverState['medium']),
            ctrl.Rule(self.LDV['hard'] & self.amplitudeOfSteer['medium'] & self.amplitudeOfAcc['medium'], self.DriverState['hard']),
            ctrl.Rule(self.LDV['low'] & self.amplitudeOfSteer['hard'] & self.amplitudeOfAcc['medium'], self.DriverState['medium']),
            ctrl.Rule(self.LDV['medium'] & self.amplitudeOfSteer['hard'] & self.amplitudeOfAcc['medium'], self.DriverState['hard']),
            ctrl.Rule(self.LDV['hard'] & self.amplitudeOfSteer['hard'] & self.amplitudeOfAcc['medium'], self.DriverState['hard']),
            ctrl.Rule(self.LDV['low'] & self.amplitudeOfSteer['low'] & self.amplitudeOfAcc['hard'], self.DriverState['medium']),
            ctrl.Rule(self.LDV['medium'] & self.amplitudeOfSteer['low'] & self.amplitudeOfAcc['hard'], self.DriverState['medium']),
            ctrl.Rule(self.LDV['hard'] & self.amplitudeOfSteer['low'] & self.amplitudeOfAcc['hard'], self.DriverState['hard']),
            ctrl.Rule(self.LDV['low'] & self.amplitudeOfSteer['medium'] & self.amplitudeOfAcc['hard'], self.DriverState['medium']),
            ctrl.Rule(self.LDV['medium'] & self.amplitudeOfSteer['medium'] & self.amplitudeOfAcc['hard'], self.DriverState['hard']),
            ctrl.Rule(self.LDV['hard'] & self.amplitudeOfSteer['medium'] & self.amplitudeOfAcc['hard'], self.DriverState['hard']),
            ctrl.Rule(self.LDV['low'] & self.amplitudeOfSteer['hard'] & self.amplitudeOfAcc['hard'], self.DriverState['medium']),
            ctrl.Rule(self.LDV['medium'] & self.amplitudeOfSteer['hard'] & self.amplitudeOfAcc['hard'], self.DriverState['hard']),
            ctrl.Rule(self.LDV['hard'] & self.amplitudeOfSteer['hard'] & self.amplitudeOfAcc['hard'], self.DriverState['hard'])
        ]

        # Создание и компиляция нечеткой модели
        self.driver_state_ctrl = ctrl.ControlSystem(rules)
        self.driver_state = ctrl.ControlSystemSimulation(self.driver_state_ctrl)

    def compute_estimate(self, Steer, Acc,Lane):
        # Присваивание входных значений
        self.driver_state.input['amplitudeOfSteer'] = Steer
        self.driver_state.input['amplitudeOfAcc'] = Acc
        self.driver_state.input['LDV'] = Lane
        # Вычисление результата
        self.driver_state.compute()

        self.DriverState.view(sim=self.driver_state)
        plt.show()

        # Возвращение выходного значения
        return math.ceil(self.driver_state.output['DriverState'])

    def plot_membership_functions(self):
        # Вывод функций принадлежности
        self.amplitudeOfSteer.view()
        self.amplitudeOfAcc.view()
        self.LDV.view()
        self.DriverState.view()

        plt.show()

# Пример использования класса
# if __name__ == "__main__":
#     controller = FuzzyLogicController(ratings_range)

#     brake_force = controller.compute_estimate(result1, result2, result4)
