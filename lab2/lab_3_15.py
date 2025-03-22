import random
N = 10

# генерация нечетных чисел
array = [random.randrange(1, 100, 2) for _ in range(N)] 

# элементы массива меньше 10
print("Исходный массив:", array)
print("Элементы массива меньше 10:", [x for x in array if x < 10])

# умножение каждого четного индекса
for i in range(0, len(array), 2):
    array[i] *= 2

# вывод полученного массива
print("Массив после умножения четных индексов на 2:", array)