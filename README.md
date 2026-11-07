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
          exclude: '.github,_config.yml'
```

### Deploy to an External Repository

`.git` directories are automatically skipped, so do not include `.git` in
`exclude`.

Set `external_repository` and provide a personal access token with write access
to the target repository. External deployments require `personal_token` and do
not use `github_token`. Same-repository deployments use `github_token` when
present; set `github_token: ""` to use `personal_token` instead.

```yaml
- name: Generate and Deploy Directory Listings
  uses: pranabdas/directory-listing@v1
  with:
    folder: .
    exclude: '.github,_config.yml'
    personal_token: ${{ secrets.DEPLOY_KEY_DRIVE }}
    external_repository: pranabdas/drive
    publish_branch: main
```

### Action Inputs (Options)

| Input | Description | Required | Default |
| :--- | :--- | :--- | :--- |
| `folder` | The target directory to process | false | `.` |
| `exclude` | Comma-separated list of files and directories to remove from deployment; `.git` directories are automatically skipped | false | `.github,.gitignore` |
| `site_url` | The base URL for the site | false | `<repository_owner>.github.io` |
| `base_url` | The base path for the site (use `.` for a site hosted at the domain root, such as Netlify) | false | `<repository_name>` |
| `site_name` | The name of the site | false | `""` (Empty string) |
| `footer_text` | Text to display in the footer (Supports `{year}`) | false | `Copyright &copy; {year}. Built with <a href="https://github.com/pranabdas/directory-listing" target="_blank">github.com/pranabdas/directory-listing</a>.` |
| `github_token` | Token for same-repo deployment; ignored for external deployments | false | `${{ github.token }}` |
| `personal_token` | Required for external deployments; used for same-repo deployments only when `github_token` is empty | false | `""` (Empty string) |
| `publish_dir` | Directory to publish | false | `.` |
| `external_repository` | External repository to deploy to (e.g., `username/repo`) | false | `""` (Empty string) |
| `publish_branch` | Branch to deploy to | false | `gh-pages` |
| `commit_message` | Commit message for the deployment | false | `deploy ref. ${{ github.sha }}` |
