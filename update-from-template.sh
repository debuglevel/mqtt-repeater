#!/bin/bash

# run this if file is not yet present or it should be updated first:
#  curl -o update-from-template.sh https://raw.githubusercontent.com/debuglevel/greeting-microservice-python/master/update-from-template.sh && chmod +x update-from-template.sh && git add --chmod=+x update-from-template.sh && git commit update-from-template.sh -m "Add/Update update-from-template.sh script"

echo "Adding template git remote..."
git remote add template https://github.com/debuglevel/greeting-microservice-python.git
echo "Fetching from git remote..."
git fetch --no-tags template

files=(
    # can usually be replaced without any merges
    update-from-template.sh
    LICENSE
    .gitlab-ci.yml
    .dockerignore
    Dockerfile
    update-openapi.py

    # might need some merges
    .gitignore
    .gitpod.yml
    .gitpod.Dockerfile
    docker-compose.yml
    docker-build-and-run.ps1
    tox.ini
    requirements-dev.txt

    # might need heavy merges
    )

echo ""
echo "The following files from the template will be processed:"
for file in "${files[@]}"; do
  echo "- $file";
done

echo ""
echo "The following runs a 'git checkout --patch' command:"
echo "  Press [y] to apply a patch."
echo "  Press [n] to discard a patch."
echo "  Press [e] to edit a patch."
echo "  Press [s] to split into smaller hunks."
echo "  Press [q] to quit that thing (maybe also useful if this script itself was updated to re-execute it)."
echo "  Press [?] to get information about all that letters you can choose."

git checkout -p template/master ${files[*]}

echo "Now you should carefully check changes before committing."