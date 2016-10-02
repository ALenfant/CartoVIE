from datetime import datetime
import re
import dateparser

__author__ = 'antonin'


NUMERIC_FIELDS = ('duration_months', 'jobs_availables', 'required_exerience_months')
FLAGS_FIELDS = ('required_education_level', 'required_education_type', 'required_languages', 'required_skills')


def clean_val(val):
    if isinstance(val, (int, datetime, list)) or val is None:
        return val  # Nothing to do
    elif isinstance(val, str):
        return val.strip()
    else:
        raise Exception("Type %s not managed! (%s)" % (type(val), val))


def clean_dict(dict):
    for key, val in dict.items():
        if key.endswith("_date"):
            val = parse_fr_date(val)
        if key in FLAGS_FIELDS:
            val = list(map(lambda x: x.strip(), val.split(" , ")))
        if key in NUMERIC_FIELDS:
            val = int(val)
        elif key == "salary":
            match = re.search('(\d+)€', val)
            val = int(match.group(1)) if match else None  # Sometimes the salary is "-"
        dict[key] = clean_val(val)


def parse_fr_date(fr_date_string):
    dt = dateparser.parse(fr_date_string, date_formats=['%d %B %Y'], languages=['fr'])
    if dt:
        print(fr_date_string, "=>", dt)
        return dt
    else:
        raise Exception("Impossible to parse date " + str(fr_date_string))
