#Food Instance. Not neccessary for program function, but helpful if program is to be expanded upon/more information for Food items need to be collected
class Food :

    #Initializor defines name and course of Food instance
    def __init__ (self, name, course):

        self._name = name
        self._course = course


    def name(self):
        
        return self._name


    def course(self):
        
        return self._course


    #String representation of Object
    def __str__ (self):
        
        return self._name + ", " + self._course
