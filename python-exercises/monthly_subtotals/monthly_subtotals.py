from collections import defaultdict


def nested_entry(key, subtot, ent):
    """ helper function """
    nested_key = ent[key]
    subtot[key][nested_key]['amount'] += ent['amount']
    subtot[key][nested_key]['num_items'] += ent['num_items']
    subtot[key][nested_key]['count'] += 1
    return subtot


def update_monthly_subtotals(subtotals, entry):
    """ takes in a current subtotals dictionary and a dictionary of key-value pairs for new entries """
    req_keys = ['amount', 'num_items', 'gender', 'currency']
    try:
        subtotals = defaultdict(str, subtotals)
        subtotals['count'] += 1
        subtotals['amount'] += entry['amount']
        subtotals['num_items'] += entry['num_items']
        nested_entry('gender', subtotals, entry)
        if entry['currency'] not in subtotals['currency'].keys():
            subtotals = defaultdict(lambda: defaultdict(dict), subtotals)
            subtotals['currency'][entry['currency']] = {'amount': 0, 'count': 0, 'num_items': 0}
        for k, v in entry.items():
            if k not in req_keys + ['count']:
                subtotals[k] = v
        nested_entry('currency', subtotals, entry)
    except KeyError:
        print('Entry must include {}, {}, {} and {}'.format(*req_keys))
        return
    return dict(subtotals)

new_entry = {"gender": "M", "amount": 17.0, "num_items": 2, "currency": "EUR"}

new_currency_entry = {"gender": "F", "amount": 15.0, "num_items": 5, "currency": "GBP"}

oct_subtotals = {"count": 15, "amount": 425, "num_items": 12, "gender": {
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
