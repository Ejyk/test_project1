# Secure Python Automation Suite

A Python-based utility project demonstrating secure coding standards, programmatic script execution, and clean dependency tracking. This codebase forms a foundational module for automated infrastructure workflows and platform testing.

## 🚀 Architectural & Engineering Best Practices
This project strictly enforces standard DevOps security configurations:
* **Zero Hardcoded Credentials:** Application access tokens, system variables, and passwords are separated from the code logic and injected dynamically via the operating system environment.
* **Declarative Dependency Tracking:** Explicit usage of `requirements.txt` to align execution frameworks and isolate local environments cleanly.
* **Source Control Governance:** Employs `.gitignore` policies to guarantee local configurations (`.env`) are never committed to version control.

## 🛠️ Prerequisites & Setup

### 1. Requirements
Ensure your execution machine has Python 3.8+ installed:
```bash
python3 --version
```

### 2. Environment Isolation
It is highly recommended to isolate the application runtimes using a Python virtual environment:
```bash
# Create the virtual environment
python3 -m venv venv

# Activate the environment (Linux / macOS)
source venv/bin/activate
```

### 3. Dependency Provisioning
Install all target libraries specified in the requirements schema:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 🔒 Configuration & Variables

To run the application safely, inject the necessary credentials as runtime system environment variables. Never append plaintext passwords inside the source code files.

Set the runtime credentials in your shell terminal:
```bash
export YAHOO_APP_PASSWORD="your-securely-generated-app-token"
```

## 🏃 Run the Application
Once the workspace dependencies are isolated and runtime conditions are set, trigger the automation handler:
```bash
python app3.py
```
