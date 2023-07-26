====================================
Network Bgp Collection Release Notes
====================================

.. contents:: Topics


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
