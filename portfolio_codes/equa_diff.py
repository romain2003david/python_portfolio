import matplotlib.pyplot as plt

import numpy as np

import scipy.integrate as sci

def euler(f_comp, y0, a, b, n=10000):

    ys = np.zeros([n, len(y0)])

    ys[0] = np.array(y0)

    width = (b-a)/n

    # computes next point thanks to current one

    for x in range(n-1):

        t = a + x*width

        ys[x+1] = ys[x] + f_comp(ys[x], t)*width

        #print(ys[x], t, f_comp(ys[x], t))

    return ys


def euler_pts(f_comp, y0, xs):

    ys = np.zeros([n, len(y0)])

    ys[0] = np.array(y0)

    for c in range(1, len(xs)):

        x = xs[c]

        width = x-xs[c-1]

        next_y = ys[c-1] + width*f_comp(ys[c-1], x)

        ys[c] = next_y

    return ys

        
#### exo 1
##
##def f_exo1(V, t):
##
##    return -V[0]**2
##
##
##a = 1
##
##b = 10
##
##n = 100
##
##y0 = [[1]]
##
##width = (b-a)/n
##
##xs = [x*width+a for x in range(n)]
##
##ys = euler(f_exo1, y0, a, b, n)
##
##error = [1/(a+width*x)-ys[x] for x in range(n)]
##
##plt.plot(xs, ys)
##
##plt.show()
##
##
##
## exo 2
##
## Partie A
##
##def f_exo2A(v, t):
##
##    return (.5)/80*1.2*0.45*.8*v[0]**2-9.18
##
##
##a = 0
##
##b = 300
##
##n = 1000
##
##y0 = [[0]]
##
##width = (b-a)/n
##
##xs = [x*width+a for x in range(n)]
##
##ys = euler(f_exo2A, y0, a, b, n)
##
####plt.plot(xs, ys)
####
####plt.show()
##
##
##def z_(V, t):
##
##    t = int(t/(b/1000))
##
##    return ys[t]
##
##zs = euler(z_, [39068], 0, 300, n)
##
##plt.plot(xs, zs)
##
##plt.show()
##
## Partie B
##
##def f_exo2A(v, t):
##
##    return np.array([(.5)/80*1.2*np.exp(-v[1]/7700)*0.45*.8*v[0]**2-9.18, v[0]])
##
##
##a = 0
##
##b = 300
##
##n = 1000
##
##v0, z0 = 0, 39068
##
##y0 = [v0, z0]
##
##width = (b-a)/n
##
##xs = [x*width+a for x in range(n)]
##
##ys = euler(f_exo2A, y0, a, b, n)
##
##plt.plot(xs, ys[:,0])
##
##plt.show()

#### exo 3
##
##def f_rc(Y, t):
##
##    return (uet - Y[0])/RC
##
##
##RC = 10**(-3)
##
##uet = 10
##
##y0 = [0]
##
##a = 0
##
##b = 15*RC
##
##n = 1000
##
##width = (b-a)/n
##
##xs = [x*width+a for x in range(n)]
##
##ys = euler_pts(f_rc, y0, xs)
##
##plt.plot(xs, ys[:,0])
##
##ys_od = sci.odeint(f_rc, y0, xs)
##
##plt.plot(xs, ys[:,0])
##
##plt.show()
##
##ecart = [ys_od[x] - ys[x] for x in range(len(xs))]
##
##plt.plot(xs, ecart)
##
##plt.show()


# exo 4

def f_lievlynx(Y, t):

    lievre, lynx = Y

    vect = [fact1*lievre-fact2*lievre*lynx, -fact3*lynx+fact4*lievre*lynx]

    return np.array(vect)


fact1 = 1.5

fact2 = 0.05

fact3 = 0.48

fact4 = 0.05
#

lynxs = [10, 15, 30, 40]


a = 0

b = 50

y0 = np.array([4, lynxs[0]])

n = 100

width = (b-a)/n

xs = [x*width+a for x in range(n)]

ys = euler_pts(f_lievlynx, y0, xs)

plt.plot(xs, ys)
    ##
    ##plt.show()

    #plt.plot(ys[:,0], ys[:,1])

plt.show()
