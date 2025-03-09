# Ansible Role: Manage `exptcp` Objects

This Ansible role is designed to manage `exptcp` objects, which represent services with VIP (Virtual IP) addresses, NodePorts, and associated metadata. The role supports adding, deleting, retrieving, and listing `exptcp` objects, and it stores the inventory in a dedicated Git repository.

---

## Table of Contents

1. [Overview](#overview)
2. [Role Structure](#role-structure)
3. [Inventory Structure](#inventory-structure)
4. [Usage](#usage)
   - [Adding an `exptcp` Object](#adding-an-exptcp-object)
   - [Deleting an `exptcp` Object](#deleting-an-exptcp-object)
   - [Retrieving an `exptcp` Object](#retrieving-an-exptcp-object)
   - [Listing `exptcp` Objects](#listing-exptcp-objects)
5. [Examples](#examples)
6. [Requirements](#requirements)
7. [License](#license)

---

## Overview

The role manages `exptcp` objects, which are defined as follows:

```yaml
name: "exptcp-<VIP_IP>-<VIP_PORT>"  # Unique name for the object
souscription: "<subscription_name>"  # Subscription name
lb:
  ip: "<VIP_IP>"                     # Virtual IP address
  port: <VIP_PORT>                   # VIP port
service:
  nodeport: <NodePort>               # NodePort assigned to the service
  targetport: <TargetPort>           # Target port for the service
  podselector: "<PodSelector>"       # Pod selector for the service
```

### The role ensures that:

- VIP IPs are assigned from a specified subnet.

- NodePorts are assigned from a specified range (30000-32767).

- The inventory is stored in a dedicated Git repository.

## Role Structure
The role has the following structure:

```bash
roles/
  manage_exptcp/
    tasks/
      main.yml           # Main entry point for tasks
      add_exptcp.yml     # Tasks for adding an exptcp object
      delete_exptcp.yml  # Tasks for deleting an exptcp object
      get_exptcp.yml     # Tasks for retrieving an exptcp object
      list_exptcp.yml    # Tasks for listing exptcp objects
      common.yml         # Common tasks (e.g., Git operations, inventory setup)
    defaults/
      main.yml           # Default variables for the role
    vars/
      main.yml           # Additional variables
    templates/
      exptcp_object.yml.j2  # Template for exptcp objects
```

## Inventory Structure
The inventory is stored in a YAML file per cluster, with the following structure:

```yaml
subscriptions:
  <subscription_name>:
    - name: "exptcp-<VIP_IP>-<VIP_PORT>"
      souscription: "<subscription_name>"
      lb:
        ip: "<VIP_IP>"
        port: <VIP_PORT>
      service:
        nodeport: <NodePort>
        targetport: <TargetPort>
        podselector: "<PodSelector>"
assigned_ips:
  - <VIP_IP_1>
  - <VIP_IP_2>
assigned_nodeports:
  - <NodePort_1>
  - <NodePort_2>
```

## Usage

### Adding an exptcp Object

To add an exptcp object, use the following command:
```yaml
ansible-playbook playbook.yml -e "action=add cluster_name=cluster1 exptcp_object.souscription=subscription1 exptcp_object.lb.port=80 exptcp_object.service.targetport=8080 exptcp_object.service.podselector='app=myapp'"
```

### Deleting an exptcp Object

To delete an exptcp object, use the following command:
```yaml
ansible-playbook playbook.yml -e "action=delete cluster_name=cluster1 exptcp_object.souscription=subscription1 exptcp_object.name=exptcp-192-168-1-1-80"
```

### Retrieving an exptcp Object

To retrieve an exptcp object by name, use the following command:
```yaml
ansible-playbook playbook.yml -e "action=get cluster_name=cluster1 exptcp_object.souscription=subscription1 exptcp_object.name=exptcp-192-168-1-1-80"
```

### Listing exptcp Objects

To list all exptcp objects for a cluster, use the following command:
```yaml
ansible-playbook playbook.yml -e "action=list cluster_name=cluster1"
```

## Examples

### Example Playbook

Here’s an example playbook to use the role:
```yaml
# playbook.yml
- hosts: localhost
  vars:
    action: "add"  # Can be "add", "delete", "get", or "list"
    cluster_name: "cluster1"  # Name of the cluster
    exptcp_object:
      souscription: "subscription1"  # Name of the subscription
      lb:
        ip: ""  # Leave empty to auto-assign an IP
        port: 80  # VIP port
      service:
        targetport: 8080  # Target port
        podselector: "app=myapp"  # Pod selector
  roles:
    - manage_exptcp
```

### Example Inventory File

After adding an exptcp object, the inventory file (exptcp_inventory.yml) might look like this:
```yaml
subscriptions:
  subscription1:
    - name: "exptcp-192-168-1-1-80"
      souscription: "subscription1"
      lb:
        ip: "192.168.1.1"
        port: 80
      service:
        nodeport: 30000
        targetport: 8080
        podselector: "app=myapp"
assigned_ips:
  - 192.168.1.1
assigned_nodeports:
  - 30000
```
