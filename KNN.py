'''
Python_version: 3.6.5
Author        : Perumal sk
Date created  : 19-oct-2018
Program desc  : Implementation of nearest neighbour for classification
'''

import math
import csv
import random
import numpy as np
import matplotlib.pyplot as plt


class nearest_neighbours_implementation:

    def __init__(self, file_name, k, split_size):
        self.k = int(k)
        self.split_size_upto_1 = float(split_size)  # your test set split in range of 0-1 ex., 0.29 or 0.55
        self.file_name = file_name  # please specify file name[iris.txt or ionosphere.txt]
        self.random_seed = 0
        self.training_set = []
        self.test_set = []
        self.predictions = []

    def main(self):
        self.load_from_csv()


        for i in range(len(self.test_set)):
            nearest_neighbours = self.obtain_all_neighbours(self.test_set[i])
            # print(nearest_nei0ghbours)
            # exit()
            found_label= self.identify_label(nearest_neighbours)
            self.predictions.append(found_label)
            # print('pred' ,found_label ,' originalll',self.test_set[i][-1])
        final_accuracy, error_rate = self.find_accuracy()
        print('Accuracy: ', final_accuracy, "Error rate: ", error_rate)
        return final_accuracy

    def obtain_all_neighbours(self, each_test):
        len_of_all_vals = len(each_test) - 1
        all_distances = []

        for i in range(len(self.training_set)):
            individual_distance = self.distance_via_eucledian(each_test, self.training_set[i], len_of_all_vals)
            all_distances.append((self.training_set[i], individual_distance))
        # print(all_distances)
        # exit()
        # Sort the distance in ascending order
        sorted_distances = []
        while all_distances:
            minimum = all_distances[0][1]
            value_to_be_modified = all_distances[0]
            find_position = 0
            for each_dis in all_distances:
                # print(each_dis[1],"each valueee",minimum)
                find_position += 1
                if each_dis[1] < minimum:
                    minimum = each_dis[1]
                    value_to_be_modified = each_dis
            # print(find_position)
            # print(distances[find_position],distances[find_position+1])
            sorted_distances.append(value_to_be_modified)
            all_distances.remove(value_to_be_modified)
        nearestneighbors = []
        for i in range(self.k):
            try:
                nearestneighbors.append(sorted_distances[i][0])
            except:
                pass
        # print(nearestneighbors,"dfdfdfd")
        return nearestneighbors

    def distance_via_eucledian(self, each_test, trainind_dist_value, total_test):
        dis = 0
        for i in range(total_test):
            dis += pow((float(each_test[i]) - float(trainind_dist_value[i])), 2)
            # print(i)
        euc_dis = math.sqrt(dis)
        return euc_dis

    def identify_label(self, near_neigh):
        label_dict = {}
        for i in range(len(near_neigh)):
            label = near_neigh[i][-1]
            # talking the label and checking for count, whilst creating a key in dict
            if label in label_dict:
                label_dict[label] += 1
            else:
                label_dict[label] = 1
        sorted_dict = []
        if self.k >= 3:
            # print(label_dict)
            while label_dict:
                minimum = next(iter(label_dict.values()))
                value_to_be_modified = next(iter(label_dict.keys()))
                for key, val in label_dict.items():
                    if val > minimum:
                        minimum = val
                        value_to_be_modified = key
                sorted_dict.append((value_to_be_modified, minimum))
                del label_dict[value_to_be_modified]
            # print(sorted_dict)
            # return only the nearest label value
            return sorted_dict[0][0]
        else:
            sorted_dict = []
            sorted_dict.append((next(iter(label_dict.keys())), next(iter(label_dict.values()))))
            # return only the nearest label value

            return sorted_dict[0][0]

    def load_from_csv(self):
        with open(self.file_name, 'r') as csvfile:
            all_lines_obj = csv.reader(csvfile, delimiter=',')
            all_lines = list(all_lines_obj)
            random.seed(self.random_seed)
            for row in range(len(all_lines)):
                for col in range(4):  # convert sample values to float excluding the last i.e., the labels
                    all_lines[row][col] = float(all_lines[row][col])
                if self.split_size_upto_1 <= random.random():
                    self.training_set.append(all_lines[row])
                else:
                    self.test_set.append(all_lines[row])
            # print(len(self.test_set),len(self.training_set))
            # print(self.test_set, self.training_set)

    def find_accuracy(self):
        right = 0
        error = []
        for i in range(len(self.test_set)):
            if self.predictions[i] == self.test_set[i][-1]:
                right += 1
                error.append(False)
            else:
                error.append(True)

        final_percentagee = right / len(self.test_set)
        error_percentage = 1 - final_percentagee

        return final_percentagee, error_percentage

knn_obj=nearest_neighbours_implementation('iris.txt',1,0.29)
accuracy=knn_obj.main()
