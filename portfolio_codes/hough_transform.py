import numpy as np
#from PIL import Image
import matplotlib.pyplot as plt
import scipy



def densite_gauss2D(i, j, sigma):
    """ centree """
    return np.exp(-(i**2+j**2)/(2*sigma))


def diagr_values(img):
    pixel_nb = img.shape[0]*img.shape[1]
    fimg = img.reshape(pixel_nb, 3)
    
    fimg_avg = np.mean(img, axis=0)
    print(fimg_avg.shape)
    print(fimg.shape)
    plt.bar(range(pixel_nb), fimg_avg)
    plt.show()


def show_imgs(imgs):
    n = len(imgs)
    f, axarr = plt.subplots(1, n, figsize=(15, 15))
    for i in range(n):
        min, max = np.min(imgs[i]), np.min(imgs[i])
        axarr[i].imshow(imgs[i], vmin=min, vmax=max)
    plt.show()


class Filtre:
    
    def __init__(self, filtre):
        
        self.filter = filtre
    
    def convolve_rgb(self, img):
        r_data = img[:,:,0]
        g_data = img[:,:,1]
        b_data = img[:,:,2]

        r = scipy.signal.convolve(r_data, self.filter, mode="same")
        g = scipy.signal.convolve(g_data, self.filter, mode="same")
        b = scipy.signal.convolve(b_data, self.filter, mode="same")

        filtered_img = np.zeros(img.shape)
        filtered_img[:,:,0] = r
        filtered_img[:,:,1] = g
        filtered_img[:,:,2] = b
        
        return filtered_img.astype(np.int32)

class FiltreGaussien(Filtre):
    
    def __init__(self, taille_convolute=9):
        
        self.taille_convolute = taille_convolute
        self.taille_filtre = 2*taille_convolute+1
        self.sigma_gauss = 10#1.4  # taille_convolute/np.sqrt(-2*np.log(eps))
    
        filtre = np.array([[densite_gauss2D(i, j, self.sigma_gauss) for j in range(-taille_convolute, taille_convolute+1)] for i in range(-taille_convolute, taille_convolute+1)])
        filtre /= sum(filtre.flatten())  # normalisation : dont loose avg color
        super().__init__(filtre)

class FiltrageSobel:
    
    def __init__(self, img):
        
        assert(type(img) in [np.array, np.ndarray])
        
        self.img = img
        self.horizontal_filter = Filtre(np.array([[-1, -2, -1], [0, 0, 0], [-1, -2, -1]]))
        self.vertical_filter = Filtre(np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]))
        self.contours_horizontaux = self.horizontal_filter.convolve_rgb(self.img)
        self.contours_verticaux = self.vertical_filter.convolve_rgb(self.img)
        self.abs_gradient = np.sqrt(np.multiply(self.contours_verticaux, self.contours_verticaux)+np.multiply(self.contours_horizontaux, self.contours_horizontaux))
        diagr_values(self.contours_horizontaux)
        diagr_values(self.abs_gradient)
        show_imgs([self.contours_horizontaux, self.contours_verticaux, self.abs_gradient])


class Image:
    
    def __init__(self, path):
        self.path = path
        self.data = plt.imread(path)
        self.bw_data = np.mean(self.data, axis=2)
        
        self.r_data = self.data[:,:,0]
        self.g_data = self.data[:,:,1]
        self.b_data = self.data[:,:,2]
    
    def apply_gauss_filter(self):

        filtre = FiltreGaussien()
        return filtre.convolve_rgb(self.data)
    
    def show(self, img):
        f, axarr = plt.subplots(1,3, figsize=(15, 15))
        axarr[0].imshow(self.data)
        axarr[1].imshow(abs(img))
        axarr[2].imshow(abs(img-self.data))
        #plt.imshow(self.data)# ,cmap='gray',vmin=0,vmax=255)
        plt.show()

    
    def save(self, path=None):
        if path == None:
            path = self.path
        plt.imsave(path, self.data)


a=np
img1 = Image("Downloads/python_portfolio/pictures/avion.jpg")
#img_gauss = img1.apply_gauss_filter()
FiltrageSobel(img1.data)#_gauss)