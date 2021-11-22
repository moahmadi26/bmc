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








public class bmc2
{
	public static void main(String[] args) throws IOException
	{
		System.out.println("\nStarting...");
		System.out.println("#####################################################");
		long timeStart = System.currentTimeMillis();
		new bmc2().run(args);
		long timeFinish = System.currentTimeMillis();
        System.out.println(" \nOperation took " + (timeFinish - timeStart) / 1000.0 + " seconds.");
	}

	public void run (String[] args) throws IOException
	{
		try {
			
			double current_prob=0;
			int path_length = 0;

			File cex_file;

			while (current_prob < Double.parseDouble(args[0])) {

				int flag = 0;
				
				while (flag == 0) {
					System.out.println("path_length: " +String.valueOf(path_length));
					try {
						String command = "python3 /Users/mo/usf/projects/probmc/bmc_2rn/ProbMC/SMT_BMC/src/main.py srn-2s " + String.valueOf(path_length);
						Process process = Runtime.getRuntime().exec(command);
						int exit_value = process.waitFor();
						System.out.println("done with python");
						cex_file = new File("./srn-2s.output");
						flag = 1;
					} catch (FileNotFoundException e) {
						path_length = path_length + 1;
						System.out.println("==========");
					}
				}	
				
				cex_file = new File("./srn-2s.output");
				Scanner cex_reader = new Scanner(cex_file);

				while(!(cex_reader.nextLine().startsWith("#"))) {}
				while(!(cex_reader.nextLine().startsWith("#"))) {}

				Graph graph = new Graph();
				HashMap state_index = new HashMap<Integer, String>();

				String temp_line = cex_reader.nextLine();
				int counter = 0;
				while (!(temp_line.startsWith("#"))){ 
					temp_line = temp_line.substring(1,temp_line.length()-1);
					state_index.put(counter, temp_line);
					graph.addNode(temp_line);
					temp_line = cex_reader.nextLine();
					counter = counter + 1;
				}

				if (counter != 0){
					temp_line = cex_reader.nextLine();
					temp_line = temp_line.substring(1,temp_line.length()-1);


					state_index.put(counter, temp_line);
					graph.addNode(temp_line);
					String target_state = temp_line;

					while(!(cex_reader.nextLine().startsWith("#"))) {}

					while(cex_reader.hasNextLine()) {
						temp_line = cex_reader.nextLine();
						String src, dst;
						src = temp_line.substring(0,temp_line.indexOf(" "));
						dst = temp_line.substring(temp_line.indexOf(" ")+1,temp_line.length());
						int src_int = Integer.parseInt(src);
						int dst_int = Integer.parseInt(dst);

						int src_value = Integer.parseInt(state_index.get(src_int).toString());
						int dst_value = Integer.parseInt(state_index.get(dst_int).toString());
						Double weight; 
						if (dst_value > src_value)
							weight = 1.0;
						else 
							weight = 0.025 * (double) src_value;
						graph.addEdge(state_index.get(src_int).toString(),state_index.get(dst_int).toString(), weight);

					}

					Set entrySet = state_index.entrySet();
					Iterator it = entrySet.iterator();
					graph.addNode("sink");
					while(it.hasNext()){
						Map.Entry me = (Map.Entry) it.next();
						Node node = graph.getNode(me.getValue().toString());
						Set<String> neighborsSet = node.getAdjacencyList();
						if (node.getAdjacencyList().size()==1) {
							String presentNode = neighborsSet.iterator().next();
						double rate;
						if (Integer.parseInt(presentNode) < Integer.parseInt(me.getValue().toString()))
							rate = 1.0;
						else
							rate = (double) (Integer.parseInt(me.getValue().toString())) * 0.025;
						graph.addEdge(me.getValue().toString(),"sink",rate);
						
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
					double result = (Double) prism.modelCheck("P=? [true U<=100 x="+String.valueOf(modelGen.getTargetState()) +"]").getResult();
					System.out.println("probablity= " + String.valueOf(result));
					System.out.println("==========");
					current_prob = result;
				}
				path_length = path_length+1;

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

		public int returnTarget() {
			return nodesMap.get("target");
		}

		public ctmcModel (Graph graph) {
			this.graph = graph;
			int count = 0; 
			Set<String> nodeLabels = graph.getNodeLabels(); 
			Iterator<String> iter = nodeLabels.iterator(); 
			while (iter.hasNext()) {
				String temp; 
				temp = iter.next();
				nodesMap.put(temp, count);
				if (temp.equals("65")){
					//System.out.println(count);
					target_state=count;
				}
				count++;
			}
		}
	
		public int getTargetState()
		{
			return target_state;
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
			// List<Edge> edgeList = graph.getEdgeList(); 
			// Iterator<Edge> iter = edgeList.iterator(); 
			// Set<String> toNodes = new HashSet<String>(); 
			// while (iter.hasNext()) {
			// 	toNodes.add(iter.next().getToNode());
			// }
			// Set<String> origToNodes = new HashSet<String>();
			// origToNodes.addAll(graph.getNodeLabels()); 
			// origToNodes.removeAll(toNodes);
			// Iterator<String> iter2 = origToNodes.iterator();
			// node = graph.getNode(iter2.next());
			int nodeInt = nodesMap.get("40");
			return new State(1).setValue(0, nodeInt);
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