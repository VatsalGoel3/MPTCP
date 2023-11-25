For 1
ip mptcp endpoint add 10.10.2.1 dev enp6s0f0 id 1 fullmesh

ip rule add from 10.10.1.1 table 1
ip rule add from 10.10.2.1 table 2

ip route add 10.10.1.0/24 dev enp6s0f1 scope link table 1
ip route add default via 10.10.1.2 dev enp6s0f1 table 1

ip route add 10.10.2.0/24 dev enp6s0f0 scope link table 2
ip route add default via 10.10.2.2 dev enp6s0f0 table 2

ip route add default scope global nexthop via 10.10.1.2 dev enp6s0f1

For 2
ip mptcp endpoint add 10.10.3.2 dev enp6s0f0 id 1 signal

ip rule add from 10.10.4.2 table 3
ip rule add from 10.10.3.2 table 4

ip route add 10.10.4.0/24 dev enp6s0f1 scope link table 3
ip route add default via 10.10.4.1 dev enp6s0f1 table 3

ip route add 10.10.3.0/24 dev enp6s0f0 scope link table 4
ip route add default via 10.10.3.1 dev enp6s0f0 table 4

ip route add default scope global nexthop via 10.10.3.1 dev enp6s0f0
