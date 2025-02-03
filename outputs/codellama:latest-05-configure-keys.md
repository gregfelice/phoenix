codellama:latest > 05-configure-keys - LLM Call Duration: 18.99578979100079
Here is an example of an Ansible role that installs software packages on every host in a given inventory:
```yaml
---
- name: Install software packages
  hosts: all
  become: true
  tasks:
    - name: Detect operating system and set package manager
      set_fact:
        os_type: "{{ ansible_distribution | lower }}"
        package_manager: "brew"
      when: os_type == "macos"

    - name: Install software packages using package manager
      package:
        name: "{{ item.name }}"
        state: present
      with_items:
        - { name: "git", version: "2.34" }
        - { name: "curl", version: "7.89" }
        - { name: "python3", version: "3.10" }
      when: package_manager == "brew"

    - name: Install software packages using package manager
      apt:
        name: "{{ item.name }}"
        state: present
      with_items:
        - { name: "git", version: "2.34" }
        - { name: "curl", version: "7.89" }
        - { name: "python3", version: "3.10" }
      when: package_manager == "apt"
```
This role will install the following software packages on every host in your inventory:

* Git 2.34
* Curl 7.89
* Python 3.10

The role uses the `ansible_distribution` variable to detect the operating system type and set the package manager accordingly. On macOS, it sets the package manager to Homebrew (which is a package manager for macOS). On Debian-based systems, it sets the package manager to APT (Advanced Package Tool).

The role then uses the `package` or `apt` module to install each software package using the corresponding package manager. The `with_items` keyword allows you to specify a list of packages and their versions that should be installed. In this case, we are installing Git 2.34, Curl 7.89, and Python 3.10.

Note that this is just an example role and you may need to modify it to fit your specific needs. You can also add more tasks or modules to the role as needed.