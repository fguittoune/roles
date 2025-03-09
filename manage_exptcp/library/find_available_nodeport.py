#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
import sys

def find_available_nodeport(assigned_ports, start_port, end_port):
    """
    Find the smallest available NodePort in the range [start_port, end_port]
    that is not in the assigned_ports list.
    """
    assigned_ports_set = set(assigned_ports)
    for port in range(start_port, end_port + 1):
        if port not in assigned_ports_set:
            return port
    return None  # No available port in the range

def main():
    module_args = dict(
        assigned_ports=dict(type='list', elements='int', required=True),
        start_port=dict(type='int', required=True),
        end_port=dict(type='int', required=True)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    assigned_ports = module.params['assigned_ports']
    start_port = module.params['start_port']
    end_port = module.params['end_port']

    available_port = find_available_nodeport(assigned_ports, start_port, end_port)

    if available_port is None:
        module.fail_json(msg="No available NodePort in the specified range.")
    else:
        module.exit_json(changed=False, available_port=available_port)

if __name__ == '__main__':
    main()