<h1 align="center">
  <img src="https://github.com/rubikproxy/github/assets/84948167/a7e665ca-3419-4468-a6e9-83bd0b8c57a3" alt="GitHub Python Code Logo" width="200"><br>
  GitHub Python Code
</h1>


<div align="center">
  <p>🐍 A Versatile GitHub Interaction Project 🚀</p>
  <p>Manage Git repositories and interact with the GitHub API with ease.</p>
</div>

<h2 align="center">Features and Functions</h2>

### `github_clone.py`

1. **Clone a GitHub Repository 📥**
   - Clone any public GitHub repository into a local directory.
   - Specify the GitHub username, repository name, and local directory.

2. **Display Active Branch 🌿**
   - Retrieve and display the active branch of the cloned repository.

3. **List Commits 📜**
   - List all commits in the cloned repository, including commit SHA and message.

4. **Add a New File ✏️**
   - Create a new file in the local repository directory and write content to it.
   - Stage the new file for commit and make a new commit.

5. **Push Changes to the Remote Repository 🚀**
   - Push committed changes to the active branch in the remote repository on GitHub.

### `gitpy.py`

Additional features and placeholders for future expansion:

1. **Create and Checkout a New Branch 🌱**
   - Create and switch to a new Git branch within the repository.

2. **Add, Commit, and Push Changes 🔄**
   - Perform Git operations to add, commit, and push changes to the repository.

3. **Pull Changes from the Remote Repository 🔄🏡**
   - Pull changes from the remote repository to keep your local repository up-to-date.

4. **Delete a Branch 🗑️**
   - Maintain a clean repository by removing unnecessary branches as needed.

### `github.py`

1. **Fetch User Profile Information 🙋**
   - Retrieve and display user profile information from GitHub, including username, name, bio, location, followers, and following.

2. **Fetch All Repositories 📦**
   - Fetch all repositories associated with the authenticated user on GitHub.
   - Cache the data for improved performance.

3. **Filter and Search Repositories 🔍**
   - Find specific repositories with ease by filtering based on public or private status.
   - Enhance your search capabilities by querying repositories using various criteria.

4. **Create and Delete Repositories 🏗️🗑️**
   - Empower GitHub users by enabling the creation of new repositories with customizable descriptions and privacy settings.
   - Exercise control over your GitHub ecosystem by securely deleting repositories, with user confirmation.

5. **Export Repository Data to JSON 📁**
   - Enable data analysis and backup strategies by exporting repository information to a structured JSON file.

6. **Get Rate Limit ⏳**
   - Stay informed about your GitHub API usage with rate limit information.
   - Monitor limits, remaining requests, and reset times to ensure optimal API interaction.

<h2 align="center">Getting Started 🚀</h2>

To utilize this project, follow these steps:

1. **Install Dependencies:**
   - Ensure you have the `GitPython` and `Requests` libraries installed. You can install them using `pip`:

   ```bash
   pip install GitPython requests
