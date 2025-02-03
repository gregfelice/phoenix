llama3.2:latest > 30-configure-postgres-server - LLM Call Duration: 18.495819583997218
Here is an example of an Ansible role to install PostgreSQL Server.

**Directory Structure**
```bash
roles/postgresql/
meta/
main.yml
tasks/
main.yml
variables/
default.yml
```

**File: roles/postgresql/meta/main.yml**

```yaml
---
# meta information for the role
name: postgresql
description: 'Install and configure Postgres'
author: Your Name
version: 1.0

# categories
categories:
  - db
  - system
```

**File: roles/postgresql/tasks/main.yml**

```yaml
---
- name: Install PostgreSQL dependencies
  apt:
    name: libpq-dev
    state: present

- name: Add PostgreSQL repository
  apt_repository:
    repo: 'http://apt.postgresql.org/pub/repos/apt {{ ansible_distribution }}{{ ansible_distribution_version }} main'
    state: present

- name: Update package list and upgrade
  apt:
    update_cache: yes
    cache_valid_time: 3600
    upgrade: dist
    state: up-to-date

- name: Install PostgreSQL
  apt:
    name: postgresql
    state: present

- name: Start PostgreSQL service
  service:
    name: postgresql
    enabled: yes
    state: started

- name: Configure PostgreSQL to start on boot
  service:
    name: postgresql
    enabled: yes
    state: restarted

- name: Create Postgres user and database
  user:
    name: {{ postres_user }}
    group: postgres
    home: /var/lib/postgresql
    append: true
  become_method: sudo

  - name: create Database
    postgresql_db:
      name: {{ postres_database }}
      state: present

- name: Create Postgres init file
  template:
    src: templates/init.d.erb
    dest: /etc/init.d/postgresql
    mode: '0644'
  become_method: sudo

- name: Make init file executable
  file:
    path: /etc/init.d/postgresql
    state: link
    create: yes
    mode: '0755'

  - name: create postgres systemd service
    template:
      src: templates/systemd.service.erb
      dest: /etc/systemd/system/postgresql.service
      mode: '0644'
    become_method: sudo

  - name: enable and start postgres service
    service:
      name: postgresql
      enabled: yes
      state: started
```

**File: roles/postgresql/templates/init.d.erb**

```erb
#!/usr/bin/env bash

# Start PostgreSQL server
pg_ctl start -D /var/lib/postgresql

# Stop PostgreSQL server on exit
trap "pg_ctl stop -D /var/lib/postgresql" EXIT
```

**File: roles/postgresql/templates/systemd.service.erb**

```erb
[Unit]
Description=PostgreSQL Server
After=network.target

[Service]
User={{ postres_user }}
ExecStart=/usr/lib/postgresql/{{ postgresql_version }}/bin/pg_ctl start -D /var/lib/postgresql
Restart=always

[Install]
WantedBy=multi-user.target
```

**File: roles/postgresql/variables/default.yml**

```yaml
---
postres_user: 'myuser'
postres_database: 'mydb'
postgresql_version: '14'
```

To use this role, you will need to create a playbook that includes the `roles` directory and specifies the host(s) where you want to install PostgreSQL.

**File: playbooks/install_postgresql.yml**

```yaml
---
- name: Install Postgres on target hosts
  hosts: weywot, yerbouti, waza
  become: yes

  roles:
    - role: postgresql
```

You can then run the playbook with `ansible-playbook`:

```bash
ansible-playbook -i hosts install_postgresql.yml
```

This will install PostgreSQL on the specified hosts and configure it to start automatically.