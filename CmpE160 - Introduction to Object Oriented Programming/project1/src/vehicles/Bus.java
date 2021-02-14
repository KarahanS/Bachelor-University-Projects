
//DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE

package vehicles;

import passengers.DiscountedPassenger;
import passengers.Passenger;

/**
 * Represents a bus with identification number and four coordinates indicating a
 * rectangular operation field. It inherits publicTransport abstract class.
 * 
 * @author Karahan Saritas
 * @see PublicTransport
 */
public class Bus extends PublicTransport {

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

	public Bus(int ID, double x1, double y1, double x2, double y2) {
		super(ID, x1, y1, x2, y2);
	}

	/**
	 * Returns the price passenger has to pay to travel by bus. It checks if the
	 * passenger is a discounted passenger or standard passenger. Regardless of the
	 * distance, bus fare is fixed at 2 liras for standard passengers and 1 lira for
	 * discounted passenger.
	 * 
	 * @param other passenger who uses the bus
	 * @return price passenger has to pay for the travel
	 */
	public double getPrice(Object other) {
		if (other instanceof Passenger) {
			Passenger o = (Passenger) other;
			if (o instanceof DiscountedPassenger) {
				return 1.0;
			} else {
				return 2;
			}
		} else
			return 0;
	}
}

//DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE
