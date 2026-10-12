import json
import unittest

import main


class LeadTests(unittest.TestCase):
    def test_budget_parse(self):
        self.assertEqual(main.parse_budget("budget around 1.5m"), 1_500_000)
        self.assertEqual(main.parse_budget("NGN 800,000"), 800_000)
        self.assertEqual(main.parse_budget("200k"), 200_000)

    def test_tiers(self):
        leads = {l["name"]: main.score(l)["tier"] for l in json.load(open("sample_leads.json"))}
        self.assertEqual(leads["Bola Adeniran"], "HOT")
        self.assertEqual(leads["Samuel Okon"], "HOT")
        self.assertEqual(leads["Ifeoma Chukwu"], "COLD")


if __name__ == "__main__":
    unittest.main()
