# ITFlowBot-AWS

A comprehensive AWS Lex-powered IT Support Bot for internal employee assistance. This bot helps automate common IT support tasks like password resets, account lockouts, software installation requests, hardware issue reporting, and ticket status checking.

## Features

### 🤖 Supported IT Support Functions
- **Password Resets**: Automated password reset initiation with email verification
- **Account Lockout Resolution**: Quick account unlock requests
- **Software Installation Requests**: Streamlined software approval workflow
- **Hardware Issue Reporting**: Automated ticket creation for hardware problems
- **Ticket Status Checking**: Real-time status updates for existing tickets
- **Interactive Help**: Guided assistance with natural language understanding

### 🏗️ Architecture
- **AWS Lex V2**: Natural language understanding and conversation management
- **AWS Lambda**: Business logic and fulfillment processing
- **CloudFormation**: Infrastructure as Code for easy deployment
- **Python 3.9**: Robust and maintainable bot logic

## Quick Start

### Prerequisites
- AWS CLI configured with appropriate permissions
- Python 3.9 or later
- Bash shell (for deployment scripts)

### Deployment

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ITFlowBot-AWS
   ```

2. **Deploy to AWS**
   ```bash
   ./scripts/deploy.sh dev us-east-1
   ```

3. **Test the bot** in the AWS Lex console or integrate with your preferred chat platform

### Quick Update Lambda Only
```bash
./scripts/update-lambda.sh dev us-east-1
```

## Project Structure

```
ITFlowBot-AWS/
├── lambda/
│   ├── bot_handler.py      # Main Lambda function
│   └── requirements.txt    # Python dependencies
├── lex-bot/
│   └── it-support-bot.json # Lex bot definition (legacy format)
├── infrastructure/
│   └── cloudformation.yaml # AWS infrastructure template
├── scripts/
│   ├── deploy.sh          # Main deployment script
│   ├── update-lambda.sh   # Lambda update script
│   └── update_lambda_code.py # Helper script
├── tests/
│   └── test_bot_handler.py # Unit tests
└── README.md
```

## Bot Conversations

### Password Reset Flow
```
User: "I need to reset my password"
Bot:  "I can help you reset your password. What's your username?"
User: "john.doe"
Bot:  "Thanks john.doe. What's your email address for verification?"
User: "john.doe@company.com"
Bot:  "Password reset initiated for john.doe. A temporary password has been sent to john.doe@company.com. Your ticket ID is IT-20240109123456."
```

### Hardware Issue Flow
```
User: "My laptop isn't working"
Bot:  "What type of hardware issue are you experiencing? (laptop, desktop, monitor, printer, etc.)"
User: "laptop"
Bot:  "Please describe the laptop issue you're experiencing:"
User: "Screen keeps flickering and goes black randomly"
Bot:  "Hardware issue reported for laptop. Description: Screen keeps flickering and goes black randomly. Your ticket ID is IT-20240109123457. A technician will contact you within 4 hours during business hours."
```

## Configuration

### Environment Variables
The Lambda function supports the following environment variables:
- `ENVIRONMENT`: Deployment environment (dev/staging/prod)
- `BOT_NAME`: Name of the bot instance

### Customization
- **Intent Handling**: Modify handlers in `lambda/bot_handler.py`
- **Bot Responses**: Update messages in the handler functions
- **Infrastructure**: Adjust resources in `infrastructure/cloudformation.yaml`

## Testing

### Run Unit Tests
```bash
python -m unittest discover tests/ -v
```

### Manual Testing
1. Deploy the bot to AWS
2. Open the AWS Lex console
3. Navigate to your bot and use the test chat interface
4. Try sample conversations:
   - "Hello"
   - "I need to reset my password"
   - "My computer isn't working"
   - "Check ticket status"

## Integration Options

### Slack Integration
Add Slack channel integration in the AWS Lex console to deploy the bot to your Slack workspace.

### Microsoft Teams
Configure Microsoft Teams integration for enterprise chat deployment.

### Web Chat
Use the AWS Connect integration or custom web chat implementation.

### Voice Support
Enable voice interactions through Amazon Connect or Alexa for Business.

## Security Considerations

- The bot uses IAM roles with minimal required permissions
- All sensitive data should be encrypted in transit and at rest
- Consider implementing additional authentication for production use
- Audit bot conversations for compliance requirements

## Monitoring & Logging

- CloudWatch Logs capture all Lambda function execution details
- Lex conversation logs are available in CloudWatch
- Set up CloudWatch alarms for error rates and response times

## Development

### Adding New Intents

1. **Update the Lambda handler** in `lambda/bot_handler.py`:
   ```python
   def handle_new_intent(slots, session_attributes):
       # Implementation here
       pass
   ```

2. **Add intent routing** in the main handler:
   ```python
   elif intent_name == 'NewIntent':
       return handle_new_intent(slots, session_attributes)
   ```

3. **Update CloudFormation template** to include the new intent

4. **Add unit tests** in `tests/test_bot_handler.py`

5. **Deploy updates**:
   ```bash
   ./scripts/update-lambda.sh dev
   ```

### Local Testing
```bash
# Install dependencies
cd lambda
pip install -r requirements.txt

# Run tests
cd ..
python -m unittest discover tests/ -v
```

## Troubleshooting

### Common Issues

1. **Bot not responding**
   - Check CloudWatch logs for Lambda errors
   - Verify Lex bot is built successfully
   - Ensure Lambda permissions are correct

2. **Intent not recognized**
   - Review sample utterances in bot definition
   - Check NLU confidence threshold settings
   - Add more training examples

3. **Deployment failures**
   - Verify AWS credentials and permissions
   - Check CloudFormation events for specific errors
   - Ensure unique resource names

### Logs Location
- Lambda logs: `/aws/lambda/ITSupportBot-fulfillment-{environment}`
- Lex logs: Amazon Lex console > Your bot > Aliases > Conversation logs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

See LICENSE file for details.

## Support

For questions or issues:
1. Check the troubleshooting section
2. Review CloudWatch logs
3. Open an issue in the repository