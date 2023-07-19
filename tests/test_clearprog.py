import datetime
from sketch3 import get_date

def test_get_date():
    expected_date = datetime.datetime.now().strftime("%Y-%m-%d")
    actual_date = get_date()
    assert actual_date == expected_date

