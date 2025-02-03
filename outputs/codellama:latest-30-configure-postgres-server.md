codellama:latest > 30-configure-postgres-server - LLM Call Duration: 13.792566207999698
Here is an Ansible role to install Postgres on a Debian system:
```yaml
---
- name: Install Postgres on Debian
  hosts: yerbouti
  become: true
  tasks:
    - name: Update package list
      apt_update:
        update_cache: yes
    - name: Install Postgres packages
      apt:
        name: postgresql
        state: present
    - name: Create Postgres user
      postgres_user:
        name: postgres
        password: "{{ ansible_password }}"
        priv: ALL=(ALL)NOPASSWD:ALL
    - name: Set Postgres password for root user
      postgres_privileges:
        name: root
        password: "{{ ansible_password }}"
        priv: ALL=(ALL)NOPASSWD:ALL
    - name: Create Postgres database
      postgres_db:
        name: mydb
        owner: postgres
```
This role uses the `apt` module to install the `postgresql` package, and the `postgres_user` and `postgres_privileges` modules to create a user with all privileges and set their password. The `postgres_db` module is used to create a database owned by the `postgres` user.

Note that this role assumes that you have already created an Ansible inventory file containing the hostnames of your machines, and that you have configured Ansible's connection credentials for each machine. If you have not done so, please refer to Ansible documentation on how to create an inventory file and configure connections.

Also note that this role does not include any logic for configuring Postgres or creating databases. It is intended as a starting point for installing and setting up Postgres on your Debian system.