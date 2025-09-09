#!/bin/bash

# Script to update just the Lambda function code
set -e

ENVIRONMENT="${1:-dev}"
REGION="${2:-us-east-1}"
STACK_NAME="it-support-bot-$ENVIRONMENT"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🔄 Updating Lambda function...${NC}"

# Get Lambda function name from CloudFormation
FUNCTION_NAME=$(aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --region "$REGION" \
    --query 'Stacks[0].Outputs[?OutputKey==`LambdaFunctionName`].OutputValue' \
    --output text)

if [ -z "$FUNCTION_NAME" ]; then
    echo "❌ Could not find Lambda function name"
    exit 1
fi

echo "Function name: $FUNCTION_NAME"

# Create deployment package
cd lambda
rm -f deployment-package.zip

# Install dependencies
if [ -f requirements.txt ]; then
    pip install -r requirements.txt -t . --quiet
fi

# Create zip
zip -r deployment-package.zip . -x "*.pyc" "__pycache__/*" "*.zip" > /dev/null

# Update function code
aws lambda update-function-code \
    --function-name "$FUNCTION_NAME" \
    --zip-file fileb://deployment-package.zip \
    --region "$REGION" > /dev/null

echo -e "${GREEN}✅ Lambda function updated successfully!${NC}"

cd ..