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
link2 = request.Link(members=[node2, node4])
link3 = request.Link(members=[node1, node3])
link4 = request.Link(members=[node3, node4])

# Add the service to run the setup script on each node
node1.addService(rspec.Execute(shell="bash", command="/local/repository/setup.sh/"))
node2.addService(rspec.Execute(shell="bash", command="/local/repository/setup.sh/"))
node3.addService(rspec.Execute(shell="bash", command="/local/repository/setup.sh/"))
node4.addService(rspec.Execute(shell="bash", command="/local/repository/setup.sh/"))

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
