## S3 Bucket ACL Permissions for VM Import/Export

Your S3 bucket needs to be configured with the correct ACL permissions.

📘 Refer to [Page 49 of the AWS VM Import/Export User Guide (PDF)](https://docs.aws.amazon.com/pdfs/vm-import/latest/userguide/vm-import-ug.pdf#image-import)

---

### 1. Object Ownership

- **ACLs enabled**
- **Object Ownership:** Object Writer

---

### 2. Access Control List (ACL)

- **Add Grantee**
  - Use the **Canonical ID** for *All other Regions*:
    ```
    c4d8eabf8db69dbe46bfe0e517100c554f01200b104d59cd408e777ba442a322
    ```
- **Permissions for each Grantee**:
  - `READ_ACP`  
    *(In the Amazon S3 console, bucket ACL should have the Read permission)*
  - `WRITE`  
    *(In the Amazon S3 console, objects should have the Write permission)*

---

### 3. Set Up `vmimport` IAM Role

#### `trust-policy.json`

<details>
<summary>Click to view JSON</summary>

```json
{
   "Version": "2012-10-17",
   "Statement": [
      {
         "Effect": "Allow",
         "Principal": { "Service": "vmie.amazonaws.com" },
         "Action": "sts:AssumeRole",
         "Condition": {
            "StringEquals":{
               "sts:Externalid": "vmimport"
            }
         }
      }
   ]
}
```
</details>

#### `role-policy.json` (Substitute your bucket name)

<details> <summary>Click to view JSON</summary>

```json

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetBucketLocation",
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": [
        "arn:aws:s3:::akalohi-aws-bucket-1",
        "arn:aws:s3:::akalohi-aws-bucket-1/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "ec2:CancelConversionTask",
        "ec2:CancelExportTask",
        "ec2:CreateImage",
        "ec2:CreateInstanceExportTask",
        "ec2:CreateTags",
        "ec2:DescribeConversionTasks",
        "ec2:DescribeExportTasks",
        "ec2:DescribeExportImageTasks",
        "ec2:DescribeImages",
        "ec2:DescribeInstanceStatus",
        "ec2:DescribeInstances",
        "ec2:DescribeSnapshots",
        "ec2:DescribeTags",
        "ec2:ExportImage",
        "ec2:ImportInstance",
        "ec2:ImportVolume",
        "ec2:StartInstances",
        "ec2:StopInstances",
        "ec2:TerminateInstances",
        "ec2:ImportImage",
        "ec2:ImportSnapshot",
        "ec2:DescribeImportImageTasks",
        "ec2:DescribeImportSnapshotTasks",
        "ec2:CancelImportTask"
      ],
      "Resource": "*"
    }
  ]
}
```

  ]
}
