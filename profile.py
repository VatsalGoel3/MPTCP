"""A Multipath testbed with four d430 nodes with multiple connections.

Instructions:
Wait for the profile instance to start, and then log in to either node via the ssh ports specified below.
"""

import geni.portal as portal
import geni.rspec.pg as rspec

# Create a portal context.
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Create four raw "PC" nodes
node1 = request.RawPC("node1")
node2 = request.RawPC("node2")
node3 = request.RawPC("node3")
node4 = request.RawPC("node4")

# Set disk images and hardware types
node1.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"
node2.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU20-64-STD"
node3.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU20-64-STD"
node4.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"

node1.hardware_type = "d430"
node2.hardware_type = "d430"
node3.hardware_type = "d430"
node4.hardware_type = "d430"

# Define interface names and IP addresses
node1.addInterface("eth1a", use_public_ip=True)
node1.addInterface("eth2a", ip="192.168.0.1", netmask="255.255.255.0")

node2.addInterface("eth1b", use_public_ip=True)
node2.addInterface("eth2a", ip="10.0.0.2", netmask="255.255.255.0")

node3.addInterface("eth3b", ip="10.0.1.2", netmask="255.255.255.0")
node3.addInterface("eth4a", ip="192.168.1.1", netmask="255.255.255.0")

node4.addInterface("eth2b", ip="192.168.0.2", netmask="255.255.255.0")
node4.addInterface("eth4b", ip="192.168.1.2", netmask="255.255.255.0")

# Add setup script service to each node
for node in [node1, node2, node3, node4]:
    node.addService(rspec.Execute(shell="bash", command="sudo chmod +x /local/repository/setup.sh && sudo /local/repository/setup.sh"))

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
