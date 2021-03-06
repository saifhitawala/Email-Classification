import os
import platform
import csv
import random
import math
import operator
import matplotlib.pyplot as plt

def loadDataset(current_path, filename, split, trainingSet=[] , testSet=[]):
	with open(current_path + filename, 'r') as csvfile:
		lines = csv.reader(csvfile)
		dataset = list(lines)
		for x in range(len(dataset)):
			for y in range(len(dataset[x])):
				dataset[x][y] = float(dataset[x][y])
			if random.random() < split:
				trainingSet.append(dataset[x])
			else:
				testSet.append(dataset[x])

def euclideanDistance(instance1, instance2, length):
	distance = 0
	for x in range(length):
		distance += pow((instance1[x] - instance2[x]), 2)
	return math.sqrt(distance)

def getNeighbors(trainingSet, testInstance, maxk):
	distances = []
	length = len(testInstance)-1
	for x in range(len(trainingSet)):
		dist = euclideanDistance(testInstance, trainingSet[x], length)
		distances.append((trainingSet[x][-1], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(maxk):
		neighbors.append(distances[x][0])
	return neighbors

def getResponse(neighbors, k):
	classVotes = {}
	for x in range(k):
		response = neighbors[x]
		if response in classVotes:
			classVotes[response] += 1
		else:
			classVotes[response] = 1
	sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
	# print(sortedVotes)
	return sortedVotes[0][0]

def getAccuracy(testSet, predictions):
	correct = 0
	for x in range(len(testSet)):
		if testSet[x][-1] == predictions[x]:
			correct += 1
	return (correct/float(len(testSet))) * 100.0

def classify(klist, trainingSet, testSet, path):
	list_of_predictions = []
	print('Completed 0.00%', end = '\r')
	for x in range(len(testSet)):
		predictions = []
		neighbors = getNeighbors(trainingSet, testSet[x], klist[-1])
		for k in klist:
			result = getResponse(neighbors, k)
			predictions.append(result)
		list_of_predictions.append(predictions)
		completed = (x+1)*100/len(testSet)
		print('Completed {0:.2f}%'.format(completed), end = '\r')
		#print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
	print('Completed 100.00%')

	for i in range(len(klist)):
		outfile = open(path + "predicted_class_"+str(klist[i])+".csv",'w') # open file for appending
		for x in range(len(testSet)):	
			outfile.write(str(list_of_predictions[x][i])+"\n")

	return list_of_predictions
	
def main(dataset_name):
	klist = [1, 3, 7, 15, 25, 33, 41, 49]
	# klist = [1, 3]
	acc = []
	ks = []
	trainingSet = []
	testSet=[]
	split = 0.67
	if platform.system() == 'Windows':
		current_path = os.path.dirname(os.path.abspath(__file__)) + "\\"
		dataset_path = current_path + dataset_name + "\\"
		results_path = dataset_path + "results\\"
	elif platform.system() == 'Linux':
		current_path = os.path.dirname(os.path.abspath(__file__)) + "/"
		dataset_path = current_path + dataset_name + "/"
		results_path = dataset_path + "results/"

	if not os.path.exists(results_path):
		os.mkdir(results_path)

	print("Loading Dataset...")
	loadDataset(dataset_path, 'mergedworkfile.csv', split, trainingSet, testSet)
	print ('Train set length: ' + repr(len(trainingSet)))
	print ('Test set length: ' + repr(len(testSet)))
	
	list_of_predictions = classify(klist, trainingSet, testSet, results_path)
		
	for i in range(len(klist)):
		predictions = []
		for x in range(len(testSet)):	
			predictions.append(list_of_predictions[x][i])
		accuracy = getAccuracy(testSet, predictions)
		acc.append(accuracy)
		ks.append(klist[i])
		print('K: ' + repr(klist[i]))
		print('Accuracy: ' + repr(accuracy) + '%')

	print('Overall Accuracy: '+ str(sum(acc)/len(acc)) + "%")
	plt.plot(ks, acc)
	plt.xlabel('K')
	plt.ylabel('Accuracy')
	plt.show()
	
	print('Find the results at: ' + results_path)

if __name__ == '__main__':
	main("dataset")
