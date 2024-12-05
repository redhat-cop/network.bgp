# BGP Detect

## Overview
The `bgp.detect` role enables users to identify bgp configuration drifts between the current running configurations and the desired state provided in a local or remote inventory. This role ensures that network devices remain compliant with their intended configurations.

## Features
- Detect bgp configuration drifts between running configurations and host variables.
- Provide detailed reports of detected changes.


## Variables

| Variable Name        | Default Value | Required | Type | Description                                                   | Example |
|:---------------------|:-------------:|:--------:|:----:|:-------------------------------------------------------------|:-------:|
| `ansible_network_os` | `""`          | no      | str  | Network OS to be used during deploy.                    | `"cisco.ios.ios"` |
| `data_store`         | `""`          | yes      | dict | Defines the source of the configurations (local or remote).   | See usage example below. |


## Usage

### Example 1: Detect configuration drift in BGP Configuration from Local Data Store
Below example playbook demonstrates how to use the `bgp.detect` role, where we `bgp.detect` will read the facts from the local data_store and detect if any configuration diff exists w.r.t running-config.

```yaml
- name: Configuration drift detection
  hosts: all
  gather_facts: false
  tasks:
  - name: Network BGP Manager
    ansible.builtin.include_role:
      name: network.bgp.detect
    vars:
      ansible_network_os: cisco.ios.ios
      data_store:
        local: "~/bgp/network"
```
### Example 2: Deploy Configuration from SCM Data Store
Below example playbook demonstrates how to use the `bgp.detect` role, where we `bgp.detect` will read the facts from the scm data_store and detect if any configuration diff exists w.r.t running-config.

```yaml
- name: Configuration drift detection
  hosts: all
  gather_facts: false
  tasks:
  - name: Network BGP Manager
    include_role:
      name: network.bgp.detect
    vars:
      ansible_network_os: cisco.ios.ios
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
When the playbook is executed successfully, the role will output a report highlighting the detected configuration drifts.

## License

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

## Author Information

- Ansible Network Content Team
