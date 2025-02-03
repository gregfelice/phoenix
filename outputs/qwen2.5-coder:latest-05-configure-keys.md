qwen2.5-coder:latest > 05-configure-keys - LLM Call Duration: 27.645889041001283
Sure, here's an example of Ansible roles that you can use to configure your system environments based on their operating systems and install software packages. Additionally, the role will create and configure SSH keys for use with Ansible.

### Role: `common_packages`

This role will detect the OS and install the necessary software packages using the appropriate package manager (`apt` for Debian and `brew` for macOS).

```yaml
# roles/common_packages/tasks/main.yml

---
- name: Ensure Python is installed
  package:
    name: "{{ item }}"
    state: present
    update_cache: yes
  loop:
    - python3
    - python3-pip
  when: ansible_os_family == "Debian"

- name: Ensure Homebrew is installed on macOS
  homebrew:
    name: brew
    state: present

- name: Ensure Python is installed on macOS using Homebrew
  package:
    name: "{{ item }}"
    state: present
  loop:
    - python3
    - python3-pip
  when: ansible_os_family == "Darwin"

- name: Ensure Git is installed
  package:
    name: "{{ item }}"
    state: present
    update_cache: yes
  loop:
    - git
  when: ansible_os_family == "Debian"

- name: Ensure Git is installed on macOS using Homebrew
  package:
    name: git
    state: present
  when: ansible_os_family == "Darwin"
```

### Role: `ssh_keys`

This role will create and configure SSH keys for use with Ansible.

```yaml
# roles/ssh_keys/tasks/main.yml

---
- name: Ensure SSH directory exists
  file:
    path: "{{ ansible_user_dir }}/.ssh"
    state: directory
    mode: '0700'

- name: Create SSH key pair if it does not exist
  command: ssh-keygen -t rsa -b 4096 -N '' -f "{{ ansible_user_dir }}/.ssh/id_rsa"
  args:
    creates: "{{ ansible_user_dir }}/.ssh/id_rsa"

- name: Ensure public key is in the authorized_keys file
  copy:
    content: "{{ lookup('file', '{{ ansible_user_dir }}/.ssh/id_rsa.pub') }}"
    dest: "{{ ansible_user_dir }}/.ssh/authorized_keys"
    mode: '0600'
```

### Playbook

You can then use these roles in a playbook to configure your environments.

```yaml
# site.yml

---
- name: Configure system environments
  hosts:
    - all
  become: yes
  roles:
    - common_packages
    - ssh_keys
```

### Inventory File

Your inventory file should look something like this:

```ini
[all]
weywot ansible_host=192.168.1.100 ansible_user=your_macos_username
yerbouti ansible_host=192.168.1.101 ansible_user=your_debian_username
waza ansible_host=192.168.1.102 ansible_user=your_debian_username
```

Replace `your_macos_username`, `your_debian_username`, and the IP addresses with the actual values for your machines.

### Running the Playbook

To run the playbook, use the following command:

```sh
ansible-playbook -i inventory site.yml
```

This will configure all the specified hosts with the required software packages and SSH keys.