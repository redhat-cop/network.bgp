# BGP Persist

## Overview
The `bgp.persist` role enables users to fetch facts for bgp configuration and store them in a YAML-formatted structure. These host variables can be saved either locally or in a remote data store, acting as a single source of truth (SOT) for network configurations.

## Features
- Fetch structured facts for bgp.
- Persist gathered facts to local directories or remote SCM repositories.
- Enable centralized and version-controlled storage for network configuration data.

## Variables

| Variable Name        | Default Value | Required | Type | Description                                                   | Example |
|:---------------------|:-------------:|:--------:|:----:|:-------------------------------------------------------------|:-------:|
| `ansible_network_os` | `""`          | no      | str  | Network OS for which the facts are being gathered.            | `"cisco.ios.ios"` |
| `data_store`         | `""`          | yes      | dict | Specifies the storage configuration (local or SCM).           | See examples below. |

## Usage
Below are examples demonstrating how to use the `bgp.persist` role:

### Example 1: Persist to Local Data Store
In this example, gathered facts are stored in a local directory:

```yaml
- name: Persist the facts into host vars
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: Network BGP Manager
    ansible.builtin.include_role:
      name: network.bgp.persist
    vars:
      ansible_network_os: cisco.ios.ios
      data_store:
        local: "~/bgp/network"
```
Example Output
When the playbook is executed, the persisted facts will be saved in the specified data store in a structured YAML format.

### Example 2: Persist to SCM repository
In this example, gathered facts are stored in a remote Git repository:

```yaml
- name: Persist the facts into remote data_store which is a GitHub repository
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: Network BGP Manager
    ansible.builtin.include_role:
      name: network.bgp.persist
    vars:
      ansible_network_os: cisco.ios.ios
      persist_empty: false
      data_store:
        scm:
          origin:
            url: "{{ your_github_repo }}"
            token: "{{ github_access_token }}"
            user:
              name: "{{ ansible_github }}"
              email: "{{ your_email@example.com }}"
```
Example Output
When the playbook is executed, the persisted facts will be saved in the specified data store in a structured YAML format.

## License

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

## Author Information

- Ansible Network Content Team
