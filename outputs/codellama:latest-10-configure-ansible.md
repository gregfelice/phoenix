codellama:latest > 10-configure-ansible - LLM Call Duration: 17.428449875000297
Ansible Role to Install Software Packages on Every Host
-------------------------------------------------------

In this role, we will install software packages on every host using the appropriate package manager based on the operating system. We will use `brew` on macOS and `apt` on Debian.

### Tasks

* Detect the operating system of each host
* Install the necessary software packages
  * Git on macOS
  * Zsh, Oh-My-Zsh, and Btop on Debian
  * Htop on Debian

### Variables

* `os_family`: The family of the operating system (Debian or macOS)
* `packages`: A list of packages to install
* `macos_packages`: A list of macOS-specific packages to install
* `debian_packages`: A list of Debian-specific packages to install

### Playbook

```yaml
---
- name: Install software packages on every host
  hosts: all
  become: true

  tasks:
    - name: Detect operating system family
      set_fact:
        os_family: "{{ ansible_system | regex_search('^macos', ignorecase=True) ? 'macos' : 'debian' }}"

    - name: Install necessary packages
      package:
        name: "{{ packages }}"
        state: present
      when: os_family == 'macos'

    - name: Install Debian-specific packages
      package:
        name: "{{ debian_packages }}"
        state: present
      when: os_family == 'debian'
```

### Example Inventory

```ini
[all]
weywot ansible_host=localhost
yerbouti ansible_host=192.168.0.100
waza ansible_host=192.168.0.101

[macos]
weywot

[debian]
yerbouti waza
```

### Example Playbook Run

```bash
ansible-playbook -i inventory install_packages.yml
```