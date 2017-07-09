import json
import unittest
import requests
from unittest import TestCase

api_base = 'http://localhost:5000'


class ChatTestCase(TestCase):
    def setUp(self):
        pass

    def submitChatTestCases(self):
        data = {'username': 'buhle', 'message': 'Hi'}
        response = requests.post(api_base + '/chat', data=json.dumps(data))
        self.assertEquals(response.status_code, 200)

    def invalidParametersTestCases(self):
        data = {'username1': 'buhle', 'message1': 'Hey'}
        response = requests.post(api_base + '/chat', data=json.dumps(data))
        self.assertEqual(response.text, 'Incorrect values supplied.')

    def savingChatTestCases(self):
        data = {'username': 'zama', 'message': 'Hala'}
        response = requests.post(api_base + '/chat', data=json.dumps(data))
        self.assertEquals(response.text, 'chat saved')

    def invalidValuesTestCases(self):
        data = {'username': '', 'message': 'Hey'}
        response = requests.post(api_base + '/chat', data=json.dumps(data))
        self.assertEqual(response.text, 'User name is required.')



