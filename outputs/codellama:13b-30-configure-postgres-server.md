codellama:13b > 30-configure-postgres-server - LLM Call Duration: 23.770927166000547

Here is an Ansible role to install PostgreSQL on a Debian-based system:
```yaml
---
- name: Install PostgreSQL
  hosts: "waza"
  become: true
  vars:
    postgres_version: "13.3"
    postgres_data_dir: "/var/lib/postgresql"
  tasks:
    - name: Add the PostgreSQL APT repository to the system
      apt_repository:
        repo: "deb https://apt.postgresql.org/pub/repos/apt {{ ansible_distribution }} main"
        state: present

    - name: Install PostgreSQL package
      apt:
        name: postgresql-{{ postgres_version }}
        state: latest
```
This role will add the PostgreSQL APT repository to the system and then install the `postgresql-13.3` package from that repository. The `become` flag is set to `true`, which means that Ansible will run the task with elevated privileges.

You can customize this role by changing the version of PostgreSQL you want to install, as well as any other configuration options for the database server. For example, if you want to use a different data directory or change the default port number, you can do so by modifying the `vars` section of the role.

Once you have defined your role, you can apply it to the target machine by running the following command:
```yaml
ansible-playbook -i hosts install_postgres.yml
```
Replace `hosts` with the path to your inventory file if you are using one. This will run the playbook and install PostgreSQL on the target machine.