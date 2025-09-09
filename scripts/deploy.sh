#!/bin/bash

# IT Support Bot Deployment Script
set -e

# Configuration
STACK_NAME="it-support-bot"
ENVIRONMENT="${1:-dev}"
REGION="${2:-us-east-1}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🤖 IT Support Bot Deployment Script${NC}"
echo "Environment: $ENVIRONMENT"
echo "Region: $REGION"
echo "Stack Name: $STACK_NAME-$ENVIRONMENT"
echo ""

# Check AWS CLI is configured
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo -e "${RED}❌ AWS CLI not configured or credentials not valid${NC}"
    exit 1
fi

echo -e "${GREEN}✅ AWS credentials validated${NC}"

# Create Lambda deployment package
echo -e "${YELLOW}📦 Creating Lambda deployment package...${NC}"
cd lambda
if [ -f deployment-package.zip ]; then
    rm deployment-package.zip
fi

# Install dependencies if requirements.txt exists
if [ -f requirements.txt ]; then
    pip install -r requirements.txt -t .
fi

# Create zip package
zip -r deployment-package.zip . -x "*.pyc" "__pycache__/*" "*.zip"
cd ..

echo -e "${GREEN}✅ Lambda package created${NC}"

# Upload Lambda code to S3 (optional, for larger packages)
# For now, we'll embed it in CloudFormation

# Deploy CloudFormation stack
echo -e "${YELLOW}🚀 Deploying CloudFormation stack...${NC}"

# Update Lambda code in CloudFormation template
python3 scripts/update_lambda_code.py

aws cloudformation deploy \
    --template-file infrastructure/cloudformation.yaml \
    --stack-name "$STACK_NAME-$ENVIRONMENT" \
    --parameter-overrides \
        Environment="$ENVIRONMENT" \
        BotName="ITSupportBot" \
    --capabilities CAPABILITY_NAMED_IAM \
    --region "$REGION"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Stack deployed successfully!${NC}"
    
    # Get stack outputs
    echo -e "${YELLOW}📋 Stack Outputs:${NC}"
    aws cloudformation describe-stacks \
        --stack-name "$STACK_NAME-$ENVIRONMENT" \
        --region "$REGION" \
        --query 'Stacks[0].Outputs[*].[OutputKey,OutputValue]' \
        --output table
else
    echo -e "${RED}❌ Stack deployment failed${NC}"
    exit 1
fi

# Build and deploy bot
echo -e "${YELLOW}🤖 Building Lex bot...${NC}"

# Get the bot ID from stack outputs
BOT_ID=$(aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME-$ENVIRONMENT" \
    --region "$REGION" \
    --query 'Stacks[0].Outputs[?OutputKey==`BotId`].OutputValue' \
    --output text)

if [ -n "$BOT_ID" ]; then
    echo "Bot ID: $BOT_ID"
    
    # Build the bot
    aws lexv2-models start-bot-resource-generation \
        --bot-id "$BOT_ID" \
        --generation-input-prompt "Build the bot" \
        --region "$REGION" || echo "Bot build may have been triggered already"
    
    echo -e "${GREEN}✅ Bot build initiated${NC}"
else
    echo -e "${RED}❌ Could not retrieve Bot ID${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Deployment completed!${NC}"
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Wait for bot build to complete (check AWS Console)"
echo "2. Test the bot in the Lex console"
echo "3. Configure chat integrations if needed"
echo ""
echo -e "${YELLOW}To update Lambda code:${NC}"
echo "./scripts/update-lambda.sh $ENVIRONMENT $REGION"