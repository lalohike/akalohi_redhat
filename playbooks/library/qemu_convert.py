#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import subprocess
import shutil

def install_qemu_img(module):
    pkg_managers = [
        ('dnf', ['dnf', '-y', 'install', 'qemu-img']),
        ('yum', ['yum', '-y', 'install', 'qemu-img']),
        ('apt-get', ['apt-get', 'update']),
        ('apt-get', ['apt-get', '-y', 'install', 'qemu-utils']),
    ]

    for name, cmd in pkg_managers:
        if shutil.which(name):
            try:
                subprocess.run(cmd, check=True)
                return
            except subprocess.CalledProcessError as e:
                continue

    module.fail_json(msg="Failed to install qemu-img. No compatible package manager found or install failed.")

def main():
    module = AnsibleModule(
        argument_spec=dict(
            input_format=dict(type='str', required=True),
            output_format=dict(type='str', required=True),
            src=dict(type='str', required=True),
            dest=dict(type='str', required=True)
        ),
        supports_check_mode=False
    )

    input_format = module.params['input_format']
    output_format = module.params['output_format']
    src = module.params['src']
    dest = module.params['dest']

    # Ensure qemu-img is installed
    if not shutil.which('qemu-img'):
        install_qemu_img(module)

    # Perform the conversion
    try:
        subprocess.run(
            ['qemu-img', 'convert', '-f', input_format, '-O', output_format, src, dest],
            check=True
        )
        module.exit_json(changed=True, msg=f"Converted {src} to {dest}", dest=dest)
    except subprocess.CalledProcessError as e:
        module.fail_json(msg=f"qemu-img conversion failed: {str(e)}")

if __name__ == '__main__':
    main()
