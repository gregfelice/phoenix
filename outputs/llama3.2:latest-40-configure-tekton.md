llama3.2:latest > 40-configure-tekton - LLM Call Duration: 54.967860415999894
Here are Ansible roles to configure your system environments for a Tekton server and automated tests for React and Python code.

**Role: tekton-server**

```yaml
---
- name: Install and configure Tekton server
  hosts: wawa
  become: yes

  tasks:
    - name: Install dependencies
      apt:
        name:
          - git
          - docker.io
          - python3-pip
          - python3-dev
        state: present

    - name: Set up Docker
      apt:
        name:
          - docker-ce
          - docker-compose
        state: present

    - name: Install Tekton
      pip:
        name: tektonpi
        state: present

    - name: Create Tekton service account
      tee:
        path: /etc/tekton pi/serviceaccount.yaml.j2
        content: |
          apiVersion: v1
          kind: ServiceAccount
          metadata:
            name: {{ ansible_hostname }}-{{ inventory_hostname }}
          spec:
            serviceAccountName: {{ ansible_hostname }}-{{ inventory_hostname }}

    - name: Create Tekton cluster
      tee:
        path: /etc/tekton pi/cluster.yaml.j2
        content: |
          apiVersion: tekton.dev/v1beta1
          kind: Cluster
          metadata:
            name: {{ ansible_hostname }}
          spec:
            serviceAccountName: {{ inventory_hostname }}-{{ ansible_hostname }}

    - name: Create Tekton pipeline
      tee:
        path: /etc/tekton pi/pipeline.yaml.j2
        content: |
          apiVersion: tekton.dev/v1beta1
          kind: Pipeline
          metadata:
            name: {{ ansible_hostname }}
          spec:
            serviceAccountName: {{ inventory_hostname }}-{{ ansible_hostname }}
            pipelines:
              - name: {{ inventory_hostname }}-{{ ansible_hostname }}
                pipelineSpec:
                  workflow: |
                    # Define a workflow to run your app
                    steps:
                      - name: Checkout code
                        git:
                          repo: https://github.com/your-repo.git
                          path: /app
                      - name: Build and deploy app
                        shell: |
                          docker build -t {{ inventory_hostname }}-{{ ansible_hostname }} .
                          docker run -it --rm {{ inventory_hostname }}-{{ ansible_hostname }}
                      - name: Run tests
                        shell: |
                          python -m unittest discover -s /app

    - name: Create Tekton pipeline template
      tee:
        path: /etc/tekton pi/pipeline-template.yaml.j2
        content: |
          apiVersion: tekton.dev/v1beta1
          kind: PipelineTemplate
          metadata:
            name: {{ ansible_hostname }}
          spec:
            serviceAccountName: {{ inventory_hostname }}-{{ ansible_hostname }}
            pipelines:
              - name: {{ inventory_hostname }}-{{ ansible_hostname }}
                pipelineSpec:
                  workflow: |
                    # Define a workflow to run your app
                    steps:
                      - name: Checkout code
                        git:
                          repo: https://github.com/your-repo.git
                          path: /app
                      - name: Build and deploy app
                        shell: |
                          docker build -t {{ inventory_hostname }}-{{ ansible_hostname }} .
                          docker run -it --rm {{ inventory_hostname }}-{{ ansible_hostname }}
                      - name: Run tests
                        shell: |
                          python -m unittest discover -s /app

    - name: Create Tekton pipeline configuration
      tee:
        path: /etc/tekton pi/pipeline-config.yaml.j2
        content: |
          apiVersion: tekton.dev/v1beta1
          kind: PipelineConfig
          metadata:
            name: {{ ansible_hostname }}
          spec:
            serviceAccountName: {{ inventory_hostname }}-{{ ansible_hostname }}
            pipelineTemplateRef:
              name: {{ inventory_hostname }}-{{ ansible_hostname }}
```

**Role: react-tests**

```yaml
---
- name: Install and configure React tests
  hosts: yerbouti
  become: yes

  tasks:
    - name: Install dependencies
      apt:
        name:
          - nodejs
          - npm
          - yarn
        state: present

    - name: Set up React project
      git:
        repo: https://github.com/your-repo.git
        dest: /app
        version: main
      notify: restart react-app

    - name: Install dependencies
      pip:
        name:
          - pytest
          - pytest-cov
        state: present

    - name: Create React test file
      tee:
        path: /app/tests/test_react.py.j2
        content: |
          import pytest
          from {{ inventory_hostname }}-{{ ansible_hostname }}
          def test_react_app():
            # Run your tests here

    - name: Install Jest
      pip:
        name:
          - jest
        state: present

    - name: Create Jest configuration file
      tee:
        path: /app/jest.config.js.j2
        content: |
          module.exports = {
            // Your Jest configuration here
          }

    - name: Run React tests
      shell:
        cmd: |
          npm run test -- -c /app/tests/test_react.py

```

**Role: python-tests**

```yaml
---
- name: Install and configure Python tests
  hosts: yerbouti
  become: yes

  tasks:
    - name: Install dependencies
      pip:
        name:
          - pytest
          - pytest-cov
        state: present

    - name: Set up Python project
      git:
        repo: https://github.com/your-repo.git
        dest: /app
        version: main
      notify: restart python-app

    - name: Install dependencies
      pip:
        name:
          - pytest-cov
        state: present

    - name: Create Python test file
      tee:
        path: /app/tests/test_python.py.j2
        content: |
          import pytest
          from {{ inventory_hostname }}-{{ ansible_hostname }}
          def test_python_app():
            # Run your tests here

    - name: Install Pytest-Cov
      pip:
        name:
          - pytest-cov
        state: present

    - name: Create Pytest-Cov configuration file
      tee:
        path: /app/pytest-cov.json.j2
        content: |
          {
            "show_cov_progress": True,
            "ignore_missing_files": False
          }

    - name: Run Python tests
      shell:
        cmd: |
          pytest --cov=app --cov-report=html

```

**Role: production-server**

```yaml
---
- name: Set up production server
  hosts: wawa
  become: yes

  tasks:
    - name: Install dependencies
      apt:
        name:
          - docker-ce
          - docker-compose
        state: present

    - name: Configure Docker
      tee:
        path: /etc/docker/daemon.json.j2
        content: |
          {
            "exec-opts": ["native.cgroupdriver=systemd"],
            "log-driver": "json-file",
            "log-opts": {
              "tags": "{{ inventory_hostname }}-{{ ansible_hostname }}"
            },
            "storage-driver": "overlay2"
          }

    - name: Set up Tekton
      tee:
        path: /etc/tekton pi/serviceaccount.yaml.j2
        content: |
          apiVersion: v1
          kind: ServiceAccount
          metadata:
            name: {{ ansible_hostname }}-{{ inventory_hostname }}
          spec:
            serviceAccountName: {{ ansible_hostname }}-{{ inventory_hostname }}

    - name: Create Tekton cluster
      tee:
        path: /etc/tekton pi/cluster.yaml.j2
        content: |
          apiVersion: tekton.dev/v1beta1
          kind: Cluster
          metadata:
            name: {{ ansible_hostname }}
          spec:
            serviceAccountName: {{ inventory_hostname }}-{{ ansible_hostname }}

    - name: Create Tekton pipeline
      tee:
        path: /etc/tekton pi/pipeline.yaml.j2
        content: |
          apiVersion: tekton.dev/v1beta1
          kind: Pipeline
          metadata:
            name: {{ ansible_hostname }}
          spec:
            serviceAccountName: {{ inventory_hostname }}-{{ ansible_hostname }}
            pipelines:
              - name: {{ inventory_hostname }}-{{ ansible_hostname }}
                pipelineSpec:
                  workflow: |
                    # Define a workflow to run your app
                    steps:
                      - name: Checkout code
                        git:
                          repo: https://github.com/your-repo.git
                          path: /app
                      - name: Build and deploy app
                        shell: |
                          docker build -t {{ inventory_hostname }}-{{ ansible_hostname }} .
                          docker run -it --rm {{ inventory_hostname }}-{{ ansible_hostname }}
                      - name: Run app
                        shell: |
                          npm start

```

To configure your environment, you will need to:

*   Install Docker and Docker Compose on your system.
*   Create a new file called `docker-compose.yml` with the following content:
    ```yml
version: '3'
services:
  web:
    build: .
    ports:
      - "80:80"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgres://user:password@db:5432/database

  db:
    image: postgres:12
    volumes:
      - db-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
```
*   Create a new file called `Dockerfile` with the following content:
    ```dockerfile
FROM python:3.9-slim

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app/

# Set working directory to /app
WORKDIR /app

# Expose port 80
EXPOSE 80

# Run command when container starts
CMD ["npm", "start"]
```
*   Create a new file called `requirements.txt` with the following content:
    ```
Flask==2.0.1
psycopg2-binary==2.9.3
```
*   Install your application using `docker-compose build` and `docker-compose up -d`.
*   Configure your environment variables by creating a new file called `.env` with the following content:
    ```
DATABASE_URL=postgres://user:password@db:5432/database
```
*   Update your `Dockerfile` to include the command to run your tests using `pytest` and `npm test`.