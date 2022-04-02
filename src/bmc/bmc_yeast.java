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








public class bmc_yeast
{
	public static void main(String[] args) throws IOException
	{
		System.out.println("\nStarting...");
		System.out.println("#####################################################");
		long timeStart = System.currentTimeMillis();
		new bmc_yeast().run(args);
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
			String graph_location = "./bmc_z3/graph.g";
			Graph graph;


			while (current_prob < prob_bound) {

				long time_1 = System.currentTimeMillis();

				script_location = "./bmc_z3/bmc_yeast.py";
				model_location = "./bmc_z3/examples/yeast_polarization.py";
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

				System.out.println("=========");



				exit_value = process.waitFor(); 
				graph_file = new File(graph_location);
				path_length = path_length + 1;
				
			}		
		} catch (FileNotFoundException e) {
				System.out.println("Error: " + e.getMessage());
				System.exit(1);
		//} catch (PrismException e) {
			//	System.out.println("Error: " + e.getMessage());
			//	System.exit(1);
		} catch (IOException e) {
				e.printStackTrace();
		}
		catch (Exception ex) {  
            ex.printStackTrace();             
        }  

	}
				
}