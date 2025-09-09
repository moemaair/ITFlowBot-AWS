#!/usr/bin/env python3
"""
Test script for IT Flow Bot Lambda function
"""

import json
import sys
import os

# Add the lambda_functions directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lambda_functions'))

from lambda_function import lambda_handler

def test_create_ticket():
    """Test ticket creation flow"""
    print("🎫 Testing ticket creation...")
    
    # Test 1: Initial request
    event = {
        "inputTranscript": "I need to create a ticket",
        "sessionState": {
            "intent": {
                "name": "CreateTicket",
                "slots": {}
            }
        },
        "sessionAttributes": {}
    }
    
    response = lambda_handler(event, None)
    print(f"Response: {response['messages'][0]['content']}")
    assert "type of issue" in response['messages'][0]['content'].lower()
    
    # Test 2: Provide ticket type
    event = {
        "inputTranscript": "Software",
        "sessionState": {
            "intent": {
                "name": "CreateTicket",
                "slots": {
                    "TicketType": {
                        "value": {
                            "interpretedValue": "Software"
                        }
                    }
                }
            }
        },
        "sessionAttributes": {}
    }
    
    response = lambda_handler(event, None)
    print(f"Response: {response['messages'][0]['content']}")
    assert "describe" in response['messages'][0]['content'].lower()
    
    # Test 3: Provide description
    event = {
        "inputTranscript": "Excel keeps crashing",
        "sessionState": {
            "intent": {
                "name": "CreateTicket",
                "slots": {
                    "TicketType": {
                        "value": {
                            "interpretedValue": "Software"
                        }
                    },
                    "Description": {
                        "value": {
                            "interpretedValue": "Excel keeps crashing"
                        }
                    }
                }
            }
        },
        "sessionAttributes": {}
    }
    
    response = lambda_handler(event, None)
    print(f"Response: {response['messages'][0]['content']}")
    assert "IT-" in response['messages'][0]['content']
    assert "Software" in response['messages'][0]['content']
    
    print("✅ Ticket creation test passed!")

def test_check_status():
    """Test ticket status check"""
    print("\n📊 Testing ticket status check...")
    
    # Test 1: Request without ticket number
    event = {
        "inputTranscript": "Check my ticket status",
        "sessionState": {
            "intent": {
                "name": "CheckTicketStatus",
                "slots": {}
            }
        },
        "sessionAttributes": {}
    }
    
    response = lambda_handler(event, None)
    print(f"Response: {response['messages'][0]['content']}")
    assert "ticket number" in response['messages'][0]['content'].lower()
    
    # Test 2: Provide ticket number
    event = {
        "inputTranscript": "IT-123456",
        "sessionState": {
            "intent": {
                "name": "CheckTicketStatus",
                "slots": {
                    "TicketNumber": {
                        "value": {
                            "interpretedValue": "IT-123456"
                        }
                    }
                }
            }
        },
        "sessionAttributes": {}
    }
    
    response = lambda_handler(event, None)
    print(f"Response: {response['messages'][0]['content']}")
    assert "IT-123456" in response['messages'][0]['content']
    
    print("✅ Status check test passed!")

def test_get_help():
    """Test help functionality"""
    print("\n❓ Testing help functionality...")
    
    event = {
        "inputTranscript": "Help",
        "sessionState": {
            "intent": {
                "name": "GetHelp",
                "slots": {}
            }
        },
        "sessionAttributes": {}
    }
    
    response = lambda_handler(event, None)
    print(f"Response: {response['messages'][0]['content']}")
    assert "IT Flow Bot" in response['messages'][0]['content']
    assert "create" in response['messages'][0]['content'].lower()
    
    print("✅ Help test passed!")

def test_fallback():
    """Test fallback functionality"""
    print("\n🤷 Testing fallback functionality...")
    
    event = {
        "inputTranscript": "Unknown command",
        "sessionState": {
            "intent": {
                "name": "UnknownIntent",
                "slots": {}
            }
        },
        "sessionAttributes": {}
    }
    
    response = lambda_handler(event, None)
    print(f"Response: {response['messages'][0]['content']}")
    assert "sorry" in response['messages'][0]['content'].lower()
    
    print("✅ Fallback test passed!")

if __name__ == "__main__":
    print("🧪 Starting IT Flow Bot Lambda function tests...\n")
    
    try:
        test_create_ticket()
        test_check_status()
        test_get_help()
        test_fallback()
        
        print("\n🎉 All tests passed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        sys.exit(1)