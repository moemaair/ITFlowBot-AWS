#!/usr/bin/env python3
"""
Script to update the Lambda code in CloudFormation template
"""

import os
import yaml
import base64

def main():
    # Read the Lambda function code
    lambda_file = 'lambda/bot_handler.py'
    cf_template = 'infrastructure/cloudformation.yaml'
    
    if not os.path.exists(lambda_file):
        print(f"Lambda file {lambda_file} not found")
        return
    
    with open(lambda_file, 'r') as f:
        lambda_code = f.read()
    
    # Read CloudFormation template
    with open(cf_template, 'r') as f:
        template = yaml.safe_load(f)
    
    # Update the Lambda code in the template
    if 'Resources' in template and 'BotFulfillmentFunction' in template['Resources']:
        template['Resources']['BotFulfillmentFunction']['Properties']['Code']['ZipFile'] = lambda_code
        print("✅ Updated Lambda code in CloudFormation template")
    else:
        print("❌ Could not find BotFulfillmentFunction in template")
        return
    
    # Write back the template
    with open(cf_template, 'w') as f:
        yaml.dump(template, f, default_flow_style=False, sort_keys=False)
    
    print("✅ CloudFormation template updated successfully")

if __name__ == '__main__':
    main()