
//DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE

package vehicles;

import locations.Location;
import passengers.DiscountedPassenger;
import passengers.Passenger;

/**
 * Represents a bus with identification number and four coordinates indicating a
 * rectangular operation field. It inherits publicTransport abstract class.
 * 
 * @author Karahan Saritas
 * @see PublicTransport
 */
public class Train extends PublicTransport {

	/**
	 * Constructs a bus with the given identification number and coordinates to
	 * create a rectangular area.
	 * 
	 * @param ID identification number, unique for each public transportation
	 *           vehicle
	 * @param x1 x-coordinate of the first corner
	 * @param y1 y-coordinate of the first corner
	 * @param x2 x-coordinate of the second corner
	 * @param y2 y-coordinate of the second corner
	 */
	public Train(int ID, double x1, double y1, double x2, double y2) {
		super(ID, x1, y1, x2, y2);
	}

	/**
	 * Returns the price passenger has to pay to travel by train. At first, it gets
	 * the distance between arrival and departure locations. Trains charge per stop.
	 * Stops are composed of 15-kilometers breaks and traveling one stop costs 5
	 * liras for standard passengers. Passenger will leave the train at the stop
	 * which is closest to the destination. Discounted passengers will pay %80 of
	 * the price.
	 * 
	 * @param other     passenger who uses the train
	 * @param departure location train is supposed to leave
	 * @param arrival   location train is supposed to arrive
	 * @return price passenger has to pay for the travel
	 */
	public double getPrice(Passenger other, Location departure, Location arrival) {
		double distance = departure.getDistance(arrival);
		double pay;
		if (distance % 15 < 7.5) {
			pay = (distance - (distance % 15)) / 15 * 5;
		} else {
			pay = (distance + (15 - (distance % 15))) / 15 * 5;
		}
		if (other instanceof DiscountedPassenger) {
			return pay * (4.0 / 5);
		} else {
			return pay;
		}
	}

}

//DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE
