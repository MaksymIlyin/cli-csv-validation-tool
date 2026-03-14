import logging

from src.data_manipulation import get_valid_data, group_data


def test_get_valid_data_returns_only_valid_rows(monkeypatch, caplog):
    raw_data = [
        {"id": "1", "category": "books", "amount": "10.00"},
        {"id": "2", "category": "food", "amount": "20.00"},
        {"id": "bad", "category": "games", "amount": "5.00"},
    ]

    validation_results = [True, False, True]

    def fake_is_valid_row(row, row_number):
        return validation_results[row_number - 1]

    monkeypatch.setattr("src.data_manipulation.is_valid_row", fake_is_valid_row)

    with caplog.at_level(logging.INFO):
        result = get_valid_data(raw_data)

    assert result == [
        {"id": "1", "category": "books", "amount": "10.00"},
        {"id": "bad", "category": "games", "amount": "5.00"},
    ]
    assert "Valid rows 2" in caplog.text
    assert "Invalid rows 1" in caplog.text


def test_get_valid_data_returns_empty_list_when_all_rows_invalid(monkeypatch, caplog):
    raw_data = [
        {"id": "1", "category": "books", "amount": "10.00"},
        {"id": "2", "category": "food", "amount": "20.00"},
    ]

    def fake_is_valid_row(row, row_number):
        return False

    monkeypatch.setattr("src.data_manipulation.is_valid_row", fake_is_valid_row)

    with caplog.at_level(logging.INFO):
        result = get_valid_data(raw_data)

    assert result == []
    assert "Valid rows 0" in caplog.text
    assert "Invalid rows 2" in caplog.text


def test_group_data_aggregates_rows_by_category(monkeypatch):
    fake_categories = ["books", "food"]

    monkeypatch.setattr("src.data_manipulation.categories", fake_categories)

    data = [
        {"category": "books", "amount": "10.00"},
        {"category": "books", "amount": "15.50"},
        {"category": "food", "amount": "20.00"},
    ]

    result = group_data(data)

    assert result == [
        {
            "category": "books",
            "row_count": 2,
            "total_amount": "25.50",
            "average_amount": "12.75",
        },
        {
            "category": "food",
            "row_count": 1,
            "total_amount": "20.00",
            "average_amount": "20.00",
        },
    ]


def test_group_data_rounds_values_correctly(monkeypatch):
    fake_categories = ["books"]

    monkeypatch.setattr("src.data_manipulation.categories", fake_categories)

    data = [
        {"category": "books", "amount": "10.55"},
        {"category": "books", "amount": "1.23"},
    ]

    result = group_data(data)

    assert result == [
        {
            "category": "books",
            "row_count": 2,
            "total_amount": "11.78",
            "average_amount": "5.89",
        }
    ]


def test_group_data_ignores_rows_from_categories_not_in_categories_list(monkeypatch):
    fake_categories = ["books"]

    monkeypatch.setattr("src.data_manipulation.categories", fake_categories)

    data = [
        {"category": "books", "amount": "10.00"},
        {"category": "music", "amount": "99.99"},
    ]

    result = group_data(data)

    assert result == [
        {
            "category": "books",
            "row_count": 1,
            "total_amount": "10.00",
            "average_amount": "10.00",
        }
    ]


def test_group_data_returns_zero_values_when_category_has_no_rows(monkeypatch):
    fake_categories = ["books", "food"]

    monkeypatch.setattr("src.data_manipulation.categories", fake_categories)

    data = [
        {"category": "books", "amount": "10.00"},
    ]

    result = group_data(data)

    assert result == [
        {
            "category": "books",
            "row_count": 1,
            "total_amount": "10.00",
            "average_amount": "10.00",
        },
        {
            "category": "food",
            "row_count": 0,
            "total_amount": "0.00",
            "average_amount": "0.00",
        },
    ]
