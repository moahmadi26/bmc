""" srn-2s ("two reaction network model")
    variables:
    s2, s2_nxt : int
 
    initial state: s2==40
 
    state transitions:
    transition 1: s2_nxt = s2+1
    transition 2: s2_nxt = s2-1
 
    Property:
            s2==65
"""

from z3 import *
from Graph import Node


def get_encoding(i):
    s2 = Int('s2.{0}'.format(i-1))
    s2_nxt = Int("s2.{0}".format(i))
    transition_1 = (s2_nxt==(s2 + 1))
    transition_2 = (s2_nxt==(s2 - 1))
    encoding = Or(transition_1, transition_2)
    return encoding

def get_property(i):
    
    s2 = Int('s2.{0}'.format(i))
    property = (s2 == 65)
    node = Node.Node('[65]')
    node.make_terminal()
    #return [property, [node]]
    return property

def get_initial_state():
    
    s2 = Int('s2.{0}'.format(0))
    state = (s2 == 40)
    node = Node.Node('[40]')
    state_vector = '[s2]'
    return [state, [node], state_vector]
    
