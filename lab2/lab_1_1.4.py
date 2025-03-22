total_sum = 0  # сумма чисел
count = 0  # кол-во чисел

print("Введите последовательность целых чисел. Для завершения ввода введите 'q':")
while True:
    user_input = input("Введите число (или 'q' для выхода): ")
    if user_input == 'q':  # условие выхода из цикла
        break
    number = int(user_input)  # преобразуем ввод в целое число
    total_sum += number  
    count += 1  

if count > 0:
    print(f"Сумма всех чисел: {total_sum}")
    print(f"Количество всех чисел: {count}")
else:
    print("Последовательность пуста.")