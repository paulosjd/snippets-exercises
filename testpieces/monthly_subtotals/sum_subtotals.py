from collections import defaultdict
import pprint


def sum_nested_dicts(dct, m_subs, dct_key):
    """ helper function """
    for i in m_subs:
        for k, v in i[dct_key].items():
            for key, value in i[dct_key][k].items():
                try:
                    dct[dct_key][k][key] += value
                except KeyError:
                    dct[dct_key][k][key] = 0
                    dct[dct_key][k][key] += value
    return dct


def sum_monthly_subtotals(m_subtotals):
    """ takes in a list of dictionaries of monthly subtotals and returns a dictionary of summed monthly subtotals.
        output test using pprint() is as expected, but attempt to write test for failed due to defaultdict? """
    d = defaultdict(int)
    for i in m_subtotals:
        for k, v in i.items():
            if type(v) == int:
                d[k] += v
    nested_dct = defaultdict(lambda: defaultdict(dict), d)
    nested_keys = ['gender', 'currency']
    for i in nested_keys:
        sum_nested_dicts(nested_dct, m_subtotals, i)
    return dict(nested_dct)


oct = {
    "count": 15,
    "amount": 425,
    "num_items": 12,
    "gender": {
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
    },
    "currency": {
        "EUR": {
            "count": 13,
            "amount": 175,
            "num_items": 6
        },
        "USD": {
            "count": 2,
            "amount": 250,
            "num_items": 6
        }
    }
}

nov = {
    "count": 2,
    "amount": 25,
    "num_items": 2,
    "gender": {
        "F": {
            "count": 1,
            "amount": 15,
            "num_items": 1
        },
        "M": {
            "count": 1,
            "amount": 10,
            "num_items": 1
        }
    },
    "currency": {
        "EUR": {
            "count": 1,
            "amount": 15,
            "num_items": 1
        },
        "USD": {
            "count": 1,
            "amount": 10,
            "num_items": 1
        }
    }
}

pprint.pprint(sum_monthly_subtotals([oct, nov]))