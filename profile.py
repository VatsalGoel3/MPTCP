"""A testbed with three d430 nodes with end-to-end connection.

Instructions:
Wait for the profile instance to start, and then log in to either node via the ssh ports specified below.
"""

import geni.portal as portal
import geni.rspec.pg as rspec
import geni.urn as URN
import geni.rspec.emulab.pnext as PN

# Create a portal context
pc = portal.Context()

# Create a Request object to start building the RSpec
request = pc.makeRequestRSpec()
request.initVNC()

# Create three raw "PC" nodes
node1 = request.RawPC("node1")
node2 = request.RawPC("node2")
node3 = request.RawPC("node3")

# Set disk images and hardware types
node1.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"
node2.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"
node3.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"

# Defining Hardware Type
node1.hardware_type = "d430"
node2.hardware_type = "d430"
node3.hardware_type = "d430"

# Creating links
link1 = request.Link(members = [node1, node2])
link2 = request.Link(members = [node2, node3])

# Start VNC
node1.startVNC()
node2.startVNC()
node3.startVNC()

# Print the RSpec
pc.printRequestRSpec(request)
