import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


from metricCalculator import *
from ExpertDB import *

class FuzzyLogicController:
    def __init__(self, membership_func):
        self.membership_func =  membership_func

        # Определение нечетких переменных входа
        self.amplitudeOfSteer = ctrl.Antecedent(np.arange(0, self.membership_func[0,2][1], 1), 'amplitudeOfSteer')
        self.amplitudeOfAcc = ctrl.Antecedent(np.arange(0, self.membership_func[1,2][1], 1), 'amplitudeOfAcc')
        self.PedalCounter= ctrl.Antecedent(np.arange(0, self.membership_func[2,2][1], 1), 'PedalCounter')
        self.LDV = ctrl.Antecedent(np.arange(0, self.membership_func[3,2][1], 1), 'LDV')
        self.MeanVelocity = ctrl.Antecedent(np.arange(0, self.membership_func[4,2][1], 1), 'MeanVelocity')
       
        # Определение нечеткой переменной выхода
        self.DriverState = ctrl.Consequent(np.arange(0, 3, 1), 'DriverState')

        # Определение функций принадлежности
        self.amplitudeOfSteer['low'] = fuzz.trimf(self.amplitudeOfSteer.universe, [self.membership_func[0,0][0],(self.membership_func[0,0][0] + self.membership_func[0,0][1])/2, self.membership_func[0,0][1]])
        self.amplitudeOfSteer['medium'] = fuzz.trimf(self.amplitudeOfSteer.universe, [self.membership_func[0,1][0], (self.membership_func[0,1][0] + self.membership_func[0,1][1])/2, self.membership_func[0,1][1]])
        self.amplitudeOfSteer['hard'] = fuzz.trimf(self.amplitudeOfSteer.universe, [self.membership_func[0,2][0], (self.membership_func[0,2][0] + self.membership_func[0,2][1])/2, self.membership_func[0,2][1]])

        self.amplitudeOfAcc['low'] = fuzz.trimf(self.amplitudeOfAcc.universe, [self.membership_func[1,0][0], (self.membership_func[1,0][0] + self.membership_func[1,0][1])/2, self.membership_func[1,0][1]])
        self.amplitudeOfAcc['medium'] = fuzz.trimf(self.amplitudeOfAcc.universe, [self.membership_func[1,1][0], (self.membership_func[1,1][0] + self.membership_func[1,1][1])/2, self.membership_func[1,1][1]])
        self.amplitudeOfAcc['hard'] = fuzz.trimf(self.amplitudeOfAcc.universe, [self.membership_func[1,2][0], (self.membership_func[1,2][0] + self.membership_func[1,2][1])/2, self.membership_func[1,2][1]])

        
        self.PedalCounter['low'] = fuzz.trimf(self.PedalCounter.universe, [self.membership_func[2,0][0], (self.membership_func[2,0][0] + self.membership_func[2,0][1])/2, self.membership_func[2,0][1]])
        self.PedalCounter['medium'] = fuzz.trimf(self.PedalCounter.universe, [self.membership_func[2,1][0], (self.membership_func[2,1][0] + self.membership_func[2,1][1])/2, self.membership_func[2,1][1]])
        self.PedalCounter['hard'] = fuzz.trimf(self.PedalCounter.universe, [self.membership_func[2,2][0], (self.membership_func[2,2][0] + self.membership_func[2,2][1])/2, self.membership_func[2,2][1]])

        self.LDV['low'] = fuzz.trimf(self.LDV.universe, [self.membership_func[3,0][0], (self.membership_func[3,0][0] + self.membership_func[3,0][1])/2, self.membership_func[3,0][1]])
        self.LDV['medium'] = fuzz.trimf(self.LDV.universe, [self.membership_func[3,1][0], (self.membership_func[3,1][0] + self.membership_func[3,1][1])/2, self.membership_func[3,1][1]])
        self.LDV['hard'] = fuzz.trimf(self.LDV.universe, [self.membership_func[3,2][0], (self.membership_func[3,2][0] + self.membership_func[3,2][1])/2, self.membership_func[3,2][1]])

        self.MeanVelocity['low'] = fuzz.trimf(self.MeanVelocity.universe, [self.membership_func[4,0][0], (self.membership_func[4,0][0] + self.membership_func[4,0][1])/2, self.membership_func[4,0][1]])
        self.MeanVelocity['medium'] = fuzz.trimf(self.MeanVelocity.universe, [self.membership_func[4,1][0], (self.membership_func[4,1][0] + self.membership_func[4,1][1])/2, self.membership_func[4,1][1]])
        self.MeanVelocity['hard'] = fuzz.trimf(self.MeanVelocity.universe, [self.membership_func[4,2][0], (self.membership_func[4,2][0] + self.membership_func[4,2][1])/2, self.membership_func[4,2][1]])


        self.DriverState['low'] = fuzz.trimf(self.DriverState.universe, [0,0.5,1])
        self.DriverState['medium'] = fuzz.trimf(self.DriverState.universe, [0.75,1.5,2])
        self.DriverState['hard'] = fuzz.trimf(self.DriverState.universe, [1.75,2.5,3])
        # Определение правил
        rules = [
            ctrl.Rule(self.amplitudeOfSteer['low'], self.DriverState['low'])
        ]

        # Создание и компиляция нечеткой модели
        self.DriverState = ctrl.ControlSystem(rules)
        self.State = ctrl.ControlSystemSimulation(self.DriverState)

    def compute_brake_force(self, Steer, Acc,Pedal,Lane,Vel):
        # Присваивание входных значений
        self.State.input['amplitudeOfSteer'] = Steer
        self.State.input['amplitudeOfAcc'] = Acc
        self.State.input['PedalCounter'] = Pedal
        self.State.input['LDV'] = Lane
        self.State.input['MeanVelocity'] = Vel
        # Вычисление результата
        self.State.compute()

        # Возвращение выходного значения
        return self.State.output['DriverState']

    def plot_membership_functions(self):
        # Вывод функций принадлежности
        self.amplitudeOfSteer.view()
        self.amplitudeOfAcc.view()
        self.PedalCounter.view()
        self.LDV.view()
        self.MeanVelocity.view()
        self.DriverState.view()

        plt.show()

# Пример использования класса
if __name__ == "__main__":
    # # Создание экземпляра контроллера нечеткой логики
    # controller = FuzzyLogicController()

    # # Вывод графиков функций принадлежности
    # controller.plot_membership_functions()

    # # Пример вычисления силы торможения и вывод графика дефаззификации
    # distance = 10
    # speed = 15
    # brake_force = controller.compute_brake_force(distance, speed)


            # VALUES (1, 'Amplitude of Steering'),
            #         (2, 'Amplitude of Acceleration'),
            #         (3, 'Depal Counter'),
            #         (4, 'Calc LDV'),
            #         (5, 'Calc Mean Velocity')
    # Создаем экземпляр класса
    calculator = DrivingMetricsCalculator()

    # Инициализируем предыдущие значения
    prev_steer = 0.0
    prev_acc = 0.0
    prev_vel = 0.0

    result1 = 0.0
    result2 = 0.0
    result3 = 0.0
    result4 = 0.0
    result5 = 0.0


    turn_list = [False, False, True, True, False]

    dist_list = [0.1, 0.3, 0.1, 0.3, 0.13]

    steer_list = [12, 20, 15, 20, 10]

    acc_list = [0.1, 0.2, 0.2, 0.4, 0.1]

    pedal_list = [True, False, False, True, False]

    vel_list = [5, 14, 12, 10, 20]


    for i in range(len(turn_list)):
        result4 += calculator.calc_ldv(turn_list[i], dist_list[i])
        result1 = calculator.calc_amp_steer(steer_list[i], prev_steer)
        result2 = calculator.calc_amp_acc(acc_list[i], prev_acc)
        result3 += calculator.depal_counter(pedal_list[i])
        result5 = calculator.calc_mean_vel(vel_list[i])

        # Обновляем предыдущие значения
        prev_steer = steer_list[i]
        prev_acc = acc_list[i]
        prev_vel = vel_list[i]

    # Выводим результаты
    # print(result1)
    # print(result2)
    # print(result3)
    # print(result4)
    # print(result5)


    # Пример использования функции
    db = DrivingMetricsDatabase('driving_metrics.db')
    # db.create_tables()
    # db.insert_example_data()

    # Выбираем экспертов, которые оценили параметр "Amplitude of Steering" со значением 1
    result = db.query_experts_by_parameter_value(rate = 2,parameter_id  = 1, value = result1)
    experts = list()
    #формируем список экспертов
    for row in result:
        experts.append(row[0])


    # Создаем словарь для хранения минимальных и максимальных значений
    ratings_range = {}

    # Находим диапазон под параметр
    for parameter in range(5):
        for i in range(3):
            min_val = 10000
            max_val = -1
            for j in range(len(experts)):
                result = db.query_values_by_parameter(parameter_id=parameter+1, expert=experts[j], rate=i+1)
                if result[0][3] < min_val:
                    min_val = result[0][3]
                if result[0][4] > max_val:
                    max_val = result[0][4]
            # Сохраняем минимальное и максимальное значение для данной оценки в словаре
            ratings_range[(parameter, i)] = (min_val, max_val)
    controller = FuzzyLogicController(ratings_range)
    controller.plot_membership_functions()

    result1 = 0
    result2 = 1
    result3 = 0
    result4 = 0
    result5 = 0
    brake_force = controller.compute_brake_force(result1, result2, result3, result4,result5)
