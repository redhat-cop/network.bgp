# Network BGP Validated Content
[![CI](https://github.com/ansible-network/network.bgp/actions/workflows/tests.yml/badge.svg?event=schedule)](https://github.com/ansible-network/network.bgp/actions/workflows/tests.yml)
[![OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/projects/7404/badge)](https://bestpractices.coreinfrastructure.org/projects/7404)

This repository contains the `network.bgp` Ansible Collection.

## Description

The `network.bgp` enables users to manage the BGP resources independent of platforms and perform BGP health checks.

## Tested with Ansible

Tested with ansible-core 2.13 releases.

## Installation
#### Install from Automation Hub

To consume this Validated Content from Automation Hub, the following needs to be added to `ansible.cfg`:

```
[galaxy]
server_list = automation_hub

[galaxy_server.automation_hub]
url=https://cloud.redhat.com/api/automation-hub/
auth_url=https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token
token=<SuperSecretToken>
```
Get the required token from the [Automation Hub Web UI](https://console.redhat.com/ansible/automation-hub/token).

With this configured, simply run the following commands:

```
ansible-galaxy collection install network.bgp
```

**Capabilities**
- `Build Brownfield Inventory`: This enables users to fetch the YAML structured resource module facts for BGP resources like bgp_global, bgp_address_family
  and bgp_neighbor_address_family and save it as host_vars to local or remote data store which could be used as a single SOT for other operations.
- `BGP Resource Management`: Users want to be able to manage the BGP global, BGP address family and BGP neighbor address family configurations.
  This also includes the enablement of gathering facts, updating BGP resource host-vars, and deploying config onto the appliance.
- `BGP Health Checks`: Users want to be able to perform health checks for BGP applications. These health checks should be  able to provide the BGP neighborship status with necessary details.
- Detect Drift and remediate: This enables users to detect any drift between provided config and the running config and if required then override the running config.

### Usage
- This platform-agnostic role enables the user to perform BGP health checks. Users can perform the following health checks:
       `all_neigbors_up`
       `all_neighbors_down`
       `min_neighbors_up`
       `bgp_status_summary`
- This role enables users to create a runtime brownfield inventory with all the BGP configurations in terms of host vars. These host vars are ansible facts that have been gathered through the *_bgp_global and *_bgp_address_family network resource modules. The tasks offered by this role could be observed below:

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
  - name: BGP Manager
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
- Persist operation fetches the bgp_global and bgp_address_family facts and stores them as host vars.
- Result of a successful Persist operation would be host_vars having YAML formatted resource facts.
- These host_vars could exist locally or even be published to a remote repository acting as SOT for operations like deploy, remediate, detect, etc.

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

#### fetch bgp resource facts and publish persisted host_vars inventory to GitHub repository.
```yaml
- name: Persist the facts into remote data_store which is a GitHub repository
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
- Gather operation gathers the running-configuration specific to bgp_global, bgp_address_family, and bgp_neighbor_address_family resources
  and display these facts in YAML formatted structures.

```yaml
- name: Display BGP resources in a structured format
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
- Deploy operation will read the facts from the provided/default or remote inventory and deploy the changes onto the appliances.

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

#### retrieve host_cars from the GitHub repository and deploy changes onto the field.
```yaml
- name: retrieve config from GitHub repo and deploy changes
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
- Detect operation will read the facts from the local provided/default inventory and detect if any configuration diff exists w.r.t running-config.

#### detect the config difference between host_vars in local data_store and running-config.

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

- Detect operation will read the facts from the GitHub repository inventory and detect if any configuration diff exists w.r.t running-config.

#### detect the config difference between host_vars in local data_store and running-config.
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
- Remediate operation will read the facts from GitHub repository and remediate if any configuration changes are there on the appliances using overridden state.

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
