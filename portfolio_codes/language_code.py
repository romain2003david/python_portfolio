from random import *


class Word:
  # class of word

  # defines some basic stuff of the language

  consonnes_nasales = ["m", "n"]
 
  consonnes_occlusives_voisees = ["b", "d", "g"]
 
  consonnes_occlusives_sourdes = ["p", "t", "k"]
 
  consonnes_fricatives_voisees = ["v", "z", "j"]
 
  consonnes_fricatives_sourdes = ["f", "s", "c"]
 
  consonnes_liquides = ["r", "l"]
 
  glides = ["y", "w"]
 
  voyelles = ["a", "e", "i", "o", "u"]
 
  consonnes = [consonnes_nasales, consonnes_occlusives_voisees, consonnes_occlusives_sourdes, consonnes_fricatives_voisees, consonnes_fricatives_sourdes, consonnes_liquides]
 
  nbr_consonnes = 0

  for liste in consonnes:
   
    nbr_consonnes += len(liste)

  def __init__(self, stored_words):

    self.stored_words = stored_words
   
    self.content = ""
 
  def set_rand_word(self, rec=100):
    """ creates word with basis C(C)V(G) """

    self.content = ""

    self.content += Word.get_rand_consonne(self)

    self.content += Word.get_rand_voyelle(self)

    if not randint(0, 9):

        self.content += Word.get_rand_letter([Word.glides])

    if self.content in self.stored_words:

      if rec == 0:

        print("It seems there's not much options left ..")

        self.content = "$"

      else:

        Word.set_rand_word(self, rec-1)

  def get_rand_letter(listes, len_liste=0, index=-1):

    if index == -1:

      if len_liste == 0:

        for liste in listes:
       
          len_liste += len(liste)

        index = randint(0, len_liste-1)

    compteur = 0
 
    while index >= len(listes[compteur]):
   
      index -= len(listes[compteur])

      compteur += 1

    return listes[compteur][index]

  def get_rand_consonne(self):

    rand_index = randint(0, Word.nbr_consonnes-1)
 
    return Word.get_rand_letter(Word.consonnes, index=rand_index)

  def get_rand_voyelle(self):

    return Word.get_rand_letter([Word.voyelles])


stored_words = []

for x in range(100):

  word = Word(stored_words)

  word.set_rand_word()

  stored_words.append(word.content)

print(*stored_words)
