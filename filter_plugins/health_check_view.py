from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
    name: health_check_view
    author: Rohit Thakur (@rohitthakur2590)
    version_added: "1.0.0"
    short_description: Generate the filtered health check dict based on the provided target.
    description:
        - Generate the filtered health check dict based on the provided target.
    options:
      health_facts:
        description: Specify the health check dictionary.
        type: dict
"""

EXAMPLES = r"""
- name: health_check
    vars:
      checks:
        - name: all_neighbors_up
          ignore_errors: true
        - name: all_neighbors_down
          ignore_errors: true
        - name: min_neighbors_up
          min_count: 1
        - name: bgp_status_summary

- set_fact:
   "bgp_health":{
        "bgp_table_version": 3,
        "local_as": 500,
        "neighbors": [
            {
                "bgp_table_version": 3,
                "input_queue": 0,
                "msg_rcvd": 52076,
                "msg_sent": 52111,
                "output_queue": 0,
                "peer": "12.0.0.1",
                "peer_as": 500,
                "peer_state": 1,
                "uptime": "4w4d",
                "version": 4
            },
            {
                "bgp_table_version": 1,
                "input_queue": 0,
                "msg_rcvd": 0,
                "msg_sent": 0,
                "output_queue": 0,
                "peer": "23.0.0.1",
                "peer_as": 500,
                "peer_state": "Idle",
                "uptime": "never",
                "version": 4
            }
        ],
        "path": {
            "memory_usage": 288,
            "total_entries": 2
        },
        "route_table_version": 3,
        "router_id": "192.168.255.229"
    }

- name: Set health checks fact
  ansible.builtin.set_fact:
     health_checks: "{{ bgp_health | health_check_view(item) }}"

ok: [192.168.22.43] => {
    "failed_when_result": false,
    "health_checks": {
        "all_neighbors_down": {
            "check_status": "unsuccessful",
            "down": 1,
            "total": 2,
            "up": 1
        },
        "all_neighbors_up": {
            "check_status": "unsuccessful",
            "down": 1,
            "total": 2,
            "up": 1
        },
        "bgp_status_summary": {
            "down": 1,
            "total": 2,
            "up": 1
        },
        "min_neighbors_up": {
            "check_status": "successful",
            "down": 1,
            "total": 2,
            "up": 1
        },
        "status": "successful"
    }
}
"""

RETURN = """
  health_checks:
    description: BGP health checks 
    type: dict

"""

from ansible.errors import AnsibleFilterError

ARGSPEC_CONDITIONALS = {}


def health_check_view(*args, **kwargs):
    params = ["health_facts", "target"]
    data = dict(zip(params, args))
    data.update(kwargs)
    if len(data) < 2:
        raise AnsibleFilterError(
            "Missing either 'health facts' or 'other value in filter input,"
            "refer 'ansible.utils.health_check_view' filter plugin documentation for details",
        )

    health_facts = data["health_facts"]
    target = data["target"]
    health_checks = {}
    health_checks['status'] = 'successful'
    if target['name'] == 'health_check':
        vars = target.get('vars')
        if vars:
            checks = vars.get('checks')
            dn_lst = []
            un_lst = []
            for item in health_facts['neighbors']:
                if item['peer_state'] in ('Established', 1):
                    item['peer_state'] = 'Established'
                    un_lst.append(item)
                else:
                    dn_lst.append(item)
            stats = {}
            stats['up'] = len(un_lst)
            stats['down'] = len(dn_lst)
            stats['total'] = stats['up'] + stats['down']

            details = {}
            data = get_health(checks)

            if data['summary']:
                n_dict = {}
                n_dict.update(stats)
                if vars.get('details'):
                    details['neighbors'] = un_lst
                    n_dict['details'] = details
                health_checks[data['summary'].get('name')] = n_dict

            if data['all_up']:
                n_dict = {}
                n_dict.update(stats)
                if vars.get('details'):
                    details['neighbors'] = un_lst
                    n_dict['details'] = details
                n_dict['check_status'] = get_status(stats, 'up')
                if n_dict['check_status'] == 'unsuccessful' and not data['all_up'].get('ignore_errors'):
                    health_checks['status'] = 'unsuccessful'
                health_checks[data['all_up'].get('name')] = n_dict

            if data['all_down']:
                n_dict = {}
                details = {}
                n_dict.update(stats)
                if vars.get('details'):
                    details['neighbors'] = dn_lst
                    n_dict['details'] = details
                n_dict['check_status'] = get_status(stats, 'down')
                if n_dict['check_status'] == 'unsuccessful' and not data['all_down'].get('ignore_errors'):
                    health_checks['status'] = 'unsuccessful'
                health_checks[data['all_down'].get('name')] = n_dict

            if data['min_up']:
                n_dict = {}
                details = {}
                n_dict.update(stats)
                if vars.get('details'):
                    details['neighbors'] = un_lst
                    n_dict['details'] = details
                n_dict['check_status'] = get_status(stats, 'min', data['min_up']['min_count'])
                if n_dict['check_status'] == 'unsuccessful'  and not data['min_up'].get('ignore_errors'):
                    health_checks['status'] = 'unsuccessful'
                health_checks[data['min_up'].get('name')] = n_dict
        else:
            health_checks = health_facts
    return health_checks


def get_status(stats, check, count=None):
    if check in ('up', 'down'):
        return 'successful' if stats['total'] == stats[check] else 'unsuccessful'
    else:
        return 'successful' if count <= stats['up'] else 'unsuccessful'

def get_ignore_status(item):
    if not item.get("ignore_errors"):
        item['ignore_errors'] = False
    return item

def is_present(health_checks, option):
    for item in health_checks:
        if item['name'] == option:
             return get_ignore_status(item)
    return None

def get_health(checks):
    dict = {}
    dict['summary'] = is_present(checks, 'bgp_status_summary')
    dict['all_up'] = is_present(checks, 'all_neighbors_up')
    dict['all_down'] = is_present(checks, 'all_neighbors_down')
    dict['min_up'] = is_present(checks, 'min_neighbors_up')

    return dict


class FilterModule(object):
    """health_check_view"""

    def filters(self):
        """a mapping of filter names to functions"""
        return {"health_check_view": health_check_view}
