
//DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE

package passengers;
import locations.Location;

/**
 * Represents a standard passenger who doesn't get discount
 * while using public transportation. It inherits Passenger 
 * superclass and creates a discounted passenger.
 * 
 * @author Karahan Saritas
 * @see Passenger
 *
 */

public class StandardPassenger extends Passenger {	
	
	/**
	 * Constructs a passenger object with the given identification number, a boolean
	 * indicating whether the passenger has a driver's license and a location object
	 * indicating current location of the passenger.
	 * 
	 * @param ID                identification number, unique for each passenger
	 * @param hasDriversLicense a boolean that gives <code>true</code> if the
	 *                          passenger has a driver's license
	 * @param l                 current location of the passenger
	 */
	
	public StandardPassenger(int ID, boolean hasDriversLicense, Location l) {
		super(ID, hasDriversLicense, l);
	}
	
	/**
	 * Constructs a passenger object with the given identification number, a
	 * location object indicating current location of the passenger and the fuel
	 * consumption rate of the car that belongs to the passenger. A new car object
	 * is initialized with owner ID and fuel consumption rate. Passenger will have a
	 * driver's license.
	 * 
	 * @param ID              identification number, unique for each passenger
	 * @param l               current location of the passenger
	 * @param fuelConsumption the amount of fuel consumed per kilometer by the car
	 */
	public StandardPassenger(int ID, Location l, double fuelConsumption) {
		super(ID, l, fuelConsumption);
	}
}

//DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE
