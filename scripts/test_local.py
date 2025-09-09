#!/usr/bin/env python3
"""
Local test script for the IT Support Bot
"""

import sys
import os
import json

# Add lambda directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lambda'))

from bot_handler import lambda_handler

def test_conversation():
    """Test a sample conversation with the bot"""
    
    print("🤖 IT Support Bot - Local Test")
    print("=" * 40)
    
    # Test greeting
    print("\n1. Testing Greeting Intent")
    event = {
        'currentIntent': {
            'name': 'GreetingIntent',
            'slots': {}
        },
        'sessionAttributes': {}
    }
    
    response = lambda_handler(event, {})
    print(f"Bot: {response['dialogAction']['message']['content']}")
    
    # Test password reset flow
    print("\n2. Testing Password Reset Flow")
    
    # Step 1: Start password reset
    event = {
        'currentIntent': {
            'name': 'PasswordReset',
            'slots': {}
        },
        'sessionAttributes': {}
    }
    
    response = lambda_handler(event, {})
    print(f"Bot: {response['dialogAction']['message']['content']}")
    
    # Step 2: Provide username
    event = {
        'currentIntent': {
            'name': 'PasswordReset',
            'slots': {'Username': 'john.doe'}
        },
        'sessionAttributes': {}
    }
    
    response = lambda_handler(event, {})
    print(f"Bot: {response['dialogAction']['message']['content']}")
    
    # Step 3: Provide email
    event = {
        'currentIntent': {
            'name': 'PasswordReset',
            'slots': {
                'Username': 'john.doe',
                'Email': 'john.doe@company.com'
            }
        },
        'sessionAttributes': {}
    }
    
    response = lambda_handler(event, {})
    print(f"Bot: {response['dialogAction']['message']['content']}")
    
    # Test hardware issue
    print("\n3. Testing Hardware Issue Flow")
    
    event = {
        'currentIntent': {
            'name': 'HardwareIssue',
            'slots': {
                'IssueType': 'laptop',
                'Description': 'Screen keeps flickering'
            }
        },
        'sessionAttributes': {}
    }
    
    response = lambda_handler(event, {})
    print(f"Bot: {response['dialogAction']['message']['content']}")
    
    # Test ticket status
    print("\n4. Testing Ticket Status Check")
    
    event = {
        'currentIntent': {
            'name': 'TicketStatus',
            'slots': {'TicketId': 'IT-20240109123456'}
        },
        'sessionAttributes': {}
    }
    
    response = lambda_handler(event, {})
    print(f"Bot: {response['dialogAction']['message']['content']}")
    
    print("\n✅ All tests completed successfully!")

if __name__ == '__main__':
    test_conversation()