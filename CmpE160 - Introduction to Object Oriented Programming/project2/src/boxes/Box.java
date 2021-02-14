
//DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE
package boxes;

import elements.User;

/**
 * Represents the parent class of inbox and outbox. Every box has an owner.
 * 
 * @author Karahan Saritas
 *
 */

public abstract class Box {
	/**
	 * User who owns this box.
	 */
	protected User owner;
	
	/**
	 * Constructs a box with the given owner.
	 * @param owner User who owns this box.
	 */
	public Box(User owner) {
		this.owner = owner;
	}

}





//DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE

