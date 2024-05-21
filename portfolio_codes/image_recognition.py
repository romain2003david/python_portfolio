from keras.models import load_model
import os
import pandas as pd
import numpy as np
import cv2
from keras.applications.inception_v3 import decode_predictions
from keras.applications.inception_v3 import InceptionV3
from keras.layers import Flatten,Dense,Activation
from tensorflow.keras.models import Model
from keras.applications.imagenet_utils import decode_predictions
from keras.applications.inception_v3 import preprocess_input
import tensorflow as tf
from keras.preprocessing import image
#from google.colab import drive
from keras.models import load_model

drive.mount('/content/drive')

##Path_train = "/content/drive/MyDrive/PACT/training_final"
##categories = [x for x in os.listdir(Path_train)]
##categories.sort()
categories = ['CANARD', 'CORBEAU', 'CYGNE', 'DINDE', 'ETOURNEAU', 'GRIVE', 'HERON', 'MERLE', 'MESANGE', 'MOINEAU', 'PAON', 'PIE', 'PIGEON', 'POULE', 'ROUGE-GORGE', 'TOURTERELLE']


gloabl_img_bot = InceptionV3(include_top=True ,input_shape=(299,299,3),weights='imagenet')
model_pas_retouch = Model(inputs=gloabl_img_bot.input,outputs=gloabl_img_bot.output)

# load the saved model
model = load_model("modelSaveFinal")

"""# True prediction: Test on unknown images """

def get_labels():

    labels = ['black Grouse', 
          'ptarmigan', 
          'ruffed Grouse', 
          'prairie Chicken', 
          'peacock', 
          'quail', 
          'partridge', 
          'african Grey Parrot', 
          'macaw', 
          'sulphur-Crested Cockatoo', 
          'lorikeet', 
          'coucal', 
          'bee Eater', 
          'hornbill', 
          'hummingbird', 
          'jacamar', 
          'toucan', 
          'drake', 
          'red-Breasted Merganser', 
          'boose', 
          'black Swan', 
          'cock', 
          'hen', 
          'ostrich', 'Struthio camelus', 
          'brambling', 'Fringilla montifringilla', 
          'goldfinch', 'Carduelis carduelis', 
          'house finch', 'linnet', 'Carpodacus mexicanus', 
          'junco', 'snowbird', 
          'indigo bunting', 'indigo finch', 'indigo bird', 'Passerina cyanea', 
          'robin', 'American robin', 'Turdus migratorius', 
          'bulbul', 
          'jay', 
          'magpie', 
          'chickadee', 
          'water ouzel', 'dipper', 
          'kite', 
          'bald eagle', 'American eagle', 'Haliaeetus leucocephalus', 
          'vulture', 
          'white stork', 
          'black stork', 
          'spoonbill', 
          'flamingo', 
          'little blue heron', 
          'american egret', 
          'bittern', 
          'crane', 
          'limpkin', 
          'european gallinule', 
          'american coot', 
          'bustard', 
          'ruddy turnstone', 
          'red-backed sandpiper', 
          'redshank', 
          'dowitcher', 
          'oystercatcher',
          'pelican',
          'king penguin',
          'albatross']
    # list of birds in imagenet
    labels2 = [word.lower() for word in labels]

    for word in labels2:

      labels2[labels2.index(word)] = word.replace(" ", "_")

    return labels2


def recog_img(filename):

  categories = ['CANARD', 'CORBEAU', 'CYGNE', 'DINDE', 'ETOURNEAU', 'GRIVE', 'HERON', 'MERLE', 'MESANGE', 'MOINEAU', 'PAON', 'PIE', 'PIGEON', 'POULE', 'ROUGE-GORGE', 'TOURTERELLE']
  # opens and resizes img

  img = cv2.resize(cv2.imread(filename), (299, 299)).astype(np.float32)
  img = np.expand_dims(img, axis=0)
  img = preprocess_input(img)

  # determines whether it is a bird or not 
  predictions_single = model_pas_retouch.predict(img)
  species = decode_predictions(predictions_single)

  guesses = [species[0][x][1] for x in range(2)]  
  
  def one_species_in_label(strs, liste_str):

    for str_ in strs:

      if (str_ in liste_str):

        return True
        
      
    return False

  if not (one_species_in_label(guesses, get_labels())):

    return "not bird"

  else: # determines which bird it is most probably

    img = cv2.resize(cv2.imread(filename), (224, 224)).astype(np.float32)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    
    predictions_single = model.predict(img) 
    #predictions_single.sort()
    
    index_guess = np.argmax(predictions_single)

    best_guess1 = categories[index_guess]

    return best_guess1#"filename : {}\n1) {}; 2) {}; 3) {};\n".format(filename, best_guess1, best_guess2, best_guess3)


