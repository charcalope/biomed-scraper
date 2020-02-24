from diagnosis_extraction import get_drug_bank_id, drug_scraper
import pickle

def failure_percentage():
    drug_file = 'data/drug_list_txts/master_drug_list.txt'
    with open(drug_file, 'r') as f:
        lines = f.readlines()

    good_lines = []
    for line in lines:
        good_lines.append(line.strip())

    failure_cases = []

    angel_lines = []

    sample_data = good_lines
    for line in sample_data:
        try:
            get_drug_bank_id(line)
            angel_lines.append(line)
        except:
            failure_cases.append(line)

    fails = len(failure_cases)
    fail_rate = fails / len(good_lines)
    print(1 - fail_rate)

    with open('data/testing_data/parsing_tests/initial_failure_cases.txt', 'w') as f:
        for failure in failure_cases:
            print(failure, file=f)

    # all drugs that pass to drug bank
    with open('data/testing_data/parsing_tests/true_positives.txt', 'w') as f2:
        for angel in angel_lines:
            print(angel, file=f2)

def apply_scraper():
    with open('data/testing_data/parsing_tests/true_positives.txt', 'r') as f:
        lines = f.readlines()

    goodlines = []
    for line in lines:
        goodlines.append(line.strip())

    failure_cases = []
    drug_dicts = []
    for line in goodlines:
        try:
            drug_dicts.append(drug_scraper(line))
        except:
            failure_cases.append(line)

    with open('drug_dictionaries.pickle', 'wb') as f:
        pickle.dump(drug_dicts, f)

    print(failure_cases)

def load_picked():
    with open('drug_dictionaries.pickle', 'rb') as f:
        dicts = pickle.load(f)

    result = dicts[0]
    print(result)

load_picked()