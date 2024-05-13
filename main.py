from ExpertDB import *
from fuzzyControl import *
from metricCalculator import *
from hiddenMarkovModel import *

import numpy as np
import math

def CreateExpertList(db, first_estimate, result):
    # Выбираем экспертов, которые оценили параметр со значением result
    result = db.query_experts_by_parameter_value(rate = first_estimate,parameter_id  = 1, value = result)
    experts = list()
    #формируем список экспертов
    for row in result:
        experts.append(row[0])
    return experts

def CreateMembershipFunc(db,experts):
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
    return ratings_range


initFlag = False
initRideFlag = True
ChangeMindFlag = False

metrics = DrivingMetricsCalculator()
hmmModel = HiddenMarkovModel()
db = DrivingMetricsDatabase('driving_metrics.db')


if initFlag:
    db.create_tables()
    db.insert_example_data()
    initFlag = False

#Создать массивы данных 
turn_list = [False, False, True, True, False]
dist_list = [0.1, 0.3, 0.1, 0.3, 0.13]
steer_list = [12, 20, 15, 20, 10]
acc_list = [0.1, 0.2, 0.2, 0.4, 0.1]
pedal_list = [True, False, False, True, False]
vel_list = [5, 14, 12, 10, 20]

current_estimate_list = list()
predict_list = list()

preview_state = 0

for iteration in range(len(dist_list)):

    #Создаем блок обратной связи, гарантированно запускается при запуске системы
    if initRideFlag or ChangeMindFlag:
        first_estimate = 1
        if initRideFlag:
            first_estimate = int(math.ceil(float(input("Оцените Ваше состояние на момент начала езды: "))))
            initRideFlag = not(initRideFlag)
            
        if ChangeMindFlag:
            first_estimate = int(math.ceil(float(input("Замечено изменение в Вашем самочувствии, оцените ваше состояние: "))))
            ChangeMindFlag = not(ChangeMindFlag)
        preview_state = first_estimate
        #Рассчитываем функции принадлежности, согласно данным пользователя
        experts = CreateExpertList(db= db, first_estimate= first_estimate, result=acc_list[iteration])
        ratings_range = CreateMembershipFunc(db = db, experts=experts)
        #Инициализируем нечеткую логику
        fuzzy = FuzzyLogicController(ratings_range)
    
    #Находим текущую оценку
    current_estimate = fuzzy.compute_estimate(Steer= steer_list[iteration], Acc = acc_list[iteration], Lane =dist_list[iteration])
    current_estimate_list.append(current_estimate)

    #Прогнозируем результат
    observations_sequence = np.array(current_estimate_list).reshape(-1, 1)
    predict_list = list(hmm_model.predict(observations_sequence))

    #Продолжаем блок обратной связи
    #Проверяем, если состояние ухудшилось, если водитель несгласен с оценкой , меняем стратегию
    if (observations_sequence[-1] != preview_state or observations_sequence[-1] < predict_list[-1]):
        state_check = bool(input("Замечено изменение в Вашем самочувствии, оцените ваше состояние, вы согласны с оценкой? True|False "))
        if not(state_check):
            ChangeMindFlag = not(ChangeMindFlag)
    preview_state = observations_sequence[-1]

# Plot the results
hmm_model.plot_results(observations_sequence, predict_list)

    


    
    

    


