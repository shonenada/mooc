# coding: utf-8

from .suite import BaseSuite


class SigninUnitTests(BaseSuite):

    def test_get(self):
        rv = self.client.open('/account/signin')
        self.assertIn('<body class="">', rv.data)
        self.assertNotIn('Forbidden', rv.data)

    def test_required_fields(self):
        rv = self.client.post('/account/signin')
        data = rv.data
        self.assertIn('"success": false', data)
        self.assertIn('"errors": true', data)
        self.assertIn('This field is required', data)

    def test_success(self):
        rv = self.client.post('/account/signin', data={
            'username': 'normal_user', 'password': 'passwd'
        })
        self.assertEqual(rv.status_code, 200)
        self.assertIn('"success": true', rv.data)
        rv = self.client.post('/account/signin', data={
            'username': 'staff', 'password': 'passwd'
        }, follow_redirects=True)
        self.assertIn('div id="main"', rv.data)

    def test_failed(self):
        rv = self.client.post('/account/signin', data={
            'username': 'no_this_user', 'password': 'wrong_password'
        }, follow_redirects=True)
        self.assertIn('"success": false', rv.data)

    def prehook(self):
        self.prepare_role()
        self.prepare_account()
