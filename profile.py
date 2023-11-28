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

# Build node 1 and 4 on Ubuntu 22.04 and node 2 and 3 on Ubuntu 20.04
node1.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"
node2.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU20-64-STD"
node3.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU20-64-STD"
node4.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"

# Set each of the node to request a d430 configuration
node1.hardware_type = "d430"
node2.hardware_type = "d430"
node3.hardware_type = "d430"
node4.hardware_type = "d430"

# Create a link between the nodes
link1 = request.Link(members=[node1, node2])
interface1_node1 = node1.addInterface("eth1a")
interface1_node1.addAddress(rspec.IPv4Address("10.0.0.1", "255.255.255.0"))

interface1_node2 = node2.addInterface("eth1b")
interface1_node2.addAddress(rspec.IPv4Address("10.0.0.2", "255.255.255.0"))

link2 = request.Link(members=[node2, node4])
interface2_node2 = node2.addInterface("eth2a")
interface2_node2.addAddress(rspec.IPv4Address("192.168.0.1", "255.255.255.0"))

interface2_node4 = node4.addInterface("eth2b")
interface2_node4.addAddress(rspec.IPv4Address("192.168.0.2", "255.255.255.0"))

link3 = request.Link(members=[node1, node3])
interface3_node1 = node1.addInterface("eth3a")
interface3_node1.addAddress(rspec.IPv4Address("10.0.1.1", "255.255.255.0"))

interface3_node3 = node3.addInterface("eth3b")
interface3_node3.addAddress(rspec.IPv4Address("10.0.1.2", "255.255.255.0"))

link4 = request.Link(members=[node3, node4])
interface4_node3 = node3.addInterface("eth4a")
interface4_node3.addAddress(rspec.IPv4Address("192.168.1.1", "255.255.255.0"))

interface4_node4 = node4.addInterface("eth4b")
interface4_node4.addAddress(rspec.IPv4Address("192.168.1.2", "255.255.255.0"))


# Add the service to run the setup script on each node
# Add the service to run the setup script on each node
node1.addService(rspec.Execute(shell="bash", command="sudo chmod +x /local/repository/setup.sh && sudo /local/repository/setup.sh"))
node2.addService(rspec.Execute(shell="bash", command="sudo chmod +x /local/repository/setup.sh && sudo /local/repository/setup.sh"))
node3.addService(rspec.Execute(shell="bash", command="sudo chmod +x /local/repository/setup.sh && sudo /local/repository/setup.sh"))
node4.addService(rspec.Execute(shell="bash", command="sudo chmod +x /local/repository/setup.sh && sudo /local/repository/setup.sh"))


# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
