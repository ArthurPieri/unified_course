# References — 04_cloud_concepts

## Shared responsibility model (vendor-neutral — all three)
- [AWS — Shared Responsibility Model](https://aws.amazon.com/compliance/shared-responsibility-model/) — canonical AWS diagram
- [Microsoft — Shared responsibility in the cloud](https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility) — Azure version
- [Google Cloud — Shared responsibilities and shared fate](https://cloud.google.com/architecture/framework/security/shared-responsibility-shared-fate) — GCP version

## Regions and availability zones
- [AWS — Global infrastructure: Regions and Availability Zones](https://aws.amazon.com/about-aws/global-infrastructure/regions_az/)
- [Azure — Regions and availability zones overview](https://learn.microsoft.com/en-us/azure/reliability/availability-zones-overview)
- [Google Cloud — Geography and regions](https://cloud.google.com/docs/geography-and-regions)

## VPC / VNet
- [AWS — What is Amazon VPC](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)
- [AWS — Subnets: public and private](https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html)
- [AWS — NAT gateways](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html)
- [Azure — Virtual Network overview](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview)
- [Azure — NAT gateway overview](https://learn.microsoft.com/en-us/azure/nat-gateway/nat-overview)
- [Google Cloud — VPC overview](https://cloud.google.com/vpc/docs/overview)
- [Google Cloud — Cloud NAT overview](https://cloud.google.com/nat/docs/overview)

## Object storage (lakehouse backbone)
- [AWS — Amazon S3 user guide: overview](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)
- [Azure — Azure Data Lake Storage Gen2 introduction](https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction)
- [Google Cloud — Cloud Storage overview](https://cloud.google.com/storage/docs/introduction)

## Managed services
- [AWS — Amazon RDS user guide](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html)
- [Azure — SQL Database (PaaS) overview](https://learn.microsoft.com/en-us/azure/azure-sql/database/sql-database-paas-overview)
- [Google Cloud — Cloud SQL overview](https://cloud.google.com/sql/docs/introduction)

## Cost drivers (egress, cross-AZ, idle)
- [AWS — EC2 on-demand pricing (data transfer section)](https://aws.amazon.com/ec2/pricing/on-demand/)
- [Azure — Bandwidth pricing](https://azure.microsoft.com/en-us/pricing/details/bandwidth/)
- [Google Cloud — VPC network pricing](https://cloud.google.com/vpc/network-pricing)

## Identity: principals, roles, short-lived credentials
- [AWS — IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html) — no long-lived keys, prefer roles
- [AWS — IAM Roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)
- [Azure — Managed identities for Azure resources](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview)
- [Google Cloud — Service accounts overview](https://cloud.google.com/iam/docs/service-account-overview)
- [Google Cloud — Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation)

## Sibling reuse
- `../../../linux_fundamentals/course/03-cloud-computing.md:L241-L285` — shared responsibility model (LFCA notes)
- `../../../linux_fundamentals/course/03-cloud-computing.md:L319-L358` — regions and AZs
- `../../../linux_fundamentals/course/03-cloud-computing.md:L857-L911` — VPC, subnets, gateways
- `../../../linux_fundamentals/course/03-cloud-computing.md:L678-L703` — hidden costs (egress, idle)
- `../../../linux_fundamentals/course/03-cloud-computing.md:L991-L998` — ingress vs egress
- `../../../dataeng/docs/cloud-migration/README.md` — lakehouse-to-cloud port notes (referenced from `references/sibling_sources.md:L97`)

## Books
- *Fundamentals of Data Engineering*, Reis & Housley, Ch. 4 — "Choosing technologies across the data engineering lifecycle" covers the managed-services trade-off explicitly
