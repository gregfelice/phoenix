llama3.2:latest > 10-configure-ansible - LLM Call Duration: 24.790420707999147
Here is an Ansible role that installs the required software packages on Debian and macOS systems:

```yml
---
- name: Install required packages
  hosts: weywot
  become: yes
  roles:
    - install_packages

- name: Install required packages (Debian)
  hosts: yerbouti, waza
  become: yes
  roles:
    - install_packages

- name: Install required packages (MacOS)
  hosts: weywot
  become: no
  roles:
    - install_packages_macos
```

```yml
---
- name: Install required packages
  hosts: all
  become: yes
  vars:
    package_manager:
      deb: apt
      brew: macos

  tasks:
  - name: Determine package manager
    set_fact:
      package_manager: "{{ package_manager | default('apt') }}"

  - name: Install Git
    apt:
      name: git
      state: present

  - name: Install Zsh
    apt:
      name: zsh
      state: present

  - name: Install Oh-my-Zsh
    apt:
      name: ohmyzsh
      state: present

  - name: Configure Oh-my-Zsh
    template:
      src: templates/zshrc.j2
      dest: /etc/zsh/zshrc
      mode: '0644'
      notify: restart zsh

  - name: Install Btop
    apt:
      name: btop
      state: present

  - name: Install Htop
    apt:
      name: htop
      state: present

- name: Install required packages (MacOS)
  hosts: weywot
  become: no
  vars:
    package_manager: "{{ package_manager | default('brew') }}"

  tasks:
  - name: Determine package manager
    set_fact:
      package_manager: "{{ package_manager | default('brew') }}"

  - name: Install Git
    brew:
      name: git
      state: present

  - name: Install Zsh
    brew:
      name: zsh
      state: present

  - name: Install Oh-my-Zsh
    template:
      src: templates/zshrc.j2
      dest: ~/.zshrc
      mode: '0644'
      notify: restart zsh

  - name: Configure Oh-my-Zsh
    template:
      src: templates/zshrc.bash.j2
      dest: ~/.zshrc
      mode: '0644'
      notify: restart zsh

  - name: Install Btop
    brew:
      name: btop
      state: present

  - name: Install Htop
    brew:
      name: htop
      state: present

- handlers:
  - name: restart zsh
    command: /bin/zsh -f
```

```yml
---
- name: templates
  files:
    path: templates
    state: dir
    mode: '0755'

- name: templates/zshrc.j2
  template:
    src: templates/zshrc.j2
    dest: /etc/zsh/zshrc.j2
    mode: '0644'
```

```yml
---
- name: templates
  files:
    path: templates
    state: dir
    mode: '0755'

- name: templates/zshrc.bash.j2
  template:
    src: templates/zshrc.bash.j2
    dest: ~/.zshrc
    mode: '0644'
```

This role first determines the package manager based on the operating system. For Debian and macOS, it uses `apt` and `brew` respectively. It then installs Git, Zsh, Oh-my-Zsh, Btop, and Htop using the chosen package manager.

For macOS, it uses a separate template for the zshrc file to handle the bash syntax used in Oh-my-Zsh.

Please make sure you have the `templates` directory created in your role's files directory. The templates are placed there so they can be used by the `template` module.

You will need to create the `templates` directory and add the two templates (`zshrc.j2` and `zshrc.bash.j2`) inside it. These templates should contain the content for the zshrc file, which is specific to Oh-my-Zsh.

For Debian:
```bash
# ~/.zshrc.j2

source /etc/zsh/zshrc

setopt unset_copy_on_assign

export EDITOR=feh --bg-size fill --bg-scale 200%
```

For macOS:
```bash
# ~/.zshrc.bash.j2

export EDITOR='feh --bg-size fill --bg-scale 200%'

if [[ -f ~/Library/Zsh/oh-my-zsh/custom/zprofile ]]; then
    source ~/Library/Zsh/oh-my-zsh/custom/zprofile
fi

unset_copy_on_assign
```

Make sure to adjust the `EDITORS` variable in your role's vars file according to your needs.

Please let me know if you need further assistance.