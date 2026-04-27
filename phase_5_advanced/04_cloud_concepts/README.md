# Module 04: Cloud Concepts (Cloud-Neutral) (6h)

> Before the vendor phases (AWS/Azure/GCP/Snowflake), you need the shared vocabulary every cloud uses: shared-responsibility, regions and AZs, VPCs and subnets, object storage as the lakehouse backbone, the managed-services trade-off, the three real cost drivers, and short-lived IAM credentials. This module is deliberately vendor-neutral. Every concept is cited to the vendor's own overview so you can recognize the same idea under three different product names.

## Learning goals
- Draw the shared-responsibility boundary for IaaS, PaaS, and SaaS, and place a real workload on it
- Distinguish a region from an availability zone, and explain why "multi-AZ" is the default HA posture
- Sketch a VPC with public and private subnets, an internet gateway, a NAT gateway, and a route table
- Explain why object storage (S3 / ADLS Gen2 / GCS) is the physical backbone of all three major cloud lakehouses
- Articulate the managed-services trade-off in one sentence — less ops, more lock-in
- Name the three dominant cost drivers (egress, cross-AZ traffic, idle capacity) and the mitigation for each
- Explain why short-lived credentials + role assumption beat long-lived access keys

## Prerequisites
- [../../phase_1_foundations/02_networking/](../../phase_1_foundations/02_networking/) — IP, CIDR, routing, NAT basics
- [../../phase_3_core_tools/01_minio_iceberg_hms/](../../phase_3_core_tools/01_minio_iceberg_hms/) — you've used S3-compatible object storage locally

## Reading order
1. This README
2. [quiz.md](quiz.md)
3. Vendor phases (Phase 6): AWS · Azure · GCP · Snowflake, in any order

## Concepts

### Shared responsibility: what the provider owns vs what you own
Every major cloud publishes the same diagram: the provider is responsible for the security **of** the cloud (physical data centers, hardware, hypervisor, network fabric) and you are responsible for security **in** the cloud (your data, your IAM, your OS patches for IaaS, your application). The split slides along the service model: in IaaS you own the OS and everything above it; in PaaS the provider handles the OS and runtime; in SaaS you mostly own identity and data. AWS, Azure, and GCP each publish an explicit diagram with slightly different wording but the same substance. Memorize the diagram, then answer every "who is responsible" question by pointing at the layer.
Ref: [AWS — Shared Responsibility Model](https://aws.amazon.com/compliance/shared-responsibility-model/) · [Microsoft — Shared responsibility in the cloud](https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility) · [Google Cloud — Shared responsibilities and shared fate](https://cloud.google.com/architecture/framework/security/shared-responsibility-shared-fate)

### Regions vs availability zones
A **region** is a geographic area — "us-east-1" (N. Virginia), "westeurope" (Netherlands), "us-central1" (Iowa). A region contains two or more **availability zones (AZs)**, each one or more physically isolated data centers with independent power, cooling, and network. AZs within a region are linked by low-latency private fiber (single-digit milliseconds) so you can build synchronous-replication HA across them; regions are further apart and you replicate asynchronously. "Multi-AZ" is the default HA posture for databases, queues, and stateful services; "multi-region" is a deliberate (and more expensive) choice for disaster recovery or data-residency. Each vendor publishes the live region/AZ list.
Ref: [AWS — Regions and Availability Zones](https://aws.amazon.com/about-aws/global-infrastructure/regions_az/) · [Azure — Regions and availability zones](https://learn.microsoft.com/en-us/azure/reliability/availability-zones-overview) · [Google Cloud — Geography and regions](https://cloud.google.com/docs/geography-and-regions)

### VPC / VNet mental model
A **VPC** (AWS, GCP) or **VNet** (Azure) is a private, isolated network inside the provider where you control the IP address space, subnets, route tables, and gateways. You pick a CIDR (say `10.0.0.0/16`), carve it into subnets (say `10.0.1.0/24` per AZ), attach route tables, and attach gateways (internet gateway for outbound, virtual private gateway / VPN for on-prem). VPC peering and transit gateways connect VPCs together without traversing the public internet. The three vendors' overviews all describe the same primitive — subnets, route tables, gateways, security groups — with the same diagram, just with different product names.
Ref: [AWS — What is Amazon VPC](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html) · [Azure — Virtual Network overview](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview) · [Google Cloud — VPC overview](https://cloud.google.com/vpc/docs/overview)

### Public vs private subnets, and the NAT gateway
A **public subnet** has a route to an **internet gateway**, so resources in it can have public IPs and accept inbound traffic from the internet. A **private subnet** has no direct internet route; resources there are only reachable from inside the VPC. A **NAT gateway** (AWS) / **NAT gateway** (Azure) / **Cloud NAT** (GCP) sits in a public subnet and lets private-subnet resources initiate outbound connections (e.g., to download packages, call an external API) without ever accepting inbound connections. The canonical architecture is: load balancers and bastions in public subnets; application servers and databases in private subnets; a NAT gateway per AZ for outbound egress. The NAT gateway is billed per hour AND per GB processed — see cost drivers below.
Ref: [AWS — Public and private subnets](https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html) · [AWS — NAT gateways](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html) · [Azure — NAT gateway](https://learn.microsoft.com/en-us/azure/nat-gateway/nat-overview) · [Google Cloud — Cloud NAT overview](https://cloud.google.com/nat/docs/overview)

### Object storage as the lakehouse backbone
Amazon S3, Azure Data Lake Storage Gen2 (ADLS), and Google Cloud Storage (GCS) are the physical foundation of every cloud lakehouse. They are all key-value object stores with flat namespaces (no real directories), eventual-to-strong consistency, 11 nines of durability, and API-compatible-enough surfaces that projects like Iceberg, Delta, and Hudi treat them as interchangeable backends. ADLS Gen2 adds a hierarchical namespace on top of Blob Storage specifically to make it friendlier for analytics. You store Parquet/ORC files, a table format (Iceberg/Delta/Hudi) writes its metadata alongside, and compute engines (Trino, Spark, BigQuery, Snowflake external tables) read those files in place. This is the single reason "cloud data engineering" looks the same across vendors.
Ref: [AWS — S3 overview](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html) · [Azure — ADLS Gen2 introduction](https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction) · [Google Cloud — Cloud Storage overview](https://cloud.google.com/storage/docs/introduction)

### Managed services: less ops, more lock-in
Every cloud offers a ladder of managed services over the same primitive: self-hosted Postgres on a VM → provider-managed Postgres (RDS / Azure Database for PostgreSQL / Cloud SQL) → proprietary auto-scaling analytics DB (Redshift / Synapse / BigQuery). Up the ladder you trade operational work (patching, HA, backups, upgrades) for lock-in (proprietary SQL extensions, pricing model, migration cost away). The rule of thumb: adopt the most-managed service you can live with for stateless and commodity workloads; for workloads where migration risk is existential, stay closer to open primitives (S3 + open file format + open table format).
Ref: [AWS — RDS overview](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html) · [Azure — managed database services](https://learn.microsoft.com/en-us/azure/azure-sql/database/sql-database-paas-overview) · [Google Cloud — Cloud SQL overview](https://cloud.google.com/sql/docs/introduction)

### The three cost drivers: egress, cross-AZ, idle
Most cloud bills are dominated by three line items that beginners overlook. **Egress:** data leaving the cloud (to the public internet, or to another region) is charged per GB; inter-region egress within the same provider is cheaper than internet egress but still non-trivial. **Cross-AZ traffic:** a packet that crosses an availability-zone boundary inside the same region also costs money on most providers — this is how multi-AZ HA quietly inflates a bill if every query reads from a replica in another AZ. **Idle capacity:** reserved-but-unused VMs, databases left running overnight, orphaned EBS volumes and NAT gateways. Each vendor publishes the pricing pages; read them once before designing anything.
Ref: [AWS — EC2 data transfer pricing](https://aws.amazon.com/ec2/pricing/on-demand/) · [Azure — Bandwidth pricing](https://azure.microsoft.com/en-us/pricing/details/bandwidth/) · [Google Cloud — Network pricing](https://cloud.google.com/vpc/network-pricing)

### Identity: principals, roles, short-lived credentials
A **principal** is anything that can be authenticated — a human user, a service account, a workload running on a VM. A **role** is a set of permissions that a principal can assume for a limited time. The modern pattern everywhere is: no long-lived access keys on disk; instead, the workload assumes a role (via instance profile, workload identity, or OIDC federation from CI/CD) and gets short-lived credentials (typically 1 hour) from the provider's token service. Long-lived access keys are the #1 credential-leak vector in every cloud-security incident report, which is why every vendor now tells you to avoid them. This module is a preview; `05_iam_primer` covers the full model.
Ref: [AWS — IAM best practices / temporary credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html) · [AWS — IAM Roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html) · [Azure — Managed identities for Azure resources](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview) · [Google Cloud — Service accounts overview](https://cloud.google.com/iam/docs/service-account-overview) · [Google Cloud — Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation)

## Labs
None in this module — it is concept-only. The hands-on follows in the vendor phases (AWS/Azure/GCP), where you actually stand up a VPC, a bucket, and a role per cloud.

## Common failures
| Symptom | Cause | Fix | Source |
|---|---|---|---|
| Surprise 5-figure bill line item | Egress from object storage to the internet (e.g., serving files directly to users) | Front with a CDN; keep data transfer inside the cloud | [AWS EC2 data transfer](https://aws.amazon.com/ec2/pricing/on-demand/) |
| Cross-AZ bill bigger than compute bill | App server in AZ-a constantly reading from DB replica in AZ-b | Pin read traffic to same-AZ replica, or consolidate to one AZ if HA is not required | [AWS data transfer pricing](https://aws.amazon.com/ec2/pricing/on-demand/) |
| Dev environment NAT gateway cost >> compute cost | NAT gateway runs 24/7 even when dev VMs are off | Put dev in a public subnet with a restricted security group, or stop the NAT gateway off-hours | [AWS NAT gateways](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html) |
| Leaked access keys on GitHub | Long-lived access keys committed to source | Delete the keys, rotate, switch workload to role assumption (instance profile / workload identity / OIDC from CI) | [AWS IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html) |
| "Region unavailable for this service" | Not every service ships in every region at the same time | Check the vendor's region/service availability page before designing a multi-region plan | [AWS regions](https://aws.amazon.com/about-aws/global-infrastructure/regions_az/) |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] Draw the shared-responsibility diagram for IaaS, PaaS, and SaaS from memory
- [ ] Explain the difference between a region and an AZ, and why multi-AZ is the default HA posture
- [ ] Sketch a two-AZ VPC with public and private subnets, an IGW, and a NAT gateway per AZ
- [ ] Name the three dominant cost drivers and a mitigation for each
- [ ] Explain why `aws_access_key_id` in a `.env` file is a code smell, and what replaces it
