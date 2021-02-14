
//DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE


package boxes;

import java.util.*;
import elements.*;

/**
 * Represents the inbox of the user. Both read and unread messages sent to the
 * user are stored in the user's inbox.
 *
 * @author Karahan Saritas
 *
 */
public class Inbox extends Box {
	/**
	 * Stack where unread messages are stored.
	 */
	private Stack unread;
	/**
	 * Queue where read messages are stored.
	 */
	private Queue read;

	/**
	 * Constructs an outbox which belongs to the given user. Initializes the stack
	 * in which unread messages are stored, and the queue in which read messages are
	 * stored.
	 * 
	 * @param user User who owns this inbox
	 */
	public Inbox(User user) {
		super(user);
		this.read = new LinkedList<>();
		this.unread = new Stack<>();
	}

	/**
	 * Gives the last message a user has had if any.
	 * 
	 * @return last message a user has had
	 */
	public Message LastMessage() {
		int size = read.size();
		Message last = null;
		for (int i = 0; i < size; i++) {
			last = (Message) read.poll();
			read.add(last);
		}
		return last;
	}

	/**
	 * Receives messages from the server, adds to the unread stack. This method also
	 * changes timeStampReceived with the given time.
	 * 
	 * @param server Coordinator of the system
	 * @param time   Moment when message is received
	 */
	public void receiveMessages(Server server, int time) {
		int size = server.getMsgs().size();
		for (int i = 0; i < size; i++) {
			Message msg = (Message) server.getMsgs().poll();
			if (msg.getSender().isFriendsWith(this.owner) && msg.getReceiver().getId() == this.owner.getId()) {
				msg.setTimeStampReceived(time);
				unread.push(msg);
				server.RemoveMessage(msg);
			} else {
				server.getMsgs().add(msg);
			}
		}
	}

	/**
	 * Reads a certain amount of messages from the unread stack. Adds the read
	 * messages to the read queue. If the num parameter is equal to zero, reads all
	 * messages.
	 * 
	 * @param num  amount of messages to be read
	 * @param time Moment when user started reading the messages
	 * @return updated time
	 */
	public int readMessages(int num, int time) {
		int increment = 0;
		if (num == 0 || num > this.unread.size()) {
			while (!unread.isEmpty()) {
				Message msg = (Message) unread.pop();
				msg.setTimeStampRead(time + increment);
				increment++;
				read.add(msg);
			}
		} else {
			for (int i = 0; i < num; i++) {
				Message msg = (Message) unread.pop();
				msg.setTimeStampRead(time + increment);
				increment++;
				read.add(msg);
			}
		}
		if (increment == 0)
			increment = 1;
		return increment;
	}

	/**
	 * Reads the given sender's messages.
	 * 
	 * @param sender User whose messages are going to be read
	 * @param time   Moment when user started reading messages
	 * @return updated time
	 */
	public int readMessages(User sender, int time) {
		int increment = 0;
		Stack<Message> temporary = new Stack<>();
		int size = unread.size();

		for (int i = 0; i < size; i++) {
			Message msg = (Message) unread.pop();
			if (msg.getSender().equals(sender)) {
				msg.setTimeStampRead(time + increment);
				increment++;
				read.add(msg);
			} else {
				temporary.push(msg);
			}
		}
		while (!temporary.isEmpty()) {
			unread.push(temporary.pop());
		}
		if (increment == 0)
			increment = 1;
		return increment;
	}

	/**
	 * Reads the message with the given ID number if it exists.
	 * 
	 * @param msgld ID number of the message to be read
	 * @param time  Moment when message is read
	 */
	public void readMessage(int msgld, int time) {
		Stack<Message> temporary = new Stack<>();
		while (!unread.isEmpty()) {
			Message msg = (Message) unread.pop();
			if (msg.getId() == msgld) {
				msg.setTimeStampRead(time);
				read.add(msg);
			} else {
				temporary.push(msg);
			}
		}
		while (!temporary.isEmpty()) {
			unread.push(temporary.pop());
		}
	}

}

//DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE

