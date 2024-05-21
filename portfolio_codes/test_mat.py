import random

moy = 0

tries = 1000000

for  x in range(tries):

  liste = [0, 0, 0, 0]

  nbr = 0

  while 0 in liste:

    nbr += 1

    x = random.randint(0, 3)

    liste[x] += 1

  moy += nbr

print(moy/tries)

    
