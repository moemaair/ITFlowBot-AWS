# ITFlowBot-AWS

An intelligent IT Flow Bot powered by AWS Lex for managing IT support requests and tickets.

## Features

- **Create IT Tickets**: Users can create tickets for hardware, software, network, and access issues
- **Check Ticket Status**: Query the status of existing IT tickets
- **Get Help**: Provides guidance on bot capabilities and usage
- **Natural Language Processing**: Powered by AWS Lex for understanding user intents

## Architecture

- **AWS Lex V2**: Conversational AI interface
- **AWS Lambda**: Fulfillment logic and business rules
- **AWS CDK**: Infrastructure as Code for deployment
- **Python 3.9**: Runtime for Lambda functions

## Quick Start

### Prerequisites

- AWS CLI configured with appropriate permissions
- Python 3.9+
- Node.js (for AWS CDK)
- AWS CDK installed (`npm install -g aws-cdk`)

### Deployment

There are two ways to deploy this bot:

#### Option 1: Automated Deployment (Recommended)

1. **Run the deployment script**:
   ```bash
   ./deploy.sh
   ```

This will:
- Install Python dependencies
- Bootstrap CDK if needed
- Deploy the Lambda function and IAM roles
- Provide you with the ARNs needed for Lex bot configuration

#### Option 2: Manual Deployment

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Bootstrap CDK** (if not done before):
   ```bash
   cdk bootstrap
   ```

3. **Deploy the stack**:
   ```bash
   cdk deploy
   ```

### Lex Bot Configuration

After deploying the infrastructure, you need to create the Lex bot:

#### Option A: Using CloudFormation Template

1. **Get the Lambda ARN and Lex Role ARN** from the CDK stack outputs
2. **Deploy the Lex bot using CloudFormation**:
   ```bash
   aws cloudformation create-stack \
     --stack-name ITFlowBot-Lex \
     --template-body file://lex-bot-template.yaml \
     --parameters ParameterKey=LambdaFunctionArn,ParameterValue=<LAMBDA_ARN> \
                  ParameterKey=LexServiceRoleArn,ParameterValue=<LEX_ROLE_ARN>
   ```

#### Option B: Manual Lex Bot Creation

1. Go to the AWS Lex V2 console
2. Create a new bot with these settings:
   - **Name**: ITFlowBot
   - **IAM Role**: Use the Lex service role ARN from CDK output
   - **Language**: English (US)

3. Create the following **Slot Types**:
   - **TicketTypeSlot**: Hardware, Software, Network, Access (with synonyms)

4. Create these **Intents**:
   - **CreateTicket**: For creating new tickets
   - **CheckTicketStatus**: For checking ticket status  
   - **GetHelp**: For getting help information

5. Configure **Lambda fulfillment** using the Lambda ARN from CDK output

6. **Build and test** the bot

### Testing

**Test Lambda function locally**:
```bash
python test_lambda.py
```

**Test the deployed bot**:
1. Go to AWS Lex console
2. Find your "ITFlowBot" 
3. Use the test window to interact with the bot

### Example Interactions

**Creating a Ticket**:
- User: "I need to create a ticket"
- Bot: "What type of issue are you experiencing? (Hardware, Software, Network, or Access)"
- User: "Software"
- Bot: "Can you please describe your software issue in more detail?"
- User: "Excel keeps crashing when I open large files"
- Bot: "I've successfully created your Software ticket with ID IT-123456..."

**Checking Status**:
- User: "What's the status of my ticket"
- Bot: "Please provide your ticket number so I can check its status."
- User: "IT-123456"
- Bot: "Your ticket IT-123456 is In Progress. Our technician is actively working on resolving your issue."

**Getting Help**:
- User: "Help"
- Bot: "I'm your IT Flow Bot assistant! Here's how I can help you..." (shows capabilities)

## Supported Intent Types

1. **CreateTicket**: Creates new IT support tickets
   - Ticket types: Hardware, Software, Network, Access
   - Collects issue description

2. **CheckTicketStatus**: Queries existing ticket status
   - Requires ticket number
   - Returns current status and next steps

3. **GetHelp**: Provides bot capabilities and usage guidance

## Project Structure

```
ITFlowBot-AWS/
├── app.py                          # CDK app entry point
├── cdk.json                        # CDK configuration
├── requirements.txt                # Python dependencies
├── itflow_bot/
│   ├── __init__.py
│   └── itflow_bot_stack.py        # CDK stack definition
└── lambda_functions/
    ├── lambda_function.py         # Lambda fulfillment handler
    └── requirements.txt           # Lambda dependencies
```

## Customization

### Adding New Intents

1. Add intent definition in `itflow_bot_stack.py`
2. Add handler function in `lambda_function.py`
3. Update the intent routing logic

### Modifying Ticket Types

Update the `TicketTypeSlot` slot type in the CDK stack with new values and synonyms.

### Integration with Ticketing Systems

The current implementation uses mock data. To integrate with real systems:

1. Add database connections to Lambda
2. Implement API calls to your ticketing system
3. Add proper error handling and validation

## Development

### Local Testing

Test Lambda function locally:
```bash
cd lambda_functions
python lambda_function.py
```

### Deployment Commands

```bash
# See differences
cdk diff

# Deploy
cdk deploy

# Destroy (cleanup)
cdk destroy
```

## Security

- IAM roles follow least privilege principle
- Lex service role has minimal required permissions
- Lambda function has appropriate execution role

## Cost Optimization

- Lambda functions use efficient Python runtime
- Lex bot configured with reasonable session timeouts
- CloudWatch logs retention can be configured as needed

## Troubleshooting

### Common Issues

1. **Deployment fails**: Check AWS credentials and permissions
2. **Bot doesn't respond**: Verify Lambda permissions for Lex invocation
3. **Intents not working**: Check fulfillment configuration in bot alias

### Logs

Check CloudWatch logs for Lambda function execution details and debugging information.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details.