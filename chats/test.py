import json
import unittest
import requests
from unittest import TestCase

api_base = 'http://localhost:5000'


class ChatTestCase(TestCase):
    def setUp(self):
        pass

    def submitChatTestCases(self):
        data = {'username': 'buhle', 'message': 'Hi', 'messageto': 'john'}
        response = requests.post(api_base + '/chat', data=json.dumps(data))
        self.assertEquals(response.status_code, 200)

    def invalidParametersTestCases(self):
        data = {'username1': '12345', 'message1': 'Hey', 'messageto': '24680'}
        response = requests.post(api_base + '/chat', data=json.dumps(data))
        self.assertEqual(response.text, 'Incorrect values supplied.')

    def savingChatTestCases(self):
        data = {'username': 'zama', 'message': 'Hala', 'messageto': 'john'}
        response = requests.post(api_base + '/chat', data=json.dumps(data))
        self.assertEquals(response.text, 'chat saved')

    def invalidValuesTestCases(self):
        data = {'username': '', 'message': 'Hey', 'messageto': 'john'}
        response = requests.post(api_base + '/chat', data=json.dumps(data))
        self.assertEqual(response.text, 'User name is required.')

    def updateChatTestCases(self):
        data = {'username': '', 'message': 'Hey', 'messageto': 'john'}
        response = requests.post(api_base + '/chat', data=json.dumps(data))
        self.assertEqual(response.text, 'User name is required.')

    def viewPreviousChatsTestCases(self):
        data = {'username': 'buhle', 'message': 'Hi', 'messageto': 'john'}
        response = requests.post(api_base + '/chat', data=json.dumps(data))
        self.assertEquals(response.status_code, 200)

        data = {'user1': 'buhle', 'user2': 'john'}
        response = requests.get(api_base + '/chat', data=json.dumps(data))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'User name is required.')
