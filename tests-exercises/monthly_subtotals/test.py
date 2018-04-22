import unittest
from monthly_subtotals.monthly_subtotals import update_monthly_subtotals


class MonthlySubtotals(unittest.TestCase):

    def setUp(self):
        self.oct_subtotals = {"count": 15, "amount": 425, "num_items": 12, "gender": {
            "F": {
                "count": 5,
                "amount": 225,
                "num_items": 7
            },
            "M": {
                "count": 10,
                "amount": 200,
                "num_items": 5
            }
        }, "currency": {
            "EUR": {
                "count": 13,
                "amount": 175,
                "num_items": 6
            },
            "USD": {
                "count": 2,
                "amount": 250,
                "num_items": 6
            }}}
        self.entry_new_currency = {"gender": "F", "amount": 15.0, "num_items": 5, "currency": "GBP"}

    def test_new_entry(self):
        self.new_entry = {"gender": "M", "amount": 17.0, "num_items": 2, "currency": "EUR"}
        self.expected_output = {"count": 16, "amount": 442, "num_items": 14, "gender": {
            "F": {
                "count": 5,
                "amount": 225,
                "num_items": 7
            },
            "M": {
                "count": 11,
                "amount": 217,
                "num_items": 7
            }
        }, "currency": {
            "EUR": {
                "count": 14,
                "amount": 192,
                "num_items": 8
            },
            "USD": {
                "count": 2,
                "amount": 250,
                "num_items": 6
            }}}
        self.output = update_monthly_subtotals(self.oct_subtotals, self.new_entry)
        self.assertEqual(self.output, self.expected_output)

    def test_new_key(self):
        self.new_key = {"gender": "M", "amount": 17.0, "num_items": 2, "currency": "EUR", "country_code": 'DK'}
        self.expected_new_key_output = {"count": 16, "amount": 442.0, "num_items": 14, "country_code": 'DK', "gender": {
            "F": {
                "count": 5,
                "amount": 225,
                "num_items": 7
            },
            "M": {
                "count": 11,
                "amount": 217.0,
                "num_items": 7
            }
        }, "currency": {
            "EUR": {
                "count": 14,
                "amount": 192.0,
                "num_items": 8
            },
            "USD": {
                "count": 2,
                "amount": 250,
                "num_items": 6
            }}}

        self.new_key_output = update_monthly_subtotals(self.oct_subtotals, self.new_key)
        self.assertEqual(self.expected_new_key_output, self.new_key_output)

    def test_new_currency(self):
        self.expected_currency_output = {"count": 16, "amount": 440, "num_items": 17, "gender": {
            "F": {
                "count": 6,
                "amount": 240,
                "num_items": 12
            },
            "M": {
                "count": 10,
                "amount": 200,
                "num_items": 5
            }
        }, "currency": {
            "EUR": {
                "count": 13,
                "amount": 175,
                "num_items": 6
            },
            "GBP": {
                "count": 1,
                "amount": 15,
                "num_items": 5
            },
            "USD": {
                "count": 2,
                "amount": 250,
                "num_items": 6
            }}}
        self.entered_new_currency = update_monthly_subtotals(self.oct_subtotals, self.entry_new_currency)
        self.assertEqual(self.expected_currency_output, self.entered_new_currency)


    def test_add_to_new_currency(self):
        self.new_currency_subtotals = {"count": 16, "amount": 440, "num_items": 17, "gender": {
            "F": {
                "count": 6,
                "amount": 240,
                "num_items": 12
            },
            "M": {
                "count": 10,
                "amount": 200,
                "num_items": 5
            }
        }, "currency": {
            "EUR": {
                "count": 13,
                "amount": 175,
                "num_items": 6
            },
            "GBP": {
                "count": 1,
                "amount": 15,
                "num_items": 5
            },
            "USD": {
                "count": 2,
                "amount": 250,
                "num_items": 6
            }}}

        self.expected_new_subtotal = {"count": 17, "amount": 455, "num_items": 22, "gender": {
            "F": {
                "count": 7,
                "amount": 255,
                "num_items": 17
            },
            "M": {
                "count": 10,
                "amount": 200,
                "num_items": 5
            }
        }, "currency": {
            "EUR": {
                "count": 13,
                "amount": 175,
                "num_items": 6
            },
            "GBP": {
                "count": 2,
                "amount": 30,
                "num_items": 10
            },
            "USD": {
                "count": 2,
                "amount": 250,
                "num_items": 6
            }}}

        self.added_to_new_currency = update_monthly_subtotals(self.new_currency_subtotals, self.entry_new_currency)
        self.assertEqual(self.expected_new_subtotal, self.added_to_new_currency)


if __name__ == "__main__":
    unittest.main()
