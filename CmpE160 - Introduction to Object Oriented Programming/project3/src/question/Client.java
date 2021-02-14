
//DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE
package question;


/**
 * Represents the client side that consists of the root node of Domain Name
 * System tree structure, an IP address for each client and a list of cached
 * contents. Cached contents store the nodes that sent to the cache.
 * 
 * @author Karahan Saritas
 */
public class Client {
	/**
	 * Root of the tree structure of Domain Name System.
	 */
	private DnsTree root;
	/**
	 * A unique IP address for each client.
	 */
	private String ipAddress;
	/**
	 * An array of cachedContent objects to store IP addresses in the cache of this
	 * client.
	 */
	private CachedContent[] cacheList;

	/**
	 * Constructs a new client with the given IP address and tree root. Also
	 * initializes the cacheList with the size of 10.
	 * 
	 * @param ipAddress unique IP address for the client
	 * @param root      Root node to access a specific tree structure
	 */
	public Client(String ipAddress, DnsTree root) {
		this.root = root;
		this.ipAddress = ipAddress;
		cacheList = new CachedContent[10];
	}

	/**
	 * Returns the IP address of the requested domain name. Initially searches for
	 * it in the cache. The hitNo is incremented by 1 if it is found in the cache.
	 * Otherwise it looks for the IP address in the Domain Name System. If there are
	 * more than one IP addresses available for the given domain name, it returns
	 * the necessary IP address according to the Round Robin algorithm.
	 * 
	 * @param domainName Requested domain name
	 * @return IP address of the requested domain name if there is any, otherwise
	 *         null
	 */
	public String sendRequest(String domainName) {
		for (int i = 0; i < cacheList.length; i++) {
			if (cacheList[i] != null) {
				if (cacheList[i].domainName.equals(domainName)) {
					cacheList[i].hitNo++;
					return cacheList[i].ipAddress;
				}
			}
		}
		String ip = this.root.queryDomain(domainName);
		addToCache(domainName, ip);
		return ip;
	}

	/**
	 * Creates a new cache record with the given domain name and IP address, then
	 * adds it to the cache of this client. If there is no space in the cache, finds
	 * the cache record with the minimum hits and replace it with the recently
	 * created record.
	 * 
	 * @param domainName domain name of the node to be added
	 * @param ipAddress  IP address that belongs to the given domain name
	 */
	public void addToCache(String domainName, String ipAddress) {
		if (cacheList[9] == null) {
			for (int i = 0; i < cacheList.length; i++) {
				CachedContent cache = cacheList[i];
				if (cache == null) {
					cacheList[i] = new CachedContent(domainName, ipAddress);
					return;
				}
				if (cache.domainName.equals(domainName) && cache.ipAddress.equals(ipAddress)) {
					return;
				}
			}
		} else {
			int min = cacheList[0].hitNo;
			int index = 0;
			for (int i = 0; i < cacheList.length; i++) {
				if (cacheList[i].hitNo < min) {
					index = i;
					min = cacheList[i].hitNo;
				}
			}
			cacheList[index] = new CachedContent(domainName, ipAddress);

		}
	}
	





	/**
	 * Represents the cache records stored in the cacheList of this client. Each
	 * cache record has its own domain name, IP address and an integer keeping the
	 * number of hits to this record.
	 * 
	 * @author Karahan Saritas
	 */
	
	private class CachedContent {
		/**
		 * Domain name of the record.
		 */
		private String domainName;
		/**
		 * IP address of the record.
		 */
		private String ipAddress;
		/**
		 * Number of hits, which is incremented by one when the local device uses a
		 * cached content without consulting Domain Name System.
		 */
		private int hitNo;

		/**
		 * Constructs a cache record with the given domain name and IP address.
		 * Additionally, assigns the hitNo to zero.
		 * 
		 * @param domainName domain name of the record
		 * @param ipAddress  IP address of the record
		 */
		private CachedContent(String domainName, String ipAddress) {
			this.domainName = domainName;
			this.ipAddress = ipAddress;
			this.hitNo = 0;
		}

	}

}

//DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE
