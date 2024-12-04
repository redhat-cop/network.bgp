# BGP Gather

## Overview
The `bgp.gather` role enables users to collect and display structured facts for bgp configuration and displays these facts in YAML formatted structures.

## Features
- Retrieve structured facts for specified network resources.
- Provides data in YAML format for easy consumption and analysis.

## Variables

| Variable Name        | Default Value | Required | Type | Description                                                   | Example |
|:---------------------|:-------------:|:--------:|:----:|:-------------------------------------------------------------|:-------:|
| `ansible_network_os` | `""`          | no      | str  | Network OS to be used during deploy.                    | `"cisco.ios.ios"` |

## Usage

### Example 1: Detect configuration drift in BGP Configuration from Local Data Store
Below is an example playbook demonstrating how to use the `gather` role, where we will retrieve facts for bgp configuration:


```yaml
- name: Display BGP resources in a structured format
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: BGP Manager
    ansible.builtin.include_role:
      name: network.bgp.gather
    vars:
      ansible_network_os: cisco.ios.ios
```

Example Output:
When the playbook is executed successfully, the output will display the structured facts for the bgp configurations.

## License

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

## Author Information

- Ansible Network Content Team
