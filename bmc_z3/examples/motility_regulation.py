""" variables: 
s1, s1_next, s2, s2_next, s3, s3_next, s4, s4_next, s5, s5_next, s6, s6_next, s7, s7_next, s8, s8_next, s9, s9_next: int

initial state: s1 == 1 && s2 == 10 && s3 == 1 && s4 == 10 && s5 == 1 && s6 == 1 && s7 == 10 && s8 == 1 && s9 == 1

state transitions: 
transition1 : s2_next=s2+1
transition2 : s2_next=s2-1
transition3 : s4_next=s4+1
transition4 : s4_next=s4-1
transition5 : s4_next=s4+1, s5_next=s5-1, s6_next=s6+1, s7_next=s7+1
transition6 : s7_next=s7-1
transition7 : s4_next=s4-1, s5_next=s5+1, s6_next=s6-1
transition8 : s4_next=s4+1, s5_next=s5-1, s6_next=s6+1
transition9 : s2_next=s2-1, s3_next=s3-1, s8_next=s8+1
transition10: s2_next=s2+1, s3_next=s3+1, s8_next=s8-1
transition11: s2_next=s2-1, s6_next=s6-1, s9_next=s9+1
transition12: s2_next=s2+1, s6_next=s6+1, s9_next=s9-1


property: 
s2 == 20
"""


from z3 import *
from Graph import Node


def get_encoding(i):
    s1 = Int('s1.{0}'.format(i-1))
    s1_nxt = Int('s1.{0}'.format(i))
    s2 = Int('s2.{0}'.format(i-1))
    s2_nxt = Int('s2.{0}'.format(i))
    s3 = Int('s3.{0}'.format(i-1))
    s3_nxt = Int('s3.{0}'.format(i))
    s4 = Int('s4.{0}'.format(i-1))
    s4_nxt = Int('s4.{0}'.format(i))
    s5 = Int('s5.{0}'.format(i-1))
    s5_nxt = Int('s5.{0}'.format(i))
    s6 = Int('s6.{0}'.format(i-1))
    s6_nxt = Int('s6.{0}'.format(i))
    s7 = Int('s7.{0}'.format(i-1))
    s7_nxt = Int('s7.{0}'.format(i))
    s8 = Int('s8.{0}'.format(i-1))
    s8_nxt = Int('s8.{0}'.format(i))
    s9 = Int('s9.{0}'.format(i-1))
    s9_nxt = Int('s9.{0}'.format(i))
    transition_1  = And(s1_nxt==s1, s2_nxt==(s2+1), s3_nxt==s3, s4_nxt==s4, s5_nxt==s5, s6_nxt==s6, s7_nxt==s7, s8_nxt==s8, s9_nxt==s9)
    transition_2  = And(s1_nxt==s1, s2_nxt==(s2-1), s3_nxt==s3, s4_nxt==s4, s5_nxt==s5, s6_nxt==s6, s7_nxt==s7, s8_nxt==s8, s9_nxt==s9)
    transition_3  = And(s1_nxt==s1, s2_nxt==s2, s3_nxt==s3, s4_nxt==(s4+1), s5_nxt==s5, s6_nxt==s6, s7_nxt==s7, s8_nxt==s8, s9_nxt==s9)
    transition_4  = And(s1_nxt==s1, s2_nxt==s2, s3_nxt==s3, s4_nxt==(s4-1), s5_nxt==s5, s6_nxt==s6, s7_nxt==s7, s8_nxt==s8, s9_nxt==s9)
    transition_5  = And(s1_nxt==s1, s2_nxt==s2, s3_nxt==s3, s4_nxt==(s4+1), s5_nxt==(s5-1), s6_nxt==(s6+1), s7_nxt==(s7+1), s8_nxt==s8, s9_nxt==s9)
    transition_6  = And(s1_nxt==s1, s2_nxt==s2, s3_nxt==s3, s4_nxt==s4, s5_nxt==s5, s6_nxt==s6, s7_nxt==(s7-1), s8_nxt==s8, s9_nxt==s9)
    transition_7  = And(s1_nxt==s1, s2_nxt==s2, s3_nxt==s3, s4_nxt==(s4-1), s5_nxt==(s5+1), s6_nxt==(s6-1), s7_nxt==s7, s8_nxt==s8, s9_nxt==s9)
    transition_8  = And(s1_nxt==s1, s2_nxt==s2, s3_nxt==s3, s4_nxt==(s4+1), s5_nxt==(s5-1), s6_nxt==(s6+1), s7_nxt==s7, s8_nxt==s8, s9_nxt==s9)
    transition_9  = And(s1_nxt==s1, s2_nxt==(s2-1), s3_nxt==(s3-1), s4_nxt==s4, s5_nxt==s5, s6_nxt==s6, s7_nxt==s7, s8_nxt==(s8+1), s9_nxt==s9)
    transition_10 = And(s1_nxt==s1, s2_nxt==(s2+1), s3_nxt==(s3+1), s4_nxt==s4, s5_nxt==s5, s6_nxt==s6, s7_nxt==s7, s8_nxt==(s8-1), s9_nxt==s9)
    transition_11 = And(s1_nxt==s1, s2_nxt==(s2-1), s3_nxt==s3, s4_nxt==s4, s5_nxt==s5, s6_nxt==(s6-1), s7_nxt==s7, s8_nxt==s8, s9_nxt==(s9+1))
    transition_12 = And(s1_nxt==s1, s2_nxt==(s2+1), s3_nxt==s3, s4_nxt==s4, s5_nxt==s5, s6_nxt==(s6+1), s7_nxt==s7, s8_nxt==s8, s9_nxt==(s9-1))


    not_zero = And(s1_nxt>=0,s2_nxt>=0,s3_nxt>=0,s4_nxt>=0,s5_nxt>=0,s6_nxt>=0, s7_nxt>=0, s8_nxt>=0, s9_nxt>=0)
    encoding = And(Or(transition_1, transition_2, transition_3, transition_4, transition_5, transition_6, transition_7, transition_8, transition_9, transition_10, transition_11, transition_12), not_zero)
    return encoding

def get_property(i):
    
    s2 = Int('s2.{0}'.format(i))
    property = (s2 == 20)
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
    s7 = Int('s7.{0}'.format(0))
    s8 = Int('s8.{0}'.format(0))
    s9 = Int('s9.{0}'.format(0))



    state = And(s1 == 1, s2 == 10, s3 == 1, s4 == 10, s5 == 1, s6 == 1, s7 == 10, s8 == 1, s9 == 1)
    node = Node.Node('[1,10,1,10,1,1,10,1,1]')
    state_vector = '[s1,s2,s3,s4,s5,s6,s7,s8,s9]'
    return [state, [node], state_vector]
    
