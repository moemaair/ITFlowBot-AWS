import json
import logging
import boto3
from datetime import datetime

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Main Lambda handler for AWS Lex IT Support Bot
    """
    logger.info(f"Received event: {json.dumps(event)}")
    
    intent_name = event.get('currentIntent', {}).get('name')
    slots = event.get('currentIntent', {}).get('slots', {})
    session_attributes = event.get('sessionAttributes', {})
    
    # Route to appropriate intent handler
    if intent_name == 'PasswordReset':
        return handle_password_reset(slots, session_attributes)
    elif intent_name == 'AccountLockout':
        return handle_account_lockout(slots, session_attributes)
    elif intent_name == 'SoftwareInstall':
        return handle_software_install(slots, session_attributes)
    elif intent_name == 'HardwareIssue':
        return handle_hardware_issue(slots, session_attributes)
    elif intent_name == 'TicketStatus':
        return handle_ticket_status(slots, session_attributes)
    elif intent_name == 'GreetingIntent':
        return handle_greeting(slots, session_attributes)
    else:
        return close(session_attributes, 'Failed', 
                    "I'm sorry, I don't understand that request. Please try asking about password resets, account lockouts, software installation, hardware issues, or ticket status.")

def handle_greeting(slots, session_attributes):
    """Handle greeting and introduction"""
    message = {
        'contentType': 'PlainText',
        'content': 'Hello! I\'m your IT Support Bot. I can help you with:\n' +
                  '• Password resets\n' +
                  '• Account lockouts\n' +
                  '• Software installation requests\n' +
                  '• Hardware issue reporting\n' +
                  '• Ticket status checks\n\n' +
                  'What can I help you with today?'
    }
    
    return close(session_attributes, 'Fulfilled', message)

def handle_password_reset(slots, session_attributes):
    """Handle password reset requests"""
    username = slots.get('Username')
    email = slots.get('Email')
    
    if not username:
        return elicit_slot(session_attributes, 'PasswordReset', slots, 'Username',
                          "I can help you reset your password. What's your username?")
    
    if not email:
        return elicit_slot(session_attributes, 'PasswordReset', slots, 'Email',
                          f"Thanks {username}. What's your email address for verification?")
    
    # Simulate password reset process
    ticket_id = generate_ticket_id()
    session_attributes['last_ticket_id'] = ticket_id
    
    message = {
        'contentType': 'PlainText',
        'content': f'Password reset initiated for {username}. ' +
                  f'A temporary password has been sent to {email}. ' +
                  f'Your ticket ID is {ticket_id}. ' +
                  'Please check your email and follow the instructions to complete the reset.'
    }
    
    return close(session_attributes, 'Fulfilled', message)

def handle_account_lockout(slots, session_attributes):
    """Handle account lockout issues"""
    username = slots.get('Username')
    
    if not username:
        return elicit_slot(session_attributes, 'AccountLockout', slots, 'Username',
                          "I can help unlock your account. What's your username?")
    
    # Simulate account unlock process
    ticket_id = generate_ticket_id()
    session_attributes['last_ticket_id'] = ticket_id
    
    message = {
        'contentType': 'PlainText',
        'content': f'Account unlock initiated for {username}. ' +
                  f'Your account should be unlocked within 5 minutes. ' +
                  f'Your ticket ID is {ticket_id}. ' +
                  'If you continue to have issues, please contact IT support directly.'
    }
    
    return close(session_attributes, 'Fulfilled', message)

def handle_software_install(slots, session_attributes):
    """Handle software installation requests"""
    software_name = slots.get('SoftwareName')
    business_justification = slots.get('BusinessJustification')
    
    if not software_name:
        return elicit_slot(session_attributes, 'SoftwareInstall', slots, 'SoftwareName',
                          "What software would you like to install?")
    
    if not business_justification:
        return elicit_slot(session_attributes, 'SoftwareInstall', slots, 'BusinessJustification',
                          f"Please provide a business justification for installing {software_name}:")
    
    # Simulate software request process
    ticket_id = generate_ticket_id()
    session_attributes['last_ticket_id'] = ticket_id
    
    message = {
        'contentType': 'PlainText',
        'content': f'Software installation request submitted for {software_name}. ' +
                  f'Your request will be reviewed by IT security team. ' +
                  f'Your ticket ID is {ticket_id}. ' +
                  'You\'ll receive an email update within 24 hours.'
    }
    
    return close(session_attributes, 'Fulfilled', message)

def handle_hardware_issue(slots, session_attributes):
    """Handle hardware issue reporting"""
    issue_type = slots.get('IssueType')
    description = slots.get('Description')
    
    if not issue_type:
        return elicit_slot(session_attributes, 'HardwareIssue', slots, 'IssueType',
                          "What type of hardware issue are you experiencing? (laptop, desktop, monitor, printer, etc.)")
    
    if not description:
        return elicit_slot(session_attributes, 'HardwareIssue', slots, 'Description',
                          f"Please describe the {issue_type} issue you're experiencing:")
    
    # Simulate hardware issue reporting
    ticket_id = generate_ticket_id()
    session_attributes['last_ticket_id'] = ticket_id
    
    message = {
        'contentType': 'PlainText',
        'content': f'Hardware issue reported for {issue_type}. ' +
                  f'Description: {description}. ' +
                  f'Your ticket ID is {ticket_id}. ' +
                  'A technician will contact you within 4 hours during business hours.'
    }
    
    return close(session_attributes, 'Fulfilled', message)

def handle_ticket_status(slots, session_attributes):
    """Handle ticket status checking"""
    ticket_id = slots.get('TicketId')
    
    if not ticket_id:
        # Check if there's a recent ticket in session
        last_ticket = session_attributes.get('last_ticket_id')
        if last_ticket:
            ticket_id = last_ticket
        else:
            return elicit_slot(session_attributes, 'TicketStatus', slots, 'TicketId',
                              "What's your ticket ID?")
    
    # Simulate ticket status lookup
    status = simulate_ticket_status(ticket_id)
    
    message = {
        'contentType': 'PlainText',
        'content': f'Ticket {ticket_id} status: {status}'
    }
    
    return close(session_attributes, 'Fulfilled', message)

def simulate_ticket_status(ticket_id):
    """Simulate ticket status lookup"""
    # In a real implementation, this would query your ticketing system
    statuses = [
        "Open - Assigned to technician",
        "In Progress - Working on resolution", 
        "Pending - Waiting for user response",
        "Resolved - Solution implemented"
    ]
    # Use ticket_id to deterministically pick a status
    return statuses[hash(ticket_id) % len(statuses)]

def generate_ticket_id():
    """Generate a simple ticket ID"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"IT-{timestamp}"

def close(session_attributes, fulfillment_state, message):
    """Close the session with a message"""
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }
    return response

def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    """Elicit a specific slot value"""
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': {
                'contentType': 'PlainText',
                'content': message
            }
        }
    }