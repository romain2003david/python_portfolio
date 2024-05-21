import scipy.signal as scp

# lire u
print("Entrer l'indice du premier terme de la suite u: ", end='')
offsetu = int(input())

print("Entrer les valeurs de la suite sur une ligne: ", end='')
u = list(map(int, input().split()))

for i, e in enumerate(u):
    print("u({})={} ".format(i + offsetu, e), end='')
print()

# lire v
print("Entrer l'indice du premier terme de la suite v: ", end='')
offsetv = int(input())

print("Entrer les valeurs de la suite sur une ligne: ", end='')
v = list(map(int, input().split()))

for i, e in enumerate(v):
    print("v({})={} ".format(i + offsetu, e), end='')
print()

# compléter u et v par des 0
a = len(u)
b = len(v)

if offsetv < offsetu:
    u = [0] * (offsetu - offsetv) + u
    a += offsetu - offsetv
    offsetu = offsetv
elif offsetu < offsetv:
    v = [0] * (offsetv - offsetu) + v
    b += offsetv - offsetu
    offsetv = offsetu

if a < b:
    u = u + [0] * (b - a)
    a = b
elif b < a:
    v = v + [0] * (a - b)
    b = a

# afficher w
print(scp.convolve(u, v))
