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
    print(experts)
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

    for key, value in ratings_range.items():
        print(f"Parameter {key[0]}, rate {key[1]}: min {value[0]}, max {value[1]}")
        print("________________________________")
        print(ratings_range[0,0][0])
    return ratings_range


initFlag = False
initRideFlag = True
ChangeMindFlag = False

metrics = DrivingMetricsCalculator()
hmmModel = HiddenMarkovModel()
hmmModel.fit()
db = DrivingMetricsDatabase('driving_metrics.db')

#Создаем базу данных, если ранее не создана
if initFlag:
    db.create_tables()
    db.insert_example_data()
    initFlag = False

#Создать массивы данных 
steer_list = [3, 1, 2,4, 8,9,11,11,11]
acc_list = [1, 1, 2,1, 9,9, 11,11,11]
pedal_list = [2, 3, 4, 3, 6,7,13,14,14 ]
dist_list = [1,1,1,1, 4,4, 7,8,9]
vel_list = [1,2,3,4,13,13,17,17]



# steer_list = [3, 1, 2,4, 8,9,11,11,11]
# acc_list = [1, 1, 2,1, 1,2, 11,11,11]
# pedal_list = [2, 3, 4, 3, 6,7,13,14,14 ]
# dist_list = [1,1,1,1, 4,4, 7,8,9]
# vel_list = [1,2,3,4,13,13,17,17]

#Списки оценок и прогнозов
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
        preview_state = first_estimate - 1
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
    # print(observations_sequence)
    # print(predict_list)
    predict_list = list(hmmModel.predict(observations_sequence))

    #Продолжаем блок обратной связи
    # #Проверяем, если состояние ухудшилось, если водитель несгласен с оценкой , меняем стратегию
    # if (observations_sequence[-1] != preview_state or observations_sequence[-1] < predict_list[-1]):
    if (observations_sequence[-1] != preview_state):
        state_check = int(input("Замечено изменение в Вашем самочувствии, оцените ваше состояние, вы согласны с оценкой? 1- Да|0 - Нет "))
        if state_check == 1:
            state_check = True
        else:
            state_check = False
        print(state_check)
        if not(state_check):
            ChangeMindFlag = True
    preview_state = observations_sequence[-1]

# Plot the results
hmmModel.plot_results(observations_sequence, predict_list)

    


    
    

    


