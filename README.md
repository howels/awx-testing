# AWX Dynamic Inventory using DNSMASQ 

This uses the leases file to build a dynamic inventory in AWX.  It goes further than other attempts because it will:
* Attempt to use the hostname and tag the IP as ansible_host
* Add the MAC address data using the 'mac' variable

This allows a user to identify devices using the hostname or MAC and target them with Ansible. It is ideal for home routers running OpenWRT and uses the file location found in these devices.

To use the script the following environment variables need to be set:

* DNSMASQ_HOSTNAME - hostname of the router/DHCP server holding the file /var/dhcp.leases
* DNSMASQ_USERNAME - username with read access to leases file
* DNSMASQ_PASSWORD - password of the user

Future ideas:
* Add SSH key support
* Add custom leases file locations, but default to /var/dhcp.leases
