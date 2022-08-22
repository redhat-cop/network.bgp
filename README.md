## Network BGP Validated Content

### Overview

The `network.bgp` enables user to manage the BGP resources independent of platforms and perform BGP health checks.

**Capabilities**
- `Build Brownfield Inventory`: Users want to be able to get the facts for BGP resources and store it as host_vars thus enabling the capability to get facts for all the hosts within the inventory and store facts in a structured format which acts as SOT.
- `BGP Resource Management`: Users want to be able to manage the BGP global and BGP address family configurations.This also includes the enablement of gathering facts, updating BGP resource host-vars and deploying config onto the appliance.
- `BGP Health Checks`: Users want to be able to perform health checks for BGP applications.These health checks should be able to provide the BGP neighborship status with necessary details.

### Usage
- This platform agnostic role enables the user to perform BGP health checks.Users can perfrom following health checks:
       `all_neigbors_up`
       `all_neighbors_down`
       `min_neighbors_up`
- This role enables users to create a runtime brownfield inventory with all the BGP configuration in terms of host vars. These host vars are ansible facts which have been gathered through the *_bgp_global and *_bgp_address_family network resource module.The tasks offered by this role could be observed as below:

#### Perform BGP Health Checks
```yaml
health_checks.yml
---
- hosts: ios
  gather_facts: false
  tasks:
  - name: BGP Manager
    include_role:
      name: network.bgp.run
    vars:
      actions:
        - name: health_check
          vars:
            details: True
            checks:
              - name: all_neighbors_up
              - name: all_neighbors_down
              - name: min_neighbors_up
                min_count: 1
```


#### Building Brownfield Inventory
```
- hosts: ios
  gather_facts: false
  tasks:
  - name: BGP Manager
    include_role:
      name: network.bgp.run
    vars:
      actions:
        - name: persist
```

#### Gather BGP Facts
```
- hosts: ios
  gather_facts: false
  tasks:
  - name: BGP Manager
    include_role:
      name: network.bgp.run
    vars:
      actions:
        - name: gather
```

#### Gather Deploy BGP Configuration
```
- hosts: ios
  gather_facts: false
  tasks:
  - name: BGP Manager
    include_role:
      name: network.bgp.run
    vars:
      actions:
        - name: deploy
```
