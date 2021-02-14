
//DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE

package passengers;

import interfaces.*;
import locations.Location;
import vehicles.*;

/**
 * Represents the passengers with ID's for each of them, a boolean indicating
 * whether or not passenger has a driver's license, card balance for public
 * transportation, a car object and a location object indicating the current
 * location of the passenger.
 * 
 * @author Karahan Saritas
 *
 */
public class Passenger implements ownCar, usePublicTransport {
	/**
	 * Identification number of this passenger.
	 */
	private int ID;
	/**
	 * Indicator that shows whether or not this passenger has a driver's license.
	 */
	private boolean hasDriversLicense;
	/**
	 * The remaining balance in the travel card for public transportation.
	 */
	private double cardBalance;
	/**
	 * The car that belongs to this passenger.
	 */
	private Car car;
	/**
	 * This passenger's current location.
	 */
	private Location currentLocation;

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

	public Passenger(int ID, boolean hasDriversLicense, Location l) {
		this.ID = ID;
		this.hasDriversLicense = hasDriversLicense;
		this.currentLocation = l;
		l.incomingPassenger(this);
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

	public Passenger(int ID, Location l, double fuelConsumption) {
		this.ID = ID;
		this.currentLocation = l;
		this.car = new Car(ID, fuelConsumption);
		this.hasDriversLicense = true;
		l.incomingPassenger(this);

	}

	/**
	 * Changes the location of this passenger using a public transportation vehicle.
	 * At first, it checks if the public transportation vehicle is able to travel
	 * between the current location and the destination.
	 * 
	 * Then it checks which public transportation type passenger is going to use and
	 * if his/her card balance will be enough to pay the price of the travel. Then
	 * card balance will be reduced according to the price of the travel. Contents
	 * of the History and Current ArrayLists will be changed. Eventually,
	 * passenger's location will be changed to destination location.
	 * 
	 * @param p public transportation vehicle
	 * @param l destination passenger is supposed to go
	 * 
	 */
	public void ride(PublicTransport p, Location l) {
		if (p.canRide(this.currentLocation, l)) {
			if (p instanceof Bus && this.cardBalance >= ((Bus) p).getPrice(this)) {
				this.cardBalance -= ((Bus) p).getPrice(this);
				Location current = this.currentLocation;
				this.currentLocation = l;
				current.outgoingPassenger(this);
				this.currentLocation.incomingPassenger(this);
			} else if (p instanceof Train && this.cardBalance >= ((Train) p).getPrice(this, currentLocation, l)) {
				this.cardBalance -= ((Train) p).getPrice(this, currentLocation, l);
				Location current = this.currentLocation;
				this.currentLocation = l;
				current.outgoingPassenger(this);
				this.currentLocation.incomingPassenger(this);
			}
		}
	}

	/**
	 * Changes the location of this passenger using his/her own car. At first, it
	 * checks if passenger has a car, then calculates the distance between current
	 * location and destination. It will compare the fuel amount of the car with
	 * necessary fuel amount to arrive the destination. If the car has sufficient
	 * fuel,Contents of the History and Current ArrayLists will be changed.
	 * Eventually, passenger's location will be changed to destination location.
	 * 
	 * @param l destination passenger is supposed to go
	 */

	public void drive(Location l) {
		if (this.car != null && this.hasDriversLicense) {
			double distance = currentLocation.getDistance(l);
			if (distance!=0 && car.getFuelAmount() >= (car.getFuelConsumption() * distance)) {
				Location current = this.currentLocation;
				this.currentLocation = l;
				current.outgoingPassenger(this);
				this.currentLocation.incomingPassenger(this);
				car.consume(car.getFuelConsumption() * distance);
			}
		}
	}

	/**
	 * Refuels the car using a try-catch statement to avoid getting any error if
	 * passenger doesn't have a car.
	 * 
	 * @param amount fuel amount to add
	 * @exception NullPointerException if this car is not initialized.
	 */
	public void refuel(double amount) {
		try {
			this.car.refuel(amount);
		} catch (Exception e) {
		}
	}

	/**
	 * Purchases a new car for the passenger regardless of his/her having a car
	 * before. Then this passenger will get a driver's license.
	 * 
	 * @param fuelConsumption the amount of fuel consumed per kilometer by the car
	 */
	public void purchaseCar(double fuelConsumption) {
		this.car = new Car(this.ID, fuelConsumption);
		this.hasDriversLicense = true;
	}

	/**
	 * Refills the travel card of the passenger. Before adding the amount, it checks
	 * if the amount is bigger than or equal to zero.
	 * 
	 * @param amount amount of money that is added to the travel card
	 */
	public void refillCard(double amount) {
		if (amount >= 0)
			this.cardBalance += amount;
	}

	/**
	 * Returns the string representation of a passenger object. If this passenger
	 * has a car, passenger ID and the remaining fuel amount with 2 digits after
	 * decimal point will be returned as a string. If the passenger doesn't have a
	 * car, passenger ID and remaining card balance with 2 digits after decimal
	 * point will be returned as a string.
	 * 
	 */
	public String toString() {
		if (this.car != null) {
			String str = String.format("%.3f", this.car.getFuelAmount());
			return String.format("Passenger %d: %s", this.ID, str.substring(0, str.length() - 1));
		} else {
			String str = String.format("%.3f", this.cardBalance);
			return String.format("Passenger %d: %s", this.ID, str.substring(0, str.length() - 1));
		}
	}

	/**
	 * @return identification number of this passenger
	 */
	public int getID() {
		return ID;
	}

	/**
	 * @return current location of this passenger
	 */
	public Location getCurrentLocation() {
		return currentLocation;
	}

}

//DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE
