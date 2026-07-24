# Github Pages Directory Listing

Generate Directory Listings for Github Pages using Github Actions.

## Usage
### Getting Started

Add a `.github/workflows/workflow.yml` to the root of your repository.
```
```yaml
name: directory-listing

on: [push]

jobs:
  pages-directory-listing:
    runs-on: ubuntu-latest
    name: Directory Listings Index
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v7

      - name: Generate Directory Listings
        uses: pranabdas/directory-listing@v1
        with:
          folder: .      # Directory to generate index
          exclude: '.git, .github, _config.yml' # Comma-separated files/directories to ignore

  deploy:
    needs: pages-directory-listing
    permissions:
      pages: write      # to deploy to Pages
      id-token: write   # to verify the deployment originates from an appropriate source

    # Deploy to the github-pages environment
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}

    # Specify runner + deployment step
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4.0.0
```

### Options
#### Checkout different branch
```
      - name: Checkout Repository
        uses: actions/checkout@v4
        with:
          ref: dummy-data    #checkout different branch
```
#### Checkout different repository
```
      - name: Checkout tools repo
        uses: actions/checkout@v4
        with:
          repository: my-org/my-tools     #repo public url
          path: my-tools                  #folder to clone to
          ref: branch-name               #branch to clone
```
#### Choosing a folder to generate indexing
```
      - name: Generate Directory Listings
        uses: jayanta525/github-pages-directory-listing@v4.0.0
        with:
          FOLDER: data    #directory to generate index
```
