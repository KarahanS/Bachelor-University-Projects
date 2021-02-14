
//DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE


package executable;

import java.io.*;
import java.util.*;

import elements.*;

/**
 * Reads an input file and implements the necessary actions according to the
 * corresponding parameters and events. Logs the results to an output file. At
 * first, creates a server with the given capacity and stores the users in an
 * arrayList. There are 10 types of events. Time increases by one each time a
 * process is executed and increases according to the given value when one of
 * the reading processes is completed.
 * 
 * 0- Creates a message and sends it from the given sender to the given
 * receiver. Message is stored in the server until receiver fetches it from the
 * server to his/her inbox. Then it checks the server load if it's necessary to
 * give a warning about the capacity or delete the all messages.
 * 
 * 1- Given user receives all the messages that are sent to him/her from the
 * server. Then it checks the server load if it's necessary to give a warning
 * about the capacity or delete the all messages.
 * 
 * 2- Given user reads a certain amount of messages. If the given number is 0,
 * then it reads all. Time is increased by the given value since it can take
 * more than 1 time unit to read messages.
 * 
 * 21- Given user reads all the messages from a specific sender. Time is
 * increased by the given value since it can take more than 1 time unit to read
 * messages.
 * 
 * 22- Given user reads a specific message if it's present in his/her inbox.
 * 
 * 3- Makes given two users friends so that they can receive and read each
 * other's messages.
 * 
 * 4- Removes each users from their friends lists. This prevents them from
 * receiving and reading each other's messages.
 * 
 * 5- Deletes all messages from the queue of the server. Current size of the
 * server is set to zero.
 * 
 * 6- Prints out the current size of the server.
 * 
 * 61- Prints the details about the last message a user has read. Details
 * include its receiver's ID, sender's ID, time stamps showing when it is
 * received and when it is read, and the body of the message
 * 
 * @author Karahan Saritas
 *
 */
public class Main {
	public static void main(String[] args) throws FileNotFoundException, IOException {

		Scanner input = new Scanner(new File(args[0]));
		PrintStream output = new PrintStream(new File(args[1]));
		PrintStream write = new PrintStream(output);
		ArrayList<User> users = new ArrayList<>();

		int numberOfUsers = input.nextInt();
		int numberOfQueries = input.nextInt();
		long capacity = input.nextLong();

		Server server = new Server(capacity);
		int time = 0;

		for (int i = 0; i < numberOfUsers; i++) {
			users.add(new User(i));
		}
		for (int i = 0; i < numberOfQueries; i++) {
			int command = input.nextInt();
			// Send a message
			if (command == 0) {
				int senderID = input.nextInt();
				int receiverID = input.nextInt();
				String messageBody = "";
				while (!input.hasNextInt() && input.hasNext()) {
					messageBody += input.nextLine().substring(1);
				}

				if (senderID >= 0 && senderID < users.size() && receiverID >= 0 && receiverID < users.size()) {
					users.get(senderID).sendMessage(users.get(receiverID), messageBody, time, server);
					server.checkServerLoad(write);

				}

				// Receive a message
			} else if (command == 1) {

				int receiverID = input.nextInt();
				if (receiverID >= 0 && receiverID < users.size()) {
					users.get(receiverID).getInbox().receiveMessages(server, time);
					server.checkServerLoad(write);

				}

				// Read a certain amount of messages
			} else if (command == 2) {
				int receiverID = input.nextInt();
				int numberOfMessages = input.nextInt();
				if (receiverID >= 0 && receiverID < users.size()) {
					time += users.get(receiverID).getInbox().readMessages(numberOfMessages, time) - 1;
				}
				// Read all the messages from a sender
			} else if (command == 21) {
				int receiverID = input.nextInt();
				int senderID = input.nextInt();
				if (senderID >= 0 && senderID < users.size() && receiverID >= 0 && receiverID < users.size()) {
					time += users.get(receiverID).getInbox().readMessages(users.get(senderID), time) - 1;

				}

				// Read a specific message
			} else if (command == 22) {
				int receiverID = input.nextInt();
				int messageID = input.nextInt();
				if (receiverID >= 0 && receiverID < users.size()) {
					users.get(receiverID).getInbox().readMessage(messageID, time);
				}

				// Add a friend
			} else if (command == 3) {
				int id1 = input.nextInt();
				int id2 = input.nextInt();
				if (id1 >= 0 && id1 < users.size() && id2 >= 0 && id2 < users.size()) {
					users.get(id1).addFriend(users.get(id2));

				}

				// Remove a friend
			} else if (command == 4) {
				int id1 = input.nextInt();
				int id2 = input.nextInt();
				if (id1 >= 0 && id1 < users.size() && id2 >= 0 && id2 < users.size()) {
					users.get(id1).removeFriend(users.get(id2));

				}

				// Flush server
			} else if (command == 5) {
				server.flush();

				// Print the current size of the server
			} else if (command == 6) {
				write.println("Current load of the server is " + server.getCurrentSize() + " characters.");

				// Print the last message a user has read
			} else if (command == 61) {
				int userID = input.nextInt();
				if (userID >= 0 && userID < users.size()) {
					Message lastMsg = users.get(userID).getInbox().LastMessage();
					if (lastMsg != null) {
						write.println(lastMsg.toString());

					}
				}

			}
			time++;

		}
		

		
	}
}




//DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE

