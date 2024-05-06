from metricCalculator import *
from ExpertDB import *
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
    result1 += calculator.calc_ldv(turn_list[i], dist_list[i])
    result2 = calculator.calc_amp_steer(steer_list[i], prev_steer)
    result3 = calculator.calc_amp_acc(acc_list[i], prev_acc)
    result4 += calculator.depal_counter(pedal_list[i])
    result5 = calculator.calc_mean_vel(vel_list[i])

    # Обновляем предыдущие значения
    prev_steer = steer_list[i]
    prev_acc = acc_list[i]
    prev_vel = vel_list[i]

# Выводим результаты
print(result1)
print(result2)
print(result3)
print(result4)
print(result5)


# Пример использования функции
db = DrivingMetricsDatabase('driving_metrics.db')

# Выбираем экспертов, которые оценили параметр "Amplitude of Steering" со значением 1
result = db.query_experts_by_parameter_value(1, 1, 6)

# Выводим результат
for row in result:
    print(row)

