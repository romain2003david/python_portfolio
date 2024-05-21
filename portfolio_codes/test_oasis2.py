import numpy as np


def peaks(liste):


  mean = sum(liste)/len(liste)

  print(mean)

  cap = 2*mean

  print(liste)
  
  liste_binaire = [(x>cap)*1 for x in liste]

  print(liste_binaire)

  for x in range(len(liste_binaire)):

    print(liste_binaire)
    elem = liste_binaire[x]

    if elem > 0:

      if len(liste_binaire) < x+1 or liste_binaire[x+1] == 1:

        liste_binaire[x+1] += liste_binaire[x]

      
      else:

        liste_binaire[x-elem//2] = 1

      liste_binaire[x] = 0

  return [x for x in range(len(liste)) if liste_binaire[x] == 1]


print(peaks([0, 0, 0, 0, 0, 0, 0, 7, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 4, 0, 0]))
