
//DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE


package elements;

/**
 * Represents the messages with unique ID's for each of them, a body (text), a
 * sender, a receiver and a sender. Messages also have time stamps showing the
 * time they are sent, received and read.
 * 
 * @author Karahan Saritas
 *
 */
public class Message implements Comparable<Message>{
	/**
	 * Number of total messages in the program.
	 */
	private static int numOfMessages = 0;
	/**
	 * Identification number of this message.
	 */
	private int id;
	/**
	 * Content (text) in this message.
	 */
	private String body;
	/**
	 * User who sends this message.
	 */
	private User sender;
	/**
	 * User who receives this message.
	 */
	private User receiver;
	/**
	 * Time when this message is sent.
	 */
	private int timeStampSent;
	/**
	 * Time when this message is read.
	 */
	private int timeStampRead;
	/**
	 * Time when this message is received.
	 */
	private int timeStampReceived;

	/**
	 * Constructs a message with the given sender, receiver and text. Gives an ID to
	 * the message according to the number of messages. Assigns the timeStampSent to
	 * the given time and adds the message to the server.
	 * 
	 * @param sender   User who sends this message
	 * @param receiver User who receives this message
	 * @param body     Text of this message
	 * @param server   Coordinator of the system
	 * @param time     Moment when this message is created and sent
	 */
	public Message(User sender, User receiver, String body, Server server, int time) {
		this.id = numOfMessages;
		numOfMessages++;
		this.sender = sender;
		this.receiver = receiver;
		this.body = body;
		this.timeStampSent = time;
		this.timeStampRead = -1;
		this.timeStampReceived = -1;
		server.AddMessage(this);

	}

	/**
	 * @return ID of this message
	 */
	public int getId() {
		return this.id;
	}

	/**
	 * @return body (text) of this message
	 */
	public String getBody() {
		return this.body;
	}

	/**
	 * Compares the given message with this message in terms of body length.
	 * 
	 * @param o Message to be compared with this message
	 * @return 1 if this message is longer than the given message, -1 if this
	 *         message is shorter than the given message and 0 if both messages have
	 *         same number of characters.
	 */
	public int compareTo(Message o) {
		int firstLength = this.body.length();
		int secondLength = o.body.length();
		if (firstLength > secondLength) {
			return 1;
		} else if (firstLength < secondLength) {
			return -1;
		} else {
			return 0;
		}
	}

	/**
	 * Checks if the given message is equal to this message.
	 * 
	 * @return true if ID of this message is equal to the ID of the given message,
	 *         false otherwise.
	 */
	public boolean equals(Object o) {
		if (o instanceof Message) {
			Message other = (Message) o;
			return (this.id == other.id);
		}
		return false;
	}

	/**
	 * Gives the string form of this message with its sender, receiver, body and
	 * time stamps showing when this message is received and read if it's been
	 * received/read.
	 * 
	 * @return String representation of this message
	 */
	public String toString() {
		String str = "";
		String received = "";
		String read = "";
		if (timeStampReceived != -1) {
			received += timeStampReceived;
		}
		if (timeStampRead != -1) {
			read += timeStampRead;
		}
		str += ("\tFrom: " + this.sender.getId() + " To: " + this.receiver.getId()+"\n");
		str += ("\tReceived: " + received + " Read: " + read+"\n");
		str += ("\t" + body);
		return str;
	}

	/**
	 * @return User who receives this message
	 */
	public User getReceiver() {
		return receiver;
	}

	/**
	 * @return User who sends this message
	 */
	public User getSender() {
		return sender;
	}

	/**
	 * @param timeStampSent timeStampsent to set
	 */
	public void setTimeStampSent(int timeStampSent) {
		this.timeStampSent = timeStampSent;
	}

	/**
	 * @param timeStampRead timeStampRead to set
	 */
	public void setTimeStampRead(int timeStampRead) {
		this.timeStampRead = timeStampRead;
	}


	/**
	 * @param timeStampReceived timeStampReceived to set
	 */
	public void setTimeStampReceived(int timeStampReceived) {
		this.timeStampReceived = timeStampReceived;
	}

}

//DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE

