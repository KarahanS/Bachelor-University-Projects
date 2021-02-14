public class KS2018400174 {
	public static void main(String[] args) {
		int stickmanHeight = Integer.parseInt(args[0]);
		int stairHeight = Integer.parseInt(args[1]);
		/* We have 4 major variables other than stickmanHeight and stairHeight throughout the process. 
		 * They are listed below with their tasks.
		 * 
		 * 1) stair ==> Main purpose of the stair variable is to determine how many frames there should be.
		 *              It will decrease one by one each time a frame is finished and a new one starts.
		 *              It is also going to be used to calculate the number of empty lines from above 
		 *              for each frame and spaces between the figure and the left side of each frame 
		 *              since number of empty lines varies according to the frame number and the number
		 *              of spaces from left side is proportional to the (stairHeight-stair)*3.
		 *              
		 * 2) interspace ==> This variable is used to generate the spaces between the stickman and the stairs.
		 *                   It takes the value of the stair variable at the very beginning of the first for 
		 *                   loop and decreases by one each time a line, which includes spaces between the 
		 *                   figure and the step of the stairs, is completed.
		 *                
		 * 3) line_count ==> This variable is just used to count the completed lines and give the number
		 *                   of the current line. When it reaches to the value of the stickmanHeight, steps of
		 *                   the stairs start to appear. At the beginning of the code, line_count is declared
		 *                   as (2 + stair), since the number of empty lines equals to the value of stair variable
		 *                   and line_count automatically increases by 2 with the lines including head and torso.
		 *                   
		 * 4) stars ==> stars variable is used to determine the number of stars which are going to fill the stairs
		 *              for each frame. It takes the value of 0 at the beginning and increases by one each time a
		 *              step is completely finished. Number of stars in a step is equal to stars*3 for each case.              
		 */
		int stair = stairHeight;                  
		for (; stair >= 0; stair--) {                                          // Value of the stair variable will decrease each time a new frame starts.
			int interspace = stair, line_count = 2 + stair, stars = 0;  
			for (int empty_lines = stair; empty_lines > 0; empty_lines--) {    // empty_lines represents the number
				System.out.println();                                          // of blank lines from above. 
			} 
			Head_and_Torso(stairHeight, stair);
			for (int body = (stickmanHeight - 3); body >= 1; body--) {         // body represents the number of body " | " parts.          
				Stickman(stairHeight, stair, " | ");
				line_count++;                                                  // line_count increases by one each time a " | " is completed.
				for (; line_count >= stickmanHeight; line_count--, interspace--, stars ++) {        			                                          
					Stairs(stars, interspace);                                 // When the value of line_count is equal to stickmanHeight,                                     		                                           
				}                                                              // program starts to generate the stairs. Each time a step
				System.out.println();                                          // is completed, interspace and line_count decreases, whereas
			}                                                                  // the value of stars increases.
			Legs(stairHeight, stair, stars,interspace);                        // This part generates the line with legs and value of stars increases by one.
			stars++;
			int left_side = stairHeight - stair;                               // left_side represents the number of blank spaces 
			for (; stars<= stairHeight; stars ++, left_side--) {               // between left side of the frame and the steps
				Stairs(stars, left_side);                                      // which stickman has passed so far.
				System.out.println();
			}
			System.out.println("\n\n");                                        // It leaves 3 empty lines after each frame.
		}
	} 
	/*  Stars_or_Spaces method is used to generate the stars or spaces according to the assigned values.
	 *  When b is assigned as " ", and a is assigned as one of the followings ( stairHeight - stair, interspace,
	 *  left_side ) it generates the spaces between the left side and the figure, figure and the stairs, left
	 *  side and the stairs according to the value of b respectively.
	 *  When a is assigned as stars and b is assigned as "*", it fills the steps with stars.
	 */
	public static void Stars_or_Spaces(int a, String b) {
		for (int e = (a) * 3; e > 0; e--) {
			System.out.print(b);
		} 
	}
	/*
	 *  Stickman is used to generate the parts of the figure. According to the value assigned
	 *  to the a variable, it prints out the corresponding part of the stickman. For example when 
	 *  a is " O ", it generates the head part.
	 */
	public static void Stickman(int stairHeight, int stair, String a) {
		Stars_or_Spaces(stairHeight - stair, " ");                               
		System.out.print(a);
	}
	/*
	 *  Stairs method is used to generate stairs and it calls Stars_of_Spaces method two times with
	 *  different variables assigned in it. Variable value is assigned as left_side and interspace
	 *  throughout the code.
	 */
	public static void Stairs(int stars, int a) {
		Stars_or_Spaces(a, " ");
		System.out.print("___|");
		Stars_or_Spaces(stars, "*");
		System.out.print("|");
	}
	/*
	 *  This method is used to create the part with legs. It calls Stickman method to generate figure and 
	 *  Stairs method to generate the corresponding step. Then it starts a new line.
	 */
	public static void Legs(int stairHeight, int stair, int stars, int interspace) {
		Stickman(stairHeight, stair, "/ \\");                    
		Stairs(stars, interspace);
		System.out.println();
	}
	/*
	 *  This method is used to generate head and arms of the figure. It calls the Stickman
	 *  method two times with different String values.
	 */
	public static void Head_and_Torso(int stairHeight, int stair) {
		Stickman(stairHeight, stair, " O ");
		System.out.println();
		Stickman(stairHeight, stair, "/|\\");
		System.out.println();
		
	}
}