
//DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE
package question;

import java.util.*;

/**
 * Represents each of the nodes in the Domain Name System tree structure. Each
 * node has a list of child nodes, a set of IP addresses of the domain it
 * represents, a queue that works as a process schedule and a boolean indicating
 * if the node has a valid domain name.
 * 
 * @author Karahan Saritas
 *
 */

public class DnsNode {
	/**
	 * List of the child nodes of this node. Stores the node objects and
	 * corresponding domain names.
	 */
	private Map<String, DnsNode> childNodeList;
	/**
	 * Indicator that shows if this node has a valid domain name.
	 */
	private boolean validDomain;
	/**
	 * Set of IP addresses of this node.
	 */
	private Set<String> ipAddresses;
	/**
	 * A queue to return IP addresses using the Round Robin algorithm.
	 */
	private Queue<String> q;

	/**
	 * Constructs a Domain Name System node with an empty list of child nodes, IP
	 * addresses and queue. Initializes validDoman as false.
	 */
	public DnsNode() {
		this.childNodeList = new HashMap<>();
		this.ipAddresses = new HashSet<>();
		this.validDomain = false;
		this.q = new LinkedList<>();
	}

	/**
	 * Adds a child node to this node in the tree structure with the given domain
	 * name and node.
	 * 
	 * @param domainName name of the domain given node represents
	 * @param Node       node to be added as child node
	 */
	public void AddSubNode(String domainName, DnsNode Node) {
		this.childNodeList.put(domainName, Node);
	}

	/**
	 * Removes the child node with the given domain name.
	 * 
	 * @param domainName name of the domain given node represents
	 */
	public void RemoveSubNode(String domainName) {
		if (childNodeList.containsKey(domainName)) {
			childNodeList.remove(domainName);
		}
	}

	/**
	 * Adds an IP address to this node. Also adds the address to the queue.
	 * 
	 * @param ipAddress IP address to be added
	 */
	public void AddIpAddress(String ipAddress) {
		if (!this.ipAddresses.contains(ipAddress)) {
			this.ipAddresses.add(ipAddress);
			this.q.add(ipAddress);
			this.validDomain = true;
		}
	}

	/**
	 * Removes an IP address from the node. Also removes it from the queue. After
	 * removing, if there is no IP address left in the list, assigns the validDomain
	 * as false.
	 * 
	 * @param ipAddress IP address to be removed
	 */
	public void RemoveIpAddress(String ipAddress) {
		if (ipAddresses.contains(ipAddress)) {
			this.ipAddresses.remove(ipAddress);
			int size = q.size();
			for (int i = 0; i < size; i++) {
				String ip = q.poll();
				if (!ip.equals(ipAddress)) {
					q.offer(ip);
				}
			}

			if (ipAddresses.size() == 0) {
				this.validDomain = false;
			}
		}
	}

	/**
	 * Returns the next IP address according to the Round Robin implementation.
	 * 
	 * @return next IP address
	 */
	public String RoundRobin() {
		if (!q.isEmpty()) {
			String ip = q.poll();
			q.offer(ip);
			return ip;
		} else {
			return null;
		}
	}

	/**
	 * Deletes all IP addresses from the list and assigns the validDomain as false.
	 */
	public void flush() {
		this.ipAddresses = new HashSet<>();
		q = new LinkedList<>();
		this.validDomain = false;
	}

	/**
	 * @return true if this node has a valid domain name, otherwise false.
	 */
	public boolean isValid() {
		return validDomain;
	}

	/**
	 * @return list of the child nodes of this node.
	 */
	public Map<String, DnsNode> getChildNodeList() {
		return childNodeList;
	}

	/**
	 * @return set of IP addresses of this node.
	 */
	public Set<String> getIpAddresses() {
		return ipAddresses;
	}
	

}


//DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE
