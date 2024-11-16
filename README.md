---

# GitLab Repository Manager

This Python script automates the process of managing and monitoring repositories within a specific GitLab group. 
It checks for updates (new commits), logs activities, and downloads the latest version of repositories when changes are detected.

---

## Features
- **List Projects:** Fetches a list of all projects in a specified GitLab group.
- **Monitor Commits:** Tracks the latest commit hash for each project.
- **Download Repositories:** Downloads projects as `.zip` files when changes are detected.
- **Logging:** Logs all activities and errors for easy debugging.
- **Persistence:** Saves commit hashes to prevent redundant downloads.

---

## Requirements

- **Python Version:** Python 3.7 or higher
- **Libraries:** Ensure the following Python libraries are installed:
  - `requests`
  - `os`
  - `logging`
  - `datetime`

---

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/gitlab-repo-manager.git
cd gitlab-repo-manager
```

### 2. Install Dependencies
Use `pip` to install the required library:
```bash
pip install requests
```

### 3. Configuration
- Set your **GitLab Access Token**:
  Replace `your-access-token` in the script with your actual GitLab personal access token, or set it as an environment variable:
  ```bash
  export ACCESS_TOKEN=your-access-token
  ```

- Specify the **Group ID** for your GitLab group:
  Update `GROUP_ID` in the script with your GitLab group ID.

---

## Usage

1. Run the script:
   ```bash
   python main.py
   ```
2. The script will:
   - Fetch a list of projects in the specified group.
   - Compare commit hashes to detect changes.
   - Download updated projects to the `Respository/downloads/` directory.
   - Log all activities in the `Respository/logs/` directory.

---

## Directory Structure
- `Respository/logs/`  
  Stores log files for each run.

- `Respository/downloads/`  
  Stores downloaded project archives.

- `Respository/commit_hashes.txt`  
  Tracks the latest commit hash for each project.

---

## Logging
Logs are saved daily in the `Respository/logs/` directory with filenames formatted as `log_YYYY_MM_DD.log`. 

---

## Contributing
Feel free to fork this repository and contribute by submitting a pull request. For major changes, please open an issue first to discuss your proposed changes.

---

## License
This project is licensed under the MIT License.

--- 
