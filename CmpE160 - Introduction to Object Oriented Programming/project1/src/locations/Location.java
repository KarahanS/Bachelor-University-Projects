
//DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE

package locations;

import java.util.ArrayList;
import passengers.Passenger;

/**
 * Represents the locations with special ID's for each of them, coordinates of x
 * and y, two ArrayLists that store the passengers in the location currently and
 * the passengers who have visited the location so far.
 * 
 * @author Karahan Saritas
 * 
 */

public class Location {

	/**
	 * Identification number of the location.
	 */
	private int ID;
	/**
	 * The x-coordinate of the location.
	 */
	private double locationX;
	/**
	 * The y-coordinate of the location.
	 */
	private double locationY;
	/**
	 * List of the passengers who have been in this location.
	 */
	private ArrayList<Passenger> history = new ArrayList<Passenger>();
	/**
	 * List of the passengers who are in this location currently.
	 */
	private ArrayList<Passenger> current = new ArrayList<Passenger>();

	/**
	 * Constructs a location object with the given ID, x and y coordinates.
	 * 
	 * @param ID        identification number, unique for each location
	 * @param locationX the x-coordinate
	 * @param locationY the y-coordinate
	 */

	public Location(int ID, double locationX, double locationY) {
		this.ID = ID;
		this.locationX = locationX;
		this.locationY = locationY;
	}

	/**
	 * Returns the distance between this location and the location given as
	 * parameter
	 * 
	 * @param other another Location object
	 * @return distance between the locations
	 */

	public double getDistance(Location other) {
		double distance_x = this.locationX - other.getLocationX();
		double distance_y = this.locationY - other.getLocationY();
		return (Math.sqrt(distance_x * distance_x + distance_y * distance_y));
	}

	/**
	 * Adds the incoming passenger to the <code>current</code> ArrayList, and adds
	 * it to the <code>history</code> ArrayList if it's been not already included. A
	 * sorting algorithm is implemented in order to rearrange the passenger IDs in
	 * their ascending order.
	 * 
	 * @param p incoming passenger
	 */

	public void incomingPassenger(Passenger p) {
		if (p.getCurrentLocation().equals(this)) {
			this.current.add(p);
			if (!this.history.contains(p)) {
				this.history.add(p);
				// History Sorting
				for (int m = 0; m < this.history.size() - 1; m++) {
					if (this.history.get(m).getID() > this.history.get(m + 1).getID()) {
						Passenger temporary = this.history.get(m);
						this.history.set(m, this.history.get(m + 1));
						this.history.set(m + 1, temporary);
						m = -1;
					}
				}
			}
			// Current Sorting
			for (int m = 0; m < this.current.size() - 1; m++) {
				if (this.current.get(m).getID() > this.current.get(m + 1).getID()) {
					Passenger temporary = this.current.get(m);
					this.current.set(m, this.current.get(m + 1));
					this.current.set(m + 1, temporary);
					m = -1;
				}
			}

		}
	}

	/**
	 * Removes the outgoing passenger from the <code>current</code> ArrayList.
	 * 
	 * @param p outgoing passenger
	 */

	public void outgoingPassenger(Passenger p) {
		if (!p.getCurrentLocation().equals(this) && current.contains(p)) {
			current.remove(p);
		}
	}

	/**
	 * Gives the string format of the location, composed of its ID, x and y
	 * coordinates.
	 * 
	 * @return string indicating the location's properties
	 */
	public String toString() {
		String str_x = String.format("%.3f", this.locationX);
		String str_y = String.format("%.3f", this.locationY);
		return String.format("Location %d: (%s, %s)", this.ID, str_x.substring(0, str_x.length() - 1),
				str_y.substring(0, str_y.length() - 1));
	}

	/**
	 * Compares this location with the given object.
	 * 
	 * @return true if given object is the same location as this location, otherwise
	 *         false
	 */
	public boolean equals(Object other) {
		if (other instanceof Location) {
			Location l = (Location) other;
			return (this.locationX == l.getLocationX() && this.locationY == l.getLocationY());
		}
		return false;
	}

	/**
	 * @return x-coordinate of this location
	 */
	public double getLocationX() {
		return locationX;
	}

	/**
	 * @return y-coordinate of this location
	 */
	public double getLocationY() {
		return locationY;
	}

	/**
	 * @return list of the passengers currently here
	 */
	public ArrayList<Passenger> getCurrent() {
		return current;
	}

}

//DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE
