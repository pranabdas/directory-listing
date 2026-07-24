# Github Pages Directory Listing

Generate Directory Listings for Github Pages and deploy them automatically using Github Actions.

## Usage

### Getting Started (Same Repository)

Add a `.github/workflows/workflow.yml` to the root of your repository. By default, the action will automatically generate the directory listing and push it to the `gh-pages` branch of the **same repository** using the default built-in `GITHUB_TOKEN`.

```yaml
name: directory-listing

on:
  push:
    branches:
      - main

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: write # Required to push to the gh-pages branch
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v7
        with:
          fetch-depth: 0  # IMPORTANT: Fetches full history so git log can find real timestamps

      - name: Generate and Deploy Directory Listings
        uses: pranabdas/directory-listing@v1
        with:
          folder: .
          exclude: '.git,.github,_config.yml'
```

### Deploy to an External Repository

```yaml
- name: Generate and Deploy Directory Listings
        uses: pranabdas/directory-listing@v1
        with:
          folder: .
          exclude: '.git,.github,_config.yml'
          personal_token: ${{ secrets.DEPLOY_KEY_DRIVE }}
          external_repository: pranabdas/drive
          publish_branch: main
```

### Action Inputs (Options)

| Input | Description | Required | Default |
| :--- | :--- | :--- | :--- |
| `folder` | The target directory to process | false | `.` |
| `exclude` | Comma-separated list of files and directories to ignore | false | `.git` |
| `site_url` | The base URL for the site | false | `<repository_owner>.github.io` |
| `base_url` | The base path for the directory | false | `<repository_name>` |
| `site_name` | The name of the site | false | `""` (Empty string) |
| `footer_text` | Text to display in the footer (Supports `{year}`) | false | `Copyright &copy; {year}. Built with <a href="https://github.com/pranabdas/directory-listing" target="_blank">github.com/pranabdas/directory-listing</a>.` |
| `github_token` | `GITHUB_TOKEN` for same-repo deployment | false | `${{ github.token }}` |
| `personal_token` | Personal access token for external repository deployment | false | `""` (Empty string) |
| `publish_dir` | Directory to publish | false | `.` |
| `external_repository` | External repository to deploy to (e.g., `username/repo`) | false | `""` (Empty string) |
| `publish_branch` | Branch to deploy to | false | `gh-pages` |
| `commit_message` | Commit message for the deployment | false | `deploy ref. ${{ github.sha }}` |
