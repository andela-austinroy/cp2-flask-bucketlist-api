from app.test_setup import BaseTestCase


class TestRegisteration(BaseTestCase):
    """Class containing registeration tests"""

    def test_creates_new_user_successfully(self):
        """Tests successfull addition of new users"""
        data = {
            'username': 'user',
            'password': 'password'
        }
        response = self.client.post(
            '/auth/register/', data=data, follow_redirects=True)

        self.assertEqual(201, response.status_code)
        response = response.data.decode('utf-8')
        self.assertIn(data['username'], response)
        self.assertIn('New user added successfully', response)

    def test_registration_without_username(self):
        """
        Ensures registeration fails if no username is supplied in the request
        """
        response = self.client.post('/auth/register/', data={
            'password': 'password'
        }, follow_redirects=True)
        # Ensure response code is 400
        self.assertEqual(400, response.status_code)
        # Decode and verify response data
        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn('Please supply a username in your request', response)

    def test_registration_without_password(self):
        """Ensures the registeration fails when no password is supplied in request"""
        response = self.client.post('/auth/register/', data={
            'username': 'austin'
        }, follow_redirects=True)
        # Ensure response code is 400
        self.assertEqual(400, response.status_code)
        # Decode and verify response data
        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn('Please supply a password in your request', response)

    def test_registration_of_duplicate_users(self):
        """Ensures duplicate users can't be registered"""
        response = self.client.post('/auth/register/', data={
            'username': 'austin',
            'password': 'password'
        }, follow_redirects=True)
        # Ensure response code is 400
        self.assertEqual(400, response.status_code)
        # Decode and verify response data
        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn('username already registered', response)


class TestLogin(BaseTestCase):
    def test_successful_login_with_valid_credentials(self):
        """
        Ensures users are successfully logged in when valid credentials are supplied
        """
        response = self.client.post('/auth/login/', data={
            'username': 'austin',
            'password': 'password'
        }, follow_redirects=True)

        response = response.data.decode('utf-8')
        # Decode and verify response data
        self.assertIn('austin', response)
        self.assertIn('token', response)

    def test_login_without_password(self):
        """Ensure users can't log in if they don't supply a password"""
        response = self.client.post('/auth/login/', data={
            'password': 'password'
        }, follow_redirects=True)
        # Ensure response code is 400
        self.assertEqual(400, response.status_code)
        # Decode and verify response data
        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn('Please supply a username in your request', response)

    def test_login_fails_no_password_submitted(self):
        response = self.client.post('/auth/login/', data={
            'username': 'austin'
        }, follow_redirects=True)
        # Ensure response code is 400
        self.assertEqual(400, response.status_code)
        # Decode and verify response data
        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn('Please supply a password in your request', response)

    def test_login_fails_invalid_credentials(self):
        response = self.client.post('/auth/login/', data={
            'username': 'john',
            'password': 'password'
        }, follow_redirects=True)
        # Ensure response code is 401
        self.assertEqual(401, response.status_code)
        # Decode and verify response data
        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn('Invalid credentials', response)
