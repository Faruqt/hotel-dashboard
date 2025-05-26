import io
import pytest
from unittest import mock
from unittest.mock import patch, MagicMock, Mock
from datetime import datetime
from fastapi import HTTPException

# local imports
from app.utils.common import (
    sanitize_filename,
    convert_string_to_datetime,
    create_pdf_from_html,
    upload_image_file,
    cleanup_image_file,
    safe_cleanup_image,
)
from app.config.settings import PDF_DIR_PATH, STATIC_DIR_PATH


@pytest.mark.parametrize(
    "title,expected",
    [
        ("My File Name", "my_file_name"),
        ("Invoice #123!", "invoice_123"),
        ("Test-File_2024", "test-file_2024"),
        (" spaces  and  symbols!@#", "spaces__and__symbols"),
        ("UPPER lower", "upper_lower"),
        ("", ""),
    ],
)
def test_sanitize_filename(title, expected):
    """Test that filenames are sanitized correctly."""
    assert sanitize_filename(title) == expected


@pytest.mark.parametrize(
    "date_string,expected",
    [
        ("2024-06-01 12:34:56.789000", datetime(2024, 6, 1, 12, 34, 56, 789000)),
        ("2024-06-01 12:34:56", datetime(2024, 6, 1, 12, 34, 56)),
    ],
)
def test_convert_string_to_datetime_valid(date_string, expected):
    """Test that valid date strings are converted correctly."""
    assert convert_string_to_datetime(date_string) == expected


@pytest.mark.parametrize(
    "date_string",
    [
        "2024/06/01 12:34:56",
        "not-a-date",
        "",
        "2024-06-01",
    ],
)
def test_convert_string_to_datetime_invalid(date_string):
    """Test that invalid date strings raise an exception."""
    with pytest.raises(Exception):
        convert_string_to_datetime(date_string)


def test_upload_image_file_success(tmp_path):
    file = Mock()
    file.filename = "test.png"
    file.file = io.BytesIO(b"fake image data")
    file.content_type = "image/png"

    with mock.patch("app.utils.common.IMAGE_DIR_PATH", str(tmp_path)):
        result = upload_image_file(file)
        assert result.endswith("_test.png")
        assert (tmp_path / result).exists()


def test_upload_image_file_no_file():
    with pytest.raises(HTTPException) as exc:
        upload_image_file(None)
    assert exc.value.status_code == 400
    assert exc.value.detail == "No file provided"


def test_upload_image_file_no_filename():
    file = Mock()
    file.filename = ""
    file.file = io.BytesIO(b"fake text data")
    file.content_type = "image/png"

    with pytest.raises(HTTPException) as exc:
        upload_image_file(file)
    assert exc.value.status_code == 400
    assert exc.value.detail == "File must have a filename"


def test_upload_image_file_not_image():
    file = Mock()
    file.filename = "test.txt"
    file.file = io.BytesIO(b"fake text data")
    file.content_type = "text/plain"

    with pytest.raises(HTTPException) as exc:
        upload_image_file(file)
    assert exc.value.status_code == 400
    assert exc.value.detail == "File must be an image"


def test_cleanup_image_file_removes_file(tmp_path):
    file_name = "to_delete.jpg"
    file_path = tmp_path / file_name
    file_path.write_bytes(b"data")

    assert file_path.exists()
    with mock.patch("app.utils.common.IMAGE_DIR_PATH", str(tmp_path)):
        cleanup_image_file(file_name)
        assert not file_path.exists()


def test_cleanup_image_file_file_not_exists(tmp_path):
    file_name = "not_exists.jpg"
    with mock.patch("app.utils.common.IMAGE_DIR_PATH", str(tmp_path)):
        # Should not raise
        cleanup_image_file(file_name)


def test_safe_cleanup_image_handles_exception():
    with mock.patch(
        "app.utils.common.cleanup_image_file", side_effect=Exception("fail")
    ):
        # Should not raise
        safe_cleanup_image("fail.jpg")


def test_create_pdf_from_html_success():
    """Test successful PDF creation."""
    with patch("app.utils.common.HTML") as mock_html_class, patch(
        "app.utils.common.os.makedirs"
    ) as mock_makedirs, patch("app.utils.common.os.path.join") as mock_join, patch(
        "app.utils.common.sanitize_filename"
    ) as mock_sanitize:

        # Setup mocks
        mock_html_instance = MagicMock()
        mock_html_class.return_value = mock_html_instance
        mock_sanitize.return_value = "sanitized_name"
        mock_join.return_value = "/path/to/sanitized_name.pdf"

        # Execute
        result = create_pdf_from_html("Test PDF", "<html>content</html>", "test_caller")

        # Assertions
        assert result == "sanitized_name.pdf"
        mock_makedirs.assert_called_once_with(PDF_DIR_PATH, exist_ok=True)
        mock_sanitize.assert_called_once_with("Test PDF")
        mock_html_class.assert_called_once_with(
            string="<html>content</html>", base_url=STATIC_DIR_PATH
        )
        mock_html_instance.write_pdf.assert_called_once_with(
            "/path/to/sanitized_name.pdf"
        )


def test_create_pdf_from_html_exception_handling():
    """Test exception handling during PDF creation."""
    with patch("app.utils.common.HTML") as mock_html_class, patch(
        "app.utils.common.os.makedirs"
    ), patch("app.utils.common.sanitize_filename", return_value="test"):

        # Setup HTML to raise exception
        mock_html_instance = MagicMock()
        mock_html_instance.write_pdf.side_effect = Exception("PDF write failed")
        mock_html_class.return_value = mock_html_instance

        # Test exception is raised
        with pytest.raises(Exception, match="PDF write failed"):
            create_pdf_from_html("test", "<html>test</html>", "test_caller")
