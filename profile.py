"""A testbed with three d430 nodes with end-to-end connection.

Instructions:
Wait for the profile instance to start, and then log in to either node via the ssh ports specified below.
"""

import geni.portal as portal
import geni.rspec.pg as rspec

# Create a portal context
pc = portal.Context()

# Create a Request object to start building the RSpec
request = pc.makeRequestRSpec()

# Create four raw "PC" nodes
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

# Add the service to run the setup script on each node
node1.addService(rspec.Execute(shell="bash", command="sudo chmod +x /local/repository/setup.sh && sudo /local/repository/setup.sh"))
node2.addService(rspec.Execute(shell="bash", command="sudo chmod +x /local/repository/setup.sh && sudo /local/repository/setup.sh"))
node3.addService(rspec.Execute(shell="bash", command="sudo chmod +x /local/repository/setup.sh && sudo /local/repository/setup.sh"))

# Start VNC
node1.startVNC()
node2.startVNC()
node3.startVNC()

# Print the RSpec
pc.printRequestRSpec(request)
