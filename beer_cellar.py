from cellar import Cellar
from urlparse import urlparse
from re import compile, findall


"""
This is a child of Cellar that has for its PARSER a function that generates keys from
urls by taking the path and splitting it into its pieces - the key is that list of pieces
"""
class BeerCellar(Cellar):
    """
    this function takes a url, grabs its path, and splits the path into its pieces. It
    returns the pieces in order in list

        HOW IT WORKS:
            * grab the path using python's urlparse from urlparse
            * create a regular expression that greedily grabs as the largest string it can without a '/' in it
            * use this expression with python's findall (from re) to grab each piece of the path
            * return the list thus found
    """

    def _parser(self, url):
        path = urlparse(url).path
        expression = compile("[^\/]{1,}")
        pieces = findall(expression)
        return pieces
