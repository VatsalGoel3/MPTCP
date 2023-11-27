For 1
ip mptcp endpoint flush
ip mptcp limits set subflow 2 add_addr_accepted 2

ip mptcp endpoint add 10.10.3.1 dev eno4 id 1 fullmesh

ip rule add from 10.10.1.1 table 1
ip rule add from 10.10.3.1 table 2

ip route add 10.10.1.0/24 dev enp5s0f1 scope link table 1
ip route add default via 10.10.1.2 dev enp5s0f1 table 1

ip route add 10.10.3.0/24 dev eno4 scope link table 2
ip route add default via 10.10.3.2 dev eno4 table 2

ip route add default scope global nexthop via 10.10.1.2 dev enp5s0f1

For 2
ip mptcp endpoint flush
ip mptcp limits set subflow 2 add_addr_accepted 2

ip mptcp endpoint add 10.10.4.2 dev eno4 id 1 signal

ip rule add from 10.10.2.2 table 3
ip rule add from 10.10.4.2 table 4

ip route add 10.10.2.0/24 dev enp5s0f1 scope link table 3
ip route add default via 10.10.2.1 dev enp5s0f1 table 3

ip route add 10.10.4.0/24 dev eno4 scope link table 4
ip route add default via 10.10.4.1 dev eno4 table 4

ip route add default scope global nexthop via 10.10.4.1 dev eno4


Extra
sysctl -w net.mptcp.enabled=1
sysctl -w net.mptcp.checksum_enabled=1
sysctl -w net.mptcp.pm_type=1
sysctl -w net.mptcp.allow_join_initial_addr_port=1
