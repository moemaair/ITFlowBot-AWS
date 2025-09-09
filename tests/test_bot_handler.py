import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock

# Add lambda directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lambda'))

from bot_handler import (
    lambda_handler,
    handle_greeting,
    handle_password_reset,
    handle_account_lockout,
    handle_software_install,
    handle_hardware_issue,
    handle_ticket_status,
    generate_ticket_id,
    simulate_ticket_status
)

class TestITSupportBot(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.sample_session_attributes = {}
        self.sample_context = {
            'function_name': 'test-function',
            'function_version': '1',
            'invoked_function_arn': 'arn:aws:lambda:us-east-1:123456789012:function:test',
            'memory_limit_in_mb': '128',
            'remaining_time_in_millis': 30000
        }

    def test_greeting_intent(self):
        """Test greeting intent handling"""
        event = {
            'currentIntent': {
                'name': 'GreetingIntent',
                'slots': {}
            },
            'sessionAttributes': {}
        }
        
        response = lambda_handler(event, self.sample_context)
        
        self.assertEqual(response['dialogAction']['type'], 'Close')
        self.assertEqual(response['dialogAction']['fulfillmentState'], 'Fulfilled')
        self.assertIn('IT Support Bot', response['dialogAction']['message']['content'])

    def test_password_reset_no_username(self):
        """Test password reset without username"""
        slots = {}
        response = handle_password_reset(slots, self.sample_session_attributes)
        
        self.assertEqual(response['dialogAction']['type'], 'ElicitSlot')
        self.assertEqual(response['dialogAction']['slotToElicit'], 'Username')

    def test_password_reset_no_email(self):
        """Test password reset with username but no email"""
        slots = {'Username': 'testuser'}
        response = handle_password_reset(slots, self.sample_session_attributes)
        
        self.assertEqual(response['dialogAction']['type'], 'ElicitSlot')
        self.assertEqual(response['dialogAction']['slotToElicit'], 'Email')

    def test_password_reset_complete(self):
        """Test complete password reset flow"""
        slots = {'Username': 'testuser', 'Email': 'test@company.com'}
        response = handle_password_reset(slots, self.sample_session_attributes)
        
        self.assertEqual(response['dialogAction']['type'], 'Close')
        self.assertEqual(response['dialogAction']['fulfillmentState'], 'Fulfilled')
        self.assertIn('Password reset initiated', response['dialogAction']['message']['content'])
        self.assertIn('testuser', response['dialogAction']['message']['content'])

    def test_account_lockout_no_username(self):
        """Test account lockout without username"""
        slots = {}
        response = handle_account_lockout(slots, self.sample_session_attributes)
        
        self.assertEqual(response['dialogAction']['type'], 'ElicitSlot')
        self.assertEqual(response['dialogAction']['slotToElicit'], 'Username')

    def test_account_lockout_complete(self):
        """Test complete account lockout flow"""
        slots = {'Username': 'testuser'}
        response = handle_account_lockout(slots, self.sample_session_attributes)
        
        self.assertEqual(response['dialogAction']['type'], 'Close')
        self.assertEqual(response['dialogAction']['fulfillmentState'], 'Fulfilled')
        self.assertIn('Account unlock initiated', response['dialogAction']['message']['content'])

    def test_software_install_no_software(self):
        """Test software install without software name"""
        slots = {}
        response = handle_software_install(slots, self.sample_session_attributes)
        
        self.assertEqual(response['dialogAction']['type'], 'ElicitSlot')
        self.assertEqual(response['dialogAction']['slotToElicit'], 'SoftwareName')

    def test_software_install_no_justification(self):
        """Test software install without business justification"""
        slots = {'SoftwareName': 'Adobe Photoshop'}
        response = handle_software_install(slots, self.sample_session_attributes)
        
        self.assertEqual(response['dialogAction']['type'], 'ElicitSlot')
        self.assertEqual(response['dialogAction']['slotToElicit'], 'BusinessJustification')

    def test_software_install_complete(self):
        """Test complete software installation flow"""
        slots = {
            'SoftwareName': 'Adobe Photoshop',
            'BusinessJustification': 'Needed for marketing materials'
        }
        response = handle_software_install(slots, self.sample_session_attributes)
        
        self.assertEqual(response['dialogAction']['type'], 'Close')
        self.assertEqual(response['dialogAction']['fulfillmentState'], 'Fulfilled')
        self.assertIn('Software installation request submitted', response['dialogAction']['message']['content'])

    def test_hardware_issue_no_type(self):
        """Test hardware issue without issue type"""
        slots = {}
        response = handle_hardware_issue(slots, self.sample_session_attributes)
        
        self.assertEqual(response['dialogAction']['type'], 'ElicitSlot')
        self.assertEqual(response['dialogAction']['slotToElicit'], 'IssueType')

    def test_hardware_issue_no_description(self):
        """Test hardware issue without description"""
        slots = {'IssueType': 'laptop'}
        response = handle_hardware_issue(slots, self.sample_session_attributes)
        
        self.assertEqual(response['dialogAction']['type'], 'ElicitSlot')
        self.assertEqual(response['dialogAction']['slotToElicit'], 'Description')

    def test_hardware_issue_complete(self):
        """Test complete hardware issue flow"""
        slots = {
            'IssueType': 'laptop',
            'Description': 'Screen is flickering and sometimes goes black'
        }
        response = handle_hardware_issue(slots, self.sample_session_attributes)
        
        self.assertEqual(response['dialogAction']['type'], 'Close')
        self.assertEqual(response['dialogAction']['fulfillmentState'], 'Fulfilled')
        self.assertIn('Hardware issue reported', response['dialogAction']['message']['content'])

    def test_ticket_status_no_id(self):
        """Test ticket status without ticket ID"""
        slots = {}
        response = handle_ticket_status(slots, self.sample_session_attributes)
        
        self.assertEqual(response['dialogAction']['type'], 'ElicitSlot')
        self.assertEqual(response['dialogAction']['slotToElicit'], 'TicketId')

    def test_ticket_status_with_session_ticket(self):
        """Test ticket status with ticket ID in session"""
        slots = {}
        session_attributes = {'last_ticket_id': 'IT-20240101123456'}
        response = handle_ticket_status(slots, session_attributes)
        
        self.assertEqual(response['dialogAction']['type'], 'Close')
        self.assertEqual(response['dialogAction']['fulfillmentState'], 'Fulfilled')
        self.assertIn('IT-20240101123456', response['dialogAction']['message']['content'])

    def test_ticket_status_complete(self):
        """Test complete ticket status flow"""
        slots = {'TicketId': 'IT-20240101123456'}
        response = handle_ticket_status(slots, self.sample_session_attributes)
        
        self.assertEqual(response['dialogAction']['type'], 'Close')
        self.assertEqual(response['dialogAction']['fulfillmentState'], 'Fulfilled')
        self.assertIn('Ticket IT-20240101123456 status:', response['dialogAction']['message']['content'])

    def test_unknown_intent(self):
        """Test handling of unknown intent"""
        event = {
            'currentIntent': {
                'name': 'UnknownIntent',
                'slots': {}
            },
            'sessionAttributes': {}
        }
        
        response = lambda_handler(event, self.sample_context)
        
        self.assertEqual(response['dialogAction']['type'], 'Close')
        self.assertEqual(response['dialogAction']['fulfillmentState'], 'Failed')
        self.assertIn("don't understand", response['dialogAction']['message'])

    def test_generate_ticket_id(self):
        """Test ticket ID generation"""
        ticket_id = generate_ticket_id()
        
        self.assertTrue(ticket_id.startswith('IT-'))
        self.assertEqual(len(ticket_id), 17)  # IT- + 14 digit timestamp

    def test_simulate_ticket_status(self):
        """Test ticket status simulation"""
        status = simulate_ticket_status('IT-20240101123456')
        
        self.assertIsInstance(status, str)
        self.assertTrue(len(status) > 0)
        
        # Test that same ticket ID returns same status
        status2 = simulate_ticket_status('IT-20240101123456')
        self.assertEqual(status, status2)

    def test_handle_greeting_direct(self):
        """Test greeting handler directly"""
        response = handle_greeting({}, {})
        
        self.assertEqual(response['dialogAction']['type'], 'Close')
        self.assertEqual(response['dialogAction']['fulfillmentState'], 'Fulfilled')
        self.assertIn('Password resets', response['dialogAction']['message']['content'])
        self.assertIn('Account lockouts', response['dialogAction']['message']['content'])

if __name__ == '__main__':
    unittest.main()