from numpy import double
import numpy as np
from sklearn.model_selection import train_test_split
from Point import Point
from rule import rule

ListPoint = []
all_average = 0
# list of the best rules
best_rules_8 = {}
best_rules_7 = {}
best_rules_6 = {}
best_rules_5 = {}
best_rules_4 = {}
best_rules_3 = {}
best_rules_2 = {}
best_rules_1 = {}
p_train8 = []
p_train7 = []
p_train6 = []
p_train5 = []
p_train4 = []
p_train3 = []
p_train2 = []
p_train1 = []

p8 = []
p7 = []
p6 = []
p5 = []
p4 = []
p3 = []
p2 = []
p1 = []
epsilon = 0.0001
array_rules = []


def slope(x1, y1, x2, y2):
    if (x2 - x1) == 0:
        m = 0
    else:
        m = (y2 - y1) / (x2 - x1)
    return m

def findMidpoint(x1, y1, x2, y2):
    y = (y2 + y1) / 2
    x = (x2 + x1) / 2
    p = Point(x, y, 0)
    return p

# Normalize the points to reach the total weight of 1
def NormalizationWeight(weight, array_weight):
    for i_weight in range(len(array_weight)):
        array_weight[i_weight] = array_weight[i_weight] / weight


def get_min_alpha(best):
    min_alpha_index = 0
    for curr_index_rule in range(len(best)):
        if curr_index_rule != min_alpha_index and best.get(curr_index_rule).alpha < best.get(min_alpha_index).alpha:
            min_alpha_index = curr_index_rule
    return min_alpha_index

def clear_list():
    ListPoint.clear()
    # list of the best rules
    best_rules_8.clear()
    best_rules_7.clear()
    best_rules_6.clear()
    best_rules_5.clear()
    best_rules_4.clear()
    best_rules_3.clear()
    best_rules_2.clear()
    best_rules_1.clear()
    p_train8.clear()
    p_train7.clear()
    p_train6.clear()
    p_train5.clear()
    p_train4.clear()
    p_train3.clear()
    p_train2.clear()
    p_train1.clear()

    p8.clear()
    p7.clear()
    p6.clear()
    p5.clear()
    p4.clear()
    p3.clear()
    p2.clear()
    p1.clear()

    array_rules.clear()

# array of all points in the world
def print_rules():
    print("The average of 1 rule: Train: ", np.sum(p_train1)/5, "Test: ", np.sum(p1)/5)
    print("The average of 2 rule: Train: ", np.sum(p_train2)/5, "Test: ", np.sum(p2)/5)
    print("The average of 3 rule: Train: ", np.sum(p_train3)/5, "Test: ", np.sum(p3)/5)
    print("The average of 4 rule: Train: ", np.sum(p_train4)/5, "Test: ", np.sum(p4)/5)
    print("The average of 5 rule: Train: ", np.sum(p_train5)/5, "Test: ", np.sum(p5)/5)
    print("The average of 6 rule: Train: ", np.sum(p_train6)/5, "Test: ", np.sum(p6)/5)
    print("The average of 7 rule: Train: ", np.sum(p_train7)/5, "Test: ", np.sum(p7)/5)
    print("The average of 8 rule: Train: ", np.sum(p_train8)/5, "Test: ", np.sum(p8)/5)



def read_file(path, name_data):
    # read the data
    file = open(path, "r")
    # array of lines from data
    fileLines = file.readlines()
    # create points from data
    if name_data == "HC":
        for line in fileLines:
            line_split = line.split()
            ListPoint.append(Point(double(line_split[0]), double(line_split[2]), int(line_split[1])))
           # change the label to (-1, 1)
        for point_train in ListPoint:
            if point_train.label == 2:
                point_train.label = -1
    else:
         for line in fileLines:
            line_split = line.split(",")
            if line_split[4].startswith("Iris-ve"):
                ListPoint.append(Point(double(line_split[1]), double(line_split[2]), 1))
            elif line_split[4].startswith("Iris-vi"):
                ListPoint.append(Point(double(line_split[1]), double(line_split[2]), -1))

    for iii in range(5):
        print("iteration: ", iii)
        adaboost()
    print_rules()


def adaboost():

    # split the data to train and test
    train, test = train_test_split(ListPoint, test_size=0.5)
    # total of points
    n_samples = len(train)

    # init the weight to be 1/n
    array_weight = np.full(n_samples, (1 / n_samples))

    # prediction array
    predictions = np.zeros(n_samples)

    # all possible straight equations from two points (rules)
    for i in range(0, n_samples):
        j = i + 1
        for j in range(j, n_samples):
            # slope of equation
            slope_m = slope(train[i].x, train[i].y, train[j].x, train[j].y)
            # finding the midpoint
            midpoint = findMidpoint(train[i].x, train[i].y, train[j].x, train[j].y)
            if slope_m == 0:
                reverse_slope = 0
            else:
                reverse_slope = (-1 / slope_m)
            # b of equation
            b_reverse = ((-1 * reverse_slope) * midpoint.x) + midpoint.y
            #
            idx_predict = 0
            # error for this rule
            true_error = 0
            alpha = 0
            # check the rule on all the points
            for point in train:
                # check if the point is under the equation
                y = reverse_slope * point.x + b_reverse
                # check whether the point is above the line or below
                # if y > point.y -> the point is below the line
                if y > point.y:
                    predictions[idx_predict] = 1
                else:
                    # the point is above the line
                    predictions[idx_predict] = -1
                #  error on every point
                # print("---------> ", predictions[idx_predict] != point.label)
                mul = 1
                if predictions[idx_predict] == point.label:
                    mul = 0
                # print("-----> ", array_weight[idx_predict])
                error_point = np.multiply(array_weight[idx_predict], mul)
                # print("error Point: " ,error_point)
                # schema of all errors
                true_error = true_error + error_point
                idx_predict = idx_predict + 1
            # If the true error > 0.5 we want the opposite rule
            print("True Error: ", true_error)
            if true_error > 0.5:
                label = 1
                final_true_error = 1 - true_error
                # print("Final True Error: ", final_true_error, "True Error: ", true_error)
            else:
                label = -1
                final_true_error = true_error
            # weight of the rule
            # print("Final True Error: ", final_true_error, "True Error: ", true_error)
            alpha = np.multiply(0.5 , (np.log((1-final_true_error + epsilon) / (final_true_error + epsilon))))
            # insert to array of rules
            array_rules.append(rule(reverse_slope, b_reverse, alpha, label, final_true_error))
            # The weight of all the points (for normalization)
            all_points_weight = 0
            # changing the weights of the points according to the error
            for idx_weight in range(len(array_weight)):
                # calculates the new weight of the point -> e^(-alfa*h(x)*label(x))
                num = (-1 * alpha) * (predictions[idx_weight] * train[idx_weight].label)
                e_exponent = np.exp(num)
                weight_point = array_weight[idx_weight] * e_exponent
                # update the new weight
                array_weight[idx_weight] = weight_point
                # sum the weights of all points
            # normalize the points
            NormalizationWeight(all_points_weight,array_weight)

    best_one_rules(train, 1)
    best_two_rules(train, 1)
    best_three_rules(train, 1)
    best_four_rules(train, 1)
    best_five_rules(train, 1)
    best_six_rules(train, 1)
    best_seven_rules(train, 1)
    best_eight_rules(train, 1)

    best_one_rules(test,2)
    best_two_rules(test, 2)
    best_three_rules(test, 2)
    best_four_rules(test, 2)
    best_five_rules(test, 2)
    best_six_rules(test, 2)
    best_seven_rules(test, 2)
    best_eight_rules(test, 2)



def best_eight_rules(test, number):
    # initialize the list in the first 8 rules
    for idx_best_rules in range(8):
        best_rules_8[idx_best_rules] = array_rules[idx_best_rules]
    for idx_rule in range(len(array_rules)):
        min_alpha = get_min_alpha(best_rules_8)
        if array_rules[idx_rule].alpha > best_rules_8.get(min_alpha).alpha:
            best_rules_8[min_alpha] = array_rules[idx_rule]
        # max_error = get_max_error(best_rules)
        # if array_rules[idx_rule].trueError < best_rules.get(max_error).trueError:
        #     best_rules[max_error] = array_rules[idx_rule]
    predict_test = np.zeros(len(test))
    temp_sum = check_test(best_rules_8, predict_test,test)
    if number == 1:
        p_train8.append(temp_sum)
    else:
        p8.append(temp_sum)

def best_seven_rules(test, number):
    # initialize the list in the first 8 rules
    for idx_best_rules in range(7):
        best_rules_7[idx_best_rules] = array_rules[idx_best_rules]
    for idx_rule in range(len(array_rules)):
        min_alpha = get_min_alpha(best_rules_7)
        if array_rules[idx_rule].alpha > best_rules_7.get(min_alpha).alpha:
            best_rules_7[min_alpha] = array_rules[idx_rule]
        # max_error = get_max_error(best_rules)
        # if array_rules[idx_rule].trueError < best_rules.get(max_error).trueError:
        #     best_rules[max_error] = array_rules[idx_rule]
    predict_test = np.zeros(len(test))
    temp_sum = check_test(best_rules_7, predict_test,test)
    if number == 1:
        p_train7.append(temp_sum)
    else:
        p7.append(temp_sum)

def best_six_rules(test, number):
    # initialize the list in the first 8 rules
    for idx_best_rules in range(6):
        best_rules_6[idx_best_rules] = array_rules[idx_best_rules]
    for idx_rule in range(len(array_rules)):
        min_alpha = get_min_alpha(best_rules_6)
        if array_rules[idx_rule].alpha > best_rules_6.get(min_alpha).alpha:
            best_rules_6[min_alpha] = array_rules[idx_rule]
    predict_test = np.zeros(len(test))
    temp_sum = check_test(best_rules_6, predict_test,test)
    if number == 1:
        p_train6.append(temp_sum)
    else:
        p6.append(temp_sum)

def best_five_rules(test, number):
    # initialize the list in the first 8 rules
    for idx_best_rules in range(5):
        best_rules_5[idx_best_rules] = array_rules[idx_best_rules]
    for idx_rule in range(len(array_rules)):
        min_alpha = get_min_alpha(best_rules_5)
        if array_rules[idx_rule].alpha > best_rules_5.get(min_alpha).alpha:
            best_rules_5[min_alpha] = array_rules[idx_rule]
    predict_test = np.zeros(len(test))
    temp_sum = check_test(best_rules_5, predict_test,test)
    if number == 1:
        p_train5.append(temp_sum)
    else:
        p5.append(temp_sum)

def best_four_rules(test, number):
    # initialize the list in the first 8 rules
    for idx_best_rules in range(4):
        best_rules_4[idx_best_rules] = array_rules[idx_best_rules]
    for idx_rule in range(len(array_rules)):
        min_alpha = get_min_alpha(best_rules_4)
        if array_rules[idx_rule].alpha > best_rules_4.get(min_alpha).alpha:
            best_rules_4[min_alpha] = array_rules[idx_rule]
    predict_test = np.zeros(len(test))
    temp_sum = check_test(best_rules_4, predict_test,test)
    if number == 1:
        p_train4.append(temp_sum)
    else:
        p4.append(temp_sum)

def best_three_rules(test,number):
    # initialize the list in the first 8 rules
    for idx_best_rules in range(3):
        best_rules_3[idx_best_rules] = array_rules[idx_best_rules]
    for idx_rule in range(len(array_rules)):
        min_alpha = get_min_alpha(best_rules_3)
        if array_rules[idx_rule].alpha > best_rules_3.get(min_alpha).alpha:
            best_rules_3[min_alpha] = array_rules[idx_rule]
    predict_test = np.zeros(len(test))
    temp_sum = check_test(best_rules_3, predict_test,test)
    if number == 1:
        p_train3.append(temp_sum)
    else:
        p3.append(temp_sum)

def best_two_rules(test, number):
    # initialize the list in the first 8 rules
    for idx_best_rules in range(2):
        best_rules_2[idx_best_rules] = array_rules[idx_best_rules]
    for idx_rule in range(len(array_rules)):
        min_alpha = get_min_alpha(best_rules_2)
        if array_rules[idx_rule].alpha > best_rules_2.get(min_alpha).alpha:
            best_rules_2[min_alpha] = array_rules[idx_rule]
    predict_test = np.zeros(len(test))
    temp_sum = check_test(best_rules_2, predict_test,test)
    if number == 1:
        p_train2.append(temp_sum)
    else:
        p2.append(temp_sum)

def best_one_rules(test, number):
    # initialize the list in the first 8 rules
    best_rules_1[0] = array_rules[0]
    for idx_rule in range(len(array_rules)):
        if array_rules[idx_rule].alpha > best_rules_1.get(0).alpha:
            best_rules_1[0] = array_rules[idx_rule]
    predict_test = np.zeros(len(test))
    temp_sum = check_test(best_rules_1, predict_test,test)
    if number == 1:
        p_train1.append(temp_sum)
    else:
        p1.append(temp_sum)


def check_test(best_rules, predict_test,test):
    for point_test in range(len(test)):
        fx = 0
        for i_best_rules in range(len(best_rules)):
            yRule = (best_rules[i_best_rules].m * test[point_test].x) + best_rules[i_best_rules].b
            # check whether the point is above the line or below
            if test[point_test].y > yRule:
                # y of the point is above the line
                signRule = best_rules[i_best_rules].sighUp
            else:
                # y of the point is below the line
                signRule = (-1 * best_rules[i_best_rules].sighUp)
            fx = fx + (best_rules[i_best_rules].alpha * signRule)
        if fx > 0:
            predict_test[point_test] = 1
        else:
            predict_test[point_test] = -1
    # Analyzing the data on what percentage of the rules are right
    true_sum = 0
    for p_idx in range(len(test)):
        if test[p_idx].label == predict_test[p_idx]:
            true_sum = true_sum + 1
    average = true_sum / len(test)
    return average



def main():

    path = "HC_Body_Temperature.txt"
    read_file(path, "HC")

    clear_list()

    path = "iris.data"
    read_file(path, "iris")




if __name__ == '__main__':
    main()


