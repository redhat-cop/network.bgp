network.bgp.health_checks
================

The role enables user to perform BGP health checks.

### Supported Health Checks:
- all_neighbors_up: Verifies if all BGP neighbors are up.
- all_neighbors_down: Verifies if all BGP neighbors are down.
- min_neighbors_up: Checks if a minimum number of BGP neighbors are up.
- bgp_status_summary: Summarizes the overall BGP status, including metrics like state, messages sent/received, and protocol version.

### Perform BGP Health Checks
- Health Checks operation fetches the current status of BGP Neighborship health.
- This can also include the details about the BGP metrics(state, message received/sent, version, etc).

```yaml
health_checks.yml
---
- name: Perform health checks
  hosts: all
  gather_facts: false
  tasks:
  - name: BGP Manager
    ansible.builtin.include_role:
      name: network.bgp.health_checks
    vars:
      ansible_network_os: cisco.ios.ios
      bgp_health_check:
        name: health_check
        vars:
          details: true
          checks:
            - name: all_neighbors_up
            - name: all_neighbors_down
              ignore_errors: true
            - name: min_neighbors_up
              min_count: 1
```