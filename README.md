# Network BGP Validated Content

This repository contains the `network.bgp` Ansible Collection.

## Description

The `network.bgp` enables user to manage the BGP resources independent of platforms and perform BGP health checks.

## Tested with Ansible

Tested with ansible-core 2.13 releases.

## Installation

```
ansible-galaxy collection install git+https://github.com/redhat-cop/network.bgp
```

You can also include it in a `requirements.yml` file and install it via `ansible-galaxy collection install -r requirements.yml` using the format:

```yaml
collections:
- name: https://github.com/redhat-cop/network.bgp.git
  type: git
  version: main
```

**Capabilities**
- `Build Brownfield Inventory`: This enables users to fetch the YAML structured resource module facts for BGP resources like bgp_global, bgp_address_family
  and bgp_neighbor_address_family and save it as host_vars to local or remote data-store which could be used as single SOT for other operations.
- `BGP Resource Management`: Users want to be able to manage the BGP global, BGP address family and BGP neighbor address family configurations.
  This also includes the enablement of gathering facts, updating BGP resource host-vars and deploying config onto the appliance.
- `BGP Health Checks`: Users want to be able to perform health checks for BGP applications.These health checks should be  able to provide the BGP neighborship status with necessary details.
- Detect Drift and remediate: This enables users to detect any drift between provided config and running config and if required then override the running config.

### Usage
- This platform agnostic role enables the user to perform BGP health checks.Users can perfrom following health checks:
       `all_neigbors_up`
       `all_neighbors_down`
       `min_neighbors_up`
       `bgp_status_summary`
- This role enables users to create a runtime brownfield inventory with all the BGP configuration in terms of host vars. These host vars are ansible facts which have been gathered through the *_bgp_global and *_bgp_address_family network resource module.The tasks offered by this role could be observed as below:

### Perform BGP Health Checks
- Health Checks operation fetch the current status of BGP Neighborship health.
- This can also include the details about the BGP metrics(state, message received/sent, version, etc).

```yaml
health_checks.yml
---
- name: Perform health checks
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: Manage BGP
    ansible.builtin.include_role:
      name: network.bgp.run
    vars:
      ansible_network_os: cisco.ios.ios
      operations:
        - name: health_check
          vars:
            details: True
            checks:
              - name: all_neighbors_up
              - name: all_neighbors_down
                ignore_errors: true
              - name: min_neighbors_up
                min_count: 1
```


### Building Brownfield Inventory with Persist
- Persist operation fetch the bgp_global and bgp_address_family facts and store them as host vars.
- Result of successful Persist operation would be host_vars having YAML formatted resource facts.
- These host_vars could exist locally or even published to remote repository acting as SOT for operations like deploy, remediate, detect, etc.

#### fetch bgp resource facts and build local data_store.
```yaml
- name: Persist the facts into host vars
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: Network BGP Manager
    ansible.builtin.include_role:
      name: network.bgp.run
    vars:
      ansible_network_os: cisco.ios.ios
      operations:
        - name: persist
      data_store:
        local: "~/backup/network"
```

#### fetch bgp resource facts and publish persisted host_vars inventory to github repository.
```yaml
- name: Persist the facts into remote data_store which is a github repository
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: Network BGP Manager
    ansible.builtin.include_role:
      name: network.bgp.run
    vars:
      ansible_network_os: cisco.ios.ios
      operations:
        - name: persist
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

### Display Structured Data with Gather
- Gather operation gathers the running-confguration specific to bgp_global, bgp_address_family and bgp_neighbor_address_family resources
  and display these facts in YAML formatted structures.

```yaml
- name: Display BGP resources in structured format
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: BGP Manager
    ansible.builtin.include_role:
      name: network.bgp.run
    vars:
      ansible_network_os: cisco.ios.ios
      operations:
        - name: gather
```

### Deploy BGP Configuration
- Deploy operation will read the facts from the provided/default or remote inventory and deploy the changes on to the appliances.

#### read host_vars from local data_store and deploy on to the field.
```yaml
- name: Deploy changes
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: Network BGP Manager
    ansible.builtin.include_role:
      name: network.bgp.run
    vars:
      ansible_network_os: cisco.ios.ios
      operations:
        - name: deploy
      data_store:
        local: "~/backup/network"
```

#### retrieve host_cars from github repository and deploy changes on to the field.
```yaml
- name: retrieve config from github repo and deploy changes
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: Network BGP Manager
    ansible.builtin.include_role:
      name: network.bgp.run
    vars:
      ansible_network_os: cisco.ios.ios
      operations:
        - name: deploy
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

### Detect configuration drift in BGP Configuration
- Detect operation will read the facts from the local provided/default inventory and detect if any configuration diff exist w.r.t running-config.

#### detect the config difference between host_vars in local data_store and running config.

```yaml
- name: Configuration drift detection
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: Network BGP Manager
    ansible.builtin.include_role:
      name: network.bgp.run
    vars:
      ansible_network_os: cisco.ios.ios
      operations:
        - name: detect
      data_store:
        local: "~/backup/network"
```

- Detect operation will read the facts from github repository inventory and detect if any configuration diff exist w.r.t running-config.

#### detect the config difference between host_vars in local data_store and running config.
```yaml
- name: Configuration drift detection
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: Network BGP Manager
    include_role:
      name: network.bgp.run
    vars:
      ansible_network_os: cisco.ios.ios
      operations:
        - name: detect
      data_store:
        scm:
          origin:
            url: "{{ your_github_repo }}"
            token: "{{ github_access_token }}"
            user:
              name: "{{ ansible_github }}"
              email: "{{ your_email@example.com }}"
```

#### Remediate configuration drift in BGP Configuration
- Remediate operation will read the facts from the locally provided/default inventory and remediate if any configuration changes are there on the appliances using overridden state.

```yaml
- name: Remediate configuration
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: Network BGP Manager
    include_role:
      name: network.bgp.run
    vars:
      ansible_network_os: cisco.ios.ios
      operations:
        - name: remediate
      data_store:
        local: "~/backup/network"
```
- Remediate operation will read the facts from github repository and remediate if any configuration changes are there on the appliances using overridden state.

```yaml
- name: Remediate configuration
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: Network BGP Manager
    include_role:
      name: network.bgp.run
    vars:
      ansible_network_os: cisco.ios.ios
      operations:
        - name: remediate
      data_store:
        scm:
          origin:
            url: "{{ your_github_repo }}"
            token: "{{ github_access_token }}"
            user:
              name: "{{ ansible_github }}"
              email: "{{ your_email@example.com }}"

### Code of Conduct
This collection follows the Ansible project's
[Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html).
Please read and familiarize yourself with this document.


## Release notes

Release notes are available [here](https://github.com/redhat-cop/network.bgp/blob/main/CHANGELOG.rst).

## Licensing

GNU General Public License v3.0 or later.

See [COPYING](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
