qwen2.5-coder:latest > 30-configure-postgres-server - LLM Call Duration: 22.016285083000184
Sure, here is an Ansible role to install and configure PostgreSQL on a Debian-based system (like `yerbouti` and `waza`). This role will ensure that PostgreSQL is installed, configured with default settings, and ready to use.

First, create the role using the following command:

```bash
ansible-galaxy init roles/postgresql
```

Now, navigate into the newly created `roles/postgresql` directory and modify the following files:

### `roles/postgresql/tasks/main.yml`
This file will contain the tasks to install PostgreSQL and its dependencies.

```yaml
---
- name: Ensure PostgreSQL is installed
  apt:
    name: postgresql postgresql-contrib
    state: present

- name: Ensure PostgreSQL service is running
  service:
    name: postgresql
    state: started
    enabled: yes

- name: Create a default PostgreSQL user
  postgresql_user:
    db: postgres
    user: postgres
    password: "{{ 'your_password' | b64decode }}"
    role_attr_flags: LOGIN,REPLICATION,CREATEDB,CREATEROLE
```

### `roles/postgresql/handlers/main.yml`
This file will contain handlers to restart PostgreSQL if changes are made.

```yaml
---
- name: Restart PostgreSQL service
  service:
    name: postgresql
    state: restarted
```

### `roles/postgresql/vars/main.yml`
This file will contain the variables for the role, such as default passwords.

```yaml
---
postgresql_password: "{{ 'your_password' | b64decode }}"
```

### `roles/postgresql/meta/main.yml`
Ensure that dependencies and metadata are correctly set up.

```yaml
---
dependencies:
  - name: ansible.posix
    version: "2.9"
```

### Usage in Playbooks
You can use this role in your playbooks to apply it to the relevant hosts (`yerbouti` and `waza`). Here is an example playbook:

#### `playbooks/install_postgresql.yml`
```yaml
---
- name: Install PostgreSQL on Debian-based systems
  hosts: yerbouti, waza
  become: yes
  roles:
    - role: postgresql
```

### Notes:
1. Replace `'your_password' | b64decode` with an actual password or use a vault to manage sensitive data.
2. Ensure that the `hosts` in your playbook match the hostnames of your machines (`yerbouti`, `waza`).
3. If you need more advanced configurations, such as creating databases or users, you can extend the role by adding tasks and handlers accordingly.

Run the playbook using:

```bash
ansible-playbook -i inventory playbooks/install_postgresql.yml
```

Replace `inventory` with your actual inventory file that contains the hostnames and IP addresses of your machines.