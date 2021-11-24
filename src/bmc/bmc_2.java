import java.io.*;
import graph.*;
import java.util.*;
import java.util.Map.Entry;
import java.util.HashMap;
import java.lang.Math;
import java.util.Scanner;
import java.util.HashMap;
import java.util.Map;

import prism.PrismDevNullLog;
import prism.Prism;
import prism.IntegerBound;
import prism.OpRelOpBound;
import prism.PrismComponent;
import prism.PrismException;
import prism.PrismLog;
import prism.PrismNotSupportedException;
import prism.PrismSettings;
import prism.PrismUtils;
import prism.ModelGenerator;
import prism.ModelType;
import prism.PrismLangException;


import explicit.StateValues;
import explicit.CTMC;
import explicit.DTMC;
import explicit.CTMCModelChecker;

import parser.ast.ModulesFile;
import parser.ast.PropertiesFile;
import parser.ast.Expression;
import parser.ast.ExpressionProb;
import parser.ast.ExpressionTemporal;
import parser.ast.ExpressionUnaryOp;
import parser.type.Type;
import parser.type.TypeInt;
import parser.State;
import parser.VarList;
import parser.ast.Declaration;
import parser.ast.DeclarationInt;








public class bmc_2
{
	public static void main(String[] args) throws IOException
	{
		System.out.println("\nStarting...");
		System.out.println("#####################################################");
		long timeStart = System.currentTimeMillis();
		new bmc_2().run(args);
		long timeFinish = System.currentTimeMillis();
        System.out.println(" \nOperation took " + (timeFinish - timeStart) / 1000.0 + " seconds.");
	}

	public void run (String[] args) throws IOException
	{
		try {
			
			double current_prob=0;
			double prob_bound=Double.parseDouble(args[0]);
			int path_length = 0;
			int exit_value;
			File graph_file;
			String path_length_string, script_location, model_location, command;
			String graph_location = "./graph.g";
			Graph graph;


			while (current_prob < prob_bound) {

				long time_1 = System.currentTimeMillis();

				script_location = "./bmc_z3/bmc_2.py";
				model_location = "./bmc_z3/examples/two_rn.py";
				path_length_string = String.valueOf(path_length);
				command = "python3 " + script_location + " " + model_location + " " + path_length_string + " " + "1";
				Process process = Runtime.getRuntime().exec(command);
				


				BufferedReader stdInput = new BufferedReader(new InputStreamReader(process.getInputStream()));

				BufferedReader stdError = new BufferedReader(new InputStreamReader(process.getErrorStream()));
				String s = null;
				while ((s = stdInput.readLine()) != null) {
				    System.out.println(s);
				}

				// Read any errors from the attempted command
				while ((s = stdError.readLine()) != null) {
				    System.out.println(s);
				}



				exit_value = process.waitFor(); 
				graph_file = new File(graph_location);
				
				Scanner graph_reader = new Scanner(graph_file);

				while(!(graph_reader.nextLine().startsWith("#"))) {}
				graph = new Graph();
				String node_line = graph_reader.nextLine();
				while(!(node_line.startsWith("#"))) {
					graph.addNode(node_line.substring(1, node_line.length()-1));
					node_line = graph_reader.nextLine();
				}
				
				// String target_state = graph_reader.nextLine();
				// target_state = target_state.substring(1,target_state.length()-1);
				
				while(!(graph_reader.nextLine().startsWith("#"))) {}


				while(graph_reader.hasNextLine()) { 
					String edge_line = graph_reader.nextLine();
					String src, dst; 
					src = edge_line.substring(1, edge_line.indexOf(" ")-1);
					dst = edge_line.substring(edge_line.indexOf(" ")+2, edge_line.length()-1);
					Double weight; 
					if (Integer.parseInt(src) < Integer.parseInt(dst))
						weight = 1.0;
					else
						weight = 0.025 * (double) Integer.parseInt(src);
					graph.addEdge(src, dst, weight);

				}



				graph.addNode("-1");
				Set nodes_set = graph.getNodeLabels();
				Iterator<String> it = nodes_set.iterator();
				while(it.hasNext()){
					Node node = graph.getNode(it.next());
					Set<String> neighbours_set = node.getAdjacencyList();
					if (neighbours_set.size()==1){
						String present_node = neighbours_set.iterator().next();
						double rate; 
						if (Integer.parseInt(present_node) < Integer.parseInt(node.getLabel()))
							rate = 1.0;
						else
							rate = (double) (Integer.parseInt(node.getLabel()) * 0.025);
						graph.addEdge(node.getLabel(), "-1", rate);
					}	
				}

				
				// Create a log for PRISM output (hidden or stdout)
				PrismLog mainLog = new PrismDevNullLog();

				// Initialise PRISM engine 
				Prism prism = new Prism(mainLog);
				prism.setEngine(Prism.EXPLICIT);
				prism.initialise();

				ctmcModel modelGen = new ctmcModel(graph);
				prism.loadModelGenerator(modelGen);


				prism.exportTransToFile(true, Prism.EXPORT_PLAIN, new File("export.dot"));
				double result = (Double) prism.modelCheck("P=? [true U<=100 x=65]").getResult();
				System.out.println("probablity= " + String.valueOf(result));
				current_prob = result;
				
				path_length = path_length+1;
				long time_2 = System.currentTimeMillis();
				System.out.println(" \nthis bound took " + (time_2 - time_1) / 1000.0 + " seconds.");
				System.out.println("==========");

			}

		} catch (FileNotFoundException e) {
				System.out.println("Error: " + e.getMessage());
				System.exit(1);
		} catch (PrismException e) {
				System.out.println("Error: " + e.getMessage());
				System.exit(1);
		} catch (IOException e) {
				e.printStackTrace();
		}
		catch (Exception ex) {  
            ex.printStackTrace();             
        }  

	}
				
	
	class ctmcModel implements ModelGenerator 
	{
		private State exploreState;
		private Graph graph;
		private HashMap<String, Integer> nodesMap = new HashMap<String, Integer>();
		private int x; 
		private Node node;
		private int target_state;


		public ctmcModel (Graph graph) {
			this.graph = graph;
			Set<String> nodeLabels = graph.getNodeLabels(); 
			Iterator<String> iter = nodeLabels.iterator(); 
			while (iter.hasNext()) {
				String temp = iter.next();
				nodesMap.put(temp, Integer.parseInt(temp));
			}
		}

		// Methods for ModelInfo

		// Models we are checking are CTMCs
		@Override
		public ModelType getModelType()
		{
			return ModelType.CTMC;
		}

		@Override
		public List<String> getVarNames()
		{
			return Arrays.asList("x");
		}

		@Override
		public List<Type> getVarTypes()
		{
			return Arrays.asList(TypeInt.getInstance());
		}


		// Methods for Model Generator

		
		//initial state is the start of the path
		@Override
		public State getInitialState() throws PrismException
		{
			// //initially we are at initial state
			return new State(1).setValue(0, 40);
		}
	
		// after a call to this many of the functions should be available in the state
		@Override
		public void exploreState(State exploreState) throws PrismException
		{
			// Store the state (for reference, and because will clone/copy it later)
			this.exploreState = exploreState;
			// Cache the value of x in this state for convenience
			x = ((Integer) exploreState.varValues[0]).intValue();
			for (String s : nodesMap.keySet()) {
				if (nodesMap.get(s) == x) {
					node = graph.getNode(s);
				}
			}
		}

		@Override
		public int getNumChoices() throws PrismException
		{
			// This is a CTMC so always exactly one nondeterministic choice (i.e. no nondeterminism)
			return 1;
		}

	
		@Override
		public int getNumTransitions(int i) throws PrismException
		{
			return node.getAdjacencyList().size();
		}

	
		@Override
		public Object getTransitionAction(int i, int offset) throws PrismException
		{
			// No action labels in this model
			return null;
		}

	
		/**
	 	* Get the probability/rate of a transition within a choice, specified by its index/offset.
	 	* @param i Index of the nondeterministic choice
	 	* @param offset Index of the transition within the choice
	 	*/
		public double getTransitionProbability(int i, int offset) throws PrismException {
			LinkedList<Edge> edges = node.getEdges();
			Iterator<Edge> iter = edges.iterator();
			int count = 0;
			double prob = 0;
			while (count<=offset) {
				prob = iter.next().getWeight();
				count++;
			}
			return prob;
		}
	
	
		/**
		 * Get the target (as a new State object) of a transition within a choice, specified by its index/offset.
		 * @param i Index of the nondeterministic choice
		 * @param offset Index of the transition within the choice
		 */
		public State computeTransitionTarget(int i, int offset) throws PrismException {
			State target = new State(exploreState); 
			Set<String> neighbors = node.getAdjacencyList();

			Iterator<String> iter = neighbors.iterator();
			int count = 0;
			Node returnNode = new Node();
			while (count <= offset) {
				String test = iter.next();
				returnNode = graph.getNode(test);
				count++;
			}
			target.setValue(0, nodesMap.get(returnNode.getLabel())); 
			return target;
		}
	
		@Override
		public VarList createVarList()
		{
			// Need to give the variable list containing the declaration of variable x 
			VarList varList = new VarList();
			try {
				varList.addVar(new Declaration("x", new DeclarationInt(Expression.Int(0), Expression.Int(graph.numNodes()))), 0, null);
			} catch (PrismLangException e) {
			}
			return varList;
		}


	}

}