# AWX Dynamic Inventory using DNSMASQ 

This uses the leases file to build a dynamic inventory in AWX.  It goes further than other attempts because it will:
* Attempt to use the hostname and tag the IP as ansible_host
* Add the MAC address data using the 'mac' variable

This allows a user to identify devices using the hostnane or MAC and target them with Ansible.
