qwen2.5-coder:latest > 10-configure-ansible - LLM Call Duration: 28.61583412499931
Here is an Ansible role that you can use to install software packages on your system environments. The role will detect if the OS is Debian or macOS and use the appropriate package manager (`apt` for Debian and `brew` for macOS). It will install the specified packages: `git`, `zsh`, `oh-my-zsh`, `btop`, and `htop`.

```yaml
---
- name: Install software packages
  hosts: all
  become: yes

  vars:
    packages_debian:
      - git
      - zsh
      - btop
      - htop

    packages_macos:
      - git
      - zsh
      - oh-my-zsh
      - btop
      - htop

  tasks:
    - name: Detect OS and set package manager
      set_fact:
        os_family: "{{ ansible_os_family }}"
        package_manager: ""
      when: ansible_os_family == "Debian"

    - name: Set package manager to apt for Debian
      set_fact:
        package_manager: "apt"
      when: ansible_os_family == "Debian"

    - name: Set package manager to brew for macOS
      set_fact:
        package_manager: "brew"
      when: ansible_os_family == "Darwin"

    - name: Install packages using apt (Debian)
      apt:
        name: "{{ item }}"
        state: present
      loop: "{{ packages_debian }}"
      when: ansible_os_family == "Debian"

    - name: Update Homebrew
      homebrew:
        state: latest

    - name: Install packages using brew (macOS)
      homebrew:
        name: "{{ item }}"
        state: present
      loop: "{{ packages_macos }}"
      when: ansible_os_family == "Darwin"
```

### Explanation:

1. **Detect OS and Set Package Manager**:
   - The role first detects the operating system family using `ansible_os_family`.
   - It initializes a variable `package_manager` to an empty string.

2. **Set Package Manager Based on OS Family**:
   - If the OS is Debian (`ansible_os_family == "Debian"`), it sets `package_manager` to `"apt"`.
   - If the OS is macOS (`ansible_os_family == "Darwin"`), it sets `package_manager` to `"brew"`.

3. **Install Packages Using apt (Debian)**:
   - The role loops through the list of packages for Debian and installs them using the `apt` module.
   - This task runs only if the OS is Debian.

4. **Update Homebrew**:
   - Before installing packages on macOS, it updates Homebrew to ensure that the latest versions are available.

5. **Install Packages Using brew (macOS)**:
   - The role loops through the list of packages for macOS and installs them using the `homebrew` module.
   - This task runs only if the OS is macOS.

### Usage:

1. Save this role code to a file named `install_packages.yml`.
2. Create an inventory file that includes your machines, e.g., `hosts.ini`:
    ```ini
    [all]
    weywot ansible_host=your_macos_ip_or_hostname
    yerbouti ansible_host=your_debian_ip_or_hostname
    waza ansible_host=your_debian_server_ip_or_hostname
    ```
3. Run the role using the following command:
    ```sh
    ansible-playbook -i hosts.ini install_packages.yml
    ```

This setup will ensure that the specified packages are installed on all your machines based on their operating system family.