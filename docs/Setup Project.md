Below is a step-by-step guide to get you from zero to a working Poetry-managed Python project on both macOS and Windows.

---

## 1. Prerequisites

* A user account with permission to install software.
* Internet access.

---

## 2. Installing Python

### 2.1 On macOS

#### a) Using Homebrew

1. **Install Homebrew** (if you haven’t already):

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. **Install Python**:

   ```bash
   brew update
   brew install python
   ```
3. **Verify**:

   ```bash
   python3 --version
   pip3 --version
   ```

#### b) Using the Official Installer

1. **Download** the macOS 64-bit installer from [https://www.python.org/downloads/macos/](https://www.python.org/downloads/macos/).
2. **Run** the `.pkg` installer and follow the prompts.
3. **Verify**:

   ```bash
   python3 --version
   pip3 --version
   ```

---

### 2.2 On Windows

#### a) Using the Microsoft Store

1. **Open** the Microsoft Store and search for “Python 3.x”.
2. **Install** the latest Python 3 release.
3. **Ensure** “Add Python to PATH” is checked.
4. **Verify** in PowerShell or Command Prompt:

   ```powershell
   python --version
   pip --version
   ```

#### b) Using the Official Installer

1. **Download** the Windows installer from [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/).
2. **Run** the `.exe` and ensure you check “Add Python 3.x to PATH” before installing.
3. **Verify**:

   ```powershell
   python --version
   pip --version
   ```

---

## 3. Installing Poetry

Poetry provides its own installer script that works on macOS, Linux, and Windows (via PowerShell or WSL).

1. **Run the installer**:

    * **macOS / Linux**

      ```bash
      curl -sSL https://install.python-poetry.org | python3 -
      ```

    * **Windows (PowerShell)**

      ```powershell
      (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
      ```

2. **Configure your shell**:

    * After installation, the installer will tell you to add something like `export PATH="$HOME/.local/bin:$PATH"` (macOS/Linux) or adjust your PATH in Windows.
    * **Restart** your terminal.

3. **Verify**:

   ```bash
   poetry --version
   ```

---

## 4. Creating a New Poetry Project

You have two main options:

| Command                                      | What it does                                                             |
| -------------------------------------------- | ------------------------------------------------------------------------ |
| `poetry new my-app`                          | Creates a new directory `my-app/` with a basic package layout and tests. |
| `mkdir my-app && cd my-app`<br>`poetry init` | Interactive prompt to configure `pyproject.toml` in an existing folder.  |

### Example: using `poetry new`

```bash
cd ~/projects
poetry new my-app
cd my-app
```

This yields:

```
my-app/
├── README.rst
├── pyproject.toml
├── my_app
│   └── __init__.py
└── tests
    └── __init__.py
```

---

## 5. Managing Dependencies

* **Install all declared deps** (after cloning an existing project or after modifying `pyproject.toml`):

  ```bash
  poetry install
  ```

* **Add a runtime dependency**:

  ```bash
  poetry add requests
  ```

* **Add a development‐only dependency** (e.g., pytest):

  ```bash
  poetry add --dev pytest
  ```

* **Remove a dependency**:

  ```bash
  poetry remove requests
  ```

---

## 6. Virtual Environments

By default, Poetry creates and manages a virtual environment per project.

* **Spawn a shell inside the venv**:

  ```bash
  poetry shell
  ```

* **Run a one-off command in the venv** (without entering shell):

  ```bash
  poetry run python my_app/main.py
  ```

* **List environments**:

  ```bash
  poetry env list
  ```

* **Use a system Python (disable venv creation)**:

  ```bash
  poetry config virtualenvs.create false --local
  ```

---

## 7. Building and Publishing

* **Build** your package (generates `dist/`):

  ```bash
  poetry build
  ```

* **Publish** to PyPI (you’ll be prompted for credentials):

  ```bash
  poetry publish --username your-username --password your-password
  ```

---

## 8. Tips & Best Practices

* Keep your `README.rst` or `README.md` up to date; Poetry reads it for project metadata.
* Pin your dependencies with care; use version constraints like `^1.2` to allow patch updates.
* Commit your `poetry.lock` file to version control to guarantee reproducible installs.
* Use `poetry run` in CI scripts to ensure commands execute in the correct environment.

---

With these steps, you’ll have a fully configured Python + Poetry workflow on both macOS and Windows. Happy coding!
