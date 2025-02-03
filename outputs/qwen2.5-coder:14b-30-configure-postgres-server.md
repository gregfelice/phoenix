qwen2.5-coder:14b > 30-configure-postgres-server - LLM Call Duration: 45.52262100000007
Certainly! Below is an Ansible role to install PostgreSQL on your specified machines (`waza`, `yerbouti`). This role assumes that you have already set up your inventory file and SSH keys for passwordless access.

### Directory Structure

First, let's create the directory structure for the Ansible role:

```
roles/
└── postgresql_installation
    ├── tasks
    │   └── main.yml
    └── handlers
        └── main.yml
```

### Tasks (tasks/main.yml)

```yaml
---
- name: Ensure PostgreSQL is installed
  package:
    name: "{{ postgresql_package_name }}"
    state: present

- name: Start and enable PostgreSQL service
  systemd:
    name: "postgresql"
    enabled: yes
    state: started

- name: Create a new PostgreSQL role
  become_user: postgres
  postgresql_user:
    db: all
    name: "{{ postgresql_role_name }}"
    password: "{{ postgresql_role_password }}"
    priv: ALL
    state: present

- name: Create a new PostgreSQL database
  become_user: postgres
  postgresql_db:
    name: "{{ postgresql_database_name }}"
    owner: "{{ postgresql_role_name }}"
    state: present
```

### Handlers (handlers/main.yml)

```yaml
---
- name: Restart PostgreSQL service
  systemd:
    name: "postgresql"
    state: restarted
```

### Role Variables

You can define the variables in your inventory file or in a separate `vars` directory within the role. Here are some example variables:

```yaml
# Example inventory file (hosts.ini)
[waza,yerbouti]
waza ansible_host=your_waza_ip_address ansible_user=root
yerbouti ansible_host=your_yerbouti_ip_address ansible_user=root

[all:vars]
postgresql_package_name=postgresql postgresql
postgresql_role_name=myuser
postgresql_role_password=mypassword
postgresql_database_name=mydatabase
```

### Playbook (site.yml)

```yaml
---
- hosts: waza,yerbouti
  become: yes
  roles:
    - postgresql_installation
```

### Running the Playbook

To run the playbook, use the following command:

```bash
ansible-playbook -i hosts.ini site.yml
```

This will install PostgreSQL on both `waza` and `yerbouti`, create a new role and database with the specified credentials.

### Notes

- The `postgresql_package_name` may vary depending on your distribution. For Debian-based systems, it is usually `postgresql`. If you are using a different OS or version, you might need to adjust this variable.
- Ensure that the SSH keys for passwordless access are set up correctly before running the playbook.
- You can customize the role further by adding more tasks, variables, and handlers as needed.

This should provide a basic setup for installing PostgreSQL on your specified machines using Ansible.