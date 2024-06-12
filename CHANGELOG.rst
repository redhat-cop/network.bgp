====================================
Network Bgp Collection Release Notes
====================================

.. contents:: Topics


v6.0.0
======

Release Summary
---------------

With this release, the minimum required version of `ansible-core` for this collection is `2.15.0`. The last version known to be compatible with `ansible-core` versions below `2.15` is v5.0.0.


Major Changes
-------------

- Bumping `requires_ansible` to `>=2.15.0`, since previous ansible-core versions are EoL now.

Documentation Changes
---------------------

- Revised the instructions on when to utilize the token.
- Update readme as per the common template.
- Updated the URL to point to validated content instead of certified content.

v5.0.0
======

Release Summary
---------------

Starting from this release, the minimum `ansible-core` version this collection requires is `2.14.0`. The last known version compatible with ansible-core<2.14 is `v4.0.0`.

Major Changes
-------------

- Bumping `requires_ansible` to `>=2.14.0`, since previous ansible-core versions are EoL now.

v4.0.0
======

Major Changes
-------------

- Change `actions` to `operations`

Bugfixes
--------

- check if BGP is not active

Documentation Changes
---------------------

- Update tests for gather, persist, detect, remediate and deploy.

v3.0.0
======

Major Changes
-------------

- Enable scm based operations(https://github.com/redhat-cop/network.bgp/issues/30)

Bugfixes
--------

- add resources.yaml file.
- rename var in task.

v2.0.0
======

Major Changes
-------------

- Add ignore error features.
- Add summary health checks.
- Update health checks to collectively fail when any health-check fails.

Minor Changes
-------------

- Implement detect and remediate task enhancements.

Bugfixes
--------

- Fix filter plugins call issue for health checks.
- Fix issue of state in remediate and detect.

Documentation Changes
---------------------

- Update README with installation commands.
- Update examples.

v1.4.0
======

Minor Changes
-------------

- correct network resource manager role invoking

v1.3.0
======

Minor Changes
-------------

- Update parsers for network platforms

v1.2.0
======

Release Summary
---------------

Re-releasing v1.1.0 with updated version tag and fixed role name.

v1.1.0
======

Release Summary
---------------

Re-releasing v1.0.0 with updated version tag and fixed URLs for issues and repository in galaxy.yml.

v1.0.0
======

Minor Changes
-------------

- Add Network BGP role.
- Fix ansible lint erros.
