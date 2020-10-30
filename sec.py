import os
import re


def get_10K_doc(cik, year, quarter):
    """
    Get the 10-K annual filing for a given company CIK for a given year
    from all filings already downloaded
    """
    txt_doc = ""
    src = r"\Users\diyan\Documents\SEC_DATA\\" + str(year) + r"\\" + quarter
    search_str = "10-K_edgar_data_" + str(int(cik))

    src_dir = os.listdir(src)

    for src_file in src_dir:
        if os.path.isfile(src + os.sep + src_file):
            if search_str in src_file:
                with open(src + os.sep + src_file, "r") as f:
                    txt_doc = f.read()
    return txt_doc


def parse_10K_doc(txt_doc):
    """
    Parse the text 10-K document using the re library
    """
    return re.sub(r'[^\x00-\x7F]+', ' ', txt_doc.replace('\n', ''))


def pull_risk_section(text):
    """
    Extract the Risk Section (Item 1A.) from the annual 10-K document
    """
    result = " "
    matches = list(re.finditer(re.compile('Item [0-9][A-Z]*\.', re.IGNORECASE), text))

    end_idx = [i for i in range(len(matches)) if matches[i][0].lower() == 'Item 2.'.lower()]
    if len(end_idx) == 0:
        return result
    else:
        end = max(end_idx)

    start_idx = [i for i in range(len(matches)) if matches[i][0].lower() == 'Item 1A.'.lower() and i < end]
    if len(start_idx) == 0:
        return result
    else:
        start = max(start_idx)

    start = matches[start].span()[1]
    end = matches[end].span()[0]

    return text[start:end]


if __name__ == '__main__':
    quarters = ['QTR1', 'QTR2', 'QTR3', 'QTR4']
    symbol = 'MSFT'
    cik = '0000789019'
    year = 2015
    for qtr in quarters:
        doc = get_10K_doc(cik, year, qtr)
        if len(doc) > 0:
            rsk_doc = pull_risk_section(parse_10K_doc(doc))
            print(qtr, rsk_doc[:100])
            break

