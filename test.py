from cellar import *

"""
TEST THE POINTY DICTIONARY
"""
obj = "object"
pd = PointyDictionary(obj)
print pd.pointer

"""
Test the Cellar
"""
c = Cellar()
values = {"a": "a", "ab": "ab", "aa": "aa", "aba": "aba"}

# generate the first barrel
c.add("a", values["a"])
print(c.get("a"))

# generate a barrel a level lower
c.add("aa", values["aa"])
print(c.get("aa"))

# add an additional value at that level
c.add("aa", "AA")
print(c.get("aa"))

# add more than one new level at once
c.add("aba", values["aba"])
print(c.get("aba"))

# add a value to an intermediate level
c.add("ab", values["ab"])
print(c.get("ab"))

# get the dictionary at a particular level
dictionary = c.dive("ab")
print(dictionary)

# go up a level this should be the dictionary at key 'a' in the
# base dictionary
dictionary = c.step_up(dictionary)
print(dictionary)

# get all values we have entered so far
print(c.get_down(""))

# get all values besides in ab
print(c.get_down("", "ab"))

# get all a values besides aba
print(c.get_down("a", "aba"))

"""
All good here :D
"""





