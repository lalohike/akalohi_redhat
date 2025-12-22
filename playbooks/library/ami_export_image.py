#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import boto3
from botocore.exceptions import ClientError

def run_module():
    module_args = dict(
        ami_id=dict(type='str', required=True),
        disk_image_format=dict(type='str', required=True),
        s3_bucket=dict(type='str', required=True),
        s3_prefix=dict(type='str', required=True),
        role_name=dict(type='str', required=True),
        region=dict(type='str', required=False, default='us-east-1')
    )

    result = dict(
        changed=False,
        msg='',
        export_task_id='',
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    try:
        ec2 = boto3.client('ec2', region_name=module.params['region'])

        response = ec2.export_image(
            DiskImageFormat=module.params['disk_image_format'],
            ImageId=module.params['ami_id'],
            S3ExportLocation={
                'S3Bucket': module.params['s3_bucket'],
                'S3Prefix': module.params['s3_prefix']
            },
            RoleName=module.params['role_name']
        )

        result['export_task_id'] = response.get('ExportImageTaskId', '')
        result['changed'] = True
        result['msg'] = f"AMI export task started: {result['export_task_id']}"

    except ClientError as e:
        error_msg = str(e)
        if "LimitExceededException" in error_msg:
            module.fail_json(
                msg="AMI export failed due to task limit exceeded.",
                details=error_msg,
                export_limit_exceeded=True,
                **result
            )
        else:
            module.fail_json(msg=f"Failed to export image: {error_msg}", **result)
    except Exception as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()

