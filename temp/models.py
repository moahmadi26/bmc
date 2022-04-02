import numpy as np

class enzymatic_futile_cycle: 
	def __init__(self): 
		
		###########################################################
		####### change this block for adding a new model ##########
		self.species_vector_ = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6']
		
		self.initial_state_ = [1, 50, 0, 1, 50, 0]

		R1_in  = [1, 1, 0, 0, 0, 0]
		R1_out = [0, 0, 1, 0, 0, 0]

		R2_in  = [0, 0, 1, 0, 0, 0]
		R2_out = [1, 1, 0, 0, 0, 0]

		R3_in  = [0, 0, 1, 0, 0, 0]
		R3_out = [1, 0, 0, 0, 1, 0]

		R4_in  = [0, 0, 0, 1, 1, 0]
		R4_out = [0, 0, 0, 0, 0, 1]

		R5_in  = [0, 0, 0, 0, 0, 1]
		R5_out = [0, 0, 0, 1, 1, 0]

		R6_in  = [0, 0, 0, 0, 0, 1]
		R6_out = [0, 1, 0, 1, 0, 0]

		R = [[R1_in, R1_out], [R2_in, R2_out], [R3_in, R3_out], [R4_in, R4_out], [R5_in, R5_out], [R6_in, R6_out]]
		self.reaction_rates_ = [1.0, 1.0, 0.1, 1.0, 1.0, 0.1]
		############# end of model descriptioon block #############
		###########################################################
		###########################################################


		self.reactions = {}
		for i, e in enumerate(R):
			R_effect = np.array(np.array(e[1])-np.array(e[0])).tolist()
			self.reactions[i+1] = [e[0], e[1], R_effect] 
	
	def species_vector(self):
		return  self.species_vector_

	def initial_state(self):
		return self.initial_state_

	def reactions_vector(self): 
		return self.reactions

	def reaction_rates(self): 
		return self.reaction_rates_


		
###############################################################
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
###############################################################



class yeast_polarization: 
	def __init__(self): 
		
		###########################################################
		####### change this block for adding a new model ##########
		self.species_vector_ = ['R', 'L', 'RL', 'G', 'Ga', 'Gbg', 'Gd']
		
		self.initial_state_ = [50, 2, 0, 50, 0, 0, 0]

		#		 ['R', 'L', 'RL', 'G', 'Ga', 'Gbg', 'Gd']
		R1_in  = [0  ,  0 ,  0  ,  0 ,  0  ,  0   ,  0]
		R1_out = [1  ,  0 ,  0  ,  0 ,  0  ,  0   ,  0]

		R2_in  = [1  ,  0 ,  0  ,  0 ,  0  ,  0   ,  0]
		R2_out = [0  ,  0 ,  0  ,  0 ,  0  ,  0   ,  0]

		R3_in  = [1  ,  1 ,  0  ,  0 ,  0  ,  0   ,  0]
		R3_out = [0  ,  1 ,  1  ,  0 ,  0  ,  0   ,  0]

		R4_in  = [0  ,  0 ,  1  ,  0 ,  0  ,  0   ,  0]
		R4_out = [1  ,  0 ,  0  ,  0 ,  0  ,  0   ,  0]

		R5_in  = [0  ,  0 ,  1  ,  1 ,  0  ,  0   ,  0]
		R5_out = [0  ,  0 ,  0  ,  0 ,  1  ,  1   ,  0]

		R6_in  = [0  ,  0 ,  0  ,  0 ,  1  ,  0   ,  0]
		R6_out = [0  ,  0 ,  0  ,  0 ,  0  ,  0   ,  1]

		R7_in  = [0  ,  0 ,  0  ,  0 ,  0  ,  1   ,  1]
		R7_out = [0  ,  0 ,  0  ,  1 ,  0  ,  0   ,  0]

		R8_in  = [0  ,  0 ,  0  ,  0 ,  0  ,  0   ,  0]
		R8_out = [0  ,  0 ,  1  ,  0 ,  0  ,  0   ,  0]

		R = [[R1_in, R1_out], [R2_in, R2_out], [R3_in, R3_out], [R4_in, R4_out], [R5_in, R5_out], [R6_in, R6_out], [R7_in, R7_out], [R8_in, R8_out]]
		self.reaction_rates_ = [0.0038, 4.0e-4, 0.042, 0.01, 0.011, 0.1, 1.05e3, 3.21]
		############# end of model descriptioon block #############
		###########################################################
		###########################################################


		self.reactions = {}
		for i, e in enumerate(R):
			R_effect = np.array(np.array(e[1])-np.array(e[0])).tolist()
			self.reactions[i+1] = [e[0], e[1], R_effect] 
	
	def species_vector(self):
		return  self.species_vector_

	def initial_state(self):
		return self.initial_state_

	def reactions_vector(self): 
		return self.reactions

	def reaction_rates(self): 
		return self.reaction_rates_
		
