###############################################################
# Topology
#  _______   5mbit, 5ms	     _______   10mbit, 10ms   _______
# |       |-----------------|  r1   |----------------|       |
# |  h1   |                 |_______|                |   h2  |
# |       |                  _______                 |       |
# |       |                 |  r2   |                |       |
# |_______|-----------------|_______|----------------|_______|
#	          10mbit, 10ms           50mbit, 10ms       
##############################################################

#!/bin/sh

sysctl -w net.ipv4.conf.all.rp_filter=0

sysctl -w net.mptcp.enabled=1

sysctl -w net.mptcp.allow_join_initial_addr_port=1

# Define subflows for MPTCP for node 1
ip mptcp endpoint flush
ip mptcp limits set subflow 2 add_addr_accepted 2

# Define subflows for MPTCP for node 4
ip mptcp endpoint flush
ip mptcp limits set subflow 2 add_addr_accepted 2

# Path Management 'in-kernel' using ip mptcp for node 1
ip mptcp endpoint add 192.168.0.1 dev eth2a id 1 fullmesh

# Path Management 'in-kernel' using ip mptcp for node 4
ip mptcp endpoint add 192.168.1.2 dev eth4b id 1 signal

# Enable IP forwarding for node 2 and 3
sysctl -w net.ipv4.ip_forward=1
sysctl -w net.ipv4.ip_forward=1

# Create two routing tables for two interace in node 1
ip rule add from 10.0.0.1 table 1
ip rule add from 192.168.0.1 table 2

# Configure the two routing tables
ip route add 10.0.0.0/24 dev eth1a scope link table 1
ip route add default via 10.0.0.2 dev eth1a table 1

ip route add 192.168.0.0/24 dev eth2a scope link table 2
ip route add default via 192.168.0.2 dev eth2a table 2

# Global Default route
ip route add default scope global nexthop via 10.0.0.2 dev eth1a


# Create two routing tables for two interace for node 4
ip rule add from 10.0.1.2 table 3
ip rule add from 192.168.1.2 table 4

# Configure the two routing tables
ip route add 10.0.1.0/24 dev eth3b scope link table 3
ip route add default via  10.0.1.1 dev eth3b table 3   

ip route add 192.168.1.0/24 dev eth4b scope link table 4
ip route add default via 192.168.1.1 dev eth4b table 4

# Global Default route
ip route add default scope global nexthop via 192.168.1.1 dev eth4b
