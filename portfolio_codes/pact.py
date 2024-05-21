from sklearn import datasets

from sklearn.neural_network import MLPClassifier



digits = datasets.load_digits()

print(digits.images[1])

print(digits.target[1])
print(dir(digits))
##
##import matplotlib.pyplot as plt
##plt.imshow(digits.images[1],cmap='binary')
##plt.title(digits.target[0])
##plt.axis('off')
##plt.show()

a
x = digits.images.reshape((len(digits.images), -1))

print(digits.target[1])


for c in [100, 200, 500, 1000, 1500]:
    mlp = MLPClassifier(hidden_layer_sizes=(20, 20, 10), max_iter=500)
    print(dir(mlp))

    x_train = x[:c]

    y_train = digits.target[:c]

    x_test = x[c:]

    y_test = digits.target[c:]

    mlp.fit(x_train, y_train)

    guess = mlp.predict(x_test)

    print(sum([guess[x] != y_test[x] for x in range(len(guess))]) /(1787-c))
