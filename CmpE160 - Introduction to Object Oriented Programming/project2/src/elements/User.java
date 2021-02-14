
//DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE
package elements;

import java.util.ArrayList;
import boxes.Inbox;
import boxes.Outbox;

/**
 * Represents the users with unique ID's for each of them, an inbox for messages
 * received and an outbox for messages sent, and an arrayList to store the
 * friends.
 * 
 * @author Karahan Saritas
 *
 */

public class User {
	/**
	 * Identification number of this user.
	 */
	private int id;
	/**
	 * An inbox object to store the upcoming messages.
	 */
	private Inbox inbox;
	/**
	 * An outbox object to store the sent messages.
	 */
	private Outbox outbox;
	/**
	 * An arrayList representing the friend list of the user.
	 */
	private ArrayList<User> friends;

	/**
	 * Constructs a user object with the given ID. Assigns new inbox and outbox
	 * objects.
	 * 
	 * @param id identification number, unique for each user
	 */
	public User(int id) {
		this.id = id;
		this.friends = new ArrayList<>();
		this.inbox = new Inbox(this);
		this.outbox = new Outbox(this);
	}

	/**
	 * Adds the given user as a friend if he is not already friend of this user.
	 * Also adds this user to the friend list of the given user.
	 * 
	 * @param other User to be added as a friend
	 */
	public void addFriend(User other) {
		if (!friends.contains(other)) {
			this.friends.add(other);
		}
		if (!other.friends.contains(this)) {
			other.friends.add(this);
		}
	}

	/**
	 * Removes the given user from the friend list if he is present in the list.
	 * Also removes this user from the friend list of the given user.
	 * 
	 * @param other User to be removed from the friend list
	 */
	public void removeFriend(User other) {
		if (friends.contains(other)) {
			this.friends.remove(other);
		}
		if (other.friends.contains(this)) {
			other.friends.remove(this);
		}
	}

	/**
	 * Returns true if this user and the given user are friends.
	 * 
	 * @param other User to be checked if he is friend with this user
	 * @return true if this user and the given user are friends, false otherwise
	 */
	public boolean isFriendsWith(User other) {
		return (this.friends.contains(other) && other.friends.contains(this));
	}

	/**
	 * Constructs a message with the given body and sends it to the given receiver
	 * at the given time. Adds the message to the outbox of this user.
	 * 
	 * @param receiver User who gets the message
	 * @param body     Content of the message
	 * @param time     Moment when message is sent
	 * @param server   Coordinator of the system
	 */
	public void sendMessage(User receiver, String body, int time, Server server) {
		Message msg = new Message(this, receiver, body, server, time);
		this.outbox.MessageSent(msg);

	}

	/**
	 * @return ID of this user
	 */
	public int getId() {
		return id;
	}

	/**
	 * @return Inbox of this user
	 */
	public Inbox getInbox() {
		return inbox;
	}
}




//DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE

