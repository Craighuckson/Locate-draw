import datetime
from sketch3 import get_date, complete_dict_from_clearsheet, handle_clear_type
FONT14 = "arial.ttf", 14

def test_get_date():
    expected_date = datetime.datetime.now().strftime("%Y-%m-%d")
    actual_date = get_date()
    assert actual_date == expected_date

def test_complete_dict_from_clearsheet():
    
    # Define test data
    clearsheet_data = {
        "current_page": "1",
        "total_pages": "10",
        "units": "feet",
        "file_name": "example.pdf",
    }
    form_data = {
        "current_page": {"text": "", "font": FONT14},
        "total_pages": {"text": "", "font": FONT14},
        "units": {"text": "", "font": FONT14},
        "file_name": {"text": "", "font": FONT14},
        "other_field": {"text": "", "font": FONT14},
    }

    # Call the function being tested
    complete_dict_from_clearsheet(clearsheet_data, form_data)

    # Check that the form data was updated correctly
    assert form_data["current_page"]["text"] == "1"
    assert form_data["total_pages"]["text"] == "10"
    assert form_data["units"]["text"] == "feet"
    assert form_data["file_name"]["text"] == "example.pdf"
    assert form_data["other_field"]["text"] == ""

def test_complete_dict_from_clearsheet_missing_key():
    # Define test data
    clearsheet_data = {
        "current_page": "1",
        "total_pages": "10",
        "file_name": "example.pdf",
    }
    form_data = {
        "current_page": {"text": "", "font": FONT14},
        "total_pages": {"text": "", "font": FONT14},
        "other_field": {"text": "", "font": FONT14},
    }

    # Call the function being tested
    complete_dict_from_clearsheet(clearsheet_data, form_data)

    # Check that the form data was updated correctly
    assert form_data["current_page"]["text"] == "1"
    assert form_data["total_pages"]["text"] == "10"
    assert form_data["other_field"]["text"] == ""

def test_complete_dict_from_clearsheet_empty_data():
    # Define test data
    clearsheet_data = {}
    form_data = {
        "current_page": {"text": "", "font": FONT14},
        "total_pages": {"text": "", "font": FONT14},
        "units": {"text": "", "font": FONT14},
        "file_name": {"text": "", "font": FONT14},
        "other_field": {"text": "", "font": FONT14},
    }

    # Call the function being tested
    complete_dict_from_clearsheet(clearsheet_data, form_data)

    # Check that the form data was updated correctly
    assert form_data["current_page"]["text"] == ""
    assert form_data["total_pages"]["text"] == ""
    assert form_data["units"]["text"] == ""
    assert form_data["file_name"]["text"] == ""
    assert form_data["other_field"]["text"] == ""

    from sketch3 import handle_clear_type

def test_handle_clear_type_msg():
    # Test that handle_clear_type returns "msg" when clear_type is between 0 and 2
    assert handle_clear_type("1") == "msg"

def test_handle_clear_type_img():
    # Test that handle_clear_type returns "img" when clear_type is not between 0 and 2
    assert handle_clear_type("2") == "img"

def test_handle_clear_type_invalid_input():
    # Test that handle_clear_type raises a ValueError when clear_type is not a valid integer
    try:
        handle_clear_type("invalid")
    except ValueError:
        pass
    else:
        assert False, "handle_clear_type did not raise ValueError for invalid input"