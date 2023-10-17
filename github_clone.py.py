import git
import os

github_username = 'rubikproxy'
repository_name = 'info'

local_directory = 'D:/my_repository'  

github_url = f'https://github.com/{github_username}/{repository_name}.git'

if not os.path.exists(local_directory):
    os.makedirs(local_directory)

repo = git.Repo.clone_from(github_url, local_directory)

print(f"Repository cloned to {local_directory}")


active_branch = repo.active_branch
print(f"Active branch: {active_branch}")

# Example 2: List commits
print("Commits in the repository:")
for commit in repo.iter_commits():
    print(f"{commit.hexsha}: {commit.summary}")


with open(os.path.join(local_directory, 'new_file.txt'), 'w') as file:
    file.write('This is a new file.')

repo.index.add(['new_file.txt'])
repo.index.commit('Added a new file.')


origin = repo.remote(name='origin')
origin.push(active_branch)

print("Changes pushed to the remote repository.")
