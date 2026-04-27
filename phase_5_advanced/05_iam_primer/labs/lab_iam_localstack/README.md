# Lab: IAM Policies on LocalStack

## Goal
Write an IAM policy that grants read-only access to the `public/` prefix of an S3 bucket, then verify on LocalStack that allowed actions succeed and other actions return `AccessDenied`.

## Prerequisites
- Docker running
- `pip install awscli-local` (provides `awslocal`)
- Dummy credentials exported: `export AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=us-east-1`

## Setup
```bash
docker run -d --name ls-iam -p 4566:4566 \
  -e SERVICES=iam,s3,sts \
  localstack/localstack:3.8

# Create a bucket with two prefixes
awslocal s3 mb s3://lab-iam-demo
echo "public content" | awslocal s3 cp - s3://lab-iam-demo/public/hello.txt
echo "private content" | awslocal s3 cp - s3://lab-iam-demo/private/secret.txt
```
Reference setup pattern: [LocalStack Getting Started](https://docs.localstack.cloud/getting-started/).

## Steps

1. **Write the least-privilege policy** to `/tmp/public-read.json`:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "ReadPublicPrefix",
         "Effect": "Allow",
         "Action": "s3:GetObject",
         "Resource": "arn:aws:s3:::lab-iam-demo/public/*"
       }
     ]
   }
   ```
   Shape adapted from [AWS Glue security best practices](https://docs.aws.amazon.com/glue/latest/dg/security-best-practices.html).

2. **Write the trust policy** to `/tmp/trust.json` allowing the root account to assume the role:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [{
       "Effect": "Allow",
       "Principal": {"AWS": "arn:aws:iam::000000000000:root"},
       "Action": "sts:AssumeRole"
     }]
   }
   ```

3. **Create role, create policy, attach it**:
   ```bash
   awslocal iam create-role --role-name PublicReader \
     --assume-role-policy-document file:///tmp/trust.json
   awslocal iam create-policy --policy-name PublicReadOnly \
     --policy-document file:///tmp/public-read.json
   awslocal iam attach-role-policy --role-name PublicReader \
     --policy-arn arn:aws:iam::000000000000:policy/PublicReadOnly
   ```

4. **Assume the role** and export session credentials:
   ```bash
   creds=$(awslocal sts assume-role \
     --role-arn arn:aws:iam::000000000000:role/PublicReader \
     --role-session-name lab)
   export AWS_ACCESS_KEY_ID=$(echo "$creds"  | jq -r .Credentials.AccessKeyId)
   export AWS_SECRET_ACCESS_KEY=$(echo "$creds" | jq -r .Credentials.SecretAccessKey)
   export AWS_SESSION_TOKEN=$(echo "$creds" | jq -r .Credentials.SessionToken)
   ```

5. **Test four cases** (2 expected successes, 2 expected `AccessDenied`):
   ```bash
   awslocal s3 cp s3://lab-iam-demo/public/hello.txt -          # expect: success
   awslocal s3api head-object --bucket lab-iam-demo --key public/hello.txt  # expect: success
   awslocal s3 cp s3://lab-iam-demo/private/secret.txt -        # expect: AccessDenied
   echo x | awslocal s3 cp - s3://lab-iam-demo/public/new.txt   # expect: AccessDenied (no PutObject)
   ```

## Verify
- [ ] Reading `public/hello.txt` prints the content
- [ ] `head-object` on `public/hello.txt` returns metadata
- [ ] Reading `private/secret.txt` fails with `AccessDenied`
- [ ] Writing to `public/new.txt` fails with `AccessDenied`

> Note: LocalStack community edition does not fully enforce IAM by default. If you see denies missing, set `ENFORCE_IAM=1` on the container or treat this lab as a policy-authoring and STS-flow exercise and re-run the assertions against a real sandbox account. Ref: [LocalStack IAM](https://docs.localstack.cloud/user-guide/aws/iam/).

## Cleanup
```bash
docker stop ls-iam && docker rm ls-iam
rm -f /tmp/public-read.json /tmp/trust.json
unset AWS_SESSION_TOKEN
```

## Troubleshooting
| Symptom | Fix |
|---|---|
| `Unable to locate credentials` | Re-export `AWS_ACCESS_KEY_ID=test` etc. before `awslocal` calls |
| `AssumeRole` returns empty | Confirm the trust policy principal ARN is `arn:aws:iam::000000000000:root` (LocalStack default account) |
| All four tests succeed (no denies) | LocalStack IAM enforcement is off; restart container with `-e ENFORCE_IAM=1` |

## Stretch goals
- Add `"Condition": {"IpAddress": {"aws:SourceIp": "10.0.0.0/8"}}` to the policy and verify requests from outside that range are denied while in-range requests still work.
- Rewrite the policy as a **bucket policy** (resource-based) and compare behaviour to the identity-based version.
- Add a deny statement for `s3:GetObject` on `private/*` and prove explicit deny overrides even an `s3:*` allow.

## References
See `../../references.md` (module-level).
