import requests
import json
import os
import logging
import getpass
from datetime import datetime, timedelta
from src.api import access_token


log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)


log_file = os.path.join(log_dir, "github_error.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

root_logger = logging.getLogger()
root_logger.addHandler(console_handler)

# GitHub username and personal access token
username = input("Enter Your username")
token = access_token

user_api_url = f"https://api.github.com/users/{username}"
repos_api_url = f"https://api.github.com/users/{username}/repos"

headers = {
    "Authorization": f"token {token}"
}

cache_file = "github_repositories_cache.json"
cache_duration = 30

def load_cached_data():
    try:
        if os.path.exists(cache_file):
            with open(cache_file, "r") as cache:
                data = json.load(cache)
                timestamp = data.get("timestamp")
                if timestamp and (datetime.now() - datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")) < timedelta(minutes=cache_duration):
                    return data.get("repositories")
    except Exception as e:
        error_message = f"An error occurred while loading cached data: {str(e)}"
        logging.error(error_message)
        print(error_message)

    return None

def save_data_to_cache(repositories):
    try:
        with open(cache_file, "w") as cache:
            data_to_cache = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "repositories": repositories
            }
            json.dump(data_to_cache, cache, indent=4)
    except Exception as e:
        error_message = f"An error occurred while saving data to cache: {str(e)}"
        logging.error(error_message)
        print(error_message)


def fetch_user_profile():
    try:
        # GET request to the GitHub API to fetch user profile information
        response = requests.get(user_api_url, headers=headers)

        # Check if the request was successful (status code 200)
        response.raise_for_status()

        # Parse the JSON response
        user_data = response.json()
        
        print("User Profile Information:")
        print(f"Username: {user_data['login']}")
        print(f"Name: {user_data['name'] or 'N/A'}")
        print(f"Bio: {user_data['bio'] or 'N/A'}")
        print(f"Location: {user_data['location'] or 'N/A'}")
        print(f"Followers: {user_data['followers']}")
        print(f"Following: {user_data['following']}")
    except requests.exceptions.RequestException as e:
        error_message = f"An error occurred while fetching user profile data: {str(e)}"
        logging.error(error_message)
        print(error_message)
    except ValueError as e:
        error_message = f"An error occurred while parsing user profile JSON data: {str(e)}"
        logging.error(error_message)
        print(error_message)
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        logging.error(error_message)
        print(error_message)

def fetch_all_repositories():
    repositories = []
    page = 1

    while True:
        try:
            response = requests.get(repos_api_url, headers=headers, params={"page": page, "per_page": 100})        
            response.raise_for_status()
            page_repositories = response.json()
            if not page_repositories:
                break
            repositories.extend(page_repositories)
            page += 1
        except requests.exceptions.RequestException as e:
            error_message = f"An error occurred while making the request: {str(e)}"
            logging.error(error_message)
            print(error_message)
            return None
        except ValueError as e:
            error_message = f"An error occurred while parsing JSON data: {str(e)}"
            logging.error(error_message)
            print(error_message)
            return None
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            logging.error(error_message)
            print(error_message)
            return None
    save_data_to_cache(repositories)

    return repositories

def create_repository():
    try:
        repo_name = input("Enter the name for your new repository: ")

        
        payload = {
            "name": repo_name,
            "description": input("Enter a description for your repository (optional): "),
            "private": input("Is this a private repository? (yes/no): ").lower() == "yes",
        }
        response = requests.post(repos_api_url, headers=headers, json=payload)

        
        if response.status_code == 201:
            print(f"Repository '{repo_name}' created successfully!")
        else:
            error_message = f"Failed to create repository '{repo_name}'. Status code: {response.status_code}"
            logging.error(error_message)
            print(error_message)
    except requests.exceptions.RequestException as e:
        error_message = f"An error occurred while creating the repository: {str(e)}"
        logging.error(error_message)
        print(error_message)
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        logging.error(error_message)
        print(error_message)

def delete_repository():
    try:
        repo_name = input("Enter the name of the repository you want to delete: ")
        delete_confirmation = input(f"Are you sure you want to delete '{repo_name}'? This action cannot be undone. (yes/no): ").lower()

        if delete_confirmation != "yes":
            print("Repository deletion canceled.")
            return


        password = getpass.getpass("Enter your GitHub password: ")

        delete_url = f"https://api.github.com/repos/{username}/{repo_name}"

        response = requests.delete(delete_url, headers=headers, auth=(username, password))

        if response.status_code == 204:
            print(f"Repository '{repo_name}' deleted successfully!")
        else:
            error_message = f"Failed to delete repository '{repo_name}'. Status code: {response.status_code}"
            logging.error(error_message)
            print(error_message)
    except requests.exceptions.RequestException as e:
        error_message = f"An error occurred while deleting the repository: {str(e)}"
        logging.error(error_message)
        print(error_message)
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        logging.error(error_message)
        print(error_message)

def fetch_repositories():
    repositories = load_cached_data()

    if repositories is None:
        repositories = fetch_all_repositories()
        if repositories is None:
            error_message = "Failed to retrieve repository data."
            logging.error(error_message)
            print(error_message)
            return

    while True:
        print("\nOptions:")
        print("1. Fetch User Profile Information")
        print("2. Filter repositories (public/private/all)")
        print("3. Search for repositories")
        print("4. Display statistics")
        print("5. Export repositories to JSON")
        print("6. Create a new repository")
        print("7. Delete a repository")
        print("8. Get Rate Limit")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            fetch_user_profile()
        elif choice == "2":
            filter_option = input("Filter repositories (public/private/all): ").lower()
            display_filtered_repositories(repositories, filter_option)
        elif choice == "3":
            search_query = input("Search for repositories (name, description, or language): ").lower()
            display_search_results(repositories, search_query)
        elif choice == "4":
            display_statistics(repositories)
        elif choice == "5":
            export_to_json(repositories)
        elif choice == "6":
            create_repository()
        elif choice == "7":
            delete_repository()
        elif choice == "8":
            get_rate_limit()
        elif choice == "9":
            print("Thank For Using The Github API-!!!")
            break
        else:
            print("Invalid choice. Please select a valid option (1/2/3/4/5/6/7/8/9).")

def display_filtered_repositories(repositories, filter_option):
    for repo in repositories:
        if (filter_option == "public" and not repo["private"]) or \
           (filter_option == "private" and repo["private"]) or \
           (filter_option == "all"):
            display_repository_details(repo)

def display_search_results(repositories, search_query):
    for repo in repositories:
        description = repo["description"]
        if description and (search_query in description.lower() or \
           (repo["language"] and search_query in repo["language"].lower())):
            display_repository_details(repo)


def display_repository_details(repo):
    print(f"Repository Name: {repo['name']}")
    print(f"Description: {repo['description'] or 'N/A'}")
    print(f"Language: {repo['language'] or 'N/A'}")
    print(f"URL: {repo['html_url']}")
    print(f"Stars: {repo['stargazers_count']}")

    fetch_additional_details(repo['url'])

    print("-" * 50)

def fetch_additional_details(repo_url):
    try:
        response = requests.get(repo_url, headers=headers)
        response.raise_for_status()
        repo_data = response.json()
        print(f"Forks: {repo_data['forks_count']}")
        print(f"Watchers: {repo_data['watchers_count']}")
        print(f"Open Issues: {repo_data['open_issues_count']}")
        print(f"Default Branch: {repo_data['default_branch']}")
    except requests.exceptions.RequestException as e:
        error_message = f"An error occurred while fetching additional details: {str(e)}"
        logging.error(error_message)
        print(error_message)
    except ValueError as e:
        error_message = f"An error occurred while parsing additional details JSON data: {str(e)}"
        logging.error(error_message)
        print(error_message)
    except Exception as e:
        error_message = f"An unexpected error occurred while fetching additional details: {str(e)}"
        logging.error(error_message)
        print(error_message)

def display_statistics(repositories):
    total_repos = len(repositories)
    total_stars = sum(repo["stargazers_count"] for repo in repositories)
    print(f"\nTotal Repositories: {total_repos}")
    print(f"Total Stars: {total_stars}")

def export_to_json(repositories):
    try:
        with open("github_repositories.json", "w") as json_file:
            json.dump(repositories, json_file, indent=4)
        print("Repository data exported to 'github_repositories.json'.")
        print("Your GitHub Account Repository Was Saved Successfully")
    except Exception as e:
        error_message = f"An error occurred while exporting to JSON: {str(e)}"
        logging.error(error_message)
        print(error_message)

def get_rate_limit():
    try:
        rate_limit_url = "https://api.github.com/rate_limit"
        response = requests.get(rate_limit_url, headers=headers)

        response.raise_for_status()

        rate_limit_data = response.json()
        core_rate_limit = rate_limit_data["resources"]["core"]

        print(f"Rate Limit: {core_rate_limit['limit']}")
        print(f"Remaining Requests: {core_rate_limit['remaining']}")
        print(f"Reset Time: {core_rate_limit['reset']} (UTC timestamp)")
    except requests.exceptions.RequestException as e:
        error_message = f"An error occurred while fetching rate limit data: {str(e)}"
        logging.error(error_message)
        print(error_message)
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        logging.error(error_message)
        print(error_message)

if __name__ == "__main__":
    fetch_repositories()
