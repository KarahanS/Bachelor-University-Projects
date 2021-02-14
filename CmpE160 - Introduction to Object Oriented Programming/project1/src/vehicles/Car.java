
//DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE

package vehicles;

/**
 * Represents the car of a passenger. Creates a car object with passenger's
 * identification number, fuel amount and fuel consumption rate.
 * 
 * @author Karahan Saritas
 *
 */

public class Car {
	/**
	 * The identification number of the owner of the car.
	 */
	private int ownerID;
	/**
	 * Remaining amount of fuel in the tank.
	 */
	private double fuelAmount;
	/**
	 * The amount of fuel consumed per kilometer by the car
	 */
	private double fuelConsumption;

	/**
	 * Constructs a car with owner's identification number and fuel consumption
	 * rate.
	 * 
	 * @param ID              the identification number of the owner of the car.
	 * @param fuelConsumption the amount of fuel consumed per kilometer by the car
	 */
	public Car(int ID, double fuelConsumption) {
		this.ownerID = ID;
		this.fuelConsumption = fuelConsumption;
	}

	/**
	 * Refuels the tank of the car with given amount of fuel.
	 * 
	 * @param amount amount of fuel to add
	 */
	public void refuel(double amount) {
		if (amount >= 0)
			this.fuelAmount += amount;
	}

	/**
	 * Consumes the given amount of fuel
	 * 
	 * @param amount amount of fuel to consume
	 */
	public void consume(double amount) {
		if (amount >= 0)
			this.fuelAmount -= amount;
	}

	/**
	 * @return the amount of fuel left in the tank
	 */
	public double getFuelAmount() {
		return fuelAmount;
	}

	/**
	 * @return the amount of fuel consumed per kilometer by the car
	 */
	public double getFuelConsumption() {
		return fuelConsumption;
	}

}

//DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE
