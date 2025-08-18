import unittest
from nps_app.utils import calculate_nps

# Mock objects to simulate database models
class MockPesquisa:
    def __init__(self, respostas):
        self.respostas = respostas

class MockResposta:
    def __init__(self, nota):
        self.nota = nota

class TestNPSCalculation(unittest.TestCase):

    def test_no_responses(self):
        """Test calculation with zero responses."""
        pesquisa = MockPesquisa(respostas=[])
        results = calculate_nps(pesquisa)
        self.assertEqual(results['nps_score'], 0)
        self.assertEqual(results['total_respostas'], 0)

    def test_all_promoters(self):
        """Test with 100% promoters."""
        respostas = [MockResposta(10), MockResposta(9)]
        pesquisa = MockPesquisa(respostas)
        results = calculate_nps(pesquisa)
        self.assertEqual(results['nps_score'], 100)
        self.assertEqual(results['promotores'], 2)

    def test_all_detractors(self):
        """Test with 100% detractors."""
        respostas = [MockResposta(0), MockResposta(6)]
        pesquisa = MockPesquisa(respostas)
        results = calculate_nps(pesquisa)
        self.assertEqual(results['nps_score'], -100)
        self.assertEqual(results['detratores'], 2)

    def test_all_passives(self):
        """Test with 100% passives."""
        respostas = [MockResposta(7), MockResposta(8)]
        pesquisa = MockPesquisa(respostas)
        results = calculate_nps(pesquisa)
        self.assertEqual(results['nps_score'], 0)
        self.assertEqual(results['passivos'], 2)

    def test_mixed_responses(self):
        """Test with a mix of all types of responses."""
        # 5 promoters, 2 passives, 3 detractors = 10 total
        # % Promoters = 50%
        # % Detractors = 30%
        # NPS Score = 50 - 30 = 20
        respostas = [
            MockResposta(9), MockResposta(10), MockResposta(9), MockResposta(10), MockResposta(9), # 5 Promoters
            MockResposta(7), MockResposta(8), # 2 Passives
            MockResposta(0), MockResposta(5), MockResposta(6) # 3 Detractors
        ]
        pesquisa = MockPesquisa(respostas)
        results = calculate_nps(pesquisa)
        self.assertEqual(results['total_respostas'], 10)
        self.assertEqual(results['promotores'], 5)
        self.assertEqual(results['passivos'], 2)
        self.assertEqual(results['detratores'], 3)
        self.assertEqual(results['nps_score'], 20)

if __name__ == '__main__':
    unittest.main()
