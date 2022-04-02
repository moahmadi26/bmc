""" variables: 
R, R_next, L, L_next, RL, RL_next, G, G_next, G_a, G_a_next, G_bg, G_bg_next, G_d, G_d_next: int

initial state: R == 50 && L == 2 && RL == 0 && G == 50 && G_a == 0 && G_bg == 0 && G_d == 0

state transitions: 
transition1: R_next=R+1
transition2: R_next=R-1
transition3: R_next=R-1, RL_next=RL+1
transition4: R_next=R+1, RL_next=RL-1
transition5: RL_next=RL-1, G_next=G-1, G_a_next=G_a+1, G_bg_next=G_bg+1
transition6: G_a_next=G_a-1, G_d_next=G_d+1
transition7: G_next=G+1, G_bg_next=G_bg-1, G_d_next=G_d-1
transition8: RL_next=RL+1


RL = R_3 - R_4 - R_5 + R_8 (# of RL molecules)
Gbg = R_5 - R_7 (#of Gbg molecules) 

property: 
G_bg == 50
"""

from z3 import *
from Graph import Node


def get_encoding(i):
    R = Int('R.{0}'.format(i-1))
    R_nxt = Int('R.{0}'.format(i))
    L = Int('L.{0}'.format(i-1))
    L_nxt = Int('L.{0}'.format(i))
    RL = Int('RL.{0}'.format(i-1))
    RL_nxt = Int('RL.{0}'.format(i))
    G = Int('G.{0}'.format(i-1))
    G_nxt = Int('G.{0}'.format(i))
    G_a = Int('G_a.{0}'.format(i-1))
    G_a_nxt = Int('G_a.{0}'.format(i))
    G_bg = Int('G_bg.{0}'.format(i-1))
    G_bg_nxt = Int('G_bg.{0}'.format(i))
    G_d = Int('G_d.{0}'.format(i-1))
    G_d_nxt = Int('G_d.{0}'.format(i))
    RL = Int('RL.{0}'.format(i-1))
    RL_nxt = Int('RL.{0}'.format(i))
    transition_1 = And(R_nxt==(R+1), L_nxt==L, RL_nxt==RL, G_nxt==G, G_a_nxt==G_a, G_bg_nxt==G_bg, G_d_nxt==G_d)
    transition_2 = And(R_nxt==(R-1), L_nxt==L, RL_nxt==RL, G_nxt==G, G_a_nxt==G_a, G_bg_nxt==G_bg, G_d_nxt==G_d)
    transition_3 = And(R_nxt==(R-1), L_nxt==L, RL_nxt==(RL+1), G_nxt==G, G_a_nxt==G_a, G_bg_nxt==G_bg, G_d_nxt==G_d)
    transition_4 = And(R_nxt==(R+1), L_nxt==L, RL_nxt==(RL-1), G_nxt==G, G_a_nxt==G_a, G_bg_nxt==G_bg, G_d_nxt==G_d)
    transition_5 = And(R_nxt==R, L_nxt==L, RL_nxt==(RL-1), G_nxt==(G-1), G_a_nxt==(G_a+1), G_bg_nxt==(G_bg+1), G_d_nxt==G_d)
    transition_6 = And(R_nxt==R, L_nxt==L, RL_nxt==RL, G_nxt==G, G_a_nxt==(G_a-1), G_bg_nxt==G_bg, G_d_nxt==(G_d+1))
    transition_7 = And(R_nxt==R, L_nxt==L, RL_nxt==RL, G_nxt==(G+1), G_a_nxt==G_a, G_bg_nxt==(G_bg-1), G_d_nxt==(G_d-1))
    transition_8 = And(R_nxt==R, L_nxt==L, RL_nxt==(RL+1), G_nxt==G, G_a_nxt==G_a, G_bg_nxt==G_bg, G_d_nxt==G_d)

    not_zero = And(R_nxt>=0,L_nxt>=0,RL_nxt>=0,G_nxt>=0,G_a_nxt>=0,G_bg_nxt>=0, G_d_nxt>=0)
    encoding = And(Or(transition_1, transition_2, transition_3, transition_4, transition_5, transition_6, transition_7, transition_8), not_zero)
    #encoding = And(Or(transition_5, transition_8), not_zero)
    return encoding

def get_property(i):
    
    G_bg = Int('G_bg.{0}'.format(i))
    property = (G_bg == 50)
    #node = Node.Node('[65]')
    #node.make_terminal()
    #return [property, [node]]
    return property

def get_initial_state():
    
    R = Int('R.{0}'.format(0))
    L = Int('L.{0}'.format(0))
    RL = Int('RL.{0}'.format(0))
    G = Int('G.{0}'.format(0))
    G_a = Int('G_a.{0}'.format(0))
    G_bg = Int('G_bg.{0}'.format(0))
    G_d = Int('G_d.{0}'.format(0))


    state = And(R == 50, L == 2, RL == 0, G == 50, G_a == 0, G_bg == 0, G_d == 0)
    node = Node.Node('[50,2,0,50,0,0,0]')
    state_vector = '[R,L,RL,G,G_a,G_bg,G_d]'
    return [state, [node], state_vector]
    
