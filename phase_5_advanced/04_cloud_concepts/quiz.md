# Quiz — 04_cloud_concepts

Eight multiple-choice questions. Answers at the bottom.

---

**1.** A company runs a Java application on an EC2 instance (IaaS). An unpatched OS CVE is exploited. Under the shared-responsibility model, who is responsible?

A. AWS — they run the data center
B. AWS — they manage the hypervisor
C. The customer — OS patching sits above the IaaS boundary
D. It is a joint responsibility with no clear owner

**2.** Which statement about regions and availability zones is correct?

A. A region is a single data center; an AZ is a rack inside it
B. An AZ is a geographic area; a region is one data center inside the AZ
C. A region contains two or more AZs, each with independent power, cooling, and network, linked by low-latency fiber
D. Regions and AZs are the same thing under different vendor branding

**3.** In a canonical two-tier VPC, where should an application database go?

A. In a public subnet with a public IP
B. In a private subnet, reachable only from within the VPC (and via NAT for outbound-only traffic)
C. Outside the VPC entirely
D. In the same subnet as the internet gateway

**4.** What is the role of a NAT gateway?

A. It gives private-subnet resources an inbound public endpoint
B. It lets private-subnet resources initiate outbound connections without accepting inbound ones
C. It replaces the internet gateway for public subnets
D. It is only required for IPv6

**5.** Why is cloud object storage (S3 / ADLS Gen2 / GCS) the foundation of every major cloud lakehouse?

A. It is the only storage with SQL support
B. It is the cheapest form of block storage
C. It is a durable, cheap, HTTP-addressable key-value store that every analytic engine can read in place using open file formats like Parquet
D. It has built-in indexing that replaces the need for a query engine

**6.** Which is the clearest statement of the managed-services trade-off?

A. Managed services are always cheaper than self-hosting
B. Managed services trade operational work for vendor lock-in
C. Managed services are required for all production workloads
D. Managed services remove the need for IAM

**7.** A team's AWS bill is dominated by an unexpectedly large "data transfer" line item. Which of the following is the *most likely* root cause worth investigating first?

A. The S3 bucket is too large
B. Egress to the internet or cross-AZ traffic between replicated services
C. Too many IAM roles
D. The NAT gateway is in the wrong region

**8.** Why does every major cloud provider recommend replacing long-lived access keys with role assumption and short-lived credentials?

A. Short-lived credentials are faster
B. Long-lived keys cannot be rotated
C. Leaked long-lived keys are the dominant credential-breach vector, and short-lived credentials bound to a role reduce blast radius when leaked
D. Roles are free and keys are billed per request

---

## Answer key

1. **C** — In IaaS, the OS and everything above it is the customer's responsibility. AWS owns the hypervisor and below. [AWS Shared Responsibility](https://aws.amazon.com/compliance/shared-responsibility-model/)
2. **C** — A region is geographic; AZs are discrete data centers within it, linked by fast private fiber. [AWS regions/AZs](https://aws.amazon.com/about-aws/global-infrastructure/regions_az/) · [Azure zones](https://learn.microsoft.com/en-us/azure/reliability/availability-zones-overview)
3. **B** — Databases belong in private subnets. Only load balancers and bastions sit in public subnets. [AWS subnets](https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html)
4. **B** — NAT gateways enable outbound-only access for private-subnet resources. [AWS NAT gateways](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html) · [Azure NAT gateway](https://learn.microsoft.com/en-us/azure/nat-gateway/nat-overview)
5. **C** — Object storage is the HTTP-addressable durable backbone; open file formats + open table formats make it interchangeable across engines. [S3 overview](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html) · [ADLS Gen2](https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction) · [GCS overview](https://cloud.google.com/storage/docs/introduction)
6. **B** — Less ops, more lock-in is the canonical framing. [Fundamentals of Data Engineering, Reis & Housley, Ch. 4]
7. **B** — Egress and cross-AZ traffic are the two biggest "hidden" data-transfer bills. [AWS EC2 pricing](https://aws.amazon.com/ec2/pricing/on-demand/) · `../../../linux_fundamentals/course/03-cloud-computing.md:L991-L998`
8. **C** — Every vendor's IAM-best-practices page names long-lived keys as the dominant leak vector and prescribes role assumption. [AWS IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
