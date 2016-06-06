"""
This holds the base classes for the Cellar datastructure.

Cheers,
Marcel
"""

class CellarNode(object):
    """
    CellarNode(parent=None)

    Attributes: parent, children, dweller
    Methods: NONE

    This class is the node for our cellar class. It keeps as attributes a parent (node), children (a
    dictionary), and a dweller (what stores the value of the node).
    """
    def __init__(self, parent=None):
        self.parent = parent
        self.children = {}
        self.dweller = None

class CellarDweller(object):
    """
    CellarDweller(node)

    Attributes: node, elements
    Methods: aggregate(other)

    This class is used to hold the data pertaining to a particular node in a cellar (instance of
    Cellar Class). It has as attributes a node (the node it belongs too) and some elements (a list,
    empty at first).

    The point of this class is to allow not only for holding data for nodes, but also aggregating
    data over several nodes. Therefore there is an aggregate method which takes another CellarDweller
    and returns a CellarDweller with None for its node attribute and an elements list which is first
    dwellers elements list extended by the second's.
    """
    def __init__(self, node):
        self.node = node
        self.elements = []

    def aggregate(self, other):
        """aggregate(other) -- This method takes another CellarDweller as input and returns a Cellar
        Dweller whose node is None and whose elements is this CellarDweller's elements extended by the
        other CellarDweller's elements."""
        new_dweller = CellarDweller(None)
        new_dweller.elements.extend(self.elements)
        new_dweller.elements.extend(other.elements)
        return new_dweller

class Cellar:
    """
    Cellar(*args) -- The *args you pass in will be passed to the dweller_class constructor
        as the arguments after the first argument each time you create a new dweller for your
        cellar. The first argument passed is a node. Because Cellar uses the CellarDweller
        class as its dweller_class you shouldn't input anything for args. It is there so
        that inheritance works smoothly.

    Attributes: None
    Methods: get(key), jump_up(dweller), get_down(dweller, dwellers_to_avoid=[])

    This class is essentially a tree of nodes where each node contains data contained
    in an object called a dweller (base class is CellarDweller). Each node's dweller
    can be reached by a key using the get method. In addition, if one has a dweller
    one can get the dweller in the parent node (i.e. the node above) using jump_up and
    one can grab the aggregate of the dweller and all dwellers below it in a tree
    using get_down. If one wants to exclude certain dwellers (and their 'descendents')
    from this aggregation one only needs to pass the list of such dwellers as the second
    (optional) argument to get_down. A couple of notes on these things:

    Aggregation of dwellers is done using the dweller's own aggregate method.

    Keys reach nodes by being parsed into a list of elements. These elements represent
    a path through the nodes by virtue of the following process:
        the first element is the key for a child of the root
        the second element is the key for a child within the child just found
        repeat...
    The method which generates these elements is _parse

    MAKING NEW KINDS OF CELLARS:
        To create a new kind of cellar:
            * Create a new class which inherits from Cellar
            * override _parse to create the kind of tree structure you want
            * set dweller_class to the class you want your dwellers to be

    RESTRICTIONS ON _parse: must return an iterable that never gives None

    RESTRICTIONS ON dweller_class: the class should inherit from CellarDweller. It
     must take a node as its first argument (it doesn't have to have more arguments
     than this, but it can if you supply those arguments to the Cellar instance at
     construction). It must have a method aggregate which returns another instance
     of the dweller_class.
    """

    def _parse(self, key):
        """_parse(key) -- This method takes a key as input and returns the key within
        a list.

        This class is intended to be overridden in classes which inherit from Cellar.
        It is this class that determines how a key is transformed into a list of
        elements used to walk through the Cellar's tree of nodes.
        """
        return [key]

    dweller_class = CellarDweller   # this is the class used to create dwellers
                                    # it can be overridden to suit classes that
                                    # inherit from Cellar

    def __init__(self, *args):
        self._root = CellarNode()
        self._args = args

    def _create_dweller(self, node):
        """_create_dweller(node) -- This method takes a node as input. It returns a dweller
        created using the class' dweller_class and self._args (which defaults to [] at class
        construction).
        """
        dweller = self.dweller_class(node, *self._args)
        return dweller


    def _dive(self, key):
        """_dive(key) -- This method takes a key for the cellar as input. It returns the node
        corresponding to this key.

            HOW IT WORKS:
                * it uses _parse to turn the key into a list of elements
                * it grabs the root as the current node
                * for every element in the elements list
                    * it checks to see if the element is a key for a child in the current node
                      and grabs that child (creating it if need be)
                    * it sets this child as the current node
                * it returns the current node
        """
        elements = self._parse(key)

        current_node = self._root

        for element in elements:
            if element not in current_node.children:
                current_node.children[element] = CellarNode(current_node)
            current_node = current_node[element]

        return current_node

    def _grab_dweller(self, node):
        """_grab_dweller(node) -- This method takes a node as input. It returns the node's
        dweller as output, creating a new one using self.args if needed.

            HOW IT WORKS:
                * it checks to see if the node's dweller is currently None
                * if it is not, it returns the dweller
                * if it is, it creates a dweller using _create_dweller passing the input node
                  as the dweller's node
        """
        if node.dweller is not None:
            return node.dweller
        else:
            dweller = self._create_dweller(node)
            node.dweller = dweller
            return dweller

    def get(self, key):
        """get(key) -- This method takes a key for the cellar as input. It returns the corresponding
        node's dweller (creating it if it doesn't exit) using a call to this classes _dive and
        _grab_dweller methods in succession.
        """
        node = self._dive(key)
        return self._grab_dweller(node)

    def jump_up(self, dweller):
        """jump_up(dweller) -- This method takes a dweller and returns the dweller in the parent node
        to the node the input dweller is in. Note that if the parent node does not exist, this method
        will return None.

            HOW IT WORKS:
                * it grabs the dweller's node
                * it checks to see if that node has a parent
                * if it does, it grabs the parent node's dweller and returns that
                * if it does not, it returns None
        """
        dwellers_node = dweller.node
        if dwellers_node.parent is not None:
            dwellers_parent = dwellers_node.parent.dweller
            return dwellers_parent
        else:
            return None

    def get_down(self, dweller, dwellers_to_avoid=[]):
        """get_down(dweller, dwellers_to_avoid=[]) -- This method takes a dweller and an optional list
        of dwellers to avoid as input. It returns the aggregate of dweller with all dwellers in nodes
        below it except those dwellers in dwellers to avoid and those below them.

            HOW IT WORKS:
                * first we check to make sure dweller isn't in dwellers to avoid. If it is we return
                  a newly created dweller created using _create_dweller (None is passed as the
                  dweller's node).
                * we then grab the node the dweller is in
                * if the node has no children we return dweller
                * if it does have children, for each of those children:
                    * we grab the dweller using _grab_dweller
                    * we call get_down on the child's dweller (passing in dwellers to avoid of course)
                    * we aggregate the result with dweller
                * then we return dweller
        """
        if dweller is in dwellers_to_avoid:
            return self.dweller_class(None, *self.args)

        node = dweller.node
        if not node.children:
            return dweller

        for key in node.children:
            child_dweller = self._grab_dweller(node.children[key])
            aggregate_dweller = self.get_down(child_dweller, dwellers_to_avoid)
            dweller = dweller.aggregate(aggregate_dweller)

        return dweller





