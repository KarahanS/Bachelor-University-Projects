
//DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE

package main;

import java.io.*;
import java.util.*;
import locations.*;
import passengers.*;
import vehicles.*;

/**
 * Reads an input file and implements the necessary actions according to the
 * commands related to the travel operations. All passengers, locations and
 * vehicles are kept in ArrayLists throughout the process. First location is
 * given as the origin point.
 * 
 * First command creates a passenger. Passenger can be a discounted or standard
 * passenger. Fuel consumption rate is given if he has a car and a different
 * constructor is called.
 * 
 * Second command creates a new location.
 * 
 * Third command creates a public transportation vehicle. At first, it takes the
 * type of the vehicle and creates a bus or a train accordingly.
 * 
 * 
 * Fourth command leads a passenger travel to a given location. Passenger uses a
 * bus, a train or his own car according to the given transportation type.
 * 
 * Fifth command leads a passenger to purchase a car. If he already has a car,
 * he changes his car with a new one.
 * 
 * Sixth command leads a passenger to refuel his/her car's tank.
 * 
 * Seventh command leads a passenger to refill his/her travel card balance.
 * 
 * At last, it prints out every location with passengers located in them. A
 * sorting algorithm is implemented in order to print out passengers in an
 * ascending order of identification numbers.
 * 
 * @author Karahan Saritas
 *
 */
public class Main {
	public static void main(String[] args) throws FileNotFoundException {

		Scanner input = new Scanner(new File(args[0]));
		PrintStream output = new PrintStream(new File(args[1]));
		ArrayList<Passenger> passengers = new ArrayList<Passenger>();
		ArrayList<Location> locations = new ArrayList<Location>();
		ArrayList<PublicTransport> vehicles = new ArrayList<PublicTransport>();

		Location l = new Location(0, 0, 0);
		locations.add(l);

		int operations = input.nextInt();

		for (int i = 0; i < operations; i++) {
			int command = input.nextInt();
			// Creating a passenger
			if (command == 1) {
				String type = input.next();
				boolean license = (input.nextInt() == 1) ? true : false;
				boolean hasACar = (input.nextInt() == 1) ? true : false;
				if (type.equals("D")) {
					DiscountedPassenger passenger;
					if (hasACar) {
						passenger = new DiscountedPassenger(passengers.size(), locations.get(0), input.nextDouble());
					} else {
						passenger = new DiscountedPassenger(passengers.size(), license, locations.get(0));
					}
					passengers.add(passenger);
				} else if (type.equals("S")) {
					StandardPassenger passenger;
					if (hasACar) {
						passenger = new StandardPassenger(passengers.size(), locations.get(0), input.nextDouble());
					} else {
						passenger = new StandardPassenger(passengers.size(), license, locations.get(0));
					}
					passengers.add(passenger);

				}

			}

			// Creating a location
			if (command == 2) {
				Location location = new Location(locations.size(), input.nextDouble(), input.nextDouble());
				locations.add(location);

			}
			// Creating a public transportation vehicle
			if (command == 3) {
				int typeOfVehicle = input.nextInt();
				if (typeOfVehicle == 1) {
					Bus bus = new Bus(vehicles.size(), input.nextDouble(), input.nextDouble(), input.nextDouble(),
							input.nextDouble());
					vehicles.add(bus);
				} else if (typeOfVehicle == 2) {
					Train train = new Train(vehicles.size(), input.nextDouble(), input.nextDouble(), input.nextDouble(),
							input.nextDouble());
					vehicles.add(train);
				} else {
					for (int m = 0; m < 4; m++)
						input.nextDouble();
				}

			}
			// Passenger travels to a location
			if (command == 4) {
				int passengerID = input.nextInt();
				int locationID = input.nextInt();
				int transportationType = input.nextInt();
				if (transportationType == 1) {
					if (passengerID >= 0 && passengerID < passengers.size() && locationID >= 0
							&& locationID < locations.size()) {
						int vehicleID = input.nextInt();
						if (vehicleID >= 0 && vehicles.size() > vehicleID && vehicles.get(vehicleID) instanceof Bus) {
							passengers.get(passengerID).ride(vehicles.get(vehicleID), locations.get(locationID));
						}
					} else
						input.nextInt();

				}
				if (transportationType == 2) {
					if (passengerID >= 0 && passengerID < passengers.size() && locationID >= 0
							&& locationID < locations.size()) {

						int vehicleID = input.nextInt();
						if (vehicleID >= 0 && vehicles.size() > vehicleID && vehicles.get(vehicleID) instanceof Train) {
							passengers.get(passengerID).ride(vehicles.get(vehicleID), locations.get(locationID));
						}
					} else
						input.nextInt();

				}
				if (transportationType == 3 && passengerID >= 0 && passengerID < passengers.size() && locationID >= 0
						&& locationID < locations.size()) {
					passengers.get(passengerID).drive(locations.get(locationID));

				}

			}
			// Passenger purchases a car
			if (command == 5) {
				int passengerID = input.nextInt();
				double fuelConsumption = input.nextDouble();
				if (passengerID >= 0 && passengerID < passengers.size()) {
					passengers.get(passengerID).purchaseCar(fuelConsumption);
				}
			}
			// Passenger refuels his/her car
			if (command == 6) {
				int passengerID = input.nextInt();
				double refuel = input.nextDouble();
				if (passengerID >= 0 && passengerID < passengers.size()) {
					passengers.get(passengerID).refuel(refuel);
				}

			}
			// Passenger refills his/her travel card
			if (command == 7) {
				int passengerID = input.nextInt();
				double travelCard = input.nextDouble();
				if (passengerID >= 0 && passengerID < passengers.size()) {
					passengers.get(passengerID).refillCard(travelCard);
				}
			}

		}

		// Output
		for (int i = 0; i < locations.size(); i++) {
			if (locations.get(i) != null) {
				if (i != 0)
					output.println();
				output.print(locations.get(i).toString());
				if (locations.get(i).getCurrent() != null) {

					for (int j = 0; j < locations.get(i).getCurrent().size(); j++) {
						output.println();
						output.print(locations.get(i).getCurrent().get(j).toString());
					}
				}
			}
		}

	}
}

//DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE
