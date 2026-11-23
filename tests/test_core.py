import unittest
from core import classify, fallback_answer, answer_question, contains_private_identifiers

class DemoTests(unittest.TestCase):
    def test_amount(self):
        self.assertEqual(classify('How much pension per month?'), 'amount')
        self.assertIn('₹4,000', fallback_answer('How much pension?', 'English'))
    def test_age(self):
        self.assertEqual(classify('minimum age 60?'), 'age')
        self.assertIn('60', fallback_answer('minimum age', 'English'))
    def test_application_window_not_invented(self):
        self.assertIn('cannot verify', fallback_answer('How to apply?', 'English'))
    def test_private_information_is_never_sent_to_ai(self):
        self.assertTrue(contains_private_identifiers('My Aadhaar number is 1234 5678 9012'))
        reply, used_ai = answer_question('My Aadhaar number is 1234 5678 9012', 'English', 'fake-key')
        self.assertFalse(used_ai)
        self.assertIn('do not enter', reply)

    def test_non_sensitive_question_remains_allowed(self):
        self.assertFalse(contains_private_identifiers('What is pension amount for a 65 year old?'))

    def test_no_key_mode(self):
        answer, used_ai = answer_question('pension amount', 'Telugu', None)
        self.assertFalse(used_ai)
        self.assertIn('₹4,000', answer)

if __name__ == '__main__':
    unittest.main()
