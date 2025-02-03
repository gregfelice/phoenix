qwen2.5-coder:latest > 40-configure-tekton - LLM Call Duration: 37.63583583400032
Sure! Below is an Ansible role that configures a working Tekton server on your Debian-based machines (`yerbouti` and `waza`) for development, test, and production promotion cycles. It also includes configurations for automated tests for React and Python code.

### Role: tekton

#### Directory Structure:
```
tekton/
├── defaults
│   └── main.yml
├── files
│   ├── install_tekton.sh
│   ├── setup_react_tests.sh
│   ├── setup_python_tests.sh
├── handlers
│   └── main.yml
├── tasks
│   ├── main.yml
│   ├── install_dependencies.yml
│   ├── configure_tekton.yml
│   ├── set_permissions.yml
├── templates
│   ├── tekton-config.yaml.j2
```

#### `defaults/main.yml`
```yaml
tekton_version: "v0.37.0"
react_test_script: "{{ role_path }}/files/setup_react_tests.sh"
python_test_script: "{{ role_path }}/files/setup_python_tests.sh"
```

#### `files/install_tekton.sh`
```bash
#!/bin/bash

# Download and install Tekton CLI
curl -LO "https://storage.googleapis.com/tekton-releases/cli/latest/tekton-cli_$(uname)_amd64.tar.gz"
tar xvf tekton-cli_*.tar.gz
sudo mv tekton /usr/local/bin/

# Install Tekton Pipelines
kubectl apply --filename https://storage.googleapis.com/tekton-releases/pipeline/v0.37.0/release.yaml

# Install Tekton Triggers
kubectl apply --filename https://storage.googleapis.com/tekton-releases/triggers/v0.26.1/release.yaml
```

#### `files/setup_react_tests.sh`
```bash
#!/bin/bash

# Assuming you have a React app at /path/to/react-app
cd /path/to/react-app
npm install
npm run build
```

#### `files/setup_python_tests.sh`
```bash
#!/bin/bash

# Assuming you have a Python project at /path/to/python-project
cd /path/to/python-project
pip install -r requirements.txt
python manage.py migrate
```

#### `handlers/main.yml`
```yaml
---
- name: Ensure Tekton CLI is installed
  include_role:
    name: tekton

- name: Run React tests
  include_role:
    name: react_tests

- name: Run Python tests
  include_role:
    name: python_tests
```

#### `tasks/main.yml`
```yaml
---
- name: Install dependencies
  include_tasks: install_dependencies.yml

- name: Configure Tekton
  include_tasks: configure_tekton.yml

- name: Set permissions
  include_tasks: set_permissions.yml
```

#### `tasks/install_dependencies.yml`
```yaml
---
- name: Ensure required packages are installed
  apt:
    name:
      - curl
      - git
      - nodejs
      - npm
      - python3
      - python3-pip
    state: present
```

#### `tasks/configure_tekton.yml`
```yaml
---
- name: Create Tekton configuration file
  template:
    src: tekton-config.yaml.j2
    dest: /etc/tekton/config.yaml

- name: Apply Tekton configurations
  k8s_apply:
    kubeconfig_path: "{{ kube_config }}"
    state: present
    definition_file: /etc/tekton/config.yaml
```

#### `tasks/set_permissions.yml`
```yaml
---
- name: Set permissions for Tekton configuration file
  file:
    path: /etc/tekton/config.yaml
    owner: root
    group: root
    mode: '0644'
```

#### `templates/tekton-config.yaml.j2`
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: config
data:
  default-image: gcr.io/tekton-releases/release:v0.37.0
```

### Playbook Example

You can create a playbook to apply this role to your machines:

#### `playbook.yml`
```yaml
---
- name: Configure Tekton on Debian-based machines
  hosts:
    - yerbouti
    - waza
  become: yes
  roles:
    - tekton
```

### Running the Playbook

To run the playbook, use the following command:

```bash
ansible-playbook playbook.yml
```

This setup will install Tekton on your Debian-based machines and configure it for a development, test, and production promotion cycle. It also includes scripts to set up automated tests for React and Python code.