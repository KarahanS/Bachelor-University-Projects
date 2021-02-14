
//DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE

package vehicles;

import locations.Location;

/**
 * Represents general properties of a public transportation vehicle. It takes an
 * identification number, unique for each vehicle and takes four coordinates
 * indicating a rectangular area for operation range.
 * 
 * @author Karahan Saritas
 *
 */

public abstract class PublicTransport {
	/**
	 * Represents an identification number, unique for each vehicle
	 */
	private int ID;
	/**
	 * Represents the corner coordinates of the rectangular area for operation
	 * range.
	 */
	private double x1, y1, x2, y2;

	/**
	 * Constructs a public transportation vehicle with the given identification
	 * number and coordinates to create a rectangular area.
	 * 
	 * @param ID identification number, unique for each public transportation
	 *           vehicle
	 * @param x1 x-coordinate of the first corner
	 * @param y1 y-coordinate of the first corner
	 * @param x2 x-coordinate of the second corner
	 * @param y2 y-coordinate of the second corner
	 */

	public PublicTransport(int ID, double x1, double y1, double x2, double y2) {
		this.ID = ID;
		this.x1 = x1;
		this.y1 = y1;
		this.x2 = x2;
		this.y2 = y2;
	}

	/**
	 * Checks if vehicle is able to travel between given two locations. At first, it
	 * checks if the arrival location is same with the departure location. If not,
	 * it takes the minimum and maximum coordinates in order to generate a
	 * rectangular operation field. Then it controls whether or not given departure
	 * and arrival locations are within the boundaries of the operation field.
	 * 
	 * @param departure location, transportation vehicle is supposed to leave
	 * @param arrival   location, transportation vehicle is supposed to arrive
	 * @return true if locations are within the operation field and they are
	 *         different from each other, otherwise false
	 */
	public boolean canRide(Location departure, Location arrival) {
		if (departure.equals(arrival))
			return false;
		double x_min = Math.min(x1, x2);
		double x_max = Math.max(x1, x2);
		double y_min = Math.min(y1, y2);
		double y_max = Math.max(y1, y2);
		return (departure.getLocationX() <= x_max && departure.getLocationX() >= x_min
				&& departure.getLocationY() <= y_max && departure.getLocationY() >= y_min
				&& arrival.getLocationX() <= x_max && arrival.getLocationX() >= x_min && arrival.getLocationY() <= y_max
				&& arrival.getLocationY() >= y_min);

	}

}

//DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE
