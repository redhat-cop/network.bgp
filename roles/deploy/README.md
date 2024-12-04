# BGP Deploy

## Overview
The `bgp.deploy` role enables users to read the config as `host_vars` from a local or remote data store and deploy network configurations if any changes are found. This role is designed to ensure that bgp configurations remain consistent and compliant across devices.

## Features
- Reads bgp configuration data from local or remote data store.
- Deploy bgp configuration only when changes are detected.


## Variables

| Variable Name        | Default Value | Required | Type | Description                                                   | Example |
|:---------------------|:-------------:|:--------:|:----:|:-------------------------------------------------------------|:-------:|
| `ansible_network_os` | `""`          | no      | str  | Network OS to be used during deploy.                    | `"cisco.ios.ios"` |
| `data_store`         | `""`          | yes      | dict | Defines the source of the configurations (local or remote).   | See usage example below. |


## Usage

### Example 1: Deploy Configuration from Local Data Store
Below example playbook demonstrates how to use the `bgp.deploy` role, where we will retrieve config from mentioned local data_store and deploy on to the network.

```yaml
- name: Deploy changes
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: Network BGP Manager
    ansible.builtin.include_role:
      name: network.bgp.deploy
    vars:
      ansible_network_os: cisco.ios.ios
      data_store:
        local: "~/bgp/network"
```
### Example 2: Deploy Configuration from SCM Data Store
Below is an example playbook demonstrating how to use the `bgp.deploy` role, where we will retrieve config from mentioned scm data_store and deploy on to the network.

```yaml
- name: retrieve config from GitHub repo and deploy changes
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: Network BGP Manager
    ansible.builtin.include_role:
      name: network.bgp.deploy
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

Example Output:
When the playbook is executed successfully, the output will show the configurations being deployed when output verbosity is debug mode.

## License

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

## Author Information

- Ansible Network Content Team
