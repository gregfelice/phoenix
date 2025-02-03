gemma2:27b > 10-configure-ansible - LLM Call Duration: 87.62193516700063
```yaml
---
- hosts: all
  become: true
  roles:
    - software

roles/software:
  tasks:
    - name: Install Git
      apt:
        name: git
        state: present
      when: ansible_os_family == "Debian"

    - name: Install Git (Brew)
      brew:
        name: git
        state: present
      when: ansible_os_family == "Darwin"

    - name: Install Zsh
      apt:
        name: zsh
        state: present
      when: ansible_os_family == "Debian"

    - name: Install Zsh (Brew)
      brew:
        name: zsh
        state: present
      when: ansible_os_family == "Darwin"

    - name: Install Oh My Zsh
      shell: sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
      become: true

    - name: Install Btop
      apt:
        name: btop
        state: present
      when: ansible_os_family == "Debian"

    - name: Install Btop (Brew)
      brew:
        name: btop
        state: present
      when: ansible_os_family == "Darwin"

    - name: Install Htop
      apt:
        name: htop
        state: present
      when: ansible_os_family == "Debian"

    - name: Install Htop (Brew)
      brew:
        name: htop
        state: present
      when: ansible_os_family == "Darwin"
```


**Explanation:**



* **hosts: all:** This line specifies that the role will be applied to all hosts defined in your Ansible inventory.

* **become: true:**  This enables privilege escalation using `sudo` (or equivalent) for tasks requiring root access.

* **roles: - software:** This defines the `software` role, which we'll create in a subdirectory named "roles".

**Inside the `software` Role:**
 
* **tasks:** A list of Ansible tasks to be executed.

*  **apt/brew tasks:**

    * Each task uses either `apt` (for Debian) or `brew` (for macOS).
    * The `when:` clause ensures that the correct package manager is used based on the `ansible_os_family` fact.

* **Oh My Zsh Installation:** 
   * This task downloads and runs the Oh My Zsh installation script directly from GitHub using a shell command.


**Important Notes:**



* **Inventory:** You'll need to have an Ansible inventory file (usually named `hosts`) that defines your machines (`weywot`, `yerbouti`, `waza`).

* **Running Ansible:**  Use the following command to run the playbook:
   ```bash
   ansible-playbook -i hosts playbook.yml
   ``` 
   Replace `playbook.yml` with the actual name of your playbook file.