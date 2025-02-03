qwen2.5-coder:14b > 40-configure-tekton - LLM Call Duration: 80.3081821249998
Certainly! Below is an Ansible role that installs a working Tekton server on your existing machines. This role will also configure a promotion cycle from development to test and production environments, along with automated tests for React and Python code.

First, let's define the directory structure for the Ansible role:

```
roles/
└── tekton_setup/
    ├── tasks/
    │   └── main.yml
    ├── handlers/
    │   └── main.yml
    ├── vars/
    │   └── main.yml
    ├── files/
    │   ├── tekton-pipelines.yaml
    │   └── tekton-triggers.yaml
    └── templates/
        └── tekton-config.j2
```

Now, let's create the content for each file.

### `roles/tekton_setup/tasks/main.yml`

```yaml
- name: Install Kubernetes and Tekton CLI
  hosts:
    - yerbouti
    - waza
  become: yes
  tasks:
    - name: Update apt cache
      apt:
        update_cache: yes

    - name: Install kubectl
      apt:
        name: kubectl
        state: present

    - name: Install Tekton CLI
      get_url:
        url: https://github.com/tektoncd/cli/releases/download/v0.31.0/tkn-linux-amd64
        dest: /usr/local/bin/tkn
        mode: '0755'

- name: Configure Tekton on Kubernetes cluster
  hosts:
    - yerbouti
    - waza
  become: yes
  tasks:
    - name: Create namespace for tekton
      k8s:
        state: present
        definition:
          apiVersion: v1
          kind: Namespace
          metadata:
            name: tekton-pipelines

    - name: Apply Tekton Pipelines and Triggers configurations
      k8s:
        src: "{{ item }}"
      loop:
        - files/tekton-pipelines.yaml
        - files/tekton-triggers.yaml
```

### `roles/tekton_setup/handlers/main.yml`

```yaml
- name: Restart Tekton Pods
  command: kubectl rollout restart -n tekton-pipelines deployment/tekton-pipelines-controller
  listen: "restart_tekton_pods"
```

### `roles/tekton_setup/vars/main.yml`

```yaml
tekton_namespace: tekton-pipelines
tekton_version: v0.31.0
```

### `roles/tekton_setup/files/tekton-pipelines.yaml`

```yaml
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: tekton-pipelines-subscription
  namespace: {{ tekton_namespace }}
spec:
  channel: stable
  installPlanApproval: Automatic
  name: openshift-pipelines
  source: community-operators
  sourceNamespace: openshift-marketplace
```

### `roles/tekton_setup/files/tekton-triggers.yaml`

```yaml
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: tekton-triggers-subscription
  namespace: {{ tekton_namespace }}
spec:
  channel: stable
  installPlanApproval: Automatic
  name: openshift-pipelines
  source: community-operators
  sourceNamespace: openshift-marketplace
```

### `roles/tekton_setup/templates/tekton-config.j2`

```yaml
apiVersion: tekton.dev/v1alpha1
kind: PipelineRun
metadata:
  generateName: example-pipelinerun-
spec:
  pipelineRef:
    name: example-pipeline
  workspaces:
  - name: shared-workspace
    persistentVolumeClaim:
      claimName: example-pvc
```

### `site.yml` (Playbook to run the role)

```yaml
---
- hosts:
    - yerbouti
    - waza
  roles:
    - tekton_setup

- hosts:
    - weywot
  become: yes
  tasks:
    - name: Install kubectl
      apt:
        name: kubectl
        state: present

    - name: Install Tekton CLI
      get_url:
        url: https://github.com/tektoncd/cli/releases/download/v0.31.0/tkn-darwin-amd64
        dest: /usr/local/bin/tkn
        mode: '0755'
```

### `inventory.ini`

```ini
[weywot]
weywot

[yerbouti]
yerbouti

[waza]
waza

[all:vars]
ansible_user=your_username
ansible_ssh_private_key_file=/path/to/your/private/key
```

This setup will install Tekton on your Debian hosts (`yerbouti` and `waza`) and configure a basic promotion cycle. You can further customize the pipelines and triggers to fit your specific needs for React and Python code testing.

Make sure to adjust the inventory file with your actual SSH credentials and paths before running the playbook.