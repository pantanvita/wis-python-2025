# test_protein_utils.py
import unittest
from protein_utils import (
    digest_trypsin,
    digest_chymotrypsin,
    calculate_mass,
    calculate_mz
)

class TestProteinUtils(unittest.TestCase):

    # --- Trypsin Digestion Tests ---
    def test_digest_trypsin_basic(self):
        seq = "AKRPQ"
        # Trypsin cleaves after K or R unless followed by P
        # A K → cleave, R followed by P → no cleavage
        expected = ["AK", "RPQ"]
        result = digest_trypsin(seq)
        self.assertEqual(result, expected)

    def test_digest_trypsin_multiple(self):
        seq = "AKRFAK"
        # Cleaves after K and R (not followed by P)
        expected = ["AK", "R", "FAK"]
        result = digest_trypsin(seq)
        self.assertEqual(result, expected)

    # --- Chymotrypsin Digestion Tests ---
    def test_digest_chymotrypsin_basic(self):
        seq = "FWYPG"
        # Cleaves after F and W, but Y followed by P = no cleavage
        expected = ["F", "W", "YPG"]
        result = digest_chymotrypsin(seq)
        self.assertEqual(result, expected)

    # --- Mass Calculation Tests ---
    def test_calculate_mass_known_peptide(self):
        seq = "ACD"  # A=71.03711, C=103.00919, D=115.02694, +18.01056
        expected_mass = 71.03711 + 103.00919 + 115.02694 + 18.01056
        result = calculate_mass(seq)
        self.assertAlmostEqual(result, expected_mass, places=5)

    def test_calculate_mass_invalid_amino_acid(self):
        with self.assertRaises(ValueError):
            calculate_mass("AXZ")  # Z is not a valid residue

    # --- m/z Calculation Tests ---
    def test_calculate_mz_singly_charged(self):
        mass = 1000.0
        charge = 1
        expected = (1000.0 + 1.007276) / 1
        result = calculate_mz(mass, charge)
        self.assertAlmostEqual(result, expected, places=5)

    def test_calculate_mz_triply_charged(self):
        mass = 1000.0
        charge = 3
        expected = (1000.0 + 3 * 1.007276) / 3
        result = calculate_mz(mass, charge)
        self.assertAlmostEqual(result, expected, places=5)


if __name__ == "__main__":
    unittest.main()
