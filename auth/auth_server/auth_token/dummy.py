import random
import string


class DummyToken(object):

    def __init__(self, length=150):
        self.len = length

    def create(self):
        return ''.join(random.choice(string.ascii_uppercase + string.digits)
                       for _ in range(self.len))

#REGEX_AWS_REPORT_FORMAT = 'data/BILLING_PERIOD=[0-9]{{4}}-[0-9]{{2}}'
#REGEX_AWS_REPORT_GROUP = 'BILLING_PERIOD=[0-9]{4}-[0-9]{2}'
#REGEX_AWS_REPORT_FORMAT_CSV_LEGACY = '[0-9]{{8}}-[0-9]{{8}}(/[0-9]{{8}}T[0-9]{{6}}Z)?'
#REGEX_AWS_REPORT_GROUP_CSV_LEGACY = '[0-9]{8}-[0-9]{8}'
#REGEX_AWS_REPORT_FORMAT_PARQUET_LEGACY = '{1}/year=[0-9]{{4}}/month=([1-9]|1[0-2])'
#REGEX_AWS_REPORT_GROUP_PARQUET_LEGACY = 'year=[0-9]{4}/month=([1-9]|1[0-2])/'

