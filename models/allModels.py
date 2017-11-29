import pickle
from keras.models import Model
from keras.layers import Dense, Input
from sklearn import mixture, tree
from sklearn.naive_bayes import GaussianNB
from random import shuffle

# Load in data
X = []
with open('../data/emojis.pickle', 'rb') as file:
    X = pickle.load(file)

Y = []
with open('../data/atmosphere.pickle', 'rb') as file:
    Y = pickle.load(file)

# Randomize Data
combined = [(X[i], Y[i]) for i in range(len(X))]

shuffle(combined)

for i in range(len(combined)):
    X[i] = combined[i][0]
    Y[i] = combined[i][1]

# Separate training and test data
split = int(len(X) * .75)
xTrain = X[:split]
xTest = X[split:]
yTrain = Y[:split]
yTest = Y[split:]

# Need to have y values in different format for neural networks
yTrainNN = [[1,0] if i == 1 else [0,1] for i in yTrain]
yTestNN = [[1,0] if i == 1 else [0,1] for i in yTest]

# Define the structure of the neural network
input = Input(shape=(75,))
dense = Dense(50, activation='relu')(input)
output = Dense(2, activation='softmax')(dense)

model = Model(inputs=input, outputs=output)

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

print('Running Neural Network...........')

# Fit to data
model.fit(xTrain, yTrainNN, epochs=20, verbose=0)

# Evaluate neural network
print(model.evaluate(xTest, yTestNN, verbose=0)[1])

# Build Gaussian Mixture Model
print('Running GMM.........')

# Fit GMM to the data
gmm = mixture.GaussianMixture(n_components=2, covariance_type='full').fit(xTrain)

# Evaluate the GMM
gmmResults = gmm.predict(xTest)

# Calculate accuracy based on correctly predicted values
gmmCount = 0

for i in range(len(gmmResults)):
    if gmmResults[i] == yTest[i]:
        gmmCount += 1

gmmAccuracy = gmmCount / len(gmmResults)

print(gmmAccuracy)

# Build the Decision Tree
print('Running Decision Tree.........')

# Fit tree to data
tree = tree.DecisionTreeClassifier().fit(xTrain, yTrain)

# Predict values using tree
treeResults = tree.predict(xTest)

# Calculate accuracy of tree
treeCount = 0

for i in range(len(treeResults)):
    if treeResults[i] == yTest[i]:
        treeCount += 1

treeAccuracy = treeCount / len(treeResults)

print(treeAccuracy)

# Build Naive Bayes
print('Running Naive Bayes.........')

# Fit naive bayes to data
bayes = GaussianNB().fit(xTrain, yTrain)

# Predict values using NB
bayesResults = bayes.predict(xTest)

# Calculate NB accuracy
bayesCount = 0

for i in range(len(bayesResults)):
    if bayesResults[i] == yTest[i]:
        bayesCount += 1

bayesAccuracy = bayesCount / len(bayesResults)

print(bayesAccuracy)

# Always select most common answer
print('Most common answer classifier........')

# Find most common answer
numBad = len([1 for i in yTrain if i == 0])
numGood = len([1 for i in yTrain if i == 1])

mostCommon = 1
if numBad > numGood:
    mostCommon = 0

# Calculate NB accuracy
totalCount = 0

for i in range(len(yTest)):
    if mostCommon == yTest[i]:
        totalCount += 1

totalAccuracy = totalCount / len(yTest)

print(totalAccuracy)