
//DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE
package question;

import java.util.*;

/**
 * Represents the main Domain Name System structure. Each structure has a root
 * node to begin with. DNS system inserts records to the tree, removes records
 * from the tree, searches for a specific domain name in the cache and returns
 * all domain names with their IP addresses as a map.
 * 
 * @author Karahan Saritas
 */
public class DnsTree {
	/**
	 * Root of the tree
	 */

	private DnsNode root;

	/**
	 * Constructs a DNS tree structure and initializes the root node.
	 */
	public DnsTree() {
		this.root = new DnsNode();
	}

	/**
	 * Inserts a new record for a given domain name. If the corresponding node is
	 * not available in the tree, it creates a new one and marks its validDomain as
	 * true. Otherwise, updates the IP address list of the node.
	 * 
	 * @param domainName domain name of the record to be added to this tree
	 * @param ipAddress  Corresponding IP address of the domain name
	 */
	public void insertRecord(String domainName, String ipAddress) {
		String[] search = Search(domainName);
		DnsNode current = root;
		for (int i = 0; i < search.length; i++) {
			if (current.getChildNodeList().containsKey(search[i])) {
				current = current.getChildNodeList().get(search[i]);
			} else {
				DnsNode node = new DnsNode();
				current.AddSubNode(search[i], node);
				current = node;
			}
		}
		current.AddIpAddress(ipAddress);

	}

	/**
	 * Removes the given IP address of a DNS node with the given domain name. If
	 * successfully removed, returns true, otherwise returns false.
	 * 
	 * @param domainName domain name of the record to be removed
	 * @return true if removing process is completed successfully, otherwise false
	 */
	public boolean removeRecord(String domainName) {
		String[] search = Search(domainName);
		DnsNode current = root;
		for (int i = 0; i < search.length - 1; i++) {
			if (current.getChildNodeList().containsKey(search[i])) {
				current = current.getChildNodeList().get(search[i]);
			} else {
				return false;
			}
		}
		if (current.getChildNodeList().containsKey(search[search.length - 1]) && current.getChildNodeList().get(search[search.length - 1]).isValid()) {
			DnsNode OurNode = current.getChildNodeList().get(search[search.length - 1]);
			OurNode.flush();

			if (OurNode.getChildNodeList().isEmpty()) {
				current.RemoveSubNode(search[search.length - 1]);
			}
			return true;
		}
		return false;

	}

	/**
	 * Removes the given IP address of a DNS node with the given domain name. If
	 * successfully removes, returns true, otherwise, returns false.
	 * 
	 * @param domainName domain name of the DNS node
	 * @param ipAddress  IP address to be removed from the node
	 * @return true if removing process is completed successfully, otherwise false
	 */
	public boolean removeRecord(String domainName, String ipAddress) {
		String[] search = Search(domainName);
		DnsNode current = root;
		for (int i = 0; i < search.length - 1; i++) {
			if (current.getChildNodeList().containsKey(search[i])) {
				current = current.getChildNodeList().get(search[i]);
			} else {
				return false;
			}
		}
		if (current.getChildNodeList().containsKey(search[search.length - 1])) {
			DnsNode OurNode = current.getChildNodeList().get(search[search.length - 1]);
			if (OurNode.getIpAddresses().contains(ipAddress)) {
				OurNode.RemoveIpAddress(ipAddress);
			} else {
				return false;
			}

			if (OurNode.getChildNodeList().isEmpty() && OurNode.getIpAddresses().isEmpty()) {
				current.RemoveSubNode(search[search.length - 1]);
			}
			return true;
		}
		return false;

	}

	/**
	 * Queries the given domain name within the DNS, and returns the next IP address
	 * of the node using the Round Robin mechanism. If there is no such domain name
	 * in the tree, returns null.
	 * 
	 * @param domainName domain name to be searched for within the DNS
	 * @return next IP address if any, otherwise null
	 */
	public String queryDomain(String domainName) {
		String[] search = Search(domainName);
		DnsNode current = root;
		for (int i = 0; i < search.length; i++) {
			if (current.getChildNodeList().containsKey(search[i])) {
				current = current.getChildNodeList().get(search[i]);
			} else {
				return null;
			}
		}
		return current.RoundRobin();
	}

	/**
	 * Returns all the valid domain names in the DNS mechanism with at least 1 IP
	 * address.
	 * 
	 * @return a Map object whose keys represent the valid domain names, and value
	 *         is the set of IP addresses of a particular domain name
	 */
	public Map<String, Set<String>> getAllRecords() {
		return getAllRecords(new HashMap<String, Set<String>>(), root, new Stack<String>());
	}

	/**
	 * Returns all the valid domain names in the DNS mechanism with at least 1 IP
	 * address. This method works recursively and updates the content of the map
	 * given as a parameter.
	 * 
	 * @param thread a stack to store domain names of recently passed node
	 * @param map    a map object to store domain names and their IP addresses
	 * @param node   node whose child nodes are going to be inspected
	 * @return a Map object whose keys represent the valid domain names, and value
	 *         is the set of IP addresses of a particular domain name
	 */
	private Map<String, Set<String>> getAllRecords(Map<String, Set<String>> map, DnsNode node, Stack<String> thread) {

		for (String key : node.getChildNodeList().keySet()) {
			DnsNode subNode = node.getChildNodeList().get(key);
			thread.push(key);
			map = getAllRecords(map, subNode, thread);
			thread.pop();
		}
		if (node.isValid()) {
			Stack<String> aux = new Stack<>();
			String domain = "";
			while (!thread.isEmpty()) {
				String str = thread.pop();
				aux.push(str);
				domain += str;
				if (!thread.isEmpty()) {
					domain += ".";
				}
			}
			while (!aux.isEmpty()) {
				thread.push(aux.pop());
			}
			map.put(domain, node.getIpAddresses());
		}
		return map;

	}

	/**
	 * Creates an array of Strings denoting the domain names. Splits the given
	 * domain name into independent parts and rebuild them to store in the array.
	 * 
	 * @param domainName domain name to be searched in the DNS
	 * @return array of domain names that needs to be searched in order to find the
	 *         node with the give domain name
	 */
	private String[] Search(String domainName) {
		String[] parts = domainName.split("\\.");
		String[] search = new String[parts.length];
		int m = 0;
		for (int i = parts.length - 1; i >= 0; i--) {
			search[m] = parts[i];
			m++;
		}
		return search;

	}
}

//DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE
