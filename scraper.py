#External libraries imported to get and parse information from Wikipedia
#Requests is used to make HTTP requests to return webpage information
#Beuatiful Soup is used to navigate and parse HTML content from requests
import requests
from bs4 import BeautifulSoup

#COURSE_X_STRINGS are lists of string constants which are common keywords on Wikipedia which can help identify food course, because Wikipedia is not consistent in identifying information
COURSE_APPETIZER_STRINGS = [
    "hors d'oeuvre",
    "side",
    "appetizer",
    "antipasto",
    "starter",
    "mezze",
    "salad",
    "soup",
    "snack",
    "savoury"
    ]

COURSE_MAIN_STRINGS = [
    "entree",
    "main",
    "primo",
    "prime",
    "roast",
    "curry",
    "dinner",
    "lunch",
    "breakfast"
    ]

COURSE_DESSERT_STRINGS = [
    "dessert",
    "sweet",
    ]

#Function create_dessert_list parses a Wikipedia page to create a list of formatted strings which are common desserts
#Function returns list "dessert_list" 
def create_dessert_list():

    dessert_list = []

    #Creates a new Response object "response" that is the response to an HTTP request at the given URL
    response = requests.get(url="https://en.wikipedia.org/wiki/List_of_desserts",)
    
    #Creates a new BeautifulSoup object "soup" that contains all HTML tags for the Response object.
    #Reponse object function .content returns HTML content page, which is converted to unicode characters using Python's parser in it's library
    soup = BeautifulSoup(response.content, 'html.parser')
    
    #Code identifies list item tags nested under all parent tags with class "div-col"
    col_list = soup.find_all(class_="div-col")

    for col in col_list:

        link_list = col.find_all("li")

        for dessert in link_list :

            #Tag.string function returns text between tags on page
            #If the string exists (is not None), formatted string is added to dessert list
            if dessert.string is not None :

                dessert_list.append(dessert.string.lower())

    return dessert_list


#Function create_appetizer_list parses a Wikipedia page to create a list of formatted strings which are common appetizers
#Function returns list "appetizer_list"
def create_appetizer_list():

    appetizer_list = []
    response = requests.get(url="https://en.wikipedia.org/wiki/Category:Appetizers",)
    soup = BeautifulSoup(response.content, 'html.parser')

    #Code identifies list item tags nested under first parent tag with class "mw-content"
    link_list = soup.find(class_="mw-content-ltr").find_all("li")

    for appetizer in link_list:

        if appetizer.string is not None :

            appetizer_list.append(appetizer.string.lower())

    return appetizer_list


#Function categorizes food item (query) into either an Appetizer, Main Course, or Dessert.
#First, function will check if query is in either lists of desserts or appetizers
#Secondly, function will request food Course information from Wikipedia, then check if recieved Course information matches any key identification Strings in any Course
#Takes in string parameter "query", lists "dessert_list" and "appetizer_list".
#Function returns "appetizer", "main course", or "dessert" depending on course identification
def define_course (query, dessert_list, appetizer_list):


    if query in dessert_list :

        return "dessert"

    elif query in appetizer_list:

        return "appetizer"

    #Format query to work in google search
    query.replace(" ", "+")

    response = requests.get(url="https://www.google.com/search?q=wikipedia+" + query,)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    #BeautifulSoup identifies first h3 tag, then finds the parent tag's href value 
    link = soup.find('h3').parent.get('href')

    #Format href value such that it can be used as a link
    link = link[link.index("=")+1 : link.index("&")]
    
    response = requests.get(url=link,)
    soup = BeautifulSoup(response.content, 'html.parser')

    #Find tag with class "infobox-label" with display text "Course"
    tag = soup.find(class_ = "infobox-label", string="Course")

    #If tag cannot be found (ie no Course information) Course cannot be identified therefore function returns "unknown"
    if tag == None :

        return "unknown"
    
    #Iterates through all string values of the sibling tag to Course
    #This is designed to work with different types of Course information values; sometimes many courses or links are given. Code focuses on all string values only
    for string in tag.find_next_sibling().stripped_strings:

        #If any keywords in COURSE_X_STRINGS are found in the formatted string values (course information), returns respective course
        for keyword in COURSE_DESSERT_STRINGS :

            if keyword in string.lower() :

                return "dessert"

        for keyword in COURSE_APPETIZER_STRINGS :

            if keyword in string.lower() :

                return "appetizer"

        for keyword in COURSE_MAIN_STRINGS :

            if keyword in string.lower() :

                return "main course"

    #If no conditions are met, return "unknown"
    return "unknown"


        



    







