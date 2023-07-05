from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Profile
from django.utils import timezone
from main.models import Note

class NoteModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', 
                                            password='testpassword')
    
    def test_str_representation(self):
        note = Note.objects.create(title='Test Note', 
                                   text='This is a test note', 
                                   last_save=timezone.now())
        self.assertEqual(str(note), 'Test Note')

    def test_get_absolute_url(self):
        note = Note.objects.create(title='Test Note', 
                                   text='This is a test note', 
                                   last_save=timezone.now())
        self.assertEqual(note.get_absolute_url(), f'/note_{note.id}')

    def test_access_field_not_blank(self):
        note = Note.objects.create(title='Test Note', 
                                   text='This is a test note', 
                                   last_save=timezone.now())
        self.assertFalse(note.access.exists())

    def test_access_field_blank(self):
        note = Note.objects.create(title='Test Note', 
                                   text='This is a test note', 
                                   last_save=timezone.now())
        user = User.objects.create_user(username='user0', 
                                        password='password0')
        note.access.add(user)
        self.assertTrue(note.access.exists())

    def test_access_field_with_users(self):
        user1 = User.objects.create_user(username='user1', password='password1')
        user2 = User.objects.create_user(username='user2', password='password2')

        note = Note.objects.create(title='Test Note', text='This is a test note', last_save=timezone.now())
        note.access.add(user1, user2)

        self.assertEqual(note.access.count(), 2)
        self.assertTrue(note.access.filter(username='user1').exists())
        self.assertTrue(note.access.filter(username='user2').exists())