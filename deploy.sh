#!/bin/bash

# Copy documents to the Lambda package
echo "Copying documentation files..."
cp -r ../documents ./
cp -r ../resouces_specification ./

echo "Building SAM application..."
sam build

echo "Deploying to AWS..."
if [ ! -f samconfig.toml ]; then
    echo "No samconfig.toml found. Running guided deployment..."
    sam deploy --guided
else
    sam deploy
fi

# Clean up copied files
rm -rf ./documents
rm -rf ./resouces_specification

echo "Deployment complete!"