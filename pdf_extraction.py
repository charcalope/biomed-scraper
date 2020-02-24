from tika import parser
import re
import spacy

# NOTE: en_ner_bionlp13cg has highest chemical recognition


def pdf2txt(file, destination):
    """ from a pdf drug list, writes a txt file of drugs"""

    def pdf2string(file):
        # parse text from pdf
        raw = parser.from_file(file)
        test = raw['content']
        # find words in content using regex
        matches = re.findall(r'(\w+)', test)
        # concatenate to single string, use '/' as marker for strings containing multiple drugs
        big_string = ' / '.join(matches)
        return big_string


    def extract_drugs(text):
        """ Extracts """
        drugs = []
        # load model
        nlp = spacy.load('en_ner_bionlp13cg_md')

        # filter chemicals only
        doc = nlp(text)
        for x in doc.ents:
            label = x.label_
            text2 = x.text

            if label == 'SIMPLE_CHEMICAL':
                drugs.append(text2)

        # filter strings with multiple words in it
        bad_drugs = []
        good_drugs = []
        for drug in drugs:
            if '/' in drug:
                bad_drugs.append(drug)
            else:
                good_drugs.append(drug)

        # split multi-word strings and rerun drug identification on each word
        for bad_drug in bad_drugs:
            candidates = bad_drug.split()
            for word in candidates:
                doc = nlp(word)
                if any(doc.ents):
                    drug_found = doc.ents[0]
                    good_drugs.append(drug_found.text)

        # unique drug names only
        drug_set = set(good_drugs)

        return drug_set

    big_string = pdf2string(file)
    drugs = extract_drugs(big_string)

    with open(destination, 'w') as f:
        for drug in drugs:
            print(drug, file=f)


def master_drug_list(filename_list, destination):
    def txt2set(file):
        good_lines = set()
        with open(file, 'r') as f:
            lines = f.readlines()

        for line in lines:
            good_lines.add(line.strip())

        return good_lines

    master_set = set()
    for name in filename_list:
        for item in txt2set(name):
            master_set.add(item)

    print(master_set)

    with open(destination, 'w') as f2:
        for x in master_set:
            print(x, file=f2)