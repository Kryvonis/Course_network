from django.test import TestCase
from network.pkg.message.models import Message
from network.pkg.message.serializers import JSONMessageSerializer


class TestMessageCreation(TestCase):
    obj = 0

    def setUp(self):
        TestMessageCreation.obj = Message(0, 0, 0, 0, 0, 0)

    def test_creation(self):
        self.assertIsNotNone(TestMessageCreation.obj)

    def test_json(self):
        self.assertIsNotNone(JSONMessageSerializer.encode(TestMessageCreation.obj))

    def test_valid_json(self):
        mock_obj = JSONMessageSerializer.encode(TestMessageCreation.obj)
        self.assertEqual(TestMessageCreation.obj, JSONMessageSerializer.decode(mock_obj))
