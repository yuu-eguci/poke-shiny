# coding: utf-8

import random


# 170/3000 の確率で 10-19 がランダムに出て、 6/3000 の確率で 20-29 が出て、それ以外は 5-9 が出る関数
def elmina_bp():
    a = random.randint(1, 3000)
    if 1 <= a <= 170:
        b = random.randint(10, 19)
    elif 171 <= a <= 176:
        b = random.randint(20, 29)
    else:
        b = random.randint(5, 9)
    return b


# 擬似色違い孵化
# 0通常出現率1/4096 1ひかおま所持3/same 2国際孵化6/same 3ひかおま国際孵化8/same
def poke_shiny(x):
    success = times = 0
    while success == 0:
        a = random.randint(1, 4096)
        times += 1
        if x == 0:
            if a == 1: success = 1
            else: continue
        elif x == 1:
            if a <= 3: success = 1
            else: continue
        elif x == 2:
            if a <= 6: success = 1
            else: continue
        else:
            if a <= 8: success = 1
            else: continue
    return '\n\nHey! I\'m %s th brother.' % times


# x は 5-9, 10-19, 20-29 の三通りで、それが出るまで振る関数。なお出るまでの回数も出る
def aim_to(x):
    w = z = 0
    while w == 0:
        y = elmina_bp()
        z += 1
        if x == 0:
            if 5 <= y <= 9 and w == 0: w = 1
            else: continue
        elif x == 1:
            if 10 <= y <= 19 and w == 0: w = 1
            else: continue
        else:
            if 20 <= y <= 29 and w == 0: w = 1
            else: continue
    return '%s\n%s times rolled.' % (y, z)
