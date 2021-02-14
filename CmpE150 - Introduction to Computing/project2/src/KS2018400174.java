import java.util.*;

public class KS2018400174 {
	public static void main(String[] args) {
		Scanner console = new Scanner(System.in);
		// Taking input one by one. We will be using the calculation statement very often.
		String statement_1 = console.nextLine();
		String statement_2 = console.nextLine();    
		String statement_3 = console.nextLine();
		String calculation = console.nextLine();
		// This is the part where calculation statement is rearranged by replacing variable values.
		calculation = Calculation_With_Variables(statement_3,Calculation_With_Variables(statement_2, Calculation_With_Variables(statement_1, calculation)));
		// Here, we add parentheses to the outside of our statement in order to be sure that there is at least one parenthesis left.
		calculation = "(" + calculation.replace(";", ")");

		while (calculation.contains("(")) {  // This process will be implemented as long as our statement involves parentheses.
			String str = "";                 // String str will be used to store the content of the most inner parentheses.
			for (int i = calculation.indexOf(")"); i >= 0; i--) {   // This for loop used to find where the beginning of the parenthesis is.
				if (calculation.charAt(i) == '(') {
					str = calculation.substring(i, calculation.indexOf(")") + 1);
					break;
				}
			}

			if (str.contains("/") || str.contains("*")) {    // At this point we are looking for divison/multiplication operators.
				for (int n = 0; n < str.length(); n++) {
					// n will be the index of operation sign.
					if (str.charAt(n) == '/' || str.charAt(n) == '*') {
						 // Calculation_Update method performs the necessary operation and returns the result.
						calculation = Calculation_Update(str, n, calculation);  
						break;                                                   
					}
				}

			} else if (str.contains("+") || str.contains("-")) { // At this point we are looking for summation/subtraction operators.
				for (int n = 0; n < str.length(); n++) {
					// n will be the index of operation sign.
					if (str.charAt(n) == '+' || str.charAt(n) == '-') {
						calculation = Calculation_Update(str, n, calculation);
						// Calculation_Update method performs the necessary operation and returns the result.
						break;
					}
				}

			} else {
				// If there is no operator to perform left, then we are going to remove the parentheses, and update the calculation statement.
				calculation = calculation.replace(str, str.substring(1, str.length() - 1));
			}
		}
		// Print out the calculation without redundant empty spaces.

		for (int k = 0; k < calculation.length(); k++) {
			if (calculation.charAt(k) != ' ')
				System.out.print(calculation.charAt(k));
		}
		console.close();
	}
	
	
	// first_value() is used to extract the first number from operation (opt) string.
	public static String first_value(String opt, char operator) {
		// We will store the value into the string first_value.
		String first_value = "";
		for (int t = 0; t < opt.indexOf(operator); t++) {
			// With this for loop, we examine each character before the operation sign and add the integers to the first_value until opt is completely examined.
			if (opt.charAt(t) != ' ')
				first_value = first_value + opt.charAt(t);
		}
		return first_value;
	}
	// second_value() is used to extract the second number from operation (opt) string.
	public static String second_value(String opt, char operator) {
		// We will store the value into the string second_value.
		String second_value = "";
		for (int l = opt.indexOf(operator) + 1; l < opt.length(); l++) {
			// With this for loop, we examine each character after the operation sign and add the integers to the second_value until opt is completely examined.
			if (opt.charAt(l) != ' ' && opt.charAt(l) != ')') {
				second_value = second_value + opt.charAt(l);
			}
		}
		return second_value;
	}

	// Operation_String() examines the content of str string which we initialized at the very beginning of the code.
	// Then it takes the substring which includes only one operation sign and two numbers.
	// We need to implement this process since original str string can involve more than one operations.
	public static String Operation_String(String str, char operator) {
		// end and start integers will be the beginning and the end indices of the substring.
		int end = 0, start = 0;
		for (int i = str.indexOf(operator) - 1; i >= 0; i--) {
			// Here we start to move back from the index of operator sign, and we will continue until we see another operator sign or parenthesis.
			if (!((str.charAt(i) <= '9' && str.charAt(i) >= '0') || str.charAt(i) == '.' || str.charAt(i) == ' ')) {
				// We stored at what point our substring should begin.
				start = i + 1;
				break;
			}
		}
		for (int m = str.indexOf(operator) + 1; m < str.length(); m++) {
			// Here we start to move forward from the index of operator sign, and we will continue until we see another operator sign or parenthesis.
			if (!((str.charAt(m) <= '9' && str.charAt(m) >= '0') || str.charAt(m) == '.' || str.charAt(m) == ' ')) {
				// We stored at what point our substring should end.
				end = m;
				break;
			}
		}
		return str.substring(start, end);
	}
	
	// Operation() method performs the requested operation and returns the latest calculation. 
	public static String Operation(String opt, String calculation, char operator, String first_value,
			String second_value) {
		// We assign a boolean here to keep the information about data type.
		boolean isValueDouble = false;
		// Here, we check whether operation string contains dot ".", so that we can understand which data type we are dealing with.
		if (opt.contains(".")) {
			isValueDouble = true;
		}
		// If opt contains dot ".", operation is supposed to give a double result. 
		if (isValueDouble) {   
			// Here, it makes the calculation according to the operator.
			if (operator == '+')
				calculation = calculation.replace(opt,
						Double.toString(Double.parseDouble(first_value) + Double.parseDouble(second_value)));
			if (operator == '-')
				calculation = calculation.replace(opt,
						Double.toString(Double.parseDouble(first_value) - Double.parseDouble(second_value)));
			if (operator == '*')
				calculation = calculation.replace(opt,
						Double.toString(Double.parseDouble(first_value) * Double.parseDouble(second_value)));
			if (operator == '/')
				calculation = calculation.replace(opt,
						Double.toString(Double.parseDouble(first_value) / Double.parseDouble(second_value)));
		}
		// If opt doesn't contain any dot ".", operation is supposed to give an integer result.
		else {
			// Here, it makes the calculation according to the operator.
			if (operator == '+')
				calculation = calculation.replace(opt,
						Integer.toString(Integer.parseInt(first_value) + Integer.parseInt(second_value)));
			if (operator == '-')
				calculation = calculation.replace(opt,
						Integer.toString(Integer.parseInt(first_value) - Integer.parseInt(second_value)));
			if (operator == '*')
				calculation = calculation.replace(opt,
						Integer.toString(Integer.parseInt(first_value) * Integer.parseInt(second_value)));
			if (operator == '/')
				calculation = calculation.replace(opt,
						Integer.toString(Integer.parseInt(first_value) / Integer.parseInt(second_value)));
		}
		return calculation;
	}

	// Calculation_With_Variables() method rearranges the calculation statement by replacing variables with their values.
	public static String Calculation_With_Variables(String statement, String calculation) {
		// Here, we are looking whether calculation statement contains the assigned variable.
		// Under the if statement we will replace the value according to its data type.
		// If the assigned variable is double but it was not written with decimal point, we need to add decimal point manually.
		if (calculation.contains(Variable_Name(statement))) {
			if (Data_Type(statement) == "int")
				calculation = calculation.replace(Variable_Name(statement), Value(statement));
			else {
				if (Value(statement).contains("."))
					calculation = calculation.replace(Variable_Name(statement), Value(statement));
				else {
					calculation = calculation.replace(Variable_Name(statement), Value(statement) + ".0");
				}
			}
		}
		return calculation;
	}
	// Value() method stores the value of the given variable.
	public static String Value(String statement) {
		// String value stores the value in the string format.
		// String search encompasses the part after the equals ("=") sign.
		String value = "";
		String search = statement.substring(statement.indexOf("="));
		for (int i = 1; i < search.length() - 1; i++) {
			if (search.charAt(i) != ' ') {
				value = value + search.charAt(i);
			}
		}
		return value;
	}
	// Data_Type() method stores the data type of the variable by reading the first character of the variable line.
	public static String Data_Type(String statement) {
		if (statement.charAt(0) == 'i')
			return "int";
		else
			return "double";
	}
	// Variable_Name() method returns the name of the variable by examining the characters before the equals ("=") sign.
	public static String Variable_Name(String statement) {
		// We are going to store the characters into the variable_name string.
		String variable_name = "";
		// String search is the part between data type and equals sign of a variable line.
		// We are going to store the characters by examining the content of the search string using for loop.
		String search = statement.substring(statement.indexOf(" "), statement.indexOf("="));
		for (int i = 0; i < search.length(); i++) {
			if (search.charAt(i) != ' ') {
				variable_name = variable_name + search.charAt(i);
			}
		}
		return variable_name;
	}
	// Calculation_Update() is the most essential method we have. At the previous methods we extracted first and second values from the string str.
	// With Operation_String() we found at which point our operation starts and at which point it ends.
	public static String Calculation_Update(String str, int n, String calculation) {
		// n is the index of operation sign. We defined it in the main method.
		char operator = str.charAt(n);
		// We have already gone over the Operation_String(), we just need to assign it to a variable called opt (operation).
		String opt = Operation_String(str, operator);
		// We send opt (operation string), calculation statement, operator statement, first value and second value of the operation into the Operation() method.
		// It will give the latest form of calculation after performing the operation.
		calculation = Operation(opt, calculation, operator, first_value(opt, operator), second_value(opt, operator));
		return calculation;
	}
}

