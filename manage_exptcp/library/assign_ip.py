#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import ipaddress

# Start from the 9th IP (index 8) to skip the first 8 IPs
REMOVED_IP_IDS = 8
def assign_ip(subnets, assigned_ips):
    for subnet in subnets:
        network = ipaddress.ip_network(subnet)
        for i in range(REMOVED_IP_IDS, network.num_addresses):  # Skip the first 8 IPs
            ip = str(network[i])
            if ip not in assigned_ips:
                return ip
    return None

def main():
    module = AnsibleModule(
        argument_spec=dict(
            subnets=dict(type='list', required=True),
            assigned_ips=dict(type='list', required=True),
        ),
    )

    subnets = module.params['subnets']
    assigned_ips = module.params['assigned_ips']

    ip = assign_ip(subnets, assigned_ips)

    module.exit_json(changed=False, ip=ip)

if __name__ == '__main__':
    main()