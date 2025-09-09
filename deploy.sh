#!/bin/bash

# IT Flow Bot AWS Deployment Script

set -e

echo "🚀 Starting IT Flow Bot AWS deployment..."

# Check if AWS CLI is configured
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo "❌ Error: AWS CLI is not configured. Please run 'aws configure' first."
    exit 1
fi

echo "✅ AWS CLI is configured"

# Check if CDK is installed
if ! command -v cdk &> /dev/null; then
    echo "❌ Error: AWS CDK is not installed. Please install with 'npm install -g aws-cdk'"
    exit 1
fi

echo "✅ AWS CDK is available"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Bootstrap CDK (if needed)
echo "🏗️  Bootstrapping CDK (this may take a few minutes on first run)..."
cdk bootstrap

# Deploy the stack
echo "🚀 Deploying IT Flow Bot infrastructure..."
cdk deploy --require-approval never

echo "✅ Infrastructure deployment complete!"

# Get the outputs
echo "📋 Getting deployment outputs..."
LAMBDA_ARN=$(aws cloudformation describe-stacks --stack-name ITFlowBotStack --query 'Stacks[0].Outputs[?OutputKey==`LambdaFunctionArn`].OutputValue' --output text)
LEX_ROLE_ARN=$(aws cloudformation describe-stacks --stack-name ITFlowBotStack --query 'Stacks[0].Outputs[?OutputKey==`LexServiceRoleArn`].OutputValue' --output text)

echo ""
echo "🎉 Deployment successful! Here are your resources:"
echo "Lambda Function ARN: $LAMBDA_ARN"
echo "Lex Service Role ARN: $LEX_ROLE_ARN"
echo ""
echo "🤖 Next steps to complete your Lex bot setup:"
echo "1. Use the CloudFormation template 'lex-bot-template.yaml' to deploy the Lex bot"
echo "2. Or manually create the bot in AWS Lex console using the provided Lambda ARN"
echo ""
echo "📖 See README.md for detailed setup instructions!"