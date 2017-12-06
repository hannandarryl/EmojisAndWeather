import pickle
from keras.models import Model
from keras.layers import Dense, Input
from sklearn import mixture, tree
from sklearn.naive_bayes import GaussianNB
from random import shuffle
import matplotlib.pyplot as plt
import numpy as np
from keras.utils import plot_model
import graphviz

def makeVector(yValue):
    vector = [0,0,0,0,0,0,0,0]
    vector[yValue] = 1

    return vector

# Load in data
X = []
with open('../data/emojis.pickle', 'rb') as file:
    X = pickle.load(file)

Y = []
with open('../data/atmosphere.pickle', 'rb') as file:
    Y = pickle.load(file)

neuralNetAcc = []
gmmAcc = []
decisionTreeAcc = []
naiveBayesAcc = []
mostCommonAcc = []

for loop in range(10):
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
    yTrainNN = [makeVector(i) for i in yTrain]
    yTestNN = [makeVector(i) for i in yTest]

    # Define the structure of the neural network
    input = Input(shape=(75,))
    dense = Dense(20, activation='relu')(input)
    output = Dense(8, activation='softmax')(dense)

    model = Model(inputs=input, outputs=output)

    # Compile the model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    print('Running Neural Network...........')

    # Fit to data
    model.fit(xTrain, yTrainNN, epochs=20, verbose=0)

    # Evaluate neural network
    neuralNetAcc.append(model.evaluate(xTest, yTestNN, verbose=0)[1])

    # classTests = [[],[],[],[],[],[],[],[]]
    #
    # for i in range(len(xTest)):
    #     classTests[yTest[i]].append(xTest[i])
    #
    # for i in range(len(classTests)):
    #     print('On ' + str(i) + '.......')
    #     if len(classTests[i]) < 1:
    #         continue
    #     print(model.evaluate(classTests[i], [makeVector(i) for test in classTests[i]], verbose=0)[1])

    # Build Gaussian Mixture Model
    print('Running GMM.........')

    # Fit GMM to the data
    gmm = mixture.GaussianMixture(n_components=8, covariance_type='full').fit(xTrain)

    # Evaluate the GMM
    gmmResults = gmm.predict(xTest)

    # Calculate accuracy based on correctly predicted values
    gmmCount = 0

    for i in range(len(gmmResults)):
        if gmmResults[i] == yTest[i]:
            gmmCount += 1

    gmmAccuracy = gmmCount / len(gmmResults)

    gmmAcc.append(gmmAccuracy)

    # Build the Decision Tree
    print('Running Decision Tree.........')

    # Fit tree to data
    theTree = tree.DecisionTreeClassifier().fit(xTrain, yTrain)

    # Predict values using tree
    treeResults = theTree.predict(xTest)

    # Calculate accuracy of tree
    treeCount = 0

    for i in range(len(treeResults)):
        if treeResults[i] == yTest[i]:
            treeCount += 1

    treeAccuracy = treeCount / len(treeResults)

    decisionTreeAcc.append(treeAccuracy)

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

    naiveBayesAcc.append(bayesAccuracy)

    # Always select most common answer
    print('Most common answer classifier........')

    # Find most common answer
    counts = [0,0,0,0,0,0,0,0]
    for num in yTrain:
        counts[num] += 1

    maxVal = 0
    mostCommon = 0
    for num in range(len(counts)):
        if counts[num] > maxVal:
            maxVal = counts[num]
            mostCommon = num

    # Calculate NB accuracy
    totalCount = 0

    for i in range(len(yTest)):
        if mostCommon == yTest[i]:
            totalCount += 1

    totalAccuracy = totalCount / len(yTest)

    mostCommonAcc.append(totalAccuracy)

# plot_model(model, to_file='model.jpg')

# dot_data = tree.export_graphviz(theTree, out_file=None)
# graph = graphviz.Source(dot_data)
# graph.render("tree.png")

print('Neural Net Average Accuracy: ' + str(np.mean(neuralNetAcc)))
print('Gaussian Mixture Average Accuracy: ' + str(np.mean(gmmAcc)))
print('Decision Tree Average Accuracy: ' + str(np.mean(decisionTreeAcc)))
print('Naive Bayes Average Accuracy: ' + str(np.mean(naiveBayesAcc)))
print('Most Common Average Accuracy: ' + str(np.mean(mostCommonAcc)))

plt.plot(neuralNetAcc, label='ANN')
plt.plot(gmmAcc, label='GMM')
plt.plot(decisionTreeAcc, label='Decision Tree')
plt.plot(naiveBayesAcc, label='Naive Bayes')
plt.plot(mostCommonAcc, label='Most Common')

#plt.legend(loc=3)

plt.show()