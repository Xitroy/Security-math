# -*- coding: utf-8 -*-
"""
@author: Zhdan
"""
import random

# --- Матричный метод вычисления фибоначи ---
def power(x, n, I, mult):
    """
    Возвращает x в степени n. Предполагает, что I – это единичная матрица, которая 
    перемножается с mult, а n – положительное целое
    """
    if n == 0:
        return I
    elif n == 1:
        return x
    else:
        y = power(x, n // 2, I, mult)
        y = mult(y, y)
        if n % 2:
            y = mult(x, y)
        return y


def identity_matrix(n):
    """Возвращает единичную матрицу n на n"""
    r = list(range(n))
    return [[1 if i == j else 0 for i in r] for j in r]


def matrix_multiply(A, B):
    BT = list(zip(*B))
    return [[sum(a * b
                 for a, b in zip(row_a, col_b))
            for col_b in BT]
            for row_a in A]


def fib(n):
    F = power([[1, 1], [1, 0]], n, identity_matrix(2), matrix_multiply)
    return F[0][1]


# --- Проверка числа тестом Люка ---
def Lucas_primality_test(n):
    
    r = n % 5; # почему-то именно 5, ну да ладно
    e = -1; # символ Лежнадра, дефолт -1 иначе поменяется позже

    if (r == 0):
        e = 0;
    if (r == 1 or r == 4):
        e = 1;
    
    fibo_n_minus_e = fib(n - e)
    # print(fibo_n_minus_e, r, e, n)
    
    # проверка по теореме 6.1
    if (fibo_n_minus_e % n == 0):
        return True;
    return False;


# --- Первые N псевдопростых по Люку чисел ---
def Task_1(n):
    counter = 0
    current = 5
    results = []
    while counter<n:
        if Lucas_primality_test(current):
            results.append(current)
            counter+=1
        current += 2
    return results


# --- Проверка числа тестом Миллера-Рабина ---
import random
 
# Функция будет вызвана k раз
# Вернет false если n составное
# true если n "возможно простое" 
# d такое число, что 2^d*r = n-1 для некоторого нечетного r >= 1
def miillerTest(r, n, fixed_a=False):
     
    # Выбираем случайное a из промежутка [2..n-2]
    # Предполагаем, что n > 4 и проверка была до вызова
        
    a = random.randint(2, n - 2) if not fixed_a else 2 #менять двойку тут
    x = a**r % n
 
    # Число a - свидетель простоты. Нашелся - вышли.
    if (x == 1 or x == n - 1):
        return True;
    
    # Возводим x в квадрат, пока не случится 1 из 3:
    # 1. r достигло n-1
    # 2. (x^2) % n == 1 - дальше нет смысла перебирать
    # 3. (x^2) % n == n-1 - свидетельство
    while (r != n - 1):
        x = (x * x) % n;
        r *= 2;
 
        if (x == 1):
            return False;
        if (x == n - 1):
            return True;
 
    # Число a не свидетельствует о простоте
    return False;
 
# Вернет false если n составное 
# true если n "возможно простое". 
# Чем больше k - тем больше проверок -> тем выше точность. 
def isPrime(n, k, fixed_a=False):
     
    # Пограничные случаи
    if (n <= 1 or n == 4):
        return False;
    if (n <= 3):
        return True;
 
    # Находим такое r при котором n = 2^d * r + 1 для некоторого r >= 1
    r = n - 1;
    while (r % 2 == 0):
        r //= 2;
 
    # Прогоняем число через тест Миллера k раз
    for i in range(k):
        if (miillerTest(r, n, fixed_a=fixed_a) == False):
            return False;
 
    return True;
 
def Task_2(n):
    # находит n простых чисел, прошедших двойную проверку (Миллером и Люком)
    def Lucas_plus_Miller_test(n, k, fixed_a):
        counter = 0
        current = 5
        results = []
        while counter<n:
            if Lucas_primality_test(current) and isPrime(current, k, fixed_a=fixed_a):
                results.append(current)
                counter+=1
            current += 2
        return results
    
    return Lucas_plus_Miller_test(n, 1, fixed_a=True)
    # k = 4; # Количество прогонов
    # print("Простые числа меньше 100: ");
    # for n in range(1,100):
    #     if (isPrime(n, k, fixed_a=False)):
    #         print(n , end=" ");
    # print()

def Task_2_part_2():
    counter = 0
    current = 5
    status = 1000
    k_weak = 1
    k_strong = 4
    while True:
        test_lucas = Lucas_primality_test(current)
        test_miller = isPrime(current, k_weak)
        test_miller_strong = isPrime(current, k_strong)
        if test_lucas and test_miller and not test_miller_strong:
            return current
        else:
            current += 2
        if status < current:
            print(current)
            status = status * 2
    return None
            
        
    
    
# Демонстрация результатов
result_task_1 = Task_1(101)
result_task_2 = Task_2(101)
print(result_task_1, len(result_task_1))
print(result_task_2, (len(result_task_2)))
print("difference:", set(result_task_1).difference(set(result_task_2)))
# print(Task_2_part_2())



def Task_3():
    counter = 0
    bad_guys_counter = 0
    bad_guys = []
    current = 5
    addition = 2
    status = 1000
    k_weak = 1
    k_strong = 4
    while current<500000:
        test_lucas = Lucas_primality_test(current)
        test_miller = isPrime(current, k_weak, fixed_a=True)
        test_miller_strong = isPrime(current, k_strong)
        if test_lucas and test_miller and not test_miller_strong:
            bad_guys_counter += 1 # счетчик составных, которые прошли оба теста
            bad_guys.append(current)
        else:
            current += 2
        if status < current:
            print(current)
            status = status * 1.5
    print("bad guys amount:", bad_guys_counter)
    return bad_guys

# Демонстрация результатов
# без оптимизаций считаться будет очень долго. Надо думать об улучшениях алгоритма
from datetime import datetime
start_time = datetime.now()
result = Task_3()
print(result, len(result))
end_time = datetime.now()
print(end_time - start_time)