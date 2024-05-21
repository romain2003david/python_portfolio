import math
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf

def fourier(k,N):
    base_fourrier= [1/math.sqrt(N) *(math.cos(2*math.pi*k/N*i) +1j*math.sin(2*math.pi*k*i/N)) for i in range(N)]
    return(base_fourrier)

def create_E(N):
    E=[]
    for k in range(N):
        E.append(fourier(k,N))
    E=np.array(E)
    return(E)


def tfd(x):
    N=len(x)
    E= create_E(N).transpose()
    res = E.dot(x)
    return [np.linalg.norm(res[x]) for x in range(len(res))]


def dessin_base(coordonnee):
    ns = [n for n in range(len(coordonnee))]

    ys = [coordonnee[n] for n in ns]
    plt.scatter(ns, ys)
    plt.show()

def generate_sinusoidal_signal(f, Fe, duration,noise_variance):
    time_array = np.linspace(0, duration, int(Fe*duration), endpoint=False)
    signal = np.sin(2*np.pi*f*time_array)
    noise = np.random.normal(0, np.sqrt(noise_variance), signal.shape)
    noisy_signal = signal + noise
    return noisy_signal


def solve(f):
    Fe=5*f
    nb_perdiode = 50
    x= generate_sinusoidal_signal(f,Fe,nb_perdiode/f,1) # création du tableau de valeurs sin de fréquence f
    
    estime_freq(x,Fe)


def signal_sursampled(x):

    nb_pt = len(x)

    y = [(x[i]+x[i+1])/2 for i in range(nb_pt-1)]

    y.append(x[-1])

    res = []

    for i in range(nb_pt):

        res.extend([x[i], y[i]])

    return res


def get_freq_fourrier(x, f, Fe):

    #facteur = 5

    return np.abs(sum([x[k]*np.exp(2j*np.pi*f*k/Fe) for k in range(len(x))]))
def get_freq_fourrier_cmplx(x, f, Fe):

    #facteur = 5

    return sum([x[k]*np.exp(2j*np.pi*f*k/Fe) for k in range(len(x))])


def hadamard(x, y):

    return [x[i]*y[i] for i in range(len(x))]


def tf_inverse_eval(liste_freq, i):

    Fe = 1

    #print(i)

    return np.abs(sum([liste_freq[k]*np.exp(-2j*np.pi*i*k/Fe) for k in range(len(liste_freq))]))

def tf_inverse(liste_freq):

    return [tf_inverse_eval(liste_freq, i) for i in range(len(liste_freq))]

def substract(x, y):

    return [x[i]-y[i] for i in range(len(x))]

def threshold_filter(x,threshold):
    for i in range(len(x)):
        if(x[i]<threshold):
            x[i]=0
    return x


def estime_freq2(x, Fe):

    test = 0

    #dessin_base(x)
    
    freqs = np.fft.fft(x)

    #print(*[(y, list(freqs).index(y)) for y in freqs if np.abs(y) > 1], len(freqs))
          

    #freqs_bruits_bas = [get_freq_fourrier_cmplx(x, 5+i, Fe) for i in range(490)] # 495

    #freqs_bruits_haut = [get_freq_fourrier(x, 530+i, Fe) for i in range(200)]  # 200
    
    freqs_bruits_completees = np.concatenate([[0 for j in range(6)],freqs[6:485],[0 for j in range(55)],freqs[540:len(x)]])
    #print(*[(freqs_bruits_completees[i], i) for i in range(len(freqs_bruits_completees)) if np.abs(freqs_bruits_completees[i]) < 1], len(freqs_bruits_completees))

    if test:
        
        print("freq du bas calculées")

    signal_freq_bruit = np.fft.ifft(freqs_bruits_completees)  # tf_inverse(freqs_bruits_completees)



    if test:

        print("freq inverse calculée")

    x_processed= substract(x, signal_freq_bruit)

    #dessin_base(signal_freq_bruit)
    #dessin_base(x_processed)
    
    
    x_fi= x_processed

    
    freqs = np.fft.fft(x_fi)

    return [np.abs(x) for x in freqs[501:527]]

    print(*[(y, list(freqs).index(y)) for y in freqs if np.abs(y) > 20], len(freqs))
     


    if test:
        
        print("sub ok")
    
    x2=x_fi
    x2 = hadamard(x_fi, np.kaiser(len(x_processed),0.75))

    x2= np.concatenate([x2,np.zeros(int(50*Fe-len(x2)))])
    freq_temp=np.abs(np.fft.fft(x2))
    freqs=[]

    k=500.5*len(freq_temp)/Fe
    f=500.5
    for i in range(26):
        temp=[]
        while(f<501.5+i):
            temp.append(freq_temp[int(k)])
            k+=1
            f+=Fe/len(freq_temp)
        freqs.append(sum(temp)/len(temp))
    
   

   

    #if test:
        
    #print(freqs)

    return freqs


def estime_freq(x, Fe):
    
    N = len(x)  # nombre d'échantillons
    tfd_result = np.abs(tfd(x))  # application de la transformée de Fourier discrète
    #
    # dessin_base(tfd_result)
    freq_step = Fe/N  # pas de fréquence
    index_max = np.argmax(tfd_result[:N//2])  # indice de la plus grande valeur dans la première moitié de la transformée de Fourier
    freq_estimee = index_max *freq_step # estimation de la fréquence à partir de la transformée de Fourier
    print("La fréquence estimée est : ", abs(freq_estimee), "Hz")
    return(abs(freq_estimee))



def fenetre_hann(nb_pt):

    return [0.5-0.5*np.cos(2*np.pi*k/nb_pt) for k in range(nb_pt)]

def fenetre_haming(nb_pt):

    return [0.54-0.46*np.cos(2*np.pi*k/nb_pt) for k in range(nb_pt)]

def fenetre_blackman(nb_pt):
     return [0.42-0.5*np.cos(2*np.pi*k/nb_pt)+0.08*np.cos(4*np.pi*k/nb_pt) for k in range(nb_pt)]


def decode_freq(frequence):

    #frequence -= 500
    # return chr(97 + round(frequence))
    return list(map(chr, range(97, 123)))[int(frequence)]



def decode(signal):
    nb_pt = len(signal)
    nb_pt_symbole= 2000
    nb_symbole = nb_pt/(nb_pt_symbole+nb_pt_symbole)
    #print(nb_symbole)

    #signaux = [signal[i*(nb_pt_symbole+nb_pt_inter):(i+1)*nb_pt_symbole+i*nb_pt_inter] for i in range(nb_symbole)]
    #frequences_detectees = [solvebis(signaux[x], Fe) for x in range(nb_symbole)]
    debut_symbole=0

    phrase = ""
    while(debut_symbole+nb_pt_symbole<=nb_pt):
        signal_symbol=signal[debut_symbole:debut_symbole+nb_pt_symbole]
        
        debut_symbole+=2500
        #print(estime_freq2(signal_symbol, 8000))
        Fe = 8000

        #signal_sursampl = signal_sursampled(signal_symbol)
        #Fe = 2*Fe

        gotten_ampli_freq = estime_freq2(signal_symbol,Fe)

        X=[i for i in range(len(gotten_ampli_freq))]
        
        #plt.plot(X,gotten_ampli_freq)
        #plt.show()

        print(gotten_ampli_freq)

        max_ampli = max(gotten_ampli_freq)

        min_ampli = min(gotten_ampli_freq)

        delta = max_ampli-min_ampli

        print(delta)

        lettre = decode_freq(np.argmax(gotten_ampli_freq))

        if max_ampli > 10:

            phrase += lettre
            print(lettre)
        
        else:

            phrase += " "
            print("space")
        


        
    
    print(phrase)
    
    #signal_symbol=signal[0:2000]
    #solvebis(signal_symbol,Fe)
x,Fe = sf.read("mess.wav")
#Fe = 200
#div = 200
#depi = 2*np.pi
#x = np.array([np.sin(depi*2*(t/div))+np.sin(depi*1*(t/div)) for t in range(5000)])  # 

 
decode(x)






