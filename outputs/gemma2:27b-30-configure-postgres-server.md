gemma2:27b > 30-configure-postgres-server - LLM Call Duration: 51.11647954200089
```yaml
---
- hosts: waza
  become: true
  roles:
    - postgresql

roles/postgresql:
  vars:
    pg_version: 14
  tasks:
    - name: Install PostgreSQL repository
      apt_repository:
        repo: 'deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main'
        state: present
        filename: postgresql.list

    - name: Update apt cache
      apt: update=yes

    - name: Install PostgreSQL server
      apt:
        name: postgresql-{{ pg_version }}
        state: present

    - name: Start and enable PostgreSQL service
      systemd:
        name: postgresql
        state: started
        enabled: yes
```

**Explanation:**


* **hosts:** Defines the target machine(s) for this role. In this case, it's "waza".
* **become:** Enables privilege escalation using sudo for tasks requiring root access.
* **roles:** Specifies the roles to be executed. Here we use a single role named "postgresql".

**Inside the `postgresql` role:**


* **vars:** Defines variables used within the role. We set the desired PostgreSQL version to 14.
* **tasks:** Contains a list of tasks to be performed:

    * **apt_repository:** Adds the PostgreSQL repository to the system's package sources.
    * **apt:** Updates the apt cache and installs the PostgreSQL server package for the specified version.
    * **systemd:** Starts the PostgreSQL service and enables it to start automatically on boot.



**Important Notes:**

* This role assumes you are using Debian-based systems. For other distributions, the repository URL and package name may differ.
* You can customize further by adding tasks for configuring user accounts, databases, etc., within this role.