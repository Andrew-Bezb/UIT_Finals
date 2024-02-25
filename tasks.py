from random import randint

"""
1. Создать программу, которая будет находить медиану списка из 20 чисел. Числа должны быть сгенерированы случайным образом. 
Если количество элементов в списке четное, медианой считается среднее значение двух центральных элементов, если нечетное - центральный элемент.
"""
# a = [randint(0, 100) for i in range(20)]
# a.sort()
# print(a)
# print((a[9] + a[10]) / 2)

"""
2. Напишите программу на Python, которая будет получать от пользователя число и выводить на экран все его делители.
[1, 3, 9497, 28491]
"""

list_of_nums = []
def sost(x):
    j = 1
    while j<=x:
        # int(x**0.5)
        if x%j==0:
            list_of_nums.append(j)
        j+=1
    return list_of_nums

print(sost(1250056789101213))

"""
3. Напишите программу на Python, которая будет получать от пользователя два числа и определять, являются ли они взаимно простыми 
(то есть не имеют общих делителей, кроме единицы). Результат должен выводиться на экран.
"""

# a,b = map(int, input().split())
#
# while a%b:
#     c = a%b
#     a, b = b, c
# else:
#     if b != 1:
#         print('Не взаимно простые')
#     else:
#         print('Взаимно простые')

"""
4. Создайте функцию для нахождения наибольшей возрастающей подпоследовательности в списке чисел.
"""

# list_of_nums = [1,2,3,0,4,5,4,5,6,7,8,9,10,1,2,3,4,5,6,8]
# biggest_set = []
# set = []
#
# for i in range(len(list_of_nums)):
#     if i != len(list_of_nums)-1:
#         if list_of_nums[i + 1] > list_of_nums[i]:
#             set.append(list_of_nums[i])
#         else:
#             set.append(list_of_nums[i])
#             if len(biggest_set) <= len(set):
#                 biggest_set = set
#                 set = []
#             else:
#                 set = []
#     else:
#         if list_of_nums[i] > list_of_nums[i-1]:
#             set.append(list_of_nums[i])
#             if len(biggest_set) <= len(set):
#                 biggest_set = set
#
# print(biggest_set)