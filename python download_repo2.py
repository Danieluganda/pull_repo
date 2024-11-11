import requests
import os
import logging
from datetime import datetime

# GitLab API setup
GROUP_ID = "15192025"
GITLAB_API_URL = f"https://gitlab.com/api/v4/groups/{GROUP_ID}/projects"
ACCESS_TOKEN = "your-access-token"  # Replace with your access token or set via environment variable

# Paths
LOG_DIR = "Respository/logs/"
DOWNLOAD_DIR = "Respository/downloads/"
COMMIT_HASH_FILE = "Respository/commit_hashes.txt"

# Ensure directories exist
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Configure logging
log_file = os.path.join(LOG_DIR, f"log_{datetime.now().strftime('%Y_%m_%d')}.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Function to list projects in the group
def list_projects():
    headers = {"PRIVATE-TOKEN": ACCESS_TOKEN}
    response = requests.get(GITLAB_API_URL, headers=headers)
    
    if response.status_code == 200:
        projects = response.json()
        logging.info("Successfully retrieved projects list.")
        return projects
    else:
        logging.error(f"Failed to retrieve projects: {response.status_code}")
        return []

# Function to retrieve and compare the latest commit hash
def get_latest_commit_hash(project_id):
    url = f"https://gitlab.com/api/v4/projects/{project_id}/repository/commits"
    headers = {"PRIVATE-TOKEN": ACCESS_TOKEN}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        commits = response.json()
        if commits:
            return commits[0]["id"]  # Return the latest commit hash
    logging.error(f"Failed to retrieve commits for project {project_id}")
    return None

# Function to read stored commit hashes from file
def read_commit_hashes():
    commit_hashes = {}
    if os.path.exists(COMMIT_HASH_FILE):
        with open(COMMIT_HASH_FILE, "r") as f:
            for line in f:
                project_id, commit_hash = line.strip().split(",")
                commit_hashes[project_id] = commit_hash
    return commit_hashes

# Function to write the latest commit hashes to file
def write_commit_hashes(commit_hashes):
    with open(COMMIT_HASH_FILE, "w") as f:
        for project_id, commit_hash in commit_hashes.items():
            f.write(f"{project_id},{commit_hash}\n")

# Function to download a project as a zip
def download_project_as_zip(project_id, project_name):
    zip_url = f"https://gitlab.com/api/v4/projects/{project_id}/repository/archive.zip"
    headers = {"PRIVATE-TOKEN": ACCESS_TOKEN}
    destination_path = os.path.join(DOWNLOAD_DIR, f"{project_name}.zip")
    
    try:
        logging.info(f"Downloading {project_name} as zip...")
        response = requests.get(zip_url, headers=headers, stream=True)
        
        if response.status_code == 200:
            with open(destination_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            logging.info(f"Downloaded {project_name} successfully.")
        else:
            logging.error(f"Failed to download {project_name}: {response.status_code}")
    except Exception as e:
        logging.error(f"An error occurred while downloading {project_name}: {e}")

# Main function to check for updates and download new versions
def main():
    commit_hashes = read_commit_hashes()
    projects = list_projects()  # Now the list_projects function is defined
    
    for project in projects:
        project_id = project["id"]
        project_name = project["name"]
        
        # Get the latest commit hash for the project
        latest_commit = get_latest_commit_hash(project_id)
        
        if latest_commit:
            stored_commit = commit_hashes.get(str(project_id))
            
            # If no stored commit or commit has changed, download the new version
            if not stored_commit or latest_commit != stored_commit:
                download_project_as_zip(project_id, project_name)
                commit_hashes[str(project_id)] = latest_commit
    
    # After processing all projects, save the updated commit hashes
    write_commit_hashes(commit_hashes)

if __name__ == "__main__":
    main()
