# Module 02: Networking Fundamentals (6h)

Enough networking to troubleshoot a data pipeline: why does `trino` resolve `hive-metastore` but not `localhost`, why does the container see port 9000 but the host sees 9001, what does a 502 at the load balancer mean. This is not a CCNA — we go as deep as "I can read `ss`, `dig`, and `curl -v` output and form a hypothesis".

## Learning goals
- Read an IPv4 address plus CIDR and compute the network range in your head for `/24`, `/16`, `/8`.
- Identify well-known, registered, and ephemeral port ranges and explain why binding to port 80 needs root.
- Describe the DNS resolution chain from `/etc/hosts` → stub resolver → recursive resolver → authoritative nameserver.
- Trace an HTTP/HTTPS request lifecycle (DNS → TCP → TLS → HTTP) and read a `curl -v` trace.
- Choose TCP vs. UDP for a given workload with a one-sentence justification.
- Explain how Docker's default bridge network lets containers reach each other by service name, and why `--network host` bypasses that.
- Diagnose a connectivity problem with `curl`, `dig`, `ss`, and (conceptually) `tcpdump`.

## Prerequisites
- [`../01_linux_bash/`](../01_linux_bash/) — you need a shell fluent enough to read command output.

## Reading order
1. This README
2. [`quiz.md`](quiz.md)
3. [`labs/lab_L1b_network_diagnostics/`](labs/lab_L1b_network_diagnostics/) — hands-on: diagnose connectivity issues in a Docker Compose stack

## Concepts

### IP addresses, subnets, CIDR
IPv4 is a 32-bit address written as four octets (`192.168.1.100`); IPv6 is 128-bit hex. CIDR notation `192.168.1.0/24` says "the first 24 bits are the network, the remaining 8 identify hosts on that network" — a `/24` gives 256 addresses, 254 usable. Private ranges (not routable on the public internet) are `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`. `127.0.0.1` is loopback (the machine itself). Docker bridge networks use private ranges by default — this is why `172.17.0.x` appears when you `docker inspect`.
Ref: `../linux_fundamentals/course/02-system-administration.md:L905-L962` · [RFC 1918: Address Allocation for Private Internets](https://datatracker.ietf.org/doc/html/rfc1918)

### Ports: well-known, registered, ephemeral
A port is a 16-bit number (0–65535) that distinguishes services on a single IP. IANA splits the range three ways: **well-known** `0–1023` (binding requires privileges on Linux — SSH/22, HTTP/80, HTTPS/443, PostgreSQL/5432 is registered not well-known, DNS/53), **registered** `1024–49151`, **dynamic/ephemeral** `49152–65535` (what the kernel hands out for the client side of an outbound connection). Linux's actual ephemeral range is configurable (`/proc/sys/net/ipv4/ip_local_port_range`) and is often narrower than the IANA range.
Ref: `../linux_fundamentals/course/02-system-administration.md:L1086-L1119` · [IANA Service Name and Transport Protocol Port Number Registry](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml) · [RFC 6335](https://datatracker.ietf.org/doc/html/rfc6335)

### TCP vs. UDP
**TCP** is connection-oriented and reliable: three-way handshake, ordered delivery, retransmission, congestion control. HTTP(S), SSH, PostgreSQL wire protocol, Kafka — all TCP. **UDP** is connectionless and unreliable: fire-and-forget datagrams, no ordering, no retransmit. DNS queries, DHCP, NTP, and most voice/video streaming use UDP because the overhead of TCP is worse than a dropped packet. If you do not know which to pick, the answer for a data platform is almost always TCP.
Ref: [RFC 9293: Transmission Control Protocol](https://datatracker.ietf.org/doc/html/rfc9293) · [RFC 768: User Datagram Protocol](https://datatracker.ietf.org/doc/html/rfc768)

### DNS resolution chain
When an application looks up `hive-metastore.internal`:
1. The stub resolver in the OS checks `/etc/hosts` first (per `/etc/nsswitch.conf`).
2. If absent, it queries the configured recursive resolver (`/etc/resolv.conf` → `127.0.0.53` on systemd-resolved, or `8.8.8.8`, etc.).
3. The recursive resolver walks the hierarchy: root `.` → TLD (`.internal` in the real world = a mess; `.com`/`.org` etc. normally) → authoritative nameserver for the zone → A/AAAA record.
4. The answer is cached according to its TTL.

Common record types you will actually see: **A** (hostname → IPv4), **AAAA** (hostname → IPv6), **CNAME** (alias to another hostname), **MX** (mail), **TXT** (SPF/DKIM/verification), **NS** (nameserver for a zone), **PTR** (reverse lookup).
Ref: `../linux_fundamentals/course/02-system-administration.md:L1006-L1082` · [RFC 1034: Domain Names — Concepts and Facilities](https://datatracker.ietf.org/doc/html/rfc1034) · [RFC 1035: Domain Names — Implementation and Specification](https://datatracker.ietf.org/doc/html/rfc1035)

### HTTP/HTTPS request lifecycle
A request to `https://api.example.com/v1/data` does this:
1. **DNS** — resolve `api.example.com` to an IP.
2. **TCP** — three-way handshake (`SYN`, `SYN-ACK`, `ACK`) to the resolved IP on port 443.
3. **TLS** — handshake negotiates cipher, verifies the server certificate chain, establishes session keys. Ref: [RFC 8446: TLS 1.3](https://datatracker.ietf.org/doc/html/rfc8446).
4. **HTTP** — the client sends a request line + headers + body; the server responds with a status line + headers + body. Ref: [RFC 9110: HTTP Semantics](https://datatracker.ietf.org/doc/html/rfc9110) · [RFC 9112: HTTP/1.1](https://datatracker.ietf.org/doc/html/rfc9112).
5. **Close** — connection closes or is reused (HTTP keep-alive) for further requests.

`curl -v https://example.com` prints every stage and is your first diagnostic tool for "is it the DNS, the TLS, or the app?".

### Docker networking (bridge vs. host)
By default, `docker compose up` creates a user-defined **bridge** network for the project. Containers on the same bridge reach each other by **service name** (Compose registers DNS entries) — `postgres://postgres:5432` works from the `dagster` container without knowing IP addresses. The container's port `5432` is only exposed to the host if you declare `ports: - "5432:5432"` (`HOST:CONTAINER`). **`network_mode: host`** removes the isolation entirely: the container shares the host's network namespace, sees the host's interfaces, and port conflicts apply directly — useful for perf-sensitive workloads, dangerous for isolation, and unavailable on Docker Desktop for macOS/Windows before recent versions.
Ref: [Docker: Networking overview](https://docs.docker.com/network/) · [Docker: Bridge network driver](https://docs.docker.com/network/drivers/bridge/) · [Docker: Host network driver](https://docs.docker.com/network/drivers/host/) · [Compose: Networking](https://docs.docker.com/compose/networking/)

### Firewalls, VPNs, proxies (troubleshooting level)
A **firewall** is a packet filter that allows/denies traffic based on rules (source/destination IP, port, protocol, connection state). When a service is "up but unreachable from the laptop," a firewall rule is the usual suspect — check both the host (`ufw status`, cloud security group) and any intermediate network. A **VPN** is an encrypted tunnel that makes your machine appear to be on a remote network — it changes your source IP and DNS resolver, which is why an API works on the office network and fails from home. A **proxy** is an intermediary that terminates your connection and opens a new one to the destination; HTTPS-aware proxies do TLS interception and will break certificate validation unless their CA is trusted.
Ref: `../linux_fundamentals/course/02-system-administration.md:L1173-L1275` · [Linux man-pages: iptables(8)](https://man7.org/linux/man-pages/man8/iptables.8.html)

### Diagnostic tools

| Tool | Use for | Example |
|---|---|---|
| `curl -v URL` | HTTP/HTTPS request trace: DNS, TCP, TLS, headers, body | `curl -v https://api.example.com/health` |
| `dig name [type]` | DNS lookup with full answer section, TTL, which server answered | `dig postgres.internal A` |
| `nslookup name` | Simpler DNS lookup; still ubiquitous | `nslookup example.com` |
| `ss -tlnp` | Listening TCP sockets + owning process | `ss -tlnp \| grep 5432` |
| `netstat -tlnp` | Legacy equivalent of `ss` | `netstat -tlnp` |
| `ping host` | Layer-3 reachability (ICMP) — may be blocked by firewalls | `ping -c 4 8.8.8.8` |
| `traceroute host` | Hop-by-hop path to destination | `traceroute trino.internal` |
| `tcpdump -i any port 5432` | Packet capture — last resort, requires root | see below |

`tcpdump` captures raw packets off an interface; you rarely need it day-to-day, but when DNS says the right IP and `ss` shows the port listening and the client still cannot connect, it is the tool that proves whether packets are leaving the client and arriving at the server. Ref: [Linux man-pages: tcpdump(1)](https://man7.org/linux/man-pages/man1/tcpdump.1.html) · `../linux_fundamentals/course/02-system-administration.md:L1123-L1170`.

## Common failures
| Symptom | Cause | Fix | Source |
|---|---|---|---|
| Container A cannot reach container B by name | They are on different Compose networks, or B has no service name | Put them on the same network; use the service name, not `localhost` | [Compose: Networking](https://docs.docker.com/compose/networking/) |
| `curl` works from the host but not from inside the container | Container uses a different DNS resolver, or the service is bound to `127.0.0.1` inside the container's namespace | Bind to `0.0.0.0`; check `/etc/resolv.conf` in the container | [Docker: Networking overview](https://docs.docker.com/network/) |
| Port shows `LISTEN` on the host but remote clients cannot connect | Host firewall or cloud security group blocks the port | Open the port in the firewall / security group | [iptables(8)](https://man7.org/linux/man-pages/man8/iptables.8.html) |
| `dig example.com` returns an answer but the browser fails | TLS/certificate problem, not DNS | `curl -v https://example.com` to read the TLS handshake error | [RFC 8446](https://datatracker.ietf.org/doc/html/rfc8446) |
| Intermittent drops on long-lived connections through a corporate proxy | Proxy idle-timeout killing TCP sessions | Enable TCP keepalives on the client | [RFC 9293](https://datatracker.ietf.org/doc/html/rfc9293) |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] State the usable host count for a `/24` and a `/16` without a calculator.
- [ ] Name the three IPv4 private ranges from memory.
- [ ] Walk through what happens between `curl https://example.com` and the first byte of HTML returned.
- [ ] Explain why two containers in the same Compose file can talk to each other using the service name but not `localhost`.
- [ ] Pick TCP or UDP for (a) streaming metrics (b) a PostgreSQL client (c) a DNS query, with a one-sentence reason each.
- [ ] Run `ss -tlnp` and identify which process is listening on which port.
