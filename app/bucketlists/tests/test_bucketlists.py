from app.test_setup import BaseTestCase


class TestBucketList(BaseTestCase):
    def test_creates_new_bucketlist_with_valid_token(self):
        """
        Tests that new bucketlists are successfully created when a valid token is used
        """
        data = {
            'bucketlist_name': 'Chelsea'
        }
        response = self.client.post(
            '/bucketlists/', data=data, headers=self.token,
            follow_redirects=True)
        # Assert the response is created
        self.assertEqual(201, response.status_code)
        # Assert the expected data is in the response
        response = response.data.decode('utf-8')
        self.assertIn(data['bucketlist_name'], response)
        self.assertIn('date_created', response)

    def test_gets_bucketlist_names_for_the_user(self):
        """
        Tests that names of bucketlists for a certain user are fetched
        """
        response = self.client.get(
            '/bucketlists/', headers=self.token, follow_redirects=True)
        # Assert the expected data is in the response
        response = response.data.decode('utf-8')
        self.assertIn('Checkpoint', response)
        self.assertIn('created_by', response)
        self.assertIn('date_created', response)

    def test_search_bucketlist_by_name(self):
        """
        Tests that we are able to search bucketlists by name
        """
        response = self.client.get(
            '/bucketlists/?q=Check', headers=self.token, follow_redirects=True)
        # Assert the expected data is in the response
        response = response.data.decode('utf-8')
        self.assertIn('Checkpoint', response)
        self.assertIn('created_by', response)
        self.assertIn('date_created', response)
        self.assertIn('next', response)
        self.assertIn('prev', response)

    def test_error_on_bucketlist_creation_with_invalid_token(self):
        """
        Tests that we can't create bucketlists with invalid tokens
        """
        data = {
            'bucketlist_name': 'Chelsea'
        }
        response = self.client.post(
            '/bucketlists/', data=data, headers=self.invalid_token,
            follow_redirects=True)
        # Assert the response is forbidden
        self.assertEqual(403, response.status_code)
        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn('invalid token', response)

    def test_error_on_bucketlist_creation_with_expired_token(self):
        """
        Tests that we can't create bucketlists with expired tokens
        """
        data = {
            'bucketlist_name': 'Chelsea'
        }
        response = self.client.post(
            '/bucketlists/', data=data, headers=self.expired_token,
            follow_redirects=True)
        # Assert the response is forbidden
        self.assertEqual(403, response.status_code)
        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn('expired token', response)


class TestSingleBucketList(BaseTestCase):
    """Classs with tests for a single bucketlist"""

    def test_get_single_bucketlist(self):
        """Test successful fetching of a bucketlist"""
        response = self.client.get(
            '/bucketlists/1', headers=self.token, follow_redirects=True)
        # Assert the expected data is in the response
        response = response.data.decode('utf-8')
        self.assertIn('items', response)
        self.assertIn('date_created', response)
        self.assertIn('created_by', response)

    def test_get_non_existent_bucketlist(self):
        """Asserts error on fetching non existent bucketlist"""
        response = self.client.get(
            '/bucketlists/1000', headers=self.token, follow_redirects=True)
        # Assert the response is not found
        self.assertEqual(404, response.status_code)
        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn('bucket list not found', response)

    def test_get_bucketlist_with_invalid_token(self):
        """Asserts user can't fetch bucketlists with invalid tokens"""
        response = self.client.get(
            '/bucketlists/1', headers=self.invalid_token,
            follow_redirects=True)
        # Assert the response is forbidden
        self.assertEqual(403, response.status_code)
        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn('invalid token', response)

    def test_get_bucketlist_with_expired_token(self):
        """Asserts user can't fetch bucketlists with expired tokens"""
        response = self.client.get(
            '/bucketlists/1', headers=self.expired_token,
            follow_redirects=True)
        # Assert the response is forbidden
        self.assertEqual(403, response.status_code)
        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn('expired token', response)

    def test_update_bucketlist_name(self):
        """Asserts user can update bucketlist names"""
        data = {'name': 'New Bucket'}
        response = self.client.put(
            '/bucketlists/1', data=data, headers=self.token,
            follow_redirects=True)
        # Assert the expected data is in the response
        response = response.data.decode('utf-8')
        self.assertIn(data['name'], response)

    def test_update_with_existing_name(self):
        """
        Asserts user can't give bucketlists the same name as existing bucketlists
        """
        data = {'name': 'Checkpoint'}
        response = self.client.put(
            '/bucketlists/1', data=data, headers=self.token,
            follow_redirects=True)
        # Assert the response is forbidden
        self.assertEqual(403, response.status_code)
        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn('A bucketlist with that name already exists', response)

    def test_deletes_users_bucketlist(self):
        """Asserts user can successfully delete a bucketlist"""
        response = self.client.delete(
            '/bucketlists/1', headers=self.token, follow_redirects=True)
        # Check for successful deletion message
        response = response.data.decode('utf-8')
        self.assertIn('Successfully deleted bucketlist', response)
