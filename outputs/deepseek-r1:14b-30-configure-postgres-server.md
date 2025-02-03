deepseek-r1:14b > 30-configure-postgres-server - LLM Call Duration: 75.96224237500064
<think>
Okay, I need to create an Ansible role to install PostgreSQL on a server. The user has three machines: weywot (MacOS), yerbouti (Debian), and waza (Debian) which is their main server for testing and production. They want the role specifically for waza.

First, I should structure the Ansible role properly. That means creating a directory with tasks, handlers, etc. But since they just need code, maybe I can focus on the key parts of the Ansible playbook or role.

I'll start by updating the package list to ensure everything is up to date. Then install PostgreSQL packages using apt-get. After installation, I should enable the service so it starts at boot and starts immediately.

Wait, for Debian, sometimes you have to select a version of PostgreSQL during installation. Maybe using 'postgresql postgresql-13' as a dependency? Or perhaps use 'apt-get install postgresql'? Hmm, maybe better to specify the exact package name if needed, but for simplicity, I'll go with 'postgresql'.

Next steps: create a database user and set up some configuration. It's common to have a 'webuser' for applications. So in the tasks, I can add a user and create a database for it.

I should also configure PostgreSQL settings. Maybe tweak the config files like pg_hba.conf to allow connections from other hosts if necessary. But since waza is the main server, maybe that's not needed right now unless they plan to connect remotely.

Another thing: ensure that after installation, the service is running. So I'll include a task to start and enable the service.

Also, consider handling any errors or prompting for user input during installation. For example, if PostgreSQL asks about data directory during installation, Ansible might need to handle that. Maybe using 'become' with 'yes' in the command to confirm.

Wait, perhaps using the 'postgresql' module in Ansible would be better than shell commands. But I'm not sure if it's available for Debian. Alternatively, using apt and then shell commands to set up the user and databases might be more straightforward.

I should write the tasks in YAML. So the steps are:

1. Update packages.
2. Install PostgreSQL server and client tools.
3. Enable PostgreSQL service.
4. Start PostgreSQL service.
5. Create a new user (webuser) with a password, maybe prompting for it or setting it securely.
6. Create a database owned by webuser.

Also, perhaps include a task to reload PostgreSQL configuration after any changes, but since we're just creating users and databases, maybe that's not necessary here.

Wait, in the example provided earlier, they used 'apt-get install postgresql' which might not be correct because on Debian, you have to choose versions. Maybe better to use 'postgresql-13' or specify the exact package name. But for simplicity, I'll proceed as before.

Another consideration: after installation, sometimes PostgreSQL requires a restart. So maybe adding a command to reload the service configuration or restart it.

I think that's the main flow. Now, putting this into Ansible tasks with the correct syntax and making sure variables are handled properly, especially for passwords which should be prompted if not provided.
</think>

Here is an Ansible role to install PostgreSQL on your system:

```yaml
---
#ansible-role-yml
- name: Update package lists
  apt:
    update_cache: yes

- name: Install PostgreSQL server and client
  apt:
    name: postgresql
    state: present
  register: postgresql_install

- name: Enable PostgreSQL service to start on boot
  ansible.builtin.systemd:
    name: postgresql.service
    enabled: yes
    state: started

- name: Create PostgreSQL user and database
  become: yes
  shell: |
    echo "CREATE USER webuser WITH ENCRYPTED PASSWORD '{{ password }}';" | sudo -u postgres psql -U postgres;
    echo "CREATE DATABASE webapp OWNER webuser;" | sudo -u postgres psql -U postgres;

- name: Ensure PostgreSQL is running
  service:
    name: postgresql
    state: started
    enabled: yes
```

To use this role, you would create a playbook like:

```yaml
---
#ansible-playbook-yml
- hosts: waza
  become: true
  vars_prompt:
    - name: password
      prompt: "Enter the desired PostgreSQL webuser password"
  roles:
    - postgresql_installation
```

This role will install PostgreSQL, enable it as a service, create a user (webuser) and database (webapp), and ensure PostgreSQL is running.

**Note:** Make sure you have `postgresql` package available in your Debian repositories. If not, add the PostgreSQL repository following their [installation instructions](https://www.postgresql.org/download/linux/debian/).