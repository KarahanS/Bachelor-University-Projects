
package interfaces;

import locations.*;
import vehicles.*;

public interface usePublicTransport {
	public void ride(PublicTransport p, Location l);
	public void refillCard(double amount);
}

