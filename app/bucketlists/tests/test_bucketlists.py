from app.test_setup import BaseTestCase
import json


class TestBucketList(BaseTestCase):
    def test_creates_new_bucketlist_with_valid_token(self):
        """
        Tests that new bucketlists are successfully created when a valid token is used
        """
        data = {
            'name': 'Chelsea'
        }
        response = self.client.post(
            '/bucketlists/', data=json.dumps(data),
            headers=self.token)
        # Assert the response is created
        self.assertEqual(201, response.status_code)
        # Assert the expected data is in the response
        response = response.data.decode('utf-8')
        self.assertIn(data['name'], response)

    def test_gets_bucketlist_for_the_user(self):
        """
        Tests that names of bucketlists for a certain user are fetched
        """
        response = self.client.get(
            '/bucketlists/', headers=self.token,
            follow_redirects=True)
        self.assertEqual(200, response.status_code)

    def test_search_bucketlist_by_name(self):
        """
        Tests that we are able to search bucketlists by name
        """
        response = self.client.get(
            '/bucketlists/?q=Check',
            headers=self.token)
        self.assertEqual(200, response.status_code)
        # Assert the expected data is in the response
        response = response.data.decode('utf-8')
        self.assertIn('Checkpoint', response)

    def test_error_on_bucketlist_creation_with_invalid_token(self):
        """
        Tests that we can't create bucketlists with invalid tokens
        """
        data = {
            'name': 'Chelsea'
        }
        response = self.client.post(
            '/bucketlists/', data=json.dumps(data),
            headers=self.invalid_token,
            follow_redirects=True)
        # Assert the response is unauthorised
        self.assertEqual(401, response.status_code)
        response = response.data.decode('utf-8')
        self.assertIn('invalid token', response)

    def test_error_on_bucketlist_creation_with_expired_token(self):
        """
        Tests that we can't create bucketlists with expired tokens
        """
        data = {
            'name': 'Chelsea'
        }
        response = self.client.post(
            '/bucketlists/', data=json.dumps(data),
            headers=self.expired_token,
            follow_redirects=True)
        # Assert the response is unauthorised
        self.assertEqual(401, response.status_code)
        response = response.data.decode('utf-8')
        self.assertIn('invalid token', response)


class TestSingleBucketList(BaseTestCase):
    """Classs with tests for a single bucketlist"""

    def test_get_single_bucketlist(self):
        """Test successful fetching of a bucketlist"""
        response = self.client.get(
            '/bucketlists/1',
            headers=self.token)
        self.assertEqual(200, response.status_code)
        # Assert the expected data is in the response
        response = response.data.decode('utf-8')
        self.assertIn('date_created', response)

    def test_get_non_existent_bucketlist(self):
        """Asserts error on fetching non existent bucketlist"""
        response = self.client.get(
            '/bucketlists/1000',
            headers=self.token)
        # Assert the response is not found
        self.assertEqual(404, response.status_code)
        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn('bucketlist not found', response)

    def test_get_bucketlist_with_invalid_token(self):
        """Asserts user can't fetch bucketlists with invalid tokens"""
        response = self.client.get(
            '/bucketlists/1', headers={"Authorization": self.invalid_token,
                                       'Content-Type': 'application/json'},
            follow_redirects=True)
        # Assert the response is unauthorised
        self.assertEqual(401, response.status_code)
        response = response.data.decode('utf-8')
        self.assertIn('invalid token', response)

    def test_get_bucketlist_with_expired_token(self):
        """Asserts user can't fetch bucketlists with expired tokens"""
        response = self.client.get(
            '/bucketlists/1', headers=self.expired_token,
            follow_redirects=True)
        # Assert the response is unauthorised
        self.assertEqual(401, response.status_code)
        response = response.data.decode('utf-8')
        self.assertIn('invalid token', response)

    def test_update_bucketlist_name(self):
        """Asserts user can update bucketlist names"""
        data = {'name': 'New Bucket'}
        response = self.client.put(
            '/bucketlists/1', data=json.dumps(data),
            headers=self.token)
        # Assert the expected data is in the response
        response = response.data.decode('utf-8')
        self.assertIn(data['name'], response)

    def test_update_non_existent_bucketlist(self):
        """Asserts user can update bucketlist names"""
        data = {'name': 'New Bucket'}
        response = self.client.put(
            '/bucketlists/1000', data=json.dumps(data),
            headers=self.token)
        # Assert the expected data is in the response
        self.assertEqual(404, response.status_code)
        response = response.data.decode('utf-8')
        self.assertIn("Bucketlist not found", response)

    def test_update_with_existing_name(self):
        """
        Asserts user can't give bucketlists the same name as existing bucketlists
        """
        data = {'name': 'Checkpoint 2'}
        response = self.client.put(
            '/bucketlists/1', data=json.dumps(data),
            headers=self.token)
        # Assert the response is forbidden
        self.assertEqual(403, response.status_code)
        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn('That bucketlist name has already been used', response)

    def test_deletes_users_bucketlist(self):
        """Asserts user can successfully delete a bucketlist"""
        response = self.client.delete(
            '/bucketlists/1',
            headers=self.token)
        self.assertEqual(200, response.status_code)
        # Check for successful deletion message
        response = response.data.decode('utf-8')
        self.assertIn('Successfully deleted bucketlist', response)


class TestBucketListItem(BaseTestCase):
    def test_create_new_bucketlist_item(self):
        data = {'name': 'Write tests for the CP',
                'description': 'write tests to help guide coding process'}
        response = self.client.post(
            '/bucketlists/1/items/', data=json.dumps(data),
            headers=self.token)

        self.assertEqual(201, response.status_code)

        response = response.data.decode('utf-8')
        self.assertIn('date_modified', response)
        self.assertIn(data['name'], response)
        self.assertIn(data['description'], response)

    def test_error_on_create_item_on_non_existent_bucketlist(self):
        data = {'name': 'Join the dark side'}
        response = self.client.post(
            '/bucketlists/100/items/', data=json.dumps(data),
            headers=self.token)

        self.assertEqual(404, response.status_code)

        response = response.data.decode('utf-8')
        self.assertIn('bucket list does not exist', response)

    def test_error_on_create_item_without_token(self):
        data = {'name': 'Join the dark side'}
        response = self.client.post(
            '/bucketlists/1/items/', data=json.dumps(data),
            follow_redirects=True)

        self.assertEqual(401, response.status_code)

        response = response.data.decode('utf-8')
        self.assertIn('invalid token', response)

    def test_update_item_name_and_description(self):
        data = {'name': 'This is updated',
                'description': 'Updated item right here'}
        response = self.client.put(
            '/bucketlists/1/items/1', data=json.dumps(data),
            headers=self.token)

        response = response.data.decode('utf-8')
        self.assertIn(data['name'], response)
        self.assertIn(data['description'], response)

    def test_update_item_to_done(self):
        data = {'done': 'true'}
        response = self.client.put(
            '/bucketlists/1/items/1', data=json.dumps(data),
            headers=self.token)

        response = response.data.decode('utf-8')
        self.assertIn('true', response)

    def test_update_item_to_pending(self):
        data = {'done': 'false'}
        response = self.client.put(
            '/bucketlists/1/items/1', data=json.dumps(data),
            headers=self.token)

        response = response.data.decode('utf-8')
        self.assertIn('false', response)

    def test_update_item_invalid_status(self):
        data = {'done': 'khal'}
        response = self.client.put(
            '/bucketlists/1/items/1', data=json.dumps(data),
            headers=self.token)

        self.assertEqual(400, response.status_code)

    def test_error_on_updating_non_existent_item(self):
        data = {'name': 'Trying to update',
                'description': 'My update attempt'}
        response = self.client.put(
            '/bucketlists/1/items/100', data=json.dumps(data),
            headers=self.token)

        self.assertEqual(404, response.status_code)

        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn("buckelist item not found", response)

    def test_delete_item(self):
        response = self.client.delete(
            '/bucketlists/1/items/1',
            headers=self.token)
        self.assertEqual(200, response.status_code)
        response = response.data.decode('utf-8')
        self.assertIn("Successfully deleted bucketlist item", response)

    def test_delete_non_existent_item(self):
        response = self.client.delete(
            '/bucketlists/1/items/1000',
            headers=self.token)
        self.assertEqual(404, response.status_code)
        response = response.data.decode('utf-8')
        self.assertIn("That bucketlist item doesn't exist", response)
