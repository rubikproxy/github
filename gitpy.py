import git
import os
import requests
from src.api import access_token

# GitHub API URL for repository information
GITHUB_API_URL = "https://api.github.com/repos"

def clone_repository():
    github_username = input("GitHub Username:")
    repository_name = input("Repository Name:")
    local_directory = input("Local Directory:")
    github_url = f'https://github.com/{github_username}/{repository_name}.git'

    if not os.path.exists(local_directory):
        os.makedirs(local_directory)

    repo = git.Repo.clone_from(github_url, local_directory)
    print(f"Repository cloned to {local_directory}")

def get_repository_info(github_username, repository_name):
    url = f"{GITHUB_API_URL}/{github_username}/{repository_name}"
    headers = {
        "Authorization": f"Bearer {access_token}"  
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        repo_info = response.json()
        return repo_info
    else:
        return None

def display_repository_info(github_username, repository_name):
    repo_info = get_repository_info(github_username, repository_name)
    if repo_info:
        print("Repository Information:")
        print(f"Name: {repo_info['name']}")
        print(f"Description: {repo_info['description']}")
        print(f"Owner: {repo_info['owner']['login']}")
        print(f"URL: {repo_info['html_url']}")
    else:
        print("Failed to retrieve repository information. Check your access token.")

if __name__ == "__main__":
    local_directory = None  
    repo = None

    while True:
        print("\nGit Repository Menu:")
        print("1. Clone a Repository")
        print("2. Get Repository Information")
        print("3. Create and Checkout a New Branch")
        print("4. Add, Commit, and Push Changes")
        print("5. Pull Changes from the Remote Repository")
        print("6. Delete a Branch")
        print("7. Exit")

        choice = input("Select an option (1/2/3/4/5/6/7): ")

        if choice == "1":
            clone_repository()
        elif choice == "2":
            github_username = input("GitHub Username:")
            repository_name = input("Repository Name:")
            display_repository_info(github_username, repository_name)
        elif choice == "3":
            if repo:
                create_branch()
            else:
                print("You must clone a repository first.")
        elif choice == "4":
            if repo:
                add_commit_push()
            else:
                print("You must clone a repository first.")
        elif choice == "5":
            if repo:
                pull_repository()
            else:
                print("You must clone a repository first.")
        elif choice == "6":
            if repo:
                delete_branch()
            else:
                print("You must clone a repository first.")
        elif choice == "7":
            print("Thank you for using the Github Python code")
            break
        else:
            print("Invalid choice. Please select a valid option.")
            continue