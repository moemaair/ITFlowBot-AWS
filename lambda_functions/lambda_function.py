import json
import logging
import random
from datetime import datetime
from typing import Dict, Any

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lex fulfillment Lambda handler for IT Flow Bot
    """
    logger.info(f"Received event: {json.dumps(event, default=str)}")
    
    try:
        # Extract relevant information from the event
        intent_name = event['sessionState']['intent']['name']
        input_transcript = event['inputTranscript']
        session_attributes = event.get('sessionAttributes', {})
        
        logger.info(f"Processing intent: {intent_name}")
        logger.info(f"Input transcript: {input_transcript}")
        
        # Route to appropriate intent handler
        if intent_name == "CreateTicket":
            return handle_create_ticket(event)
        elif intent_name == "CheckTicketStatus":
            return handle_check_ticket_status(event)
        elif intent_name == "GetHelp":
            return handle_get_help(event)
        else:
            return handle_fallback(event)
            
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return create_response(
            "I'm sorry, I encountered an error while processing your request. Please try again.",
            "Failed"
        )

def handle_create_ticket(event: Dict[str, Any]) -> Dict[str, Any]:
    """Handle ticket creation intent"""
    slots = event['sessionState']['intent']['slots']
    
    ticket_type = slots.get('TicketType', {}).get('value', {}).get('interpretedValue') if slots.get('TicketType') else None
    description = slots.get('Description', {}).get('value', {}).get('interpretedValue') if slots.get('Description') else None
    
    # Check if we have all required information
    if not ticket_type:
        return elicit_slot(
            event,
            'TicketType',
            "What type of issue are you experiencing? (Hardware, Software, Network, or Access)"
        )
    
    if not description:
        return elicit_slot(
            event,
            'Description',
            f"Can you please describe your {ticket_type.lower()} issue in more detail?"
        )
    
    # Generate a mock ticket number
    ticket_number = f"IT-{random.randint(100000, 999999)}"
    
    message = f"I've successfully created your {ticket_type} ticket with ID {ticket_number}. " \
              f"Your issue: '{description}' has been logged and assigned to our IT team. " \
              f"You should receive an email confirmation shortly, and we'll work on resolving your issue as soon as possible."
    
    logger.info(f"Created ticket {ticket_number} for {ticket_type} issue: {description}")
    
    return create_response(message, "Fulfilled")

def handle_check_ticket_status(event: Dict[str, Any]) -> Dict[str, Any]:
    """Handle ticket status check intent"""
    slots = event['sessionState']['intent']['slots']
    
    ticket_number = slots.get('TicketNumber', {}).get('value', {}).get('interpretedValue') if slots.get('TicketNumber') else None
    
    if not ticket_number:
        return elicit_slot(
            event,
            'TicketNumber',
            "Please provide your ticket number so I can check its status."
        )
    
    # Mock ticket status (in a real implementation, this would query a database)
    statuses = ["Open", "In Progress", "Pending User Response", "Resolved", "Closed"]
    status = random.choice(statuses)
    
    if status == "Open":
        message = f"Your ticket {ticket_number} is currently Open and in our queue. Our team will begin working on it soon."
    elif status == "In Progress":
        message = f"Good news! Your ticket {ticket_number} is In Progress. Our technician is actively working on resolving your issue."
    elif status == "Pending User Response":
        message = f"Your ticket {ticket_number} is Pending User Response. Please check your email for additional information we need from you."
    elif status == "Resolved":
        message = f"Your ticket {ticket_number} has been Resolved! Please check your email for the resolution details and confirm if the issue is fixed."
    else:  # Closed
        message = f"Your ticket {ticket_number} has been Closed. If you're still experiencing issues, please create a new ticket."
    
    logger.info(f"Checked status for ticket {ticket_number}: {status}")
    
    return create_response(message, "Fulfilled")

def handle_get_help(event: Dict[str, Any]) -> Dict[str, Any]:
    """Handle general help intent"""
    message = """I'm your IT Flow Bot assistant! Here's how I can help you:

🎫 **Create a Ticket**: Say "I need to create a ticket" or "Report an issue" to log a new IT request
📊 **Check Status**: Ask "What's the status of my ticket" to check on existing tickets  
❓ **Get Help**: Ask me about my capabilities anytime

I can help with:
• Hardware issues (computers, printers, etc.)
• Software problems (applications, programs)
• Network connectivity issues
• Access and permission requests

Just tell me what you need help with, and I'll guide you through the process!"""
    
    return create_response(message, "Fulfilled")

def handle_fallback(event: Dict[str, Any]) -> Dict[str, Any]:
    """Handle fallback intent"""
    message = "I'm sorry, I didn't understand that. I can help you create IT tickets, check ticket status, or provide general help. " \
              "Try saying something like 'I need to create a ticket' or 'Check my ticket status'."
    
    return create_response(message, "Fulfilled")

def elicit_slot(event: Dict[str, Any], slot_name: str, message: str) -> Dict[str, Any]:
    """Elicit a specific slot value from the user"""
    return {
        "sessionState": {
            "sessionAttributes": event.get('sessionAttributes', {}),
            "dialogAction": {
                "type": "ElicitSlot",
                "slotToElicit": slot_name
            },
            "intent": event['sessionState']['intent']
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": message
            }
        ]
    }

def create_response(message: str, fulfillment_state: str) -> Dict[str, Any]:
    """Create a standard response"""
    return {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                "state": fulfillment_state
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": message
            }
        ]
    }