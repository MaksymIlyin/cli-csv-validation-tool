from datetime import datetime, timedelta

import pytest

import src.validation as m


# ----------------------------
# check_input_file
# ----------------------------

def test_check_input_file_exists(monkeypatch):
    monkeypatch.setattr(m.os.path, "isfile", lambda path: True)
    m.check_input_file("input.csv")  # should not raise


def test_check_input_file_missing_exits(monkeypatch):
    monkeypatch.setattr(m.os.path, "isfile", lambda path: False)

    with pytest.raises(SystemExit) as exc:
        m.check_input_file("missing.csv")

    assert exc.value.code == 0


# ----------------------------
# check_headers
# ----------------------------

def test_check_headers_valid(monkeypatch):
    monkeypatch.setattr(m, "input_schema", ["id", "category", "amount", "created_at"])
    headers = ["id", "category", "amount", "created_at"]

    m.check_headers(headers)


def test_check_headers_valid_different_order(monkeypatch):
    monkeypatch.setattr(m, "input_schema", ["id", "category", "amount", "created_at"])
    headers = ["id", "category", "amount", "created_at"][::-1]

    m.check_headers(headers)


def test_check_headers_wrong_length_exits(monkeypatch):
    monkeypatch.setattr(m, "input_schema", ["id", "category", "amount", "created_at"])
    headers = ["id", "category"]

    with pytest.raises(SystemExit) as exc:
        m.check_headers(headers)

    assert exc.value.code == 0


def test_check_headers_missing_required_column_exits(monkeypatch):
    monkeypatch.setattr(m, "input_schema", ["id", "category", "amount", "created_at"])
    headers = ["id", "category", "amount", "other_column"]

    with pytest.raises(SystemExit) as exc:
        m.check_headers(headers)

    assert exc.value.code == 0


# ----------------------------
# check_output_folder
# ----------------------------

def test_check_output_folder_existing(monkeypatch):
    monkeypatch.setattr(m.os.path, "dirname", lambda path: "/tmp/output")
    monkeypatch.setattr(m.os.path, "isdir", lambda path: True)

    called = {"makedirs": False}

    def fake_makedirs(path):
        called["makedirs"] = True

    monkeypatch.setattr(m.os, "makedirs", fake_makedirs)

    m.check_output_folder("/tmp/output/file.csv")

    assert called["makedirs"] is False


def test_check_output_folder_creates_missing_folder(monkeypatch):
    monkeypatch.setattr(m.os.path, "dirname", lambda path: "/tmp/output")
    monkeypatch.setattr(m.os.path, "isdir", lambda path: False)

    created = {}

    def fake_makedirs(path):
        created["path"] = path

    monkeypatch.setattr(m.os, "makedirs", fake_makedirs)

    m.check_output_folder("/tmp/output/file.csv")

    assert created["path"] == "/tmp/output"


# ----------------------------
# is_valid_id
# ----------------------------

def test_is_valid_id_valid():
    assert m.is_valid_id("123", 1) is True


def test_is_valid_id_invalid():
    assert m.is_valid_id("12a", 1) is False


# ----------------------------
# is_valid_category
# ----------------------------

def test_is_valid_category_valid(monkeypatch):
    monkeypatch.setattr(m, "categories", ["food", "travel", "books"])
    assert m.is_valid_category("food", 2) is True


def test_is_valid_category_invalid(monkeypatch):
    monkeypatch.setattr(m, "categories", ["food", "travel", "books"])
    assert m.is_valid_category("cars", 2) is False


# ----------------------------
# is_valid_amount
# ----------------------------

def test_is_valid_amount_valid():
    assert m.is_valid_amount("12.34", 3) is True


def test_is_valid_amount_not_float():
    assert m.is_valid_amount("abc", 3) is False


def test_is_valid_amount_wrong_decimal_places_one_digit():
    assert m.is_valid_amount("12.3", 3) is False


def test_is_valid_amount_wrong_decimal_places_no_decimal_part():
    assert m.is_valid_amount("12", 3) is False


def test_is_valid_amount_wrong_decimal_places_no_integral_part():
    assert m.is_valid_amount(".12", 3) is False


def test_is_valid_amount_wrong_decimal_places_three_digits():
    assert m.is_valid_amount("12.345", 3) is False


# ----------------------------
# is_valid_created_at
# ----------------------------

def test_is_valid_created_at_valid():
    past = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d-%H:%M:%S")
    assert m.is_valid_created_at(past, 4) is True


def test_is_valid_created_at_wrong_format():
    assert m.is_valid_created_at("2026/01/01 10:00:00", 4) is False


def test_is_valid_created_at_corrupted_format():
    assert m.is_valid_created_at("2026-44-01-10:00:00", 4) is False


def test_is_valid_created_at_future():
    future = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d-%H:%M:%S")
    assert m.is_valid_created_at(future, 4) is False


# ----------------------------
# is_valid_status
# ----------------------------

def test_is_valid_status_correct_status():
    assert m.is_valid_status("active", 5) is True


def test_is_valid_status_incorrect_status():
    # This test documents the CURRENT buggy behavior
    assert m.is_valid_status("unknown", 5) is False


# ----------------------------
# is_valid_row
# ----------------------------

def test_is_valid_row_none_value():
    row = {
        "id": None,
        "category": "food",
        "amount": "12.34",
        "created_at": "2025-01-01-10:00:00",
    }
    assert m.is_valid_row(row, 10) is False


def test_is_valid_row_empty_string():
    row = {
        "id": "",
        "category": "food",
        "amount": "12.34",
        "created_at": "2025-01-01-10:00:00",
    }
    assert m.is_valid_row(row, 10) is False


def test_is_valid_row_invalid_id(monkeypatch):
    row = {
        "id": "abc",
        "category": "food",
        "amount": "12.34",
        "created_at": "2025-01-01-10:00:00",
    }
    monkeypatch.setattr(m, "categories", ["food", "travel"])
    assert m.is_valid_row(row, 10) is False


def test_is_valid_row_invalid_category(monkeypatch):
    row = {
        "id": "1",
        "category": "cars",
        "amount": "12.34",
        "created_at": "2025-01-01-10:00:00",
    }
    monkeypatch.setattr(m, "categories", ["food", "travel"])
    assert m.is_valid_row(row, 10) is False


def test_is_valid_row_invalid_amount(monkeypatch):
    row = {
        "id": "1",
        "category": "food",
        "amount": "12.3",
        "created_at": "2025-01-01-10:00:00",
    }
    monkeypatch.setattr(m, "categories", ["food", "travel"])
    assert m.is_valid_row(row, 10) is False


def test_is_valid_row_invalid_created_at(monkeypatch):
    row = {
        "id": "1",
        "category": "food",
        "amount": "12.34",
        "created_at": "bad-date",
    }
    monkeypatch.setattr(m, "categories", ["food", "travel"])
    assert m.is_valid_row(row, 10) is False


def test_is_valid_row_valid(monkeypatch):
    row = {
        "id": "1",
        "category": "food",
        "amount": "12.34",
        "created_at": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d-%H:%M:%S"),
    }
    monkeypatch.setattr(m, "categories", ["food", "travel"])
    assert m.is_valid_row(row, 10) is True
