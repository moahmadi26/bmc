""" variables: 
s1, s1_next, s2, s2_next, s3, s3_next, s4, s4_next, s5, s5_next, s6, s6_next: int
p1, p2, p3, p4, p5, p6
initial state: s1 == 1 && s4 == 1 && s2 == 50 && s5 == 50 && s3 == 0 && s6 == 0

state transitions: 
transition1: s1_next=s1-1, s2_next=s2-1, s3_next=s3+1
transition2: s3_next=s3-1, s1_next=s1+1, s2_next=s2+1
transition3: s3_next=s3-1, s1_next=s1+1, s5_next=s5+1
transition4: s4_next=s4-1, s5_next=s5-1, s6_next=s6+1
transition5: s6_next=s6-1, s4_next=s4+1, s5_next=s5+1
transition6: s6_next=s6-1, s4_next=s4+1, s2_next=s2+1

property: 
s5 == 40
"""

from z3 import *
from Graph import Node


def get_encoding(i):
    s1 = Int('s1.{0}'.format(i-1))
    s1_nxt = Int("s1.{0}".format(i))
    s2 = Int('s2.{0}'.format(i-1))
    s2_nxt = Int("s2.{0}".format(i))
    s3 = Int('s3.{0}'.format(i-1))
    s3_nxt = Int("s3.{0}".format(i))
    s4 = Int('s4.{0}'.format(i-1))
    s4_nxt = Int("s4.{0}".format(i))
    s5 = Int('s5.{0}'.format(i-1))
    s5_nxt = Int("s5.{0}".format(i))
    s6 = Int('s6.{0}'.format(i-1))
    s6_nxt = Int("s6.{0}".format(i))
    transition_1 = And(s1_nxt==(s1-1), s2_nxt==(s2-1), s3_nxt==(s3+1), s4_nxt==s4, s5_nxt==s5, s6_nxt==s6)
    transition_2 = And(s1_nxt==(s1+1), s2_nxt==(s2+1), s3_nxt==(s3-1), s4_nxt==s4, s5_nxt==s5, s6_nxt==s6)
    transition_3 = And(s1_nxt==(s1+1), s2_nxt==s2, s3_nxt==(s3-1), s4_nxt==s4, s5_nxt==(s5+1), s6_nxt==s6)
    transition_4 = And(s1_nxt==s1, s2_nxt==s2, s3_nxt==s3, s4_nxt==(s4-1), s5_nxt==(s5-1), s6_nxt==(s6+1))
    transition_5 = And(s1_nxt==s1, s2_nxt==s2, s3_nxt==s3, s4_nxt==(s4+1), s5_nxt==(s5+1), s6_nxt==(s6-1))
    transition_6 = And(s1_nxt==s1, s2_nxt==(s2+1), s3_nxt==s3, s4_nxt==(s4+1), s5_nxt==s5, s6_nxt==(s6-1))
    not_zero = And(s1_nxt>=0,s2_nxt>=0,s3_nxt>=0,s4_nxt>=0,s5_nxt>=0,s6_nxt>=0)
    #encoding = And(Or(transition_1, transition_2, transition_3, transition_4, transition_5, transition_6), not_zero)
    #encoding = And(Or(transition_1, transition_3, transition_4, transition_5, transition_6), not_zero)
    p = Real('p.{0}'.format(i-1))
    p_nxt = Real('p.{0}'.format(i))
    p1 = s1/(s1+s2+s3+s4+s5+s6)
    p2 = s2/(s1+s2+s3+s4+s5+s6)
    p3 = s3/(s1+s2+s3+s4+s5+s6)
    p4 = s4/(s1+s2+s3+s4+s5+s6)
    p5 = s5/(s1+s2+s3+s4+s5+s6)
    p6 = s6/(s1+s2+s3+s4+s5+s6)
    trans_1 = And(transition_1, p_nxt==(p1*p))
    trans_2 = And(transition_2, p_nxt==(p2*p))
    trans_3 = And(transition_3, p_nxt==(p3*p))
    trans_4 = And(transition_4, p_nxt==(p4*p))
    trans_5 = And(transition_5, p_nxt==(p5*p))
    trans_6 = And(transition_6, p_nxt==(p6*p))
    encoding = And(Or(trans_1, trans_2, trans_3, trans_4, trans_5, trans_6), not_zero)

    return encoding

def get_property(i):
    
    s5 = Int('s5.{0}'.format(i))
    property = (s5 == 40)
    #node = Node.Node('[65]')
    #node.make_terminal()
    #return [property, [node]]
    return property

def get_initial_state():
    
    s1 = Int('s1.{0}'.format(0))
    s2 = Int('s2.{0}'.format(0))
    s3 = Int('s3.{0}'.format(0))
    s4 = Int('s4.{0}'.format(0))
    s5 = Int('s5.{0}'.format(0))
    s6 = Int('s6.{0}'.format(0))
    p = Real('p.{0}'.format(0))

    state = And(s1 == 1, s4 == 1, s2 == 50, s5 == 50, s3 == 0, s6 == 0, p == 1)
    node = Node.Node('[1,50,0,1,50,0]')
    state_vector = '[s1,s2,s3,s4,s5,s6]'
    return [state, [node], state_vector]
    
