""" variables: 
sc, sc_next, ph, ph_next, sm, sm_next: int

initial state: sc == 0 && ph == 1 && sm == 0

state transitions: 
transition1: sc_next=sc+1
transition2: sc_next=sc-1, sm_next=sm+1
transition3: ph_next=ph+1
transition4: sc_next=sc-1, ph_next=ph-1, sm_next=sm+1
transition5: sm_next=sm-1

two possible properties: 
1)sc=c
2)sc=c && sm=c
"""

from z3 import *
from Graph import Node

#size of queue, c, in the tandem model
c = 127

#rates in the tandem model
lamb = 4 * c
mu1a = 0.1 * 2
mu1b = 0.1 * 2
mu2 = 2
kappa = 4

def get_encoding(i):
    sc = Int('sc.{0}'.format(i-1))
    sc_nxt = Int("sc.{0}".format(i))
    ph = Int('ph.{0}'.format(i-1))
    ph_nxt = Int("ph.{0}".format(i))
    sm = Int('sm.{0}'.format(i-1))
    sm_nxt = Int("sm.{0}".format(i))
    transition_1 = And(sc<c, sc_nxt==(sc+1), ph_nxt==ph, sm_nxt==sm)
    transition_2 = And(sc>0, ph==1, sm<c, sc_nxt==(sc-1), ph_nxt==ph, sm_nxt==(sm+1))
    transition_3 = And(sc>0, ph==1,sc_nxt==sc, ph_nxt==2, sm_nxt==sm)
    transition_4 = And(sc>0, ph==2, sm<c, sc_nxt==(sc-1), ph_nxt==1, sm_nxt==(sm+1))
    transition_5 = And(sm>0, sc_nxt==sc, ph_nxt==ph, sm_nxt==(sm-1))
    
    bounds = And(0<=sc_nxt, sc_nxt<=c, Or(ph_nxt==1, ph_nxt==2), 0<=sm_nxt, sm_nxt<=c)
    encoding = And(Or(transition_1, transition_2, transition_3, transition_4, transition_5), bounds)
    return encoding

def get_property(i):
    
    sc = Int('sc.{0}'.format(i))
    sm = Int('sm.{0}'.format(i))
    property = And(sc == c)
    return property

def get_initial_state():
    
    sc = Int('sc.{0}'.format(0))
    ph = Int('ph.{0}'.format(0))
    sm = Int('sm.{0}'.format(0))


    state = And(sc == 0, ph == 1, sm == 0)
    node = Node.Node('[0,1,0]')
    state_vector = '[sc,ph,sm]'
    return [state, [node], state_vector]
    
