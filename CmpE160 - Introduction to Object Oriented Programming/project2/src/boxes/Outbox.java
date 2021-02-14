
//DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE

package boxes;

import java.util.LinkedList;
import java.util.Queue;

import elements.Message;
import elements.User;

/**
 * Represents the outbox of the user. Stores the messages sent by the user.
 * 
 * @author Karahan Saritas
 *
 */
public class Outbox extends Box {
	/**
	 * Queue where sent messages are stored.
	 */
	private Queue sent;

	/**
	 * Constructs an outbox which belongs to the given user. Initializes queue where
	 * sent messages are stored.
	 * 
	 * @param owner User who owns this outbox
	 */
	public Outbox(User owner) {
		super(owner);
		sent = new LinkedList<>();
	}

	/**
	 * Adds the sent message to the queue.
	 * @param msg
	 */
	public void MessageSent(Message msg) {
		sent.add(msg);
	}

}



//DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE

