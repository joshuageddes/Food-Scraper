#External Python File Imports
from scraper import *
from food_class import *

#Function read_file iterates through each line of a given text file to pull food items, then formats them into Food instances
#Instances are added to dictionary of lists "data", where food items are sorted into courses.
#Takes in string parameter "filename", and returns dictionary "data"
def read_file(filename):

    data = {"appetizer":[], "main course":[], "dessert":[], "unknown":[]}

    dessert_list = create_dessert_list()
    appetizer_list = create_appetizer_list()

    #Opens file "filename" located in folder as program. 
    with open (filename) as fileIn:

        item_counter = 0

        for line in fileIn:

            item_counter +=1
            
            #Assigns variable food to given stripped line of text
            food = line.strip()

            #Progress Update printed to Console
            print(f'Sorting item {item_counter} : {food}')

            course = define_course(food, dessert_list, appetizer_list)

            #Food object with name and course information is added to one of multiple lists classified in a dictionary by course
            data[course].append(Food(food, course))

    return data


#Function write_file writes a new text file in same directory containing all food items sorted by course
#Data is formatted for readability, then added to written string
#Takes in string parameter "filename" and dictionary "data"
def write_file(data, filename):

    #All formatted text output stored in a single string
    string = ""

    #For every key in dictionary, or every category of course, write a header of information
    for course in data:

        string += "List of " + course.capitalize() + "s : \n"
        
        #If no objects are in list of the corresponding key (Special Case), output None
        if len(data[course]) == 0 :
            
            string += "None \n"
            
        else :
            
            #Iterate through objects in list of the corresponding key, formatting and adding to string
            for food in data[course]:

                string += food.name().capitalize() + "\n"

        string += "\n\n"

    with open(filename, "w") as fileOut:
        fileOut.write(string)
        
    #Program completion printed to console
    print("Done!")


data = read_file("food.txt")
write_file(data, "sorted_food.txt")
