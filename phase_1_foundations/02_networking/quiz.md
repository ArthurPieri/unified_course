# 02 Networking — Exit Quiz

8 questions. One best answer each. Answer key with primary-source citations at the bottom.

---

**Q1.** Which of the following IPv4 blocks is NOT a private range per RFC 1918?
A) `10.0.0.0/8`
B) `172.16.0.0/12`
C) `192.168.0.0/16`
D) `169.254.0.0/16`

**Q2.** A `/24` subnet provides how many usable host addresses?
A) 256
B) 254
C) 128
D) 62

**Q3.** Which protocol pair does a browser use to load `https://example.com`?
A) UDP then HTTP
B) TCP, then TLS, then HTTP
C) TLS only
D) HTTP then TCP

**Q4.** A teammate says "DNS is down." `dig @8.8.8.8 example.com A` returns an answer. The most accurate statement is:
A) DNS is fully working
B) The recursive resolver at `8.8.8.8` answered for this name — the local stub/resolver config may still be broken
C) Only IPv6 DNS is broken
D) The authoritative server is down

**Q5.** Two services in the same `docker-compose.yml`, `app` and `db`, are on the default project network. How should `app` connect to PostgreSQL?
A) `localhost:5432`
B) `127.0.0.1:5432`
C) `db:5432`
D) The host's LAN IP

**Q6.** Which tool is the right first step to inspect the TLS handshake for a failing HTTPS request?
A) `ping`
B) `dig`
C) `curl -v`
D) `traceroute`

**Q7.** You run `ss -tlnp` and see no line for port 5432, but `docker compose ps` shows the Postgres container as running. The most likely explanation is:
A) PostgreSQL is not listening at all
B) The container is running but its port is not published to the host (no `ports:` mapping), so the host sees nothing on 5432
C) A firewall is dropping the SYN
D) DNS is misconfigured

**Q8.** Which statement about TCP vs. UDP is correct?
A) UDP guarantees ordered delivery
B) TCP retransmits lost segments; UDP does not
C) HTTP/1.1 runs over UDP
D) DNS queries always use TCP

---

## Answer key

**Q1 — D.** `169.254.0.0/16` is link-local, defined in RFC 3927, not RFC 1918 private space. Ref: [RFC 1918](https://datatracker.ietf.org/doc/html/rfc1918).

**Q2 — B (254).** `/24` = 256 addresses minus network (`.0`) and broadcast (`.255`) = 254 usable. Ref: [RFC 1878: Variable Length Subnet Table](https://datatracker.ietf.org/doc/html/rfc1878).

**Q3 — B.** DNS → TCP handshake → TLS handshake → HTTP request/response. Ref: [RFC 9112: HTTP/1.1](https://datatracker.ietf.org/doc/html/rfc9112) · [RFC 8446: TLS 1.3](https://datatracker.ietf.org/doc/html/rfc8446).

**Q4 — B.** `dig @8.8.8.8` bypasses the local resolver; a success there only proves 8.8.8.8 can answer, not that the system's default resolver works. Ref: [dig(1)](https://man7.org/linux/man-pages/man1/dig.1.html) · [RFC 1034](https://datatracker.ietf.org/doc/html/rfc1034).

**Q5 — C (`db:5432`).** Compose creates a project network and registers each service as a DNS name; `localhost` inside `app` is `app` itself. Ref: [Compose: Networking](https://docs.docker.com/compose/networking/).

**Q6 — C (`curl -v`).** `curl -v` prints each handshake stage including the TLS certificate exchange and any verification error. Ref: [curl(1)](https://curl.se/docs/manpage.html).

**Q7 — B.** `ports:` in Compose maps container ports to host ports; without it, the container listens inside its network namespace only. Ref: [Docker: Bridge network driver](https://docs.docker.com/network/drivers/bridge/) · [Compose: Networking](https://docs.docker.com/compose/networking/).

**Q8 — B.** TCP provides retransmission and ordered delivery; UDP does not. DNS uses UDP by default and falls back to TCP for large responses/zone transfers. Ref: [RFC 9293: TCP](https://datatracker.ietf.org/doc/html/rfc9293) · [RFC 768: UDP](https://datatracker.ietf.org/doc/html/rfc768) · [RFC 1035: DNS Implementation](https://datatracker.ietf.org/doc/html/rfc1035).
