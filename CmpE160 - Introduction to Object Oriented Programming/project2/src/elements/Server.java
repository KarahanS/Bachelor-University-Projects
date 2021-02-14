
//DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE
package elements;

import java.io.PrintStream;
import java.util.LinkedList;
import java.util.Queue;

/**
 * Represents the mechanism where all non-received messages are stored in a
 * first come, first served manner. It stores the messages and prints out
 * warning messages if necessary. Deletes all message if capacity is exceeded.
 * 
 * @author Karahan Saritas
 *
 */
public class Server {
	/**
	 * Capacity of the server.
	 */
	private long capacity;
	/**
	 * Total number of the characters of messages' bodies in the store.
	 */
	private long currentSize;
	/**
	 * A queue where non-received messages are stored.
	 */
	private Queue msgs;
	/**
	 * Current load of this server.
	 */
	private long currentLoad;

	/**
	 * Constructs a server with the given store capacity. Sets the currentSize and
	 * currentLoad to zero and initializes the queue where non-received messages are
	 * stored.
	 * 
	 * @param capacity capacity of the server
	 */
	public Server(long capacity) {
		this.capacity = capacity;
		this.currentSize = 0;
		this.msgs = new LinkedList<>();
		this.currentLoad = 0;

	}

	/**
	 * Checks the current load of the server. Prints the warnings about the
	 * capacity. If size exceeds the capacity, prints a warning and deletes all
	 * messages in the store.
	 * 
	 * @param printer a printer to print out the necessary warnings to the output
	 *                file
	 */
	public void checkServerLoad(PrintStream printer) {
		long oldLoad = this.currentLoad;
		this.currentLoad = (currentSize * 100) / capacity;
		if (currentLoad >= 100) {
			printer.println("Server is full. Deleting all messages...");
			this.flush();
		}

		else if ((oldLoad < 50 && currentLoad >= 50 && currentLoad < 80)
				|| (oldLoad >= 80 && currentLoad >= 50 && currentLoad < 80)) {
			printer.println("Warning! Server is 50% full.");
		} else if ((oldLoad < 80 && currentLoad >= 80)) {
			printer.println("Warning! Server is 80% full.");
		}

	}

	/**
	 * Removes the given message's body length from the current size of the server
	 * 
	 * @param msg Message to be removed from the server
	 */
	public void RemoveMessage(Message msg) {
		this.currentSize -= msg.getBody().length();
	}
	/**
	 * Adds the given message to the server and increases the current size by the message's body length
	 * @param msg Message to be added to the server
	 */
	public void AddMessage(Message msg) {
		this.currentSize += msg.getBody().length();
		this.msgs.add(msg);
	}

	/**
	 * Empties the queue, deletes all messages. Sets the current load and current size to zero.
	 */
	public void flush() {
		while (!this.msgs.isEmpty()) {
			this.msgs.poll();
		}
		this.currentLoad = 0;
		this.currentSize = 0;
	}

	/**
	 * @return current size of the server
	 */
	public long getCurrentSize() {
		return this.currentSize;
	}

	/**
	 * @return queue where non-received messages are stored
	 */
	public Queue getMsgs() {
		return msgs;
	}

}




//DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE

