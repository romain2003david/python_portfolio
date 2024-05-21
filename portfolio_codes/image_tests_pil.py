from pig_tv import *

import matplotlib.image as mpimg
import numpy as np

image_path = select_picture()

print(image_path+".png")

img = mpimg.imread(image_path)

