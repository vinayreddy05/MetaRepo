import requests
from requests.auth import HTTPBasicAuth
import json
import base64

# GitHub credentials
token = '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'
org_name = 'qfadder11'
template_repo = 'GitTemplateRepo'  # The template repository name
new_repo_name = 'GITAUTOREPO'  # The new repository name

# Variables to replace
variables = {
    'NAMESPACE': 'it-css-hml',
    'NEWREPONAME': 'it-css-hml-pipeline',
}

# GitHub API URL for creating repositories from a template
generate_url = f'https://api.github.com/repos/{org_name}/{template_repo}/generate'

# Repository data
payload = {
    'owner': org_name,
    'name': new_repo_name,
    'description': 'Description of your new repository',
    'private': False  # Set to True if you want to create a private repository
}

# Make the API request to create the repository from the template
headers = {
    'Accept': 'application/vnd.github.baptiste-preview+json',
    'Authorization': f'token {token}'
}

response = requests.post(generate_url, headers=headers, data=json.dumps(payload))

if response.status_code == 201:
    print(f'Successfully created repository {new_repo_name} from template {template_repo}')
else:
    print(f'Failed to create repository {new_repo_name} from template {template_repo}')
    print('Response:', response.json())
    exit()

# Function to fetch file content and SHA
def fetch_file_content(repo, path):
    contents_url = f'https://api.github.com/repos/{org_name}/{repo}/contents/{path}'
    response = requests.get(contents_url, headers=headers)
    if response.status_code == 200:
        file_data = response.json()
        sha = file_data['sha']
        file_content = base64.b64decode(file_data['content']).decode('utf-8')
        return sha, file_content
    else:
        print(f'Failed to retrieve {path}')
        print('Response:', response.json())
        exit()

# Function to update file content on GitHub
def update_file_content(repo, path, content, sha):
    update_payload = {
        'message': f'Update {path} with new values',
        'content': base64.b64encode(content.encode()).decode('utf-8'),
        'sha': sha
    }
    contents_url = f'https://api.github.com/repos/{org_name}/{repo}/contents/{path}'
    response = requests.put(contents_url, headers=headers, data=json.dumps(update_payload))
    if response.status_code == 200:
        print(f'Successfully updated {path}')
    else:
        print(f'Failed to update {path}')
        print('Response:', response.json())

# Define the files and changes to be made
files_to_update = ['README.md', 'config.py', 'settings.yaml']

# Update each file
for file_path in files_to_update:
    sha, content = fetch_file_content(new_repo_name, file_path)
    for variable, new_value in variables.items():
        content = content.replace(f'${{{variable}}}', new_value)
    update_file_content(new_repo_name, file_path, content, sha)
