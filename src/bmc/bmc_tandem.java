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








public class bmc_tandem
{
	public static void main(String[] args) throws IOException
	{
		System.out.println("\nStarting...");
		System.out.println("#####################################################");
		long timeStart = System.currentTimeMillis();
		new bmc_tandem().run(args);
		long timeFinish = System.currentTimeMillis();
        System.out.println(" \nOperation took " + (timeFinish - timeStart) / 1000.0 + " seconds.");
	}

	public void run (String[] args) throws IOException
	{
		try {
			
			
			//tandem model constants/rates
			int c = 127;
			double lambda = 4 * c;
			double mu1a = 0.1 * 2; 
			double mu1b = 0.9 * 2;
			double mu2 = 2; 
			double kappa = 4;




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

				script_location = "./bmc_z3/bmc_tandem_scaf.py";
				model_location = "./bmc_z3/examples/tandem.py";
				path_length_string = String.valueOf(path_length);
				command = "python3 " + script_location + " " + model_location + " " + path_length_string + " " + "1";
				Process process = Runtime.getRuntime().exec(command);
				


				BufferedReader stdInput = new BufferedReader(new InputStreamReader(process.getInputStream()));

				BufferedReader stdError = new BufferedReader(new InputStreamReader(process.getErrorStream()));
				String s = null;
				while ((s = stdInput.readLine()) != null) {
				    System.out.println(s);
				    break;
				}

				// Read any errors from the attempted command
				while ((s = stdError.readLine()) != null) {
				    System.out.println(s);
				}

				// System.out.println("=======================================================");



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
				
				node_line = graph_reader.nextLine();
				while(!(node_line.startsWith("#"))) {
					// graph.addNode(node_line.substring(1, node_line.length()-1));
					node_line = graph_reader.nextLine();
				}

				graph.addNode("target");

				while(graph_reader.hasNextLine()) { 
					String edge_line = graph_reader.nextLine();
					String src, dst; 
					src = edge_line.substring(1, edge_line.indexOf(" ")-1);
					dst = edge_line.substring(edge_line.indexOf(" ")+2, edge_line.length()-1);
					String src_keep = src;
					String dst_keep = dst;
					Double weight; 
					int sc_o,sc_n;
					int ph_o,ph_n;
					int sm_o,sm_n;
					

					sc_o = Integer.parseInt(src.substring(0,src.indexOf(",")));
					src = src.substring(src.indexOf(",")+1, src.length());
					ph_o = Integer.parseInt(src.substring(0,src.indexOf(",")));
					src = src.substring(src.indexOf(",")+1, src.length());
					sm_o = Integer.parseInt(src);

					sc_n = Integer.parseInt(dst.substring(0,dst.indexOf(",")));
					dst = dst.substring(dst.indexOf(",")+1, dst.length());
					ph_n = Integer.parseInt(dst.substring(0,dst.indexOf(",")));
					dst = dst.substring(dst.indexOf(",")+1, dst.length());
					sm_n = Integer.parseInt(dst);
					
					
					//transition1
					if ((sc_o<c) && (sc_n-sc_o==1) && (ph_n-ph_o==0) && (sm_n-sm_o==0)){

						weight = lambda;
					}
					//transition2
					else if ((sc_o>0) && (ph_o==1) && (sm_o<c) && (sc_n-sc_o==-1) 
						&& (ph_n-ph_o==0) && (sm_n-sm_o==1)){

						weight = mu1b;
					}
					//transition3
					else if ((sc_o>0) && (ph_o==1) && (sc_n-sc_o==0) 
						&& (ph_n-ph_o==1) && (sm_n-sm_o==0)){

						weight = mu1a;
					}
					//transition4
					else if ((sc_o>0) && (ph_o==2) && (sm_o<c) && (sc_n-sc_o==-1) 
						&& (ph_n-ph_o==-1) && (sm_n-sm_o==1)){

						weight = mu2;
					}
					//transition5
					else if ((sm_o>0) && (sc_n-sc_o==0) 
						&& (ph_n-ph_o==0) && (sm_n-sm_o==-1)){

						weight = kappa;
					}
					else {
						weight = 1.0;
						System.out.println("error!");
					}

					if ((sc_n == c)) {
						graph.addEdge(src_keep, "target", weight);
					}
					else {
						graph.addEdge(src_keep, dst_keep, weight);
					}

				}



				//sink node
				graph.addNode("sink");
				Set nodes_set = graph.getNodeLabels();
				Iterator<String> it = nodes_set.iterator();
				while(it.hasNext()){
					Node node = graph.getNode(it.next());
					Set<String> neighbours_set = node.getAdjacencyList();
					if (neighbours_set.size()>=1){
						String present_node = neighbours_set.iterator().next();
						String node_label = node.getLabel();
						
						int sc = Integer.parseInt(node_label.substring(0,node_label.indexOf(",")));
						node_label = node_label.substring(node_label.indexOf(",")+1, node_label.length());
						int ph = Integer.parseInt(node_label.substring(0,node_label.indexOf(",")));
						node_label = node_label.substring(node_label.indexOf(",")+1, node_label.length());
						int sm = Integer.parseInt(node_label);
						
						double rate = 0.0;
						if (sc<c)
							rate = rate + lambda;
						if (sc>0 && ph==1 && sm<c)
							rate = rate + mu1b;
						if (sc>0 && ph==1)
							rate = rate + mu1a;
						if (sc>0 && ph==2 && sm<c)
							rate = rate + mu2; 
						if (sm>0)
							rate = rate + kappa;

						double current_rate = 0.0;
						LinkedList<Edge> edges = node.getEdges(); 
						Iterator<Edge> edge_it = edges.iterator();
						
						while (edge_it.hasNext()){ 
							current_rate += edge_it.next().getWeight();
						}
						
						rate = rate - current_rate;

						graph.addEdge(node.getLabel(), "sink", rate);
					}	
				}

				//System.out.println(graph.toString());
				// Create a log for PRISM output (hidden or stdout)
				PrismLog mainLog = new PrismDevNullLog();

				// Initialise PRISM engine 
				Prism prism = new Prism(mainLog);
				prism.setEngine(Prism.EXPLICIT);
				prism.initialise();

				ctmcModel modelGen = new ctmcModel(graph);
				prism.loadModelGenerator(modelGen);


				prism.exportTransToFile(true, Prism.EXPORT_PLAIN, new File("export.dot"));
				double result = (Double) prism.modelCheck("P=? [true U<=2 x=-1]").getResult();
				System.out.println("probablity= " + String.valueOf(result));
				current_prob = result;
				
				long time_2 = System.currentTimeMillis();
				System.out.println(" \nthis bound took " + (time_2 - time_1) / 1000.0 + " seconds.");
				System.out.println("==========");


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
		private int init_state;


		public ctmcModel (Graph graph) {
			int count = 1;
			this.graph = graph;
			Set<String> nodeLabels = graph.getNodeLabels(); 
			Iterator<String> iter = nodeLabels.iterator(); 
			while (iter.hasNext()) {
				String node_label = iter.next();
				//System.out.println(node_label);
				String node_label_keep = node_label;
				if ((node_label != "sink") && (node_label != "target")) {
					
					int sc = Integer.parseInt(node_label.substring(0,node_label.indexOf(",")));
					node_label = node_label.substring(node_label.indexOf(",")+1, node_label.length());
					int ph = Integer.parseInt(node_label.substring(0,node_label.indexOf(",")));
					node_label = node_label.substring(node_label.indexOf(",")+1, node_label.length());
					int sm = Integer.parseInt(node_label);
					
					if ((sc == 127)) 
					{
						nodesMap.put(node_label_keep, -1);
					}
					if ((sc == 0) && (ph == 1) && (sm == 0)) {
						nodesMap.put(node_label_keep, 0);
					}
					else {
						nodesMap.put(node_label_keep, count);
						count = count + 1;
					}
				}
				else if (node_label == "target") {
					nodesMap.put(node_label_keep, -1);
				}
				else {
					nodesMap.put(node_label_keep, -2);
				}
				
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
			return new State(1).setValue(0, 0);
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