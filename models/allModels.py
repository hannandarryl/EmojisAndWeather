import pickle
from keras.models import Model
from keras.layers import Dense, Input
from sklearn import mixture, tree
from sklearn.naive_bayes import GaussianNB

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

input = Input(shape=(75,))
dense = Dense(50, activation='relu')(input)
output = Dense(1)(dense)

model = Model(inputs=input, outputs=output)

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

print('Running Neural Network...........')

model.fit(xTrain, yTrain, epochs=20, verbose=0)

print(model.evaluate(xTest, yTest))


print('Running GMM.........')
# Fit a Gaussian mixture with EM using five components
gmm = mixture.GaussianMixture(n_components=2, covariance_type='full').fit(xTrain)

gmmResults = gmm.predict(xTest)

gmmCount = 0

for i in range(len(gmmResults)):
    if gmmResults[i] == yTest[i]:
        gmmCount += 1

gmmAccuracy = gmmCount / len(gmmResults)

print(gmmAccuracy)


print('Running Decision Tree.........')

tree = tree.DecisionTreeClassifier().fit(xTrain, yTrain)

treeResults = tree.predict(xTest)

treeCount = 0

for i in range(len(treeResults)):
    if treeResults[i] == yTest[i]:
        treeCount += 1

treeAccuracy = treeCount / len(treeResults)

print(treeAccuracy)


print('Running Naive Bayes.........')

bayes = GaussianNB().fit(xTrain, yTrain)

bayesResults = bayes.predict(xTest)

bayesCount = 0

for i in range(len(bayesResults)):
    if bayesResults[i] == yTest[i]:
        bayesCount += 1

bayesAccuracy = bayesCount / len(bayesResults)

print(bayesAccuracy)