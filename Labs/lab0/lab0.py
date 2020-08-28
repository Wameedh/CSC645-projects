########################################################################################################################
# Class: Computer Networks
# Date: 08/28/2020
# Lab0: Getting Started with Python
# Goal: Learning the basics of Python
# Student Name: Wameedh Mohammed Ali
# Student ID: 920678405
# Student Github Username: Wameedh
# Instructions: Complete the TODO sections for each problem
# Guidelines: Read each problem carefully, and implement them correctly. Grade is based on lab correctness/completeness
#               No partial credit will be given.
#               No unit test are provided for lab #0
########################################################################################################################

########################## Problem 0: Print  ###########################################################################
"""
Print your name, student id and Github username
Sample output:
Name: Jose
SID: 91744100
Github Username:
"""
name = "Wameedh Mohammed Ali" # TODO: your name
SID = 920678405 # TODO: your student id
git_username = "Wameedh" # TODO: your github username
print(name)
print(SID)
print(git_username)
print('\n')

########################## Problem 1: Processing user input ############################################################
"""
Accept two int values from the user, and print their product. If their product is greater than 500, 
then print their sum

Sample output:
Enter the first integer: 2
Enter the second integer: 4
Result is 8
Enter the first integer: 2
Enter the second integer: 1000
Result is 1002
"""
print("Problem 1 ********************") # problem header (don't modify)
# TODO: your code here

firstInt = int(input("Enter the first integer: "))
secondtInt = int(input("Enter the second integer: "))

productOffirstAndsecond = firstInt * secondtInt
if productOffirstAndsecond < 500:
    print("Result is {}".format(productOffirstAndsecond))
else:
    print("Result is {}".format(firstInt + secondtInt))


########################## Problem 2: String Processing ##############################################################
"""
Given a string print the number of times the string "Alice" appears anywhere in the given string

For example, given the string: "Alice and Bob go to the same school. They learned today in class how to treat a lice 
infestation, and Alice found the lecture really interesting" 
the sample output would be: 'Alice' found 2 times. 
"""
print("Problem 2 ********************") # problem header (don't modify)
# the given string
myString = "Alice and Bob go to the same school. They learned today in class how to treat a lice" \
           "infestation, and Alice found the lecture really interesting"
# TODO: your code here

numberOfTimes = myString.count("Alice")
outPut = "'Alice' found {} times."
print(outPut.format(numberOfTimes))

########################## Problem 3: Loops ############################################################################
"""
Given a list of numbers iterate over them and output the sum of the current number and previous one.

Given: [5, 10, 24, 32, 88, 90, 100] 
Outputs: 5, 15, 34, 56, 120, 178, 190.
"""
print("Problem 3 ********************") # problem header (don't modify)
numbers = [5, 10, 24, 32, 88, 90, 100]
# TODO: your code here
y = 0
for x in numbers:
    print(x + y)
    y = x

########################## Problem 4: Functions/Methods/Lists ##########################################################
"""
Create the method mergeOdds(l1, l2) which takes two unordered lists as parameters, and returns a new list with all the 
odd numbers from the first a second list sorted in ascending. Function signature is provided for you below

For example: Given l1 = [2,1,5,7,9] and l2 = [32,33,13] the function will return odds = [1,5,7,9,13,33] 
"""
print("Problem 4 ********************") # problem header (don't modify)
# function skeleton
def merge_odds(l1, l2):
    odds = []
    # TODO: your code here
    l3 = l1 + l2 # merge the two list
    for x in l3: # iterate over the new list
        if x%2 != 0: # check if the number is odd
            odds.append(x) # we append to the end of odds[]
    odds.sort() # sort the list in ascending order
    return odds
l1 = [2,1,5,7,9]
l2 = [32,33,13]
odds = merge_odds(l1, l2)
print(odds)

########################## Problem 5: Functions/Methods/Dictionaries ###################################################
"""
Refactor problem #4 to return a python dictionary instead a list where the keys are the index of the odd numbers in l1,
and l2, and the values are the odd numbers. 

For example: Given l1 = [2,1,5,7,9] and l2 = [32,33,13] the function will return odds = {1: [1, 33], 2: [5,13], 3: [7], 4: [9]} 
"""
print("Problem 5 ********************") # problem header

# function skeleton
def merge_odds(l1, l2):
    odds = {}
    # TODO: your code here
    def sortListIntoDict(list, odds): # this method would search a given list and get the odds value,
        # then it assign them into a dictionary with their index as a the key
        for i, val in enumerate(list):  # iterate over the l1
            if val % 2 != 0:  # check if the number is odd
                if i in odds.keys(): # check if key is exists
                    odds[i].append(val) # will just add new value to that key without deleting the old value
                else:
                    odds[i] = [val] # create new value in the dictionary

    sortListIntoDict(l1, odds)
    sortListIntoDict(l2, odds)
    return odds

l1 = [2,1,5,7,9]
l2 = [32,33,13]
odds = merge_odds(l1, l2)
print(odds)
