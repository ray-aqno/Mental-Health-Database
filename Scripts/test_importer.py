"""
Tests for importer.py payload builders and data loading.

Run with: pytest test_importer.py -v
"""

import json
import os
import tempfile

import pytest
from importer import build_resource_payload, build_college_payload, load_data_file


# ===== build_resource_payload =====

class TestBuildResourcePayload:
    def test_full_resource(self):
        data = {
            "service_name": "CAPS",
            "description": "Counseling services",
            "contact_email": "caps@osu.edu",
            "contact_phone": "(614) 292-5766",
            "contact_website": "https://ccs.osu.edu",
            "department": "Student Life",
            "office_hours": "Monday-Friday 8-5",
            "location": "4th Floor",
            "freshman_notes": "Free for freshmen",
        }
        result = build_resource_payload(data, college_id=42)

        assert result["collegeId"] == 42
        assert result["serviceName"] == "CAPS"
        assert result["description"] == "Counseling services"
        assert result["contactEmail"] == "caps@osu.edu"
        assert result["contactPhone"] == "(614) 292-5766"
        assert result["contactWebsite"] == "https://ccs.osu.edu"
        assert result["department"] == "Student Life"
        assert result["officeHours"] == "Monday-Friday 8-5"
        assert result["location"] == "4th Floor"
        assert result["freshmanNotes"] == "Free for freshmen"

    def test_empty_resource_uses_defaults(self):
        result = build_resource_payload({})
        assert result["collegeId"] == 0
        assert result["serviceName"] == "Counseling Services"
        assert result["description"] == ""
        assert result["contactEmail"] == ""

    def test_partial_resource(self):
        data = {"service_name": "Wellness", "contact_phone": "555-1234"}
        result = build_resource_payload(data, college_id=10)
        assert result["serviceName"] == "Wellness"
        assert result["contactPhone"] == "555-1234"
        assert result["contactEmail"] == ""
        assert result["collegeId"] == 10

    def test_missing_keys_dont_raise(self):
        # Should not raise KeyError for any missing field
        result = build_resource_payload({"unrelated_key": "value"})
        assert result["serviceName"] == "Counseling Services"


# ===== build_college_payload =====

class TestBuildCollegePayload:
    def test_full_college(self):
        data = {
            "name": "Ohio State University",
            "location": "Columbus, Ohio",
            "latitude": 40.0067,
            "longitude": -83.0305,
            "website": "https://www.osu.edu",
            "resources": [
                {"service_name": "CAPS", "contact_email": "caps@osu.edu"},
            ],
        }
        result = build_college_payload(data)

        assert result["name"] == "Ohio State University"
        assert result["location"] == "Columbus, Ohio"
        assert result["latitude"] == 40.0067
        assert result["longitude"] == -83.0305
        assert result["website"] == "https://www.osu.edu"
        assert len(result["resources"]) == 1
        assert result["resources"][0]["serviceName"] == "CAPS"

    def test_college_no_resources(self):
        data = {
            "name": "Test University",
            "location": "Test, Ohio",
            "latitude": 40.0,
            "longitude": -83.0,
            "website": "https://test.edu",
        }
        result = build_college_payload(data)
        assert result["resources"] == []

    def test_college_multiple_resources(self):
        data = {
            "name": "Test University",
            "location": "Test, Ohio",
            "latitude": 40.0,
            "longitude": -83.0,
            "website": "https://test.edu",
            "resources": [
                {"service_name": "CAPS"},
                {"service_name": "Wellness Center"},
                {"service_name": "Crisis Line"},
            ],
        }
        result = build_college_payload(data)
        assert len(result["resources"]) == 3

    def test_missing_fields_return_none(self):
        result = build_college_payload({})
        assert result["name"] is None
        assert result["resources"] == []


# ===== load_data_file =====

class TestLoadDataFile:
    def test_valid_json_file(self):
        data = [{"name": "Test U", "location": "Test, OH"}]
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump(data, f)
            f.flush()
            path = f.name

        try:
            result = load_data_file(path)
            assert len(result) == 1
            assert result[0]["name"] == "Test U"
        finally:
            os.unlink(path)

    def test_file_not_found(self):
        with pytest.raises(SystemExit):
            load_data_file("nonexistent_file_12345.json")

    def test_invalid_json(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            f.write("{not valid json")
            f.flush()
            path = f.name

        try:
            with pytest.raises(SystemExit):
                load_data_file(path)
        finally:
            os.unlink(path)

    def test_json_not_array(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump({"name": "not an array"}, f)
            f.flush()
            path = f.name

        try:
            with pytest.raises(SystemExit):
                load_data_file(path)
        finally:
            os.unlink(path)

    def test_empty_array(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump([], f)
            f.flush()
            path = f.name

        try:
            with pytest.raises(SystemExit):
                load_data_file(path)
        finally:
            os.unlink(path)
