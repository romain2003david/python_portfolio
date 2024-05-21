from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
from pig_tv import *


class ImageTreatment:
    def __init__(self, path):

        img = Image.open(path)
        img_np = np.asarray(img)
        shape = img_np.shape[:2]
        div_fact = 3
        img = img.resize((shape[0]//div_fact, shape[1]//div_fact))
        self.image = np.asarray(img)
        self.image_bw = np.zeros(self.image.shape[:2])
        self.image_bw = np.mean(self.image, axis=2)
        self.shape = self.image.shape[:2]
        
        self.line_field = np.zeros(list(self.image.shape[:2])+[2])  # defines line at each point
        self.line_field_defined = False
    
    def show_bw(self):
        plt.imshow(255-self.image_bw, cmap="Greys", interpolation='nearest')
        plt.show()
    
    def line_field_pt(self, x, y):
        angle, norme, pi = 0, 0, np.pi
        val = self.image_bw[y-1, x-1]
        
        diff1 = abs(self.image_bw[y-1, x-1]-val)+abs(self.image_bw[y+1, x+1]-val)# between 0 and 255*2  # 3pi/4
        diff2 = abs(self.image_bw[y+1, x-1]-val)+abs(self.image_bw[y-1, x+1]-val)  # pi/4
        diff3 = abs(self.image_bw[y, x-1]-val)+abs(self.image_bw[y, x+1]-val)  # 0
        diff4 = abs(self.image_bw[y-1, x]-val)+abs(self.image_bw[y+1, x]-val)  # pi/2
        diffs = [diff1, diff2, diff3, diff4]
        
        factors = [1/(diff+0.1) for diff in diffs]
        total = sum(factors)
        
        angles = [3*pi/4, pi/4, 0, pi/2]
        for i in range(4):
            angle += angles[i]*factors[i]/total
        
        smallest_diff = min(diffs)
        diffs.remove(smallest_diff)
        scd_smallest_diff = min(diffs)
        direction_variance = scd_smallest_diff-smallest_diff  # between 2*255 and 0
        #if direction_variance 
        norme = min(5, (1/(smallest_diff+1))*(direction_variance))
        return norme, angle

    def define_line_field(self):
        if self.line_field_defined:
            return 
        self.line_field_defined = True

        normalizer = 5
        for y in range(1, self.shape[0]-1):
            print(y)
            for x in range(1, self.shape[1]-1):
                norme, angle = self.line_field_pt(x, y)
                self.line_field[y, x] = [normalizer*norme*np.cos(angle), normalizer*norme*np.sin(angle)]
    
    def display_line_field(self):
        self.define_line_field()
        screen.fill(WHITE)

        for y in range(1, self.shape[0]-1):
            for x in range(1, self.shape[1]-1):
                if not random.randint(0, 10):
                    middle = np.array([x, y])
                    vect = self.line_field[y, x]
                    pygame.draw.line(screen, BLACK, middle-vect/2, middle+vect/2)
        pygame.display.update()
        wait()
    
    def display_stippled_img(self):
        #grey_level = sum(self.image_bw.flatten())  # between 0 and 255
        #proba_white = grey_level/255
        screen.fill(WHITE)
        for y in range(self.shape[0]):
            for x in range(self.shape[1]):
                val = self.image_bw[y, x]
                if val/255<random.random():
                    if not random.randint(0, 1):
                        pygame.draw.circle(screen, BLACK, [x, y], 1)
        pygame.display.update()
        wait()
    
    def display_stippled_line_field(self):
        self.define_line_field()
        screen.fill(WHITE)
        for y in range(1, self.shape[0]-1):
            for x in range(1, self.shape[1]-1):
                val = self.image_bw[y, x]
                if val/255<random.random():
                    if not random.randint(0, 1):
                        middle = np.array([x, y])
                        vect = self.line_field[y, x]
                        pygame.draw.line(screen, BLACK, middle-vect/2, middle+vect/2)
                        #pygame.draw.circle(screen, BLACK, [x, y], 1)
        pygame.display.update()
        wait()   
        


image = ImageTreatment("Downloads/python_portfolio/pictures/avion.jpg")
#image.show_bw()
image.display_stippled_line_field()
#image.display_line_field()
#image.display_stippled_img()