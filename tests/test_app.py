import unittest
from nps_app import create_app, db
from nps_app.settings import TestConfig
from nps_app.models import Cliente, Pesquisa, Resposta

class AppTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a test environment."""
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        """Tear down the test environment."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        """Test if the application object exists."""
        self.assertFalse(self.app is None)
        self.assertTrue(self.app.config['TESTING'])

    def test_home_page(self):
        """Test if the home page loads."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Bem-vindo ao Aplicativo de NPS' in response.data)

    def test_survey_submission(self):
        """Test submitting a survey response."""
        # 1. Create a survey and a customer for the test
        p = Pesquisa(nome='Test Survey')
        c = Cliente(email='test@example.com', nome='Test User')
        db.session.add(p)
        db.session.add(c)
        db.session.commit()

        # 2. Simulate a POST request to the survey page
        response = self.client.post(
            f'/survey/{p.id}/{c.id}',
            data={'score': '9', 'comment': 'Great!'},
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Obrigado por sua resposta!' in response.data)

        # 3. Verify the response was saved to the database
        resposta = Resposta.query.one()
        self.assertEqual(resposta.nota, 9)
        self.assertEqual(resposta.comentario, 'Great!')
        self.assertEqual(resposta.cliente_id, c.id)

if __name__ == '__main__':
    unittest.main()
