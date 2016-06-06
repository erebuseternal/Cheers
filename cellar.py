class PointyDictionary(dict):
    def __init__(self, obj=None):
        super(PointyDictionary, self).__init__()
        self.pointer = obj


"""
***** CELLAR CLASS *****

WHAT
The class is a data structure composed of a series of pointydictionaries embedded within
another under keys which are not None. Each dictionary can also have a list under the key
None. Each pointydictionary's pointer points to the pointydictionary it is embedded in

HOW
This data structure is all about reaching specific pointydictionaries. Each pointydictionary is reached
using a particular key. This works via the following. The key is parsed into a list using the
PARSER function specific to this class. Each element of this list represents a key. The first
element is used to graba pointydictionary within the base_dictionary, the next key is used to
grab a pointydictionary within that pointydictionary and so forth until we run out of keys.
The pointydictionary we result with is the pointydictionary corresponding to that key. The
element at the key None within this pointydictionary (if it exists) is a list of values
corresponding to that key in particular

WHY
The following class is a data structure created to store resources based on urls
where all resources belonging to a specific url can be grabbed but also all resources
with urls as or more specific as a certain url can be grabbed as well. The class abstracts
away from using actual urls, but that was the impetus for creating the class.

**********
CONSTRUCTOR
this constructor takes NO INPUT arguments

METHODS
dive(key) - get the pointydictionary corresponding to a key
stepup(dictionary) - get the pointydictionary in which the pointydictionary, dictionary,
                     is embedded
add(key, value) - add a value to the corresponding key
get(key) - grab the list of values at the corresponding key (if they exist)
get_down_dict(dictionary, avoid_dictionary) - grabs all values in the pointydictionary,
                        dictionary, and all embedded pointydictionaries except for
                        avoid_dictionary and all embedded pointydictionaries
get_down(key, avoid_key) - grabs all values in the pointydictionary corresponding to key
                        and all deeper pointydictionaries except avoid_key's dictionary
                        and all pointydictionaries within it

**********

CHANGING THE PARSER
To change the parser simply create a new Cellar class that inherits from this one
and set the PARSER in this class definition to whatever function you want

RULES FOR PARSERS
    * they must return a list that does not contain any None values
"""


class Cellar:
    def test_parser(self, string):
        return string

    PARSER = test_parser

    def __init__(self):
        self.base_dictionary = PointyDictionary()

    """
    This grabs a dictionary corresponding to the input key

        HOW IT WORKS

            * we use the parser to turn our key into a list
            * we set a current_dictionary variable to self.base_dictionary
            * for each element of the list
                * we grab the pointydictionary at that key in the current_dictionary (creating
                  it if it doesn't exist and setting the pointer as the current_dictionary)
                * we set this pointydictionary as the current_dictionary
            * we return the current_dictionary
    """

    def dive(self, key):
        elements = self.PARSER(key)

        current_dictionary = self.base_dictionary

        for element in elements:
            if element not in current_dictionary:
                current_dictionary[element] = PointyDictionary(current_dictionary)
            current_dictionary = current_dictionary[element]

        return current_dictionary

    """
    This grabs the pointydictionary above the input pointydictionary

        HOW IT WORKS:

            * It just grabs the pointydictionary in the pointer
    """

    def step_up(self, dictionary):
        return dictionary.pointer

    """
    This allows us to add a specific value under a specific index

        HOW IT WORKS

            * we dive to the pointydictionary corresponding to this key
            * then we grab the list within the pointydictionary that is the value to the key None
              (creating it if it doesn't exist)
            * we append our input value to that list
    """

    def add(self, key, value):
        dictionary = self.dive(key)

        if None not in dictionary:
            dictionary[None] = []
        values = dictionary[None]

        values.append(value)

    """
    This grabs all of the values that were added in with this key

        HOW IT WORKS:

            * we dive to the pointydictionary corresponding to this key
            * then we return the element at the key None within pointydictionary (if it exists
              returning an empty list otherwise)
    """

    def get(self, key):
        dictionary = self.dive(key)

        if None in dictionary:
            return dictionary[None]
        else:
            return []

    """
    This grabs all values at levels below a pointydictionary except within avoid_dictionary
    (if it is specified)


        HOW IT WORKS:

            * we create a values list
            * we extend values by the list at None in the pointydictionary (corresponding to the
              key) if it exists
            * we then loop through the rest of the keys in the pointydictionary
                * we grab the pointydictionary corresponding to each key (if it is not
                  avoid_dictionary) and call getup_dict on that pointydictionary
                * we extend values by the result of that call
            * we return the values list
    """

    def get_down_dict(self, dictionary, avoid_dictionary=PointyDictionary()):
        values = []

        if None in dictionary:
            values.extend(dictionary[None])

        for key in dictionary:
            if key is not None and dictionary[key] is not avoid_dictionary:
                new_dictionary = dictionary[key]
                values.extend(self.get_down_dict(new_dictionary, avoid_dictionary))

        return values

    """
    This uses the key and avoid_key (if it exists) to get the pointydictionary and avoid_dictionary
    to use in getup_dict. I.e. this allows us to getup using keys instead of pointydictionaries.

        HOW IT WORKS:

            * we grab the dictionary belonging to the key
            * if avoid_key is None we call getup_dict with just the dictionary
            * if it isn't None we grab the avoid_dictionary and call getup_dict with full
              arguments
            * we return the values
    """

    def get_down(self, key, avoid_key=None):
        dictionary = self.dive(key)

        if not avoid_key:
            return self.get_down_dict(dictionary)
        else:
            avoid_dictionary = self.dive(avoid_key)
            return self.get_down_dict(dictionary, avoid_dictionary)



