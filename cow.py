# введите "end" для завершения


from random import randint


n = int(input('введите количество цифр : '))
zz = str(randint(0,10**n-1))
zag = ('0'*(n-len(zz)))+zz
# print('*** '+zag+' ***')
m = [j for j in zag]
popytka = 1

aa = input('попытка '+str(popytka)+': ')

while aa != 'end':
    a = [j for j in aa]
    # проверяем на быков
    for i in range(n):
        if a[i] == zag[i]:
            m[i] = 'b'
            a[i] = 'B'
   
    # проверяем на коров
    for i in range(n):
        if m.count(a[i]) > 0:
            found = m.index(a[i])
            m[found] = 'k'
    if m.count('b') != n:
        print(m.count('b'), 'БЫКОВ  ', m.count('k'), 'КОРОВ')
        popytka +=1
        aa = input('попытка '+str(popytka)+': ')
        m = [j for j in zag]
    else:
        print('поздравляю! Вы угадали с', popytka, 'попытки')
        aa = 'end'