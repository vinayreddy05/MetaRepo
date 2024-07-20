import requests
import json

# GitHub credentials
token = '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'
org_name = 'qfadder11'
template_repo = 'GitTemplateRepo'  # The template repository name
new_repo_name = 'new-repo'  # The new repository name

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
