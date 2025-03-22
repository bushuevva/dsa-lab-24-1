num1 = float(input('Введите первое число: '))
num2 = float(input('Введите второе число: '))
num3 = float(input('Введите третье число: '))

# создание списка из чисел
numbers = [num1, num2, num3]

print("Числа в интервале [1, 50]:")
for num in numbers:
    if 1 <= num <= 50:
        print(num)