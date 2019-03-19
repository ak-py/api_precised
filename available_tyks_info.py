tyk_info = [
    {'id': '101', 'title': 'Pricing - High', 'avg_accuracy': '91%',
        'format': '6 - 3 Pros & 3 Cons', 'status': 'OK'},
    {'id': '102', 'title': 'Pricing - Low', 'avg_accuracy': '91%',
        'format': '6 - 3 Pros & 3 Cons', 'status': 'OK'},
    {'id': '103', 'title': 'Accounting - Cash', 'avg_accuracy': '94%',
        'format': '2 - 1 Pros & 1 Cons', 'status': 'OK'},
    {'id': '104', 'title': 'Accounting - Accrual', 'avg_accuracy': '94%',
        'format': '2 - 1 Pros & 1 Cons', 'status': 'OK'},
    {'id': '105', 'title': 'Location - Mid-Town', 'avg_accuracy': '92%',
        'format': '6 - 3 Pros & 3 Cons', 'status': 'OK'},
    {'id': '106', 'title': 'Location - North-End', 'avg_accuracy': '95%',
        'format': '6 - 3 Pros & 3 Cons', 'status': 'OK'},
    {'id': '107', 'title': 'Location - Strip Mall', 'avg_accuracy': '89%',
        'format': '6 - 3 Pros & 3 Cons', 'status': 'OK'},
    {'id': '108', 'title': 'Over-Ripe Tomatoes - BUYING', 'avg_accuracy': '90%',
        'format': '2 - 1 Pros & 1 Cons', 'status': 'OK'},
    {'id': '109', 'title': 'Over-Ripe Tomatoes - NOT BUYING',
        'avg_accuracy': '90%', 'format': '2 - 1 Pros & 1 Cons', 'status': 'OK'},
    {'id': '110', 'title': 'Uniform - PROVIDE', 'avg_accuracy': '84%',
        'format': '2 - 1 Pros & 1 Cons', 'status': 'OK'},
    {'id': '111', 'title': 'Uniform - NOT PROVIDE', 'avg_accuracy': '82%',
        'format': '2 - 1 Pros & 1 Cons', 'status': 'OK'},
]

tyk_ids = [tyk['id'] for tyk in tyk_info]
tyk_ids_format_six = [tyk['id']
                      for tyk in tyk_info if tyk['format'] == '6 - 3 Pros & 3 Cons']
tyk_ids_format_two = [tyk['id']
                      for tyk in tyk_info if tyk['format'] == '2 - 1 Pros & 1 Cons']
