import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintStream;
import java.util.Scanner;

public class KS2018400174 {
	public static void main(String[] args) 
	throws FileNotFoundException, IOException
	{
		// We take two arguments as integer (mode) and String (file name) respectively.
		int mode = Integer.parseInt(args[0]);
		String input = args[1];
		// Declaring a scanner variable to read the contents of the input.ppm
		Scanner console = new Scanner(new File(input));
		// We get the header, number of columns,rows and maximum value from the input.
		String header = console.nextLine();  
		int column = console.nextInt();
		int row = console.nextInt();
		int max_value = console.nextInt();
		
		// Creating the 3D Array
		int[][][] RGB_Values =  Original_Array(row, column, console);
		// Array consists of all RGB values.
		// Writing a new file.
		if (mode==0) {
			Output("output.ppm", header, column, row, max_value, RGB_Values);
		}

		// Writing the black-and-white version.
		if(mode ==1) {

			// 3 for loops, standing for rows, columns and channels respectively.
			for(int r=0; r<row; r++) {
				for(int c=0; c<column; c++) {
					// We declare a variable named sum in order to store RGB values of each channel.
					int sum=0;
					for(int i=0; i<3; i++) {
						sum+= RGB_Values[r][c][i];
					}
					// We take the average of the sum in order to get a black-and-white picture.
					int average = sum/3;
					// Printing the RGB values to the output.
					for(int i=0;i<3;i++) {
						RGB_Values[r][c][i]=average;
					}		
				}	
			}
			// Creating the output file named black-and-white.ppm. 
			Output("black-and-white.ppm", header, column, row, max_value, RGB_Values);
			// Black-and-white version is completed.
		}
		
		// Taking filter
		if(mode ==2) {
			// We take the third argument as filter.
			String filter = args[2];
			// Declaring a scanner variable to read the content of the filter.
		Scanner console_filter = new Scanner(new File(filter));
		// We take the dimensions of the filter matrix.
		String dimension = console_filter.nextLine().substring(0,1);
		int dim = Integer.parseInt(dimension);
		// We create a filter array according to the dimension we took before.
		// This array will include the numbers we need to multiply with RGB values.
		int[][] filter_array = new int[dim][dim];
		// Taking the content of filter with two for loops.
		for (int i=0; i<dim; i++) {
			for(int m=0; m<dim; m++) {
				filter_array[i][m]=console_filter.nextInt();			
		}
	}
		// Filter is completed.
		// We create a new file named convolution.ppm.
		File convolution= new File("convolution.ppm");
		convolution.createNewFile();
		// Header is same for all ppm files we are dealing with. 
		// In convolution, we are going to lose some pixels. 
		// So we will have different row and column values.
		PrintStream write3 = new PrintStream(convolution);
		write3.println(header);
		write3.print(column-(dim-1));
		write3.println(" "+(row-(dim-1)));
		write3.println(max_value);
		
		// First for loop to indicate row number.
		for(int r=0; r<=row-dim; r++) {
			// Second for loop to indicate column number.
				 for(int c=0; c<=column-dim; c++){
					 // We assign a variable named total to store the sums we get from each channel.
					 int total=0;
					 // Third for loop to indicate channel number.
					 for(int i=0; i<3; i++) {
						 // We assign another variable named sum that stores the results of multiplication process.
						 int sum=0;
						 // Fourth for loop to indicate the number of rows we need to examine with filter for each case.
					 for(int sub_r=0; sub_r<dim; sub_r++) {	
						 // Fifth for loop to indicate the number of columns we need to examine with filter for each case.
						for(int sub_c=0; sub_c<dim; sub_c++) {
							// We declare a variable named matrix which consists of the number we will use in multiplication.
							int matrix = RGB_Values[sub_r+r][sub_c+c][i];
							sum+=matrix*filter_array[sub_r][sub_c];
							}	
						}
					 // If sum is below 0, we will make it equal to 0. If sum is above 255, we will make it equal to 255.
					 if(sum<0)
						 sum=0;
					 if(sum>255)
						 sum=255;
					 total+= sum;
				 }
					 // We divide the total by 3 in order to get an average for three different RGB channels.
					 for(int i=0; i<3; i++) 
					 write3.print((total/3)+" ");
					 write3.print("\t");
				 }
				 write3.println();
				}
		 write3.close();
		}
		// Convolution is completed.
		
		// Quantization part
		if(mode==3) {
			// We create a new array that consists of four dimensions.
			// Aim of this array is to remind us the pixels we visited so that we won't visit them again.
			// For now, all values correspond to zero. As we start to visit the channels,
			// channels we visited will be marked as one in the array.
			int[][][][] Store = new int[row][column][3][1];
			// We get the range as an argument.
			String range_value = args[2];
			int range = Integer.parseInt(range_value);		
			
			// We will examine each channel. First we will start with red,
			// visit every column for first row and go row by row.
			// We will implement same procedure for green and blue.
			for(int channel=0; channel<3; channel++) {
				for (int r=0; r<row; r++) {
					for(int c=0; c<column; c++) {
						// We change the content of RGB_Values by changing the neighbors
						// in the range. This process is done by a method named Recursion.
						RGB_Values=Recursion(Store, RGB_Values, r,c,channel,range);
						}
					}
				}
			// After changing RGB_Values Array, we can print out the contents of it to a file named quantized.ppm.
			Output("quantized.ppm", header, column, row, max_value, RGB_Values);
			}
		}	
		
	// Recursion method is written in order to visit every neighbor (also neighbors of these neighbors which satisfy the requirements)
	// of each pixel recursively. It takes six parameters. Store Array is taken in order to mark the pixels we visited so far.
	// RGB_Values is taken since it is the array representation of the image we are going to inspect. 
	// r stands for row.
	// c stands for column.
	// Channel and range integers are also taken, so that we can examine neighbors easily.
	// This method will be used to check neighbors of each pixel. If one of the neighbors satisfies the conditions, 
	// we change its value, mark its location in the Store Array and call the recursion method again.
		public static int[][][] Recursion(int[][][][] Store, int[][][] RGB_Values, int r, int c, int channel, int range) {
			// We need to check whether the pixel we are about to examine was visited before. 
			if(Store[r][c][channel][0]==0)  {
				// At first, we examine the neighbors located at row+1 and row-1. 
				
				// If our row value is the last row, we don't look to row+1.
				if(( r!=RGB_Values.length-1) &&(Math.abs(RGB_Values[r+1][c][channel]-RGB_Values[r][c][channel])<=range)  
						&& (Store[r+1][c][channel][0]==0)) {
					RGB_Values[r+1][c][channel]=RGB_Values[r][c][channel];
					Store[r][c][channel][0]=1;
	
					RGB_Values = Recursion(Store, RGB_Values, r+1, c, channel, range);
		
				    }
				// If our row value is the first row, we don't look to row-1.
				    if( r!=0 && (Math.abs(RGB_Values[r-1][c][channel]-RGB_Values[r][c][channel])<=range) && 
							Store[r-1][c][channel][0]== 0) {
						RGB_Values[r-1][c][channel]=RGB_Values[r][c][channel];
						Store[r][c][channel][0]=1;

						RGB_Values = Recursion(Store, RGB_Values, r-1, c, channel, range);
		
					}
				    // Secondly we examine the neighbors located at column+1 and column-1.
				    // If our column value is the last column, we don't look to column+1.
				    if(c!=RGB_Values[0].length-1 && (Math.abs(RGB_Values[r][c+1][channel]-RGB_Values[r][c][channel])<=range) &&  
							Store[r][c+1][channel][0]==0 ) {
							RGB_Values[r][c+1][channel]=RGB_Values[r][c][channel];
							Store[r][c][channel][0]=1;
							RGB_Values = Recursion(Store, RGB_Values, r, c+1, channel, range);

					}
				  // If our column value is the first column, we don't look to column-1.
					if( (c!=0  && Math.abs(RGB_Values[r][c-1][channel]-RGB_Values[r][c][channel])<=range)  &&
							Store[r][c-1][channel][0]==0) {
						RGB_Values[r][c-1][channel]=RGB_Values[r][c][channel];
						Store[r][c][channel][0]=1;
						RGB_Values = Recursion(Store, RGB_Values, r, c-1, channel, range);

					}
					// If our channel is green, we don't look to channel+1.
			    if(channel!=2 && (Math.abs(RGB_Values[r][c][channel+1]-RGB_Values[r][c][channel])<=range) && 
						Store[r][c][channel+1][0]==0) {
					RGB_Values[r][c][channel+1]=RGB_Values[r][c][channel];
					Store[r][c][channel][0]=1;
					RGB_Values = Recursion(Store, RGB_Values, r, c, channel+1, range);
				
				}
			 // If our channel is red, we don't look to channel-1.
			    if(channel!=0 && (Math.abs(RGB_Values[r][c][channel-1]-RGB_Values[r][c][channel])<=range) && 
			    		Store[r][c][channel-1][0]==0) {
					RGB_Values[r][c][channel-1]=RGB_Values[r][c][channel];
					Store[r][c][channel][0]=1;
					RGB_Values = Recursion(Store, RGB_Values, r, c, channel-1, range);
				}
			    
			    }
			Store[r][c][channel][0]=1;
		    return RGB_Values;
		}
		
		// Output method is written in order to print out the content of an array representing
		// the last form of the image. It takes a file name, header of the image, number of 
		// columns and rows, maximum value and the array itself. 
 		public static void Output(String file, String header, int column, int row, int max_value, int[][][] RGB_Values) throws IOException {
 			// We create a new file.
			File output = new File(file);
			output.createNewFile();
			PrintStream write = new PrintStream(output);
			// We print out the header section including column, row and maximum value.
			write.println(header);
			write.print(column);
			write.println(" "+row);
			write.println(max_value);
			// We are using three nested for loops to print out
			// the contents of RGB_Values array, which basically represents the image.
			for(int r=0; r<row; r++) {
				for(int c=0; c<column; c++) {
					for(int i=0; i<3; i++) {
						write.print(RGB_Values[r][c][i]+" ");
					}
					write.print("\t");
				}
				write.println();
			}
			write.close();
			
		}	
 		
 		// Original_Array is created in order to design an array
 		// which will represent the ppm image.
 		// We will be using this array throughout the project.
 		// This method takes row and column values, also a scanner variable
 		// to read the arguments.
	public static int[][][] Original_Array(int row, int column, Scanner console){
		int[][][] RGB_Values = new int[row][column][3];
		// We fill the array with integers from the input file one by one.
		for(int r=0; r<row; r++) {
			for(int c=0; c<column; c++) {
				for(int i=0; i<3; i++) {
					RGB_Values[r][c][i]= console.nextInt();
				}
			}
		}	
		return RGB_Values;
	}
}
