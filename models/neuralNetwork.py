import pickle
from keras.models import Model
from keras.layers import Dense, Input

# Load in data
X = []
with open('../data/emojis.pickle', 'rb') as file:
    X = pickle.load(file)

Y = []
with open('../data/atmosphere.pickle', 'rb') as file:
    Y = pickle.load(file)

split = int(len(X) * .75)
xTrain = X[:split]
xTest = X[split:]
yTrain = Y[:split]
yTest = Y[split:]

input = Input(shape=(74,))
dense = Dense(10, activation='relu')(input)
output = Dense(1)(dense)

model = Model(inputs=input, outputs=output)

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.fit(xTrain, yTrain, epochs=100)

print(model.evaluate(xTest, yTest))