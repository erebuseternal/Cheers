"""
This module holds the Cellar subclass BeerCellar and its supporting dweller_class
and helper function(s).

Cheers,
Marcel
"""

from cellar import Cellar, CellarDweller
from urlparse import urlparse
from re import compile, findall


def aggregate_count_dictionaries(dict1, dict2):
    """aggregate_count_dictionaries(dict1, dict2) -- This function takes two dictionaries
    which have values that are numbers and returns a single dictionary where for each
    key common to dict1 and dict2 the corresponding values have been added.

        HOW IT WORKS:
            * we create a new dictionary
            * for each key in dict1
                * we look to see if the key is in dict2
                * if it is, we add the corresponding values together and set it under the
                  key in our new dictionary. We then delete the entry from dict2
                * if it isn't, we set the value corresponding to the key in our new
                  dictionary to the one in dict1
            * we add all the key value pairs remaining in dict2 to our new dictionary
    """
    new_dict = {}
    for key in dict1:
        if key in dict2:
            new_dict[key] = dict1[key] + dict2[key]
            del dict2[key]
        else:
            new_dict[key] = dict1[key]
    for key in dict2:
        new_dict[key] = dict2[key]
    return new_dict


class Barrel(CellarDweller):
    """Barrel(node)

    Attributes: node, subresource_counts, count
    Methods: aggregate(other)

    This class is a dweller for a cellar. It holds subresource_counts in a dictionary where the keys should
    be subresource urls and the values the number of times that subresource has been found for the url
    corresponding to the node this Barrel is in. It also holds a count, which should count how many beers
    have been found with this particular url.

    Aggregation works as you would expect, summing subresource counts and the count itself.
    """
    def __init__(self, node):
        self.node = node
        self.subresource_counts = {}
        self.count = 0

    def aggregate(self, other):
        """aggregate(other) -- This method takes another Barrel and returns a new Barrel whose count
        is the sum of this and the other barrel's counts and whose subresource attribute is the
        aggregate of the subresource_counts of this barrel and the other. The node for this barrel is None.

            HOW IT WORKS:
                * create a new Barrel passing in None for node
                * add the counts and set it to the new count
                * aggregate the subresource_counts using aggregate_count_dictionaries from this module
        """
        new_barrel = Barrel(None)
        new_barrel.count = self.count + other.count
        new_barrel.subresources = aggregate_count_dictionaries(self.subresource_counts, other.subresource_counts)
        return new_barrel


class BeerCellar(Cellar):
    """
    BeerCellar()

    Attributes: NONE
    Methods: get(key), jump_up(dweller), get_down(dweller, dwellers_to_avoid)

    This class is a Cellar subclass which uses url's for keys. Specifically _parse takes the path
    from the url, and generates a list of that path's components. Therefore the further down this
    cellar's tree you go, the more specific your url.

    The dweller class is a Barrel which holds a subresource count and a total count and aggregates
    these as you would expect when a get_down is called.
    """

    dweller_class = Barrel

    def _parse(self, url):
        """_parse(url) -- This function takes a url, grabs its path, and splits the path into its pieces. It
        returns the pieces in order in list

            HOW IT WORKS:
                * grab the path using python's urlparse from urlparse
                * create a regular expression that greedily grabs as the largest string it can without a '/' in it
                * use this expression with python's findall (from re) to grab each piece of the path
                * return the list thus found
        """
        path = urlparse(url).path
        expression = compile("[^\/]{1,}")
        pieces = findall(expression, path)
        return pieces
