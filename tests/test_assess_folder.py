"""One folder of photos in, one honest report out.

The proof ran only over cached test sets, so a real photo from the business
could not be put through the engine. A folder is the smallest input that a
capture page, a WhatsApp handler or a person at a desk can all produce.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image

from buyscape.cli import load_folder_case


def _jpg(path: Path) -> None:
    Image.new("RGB", (64, 48), (120, 120, 120)).save(path, format="JPEG")


def test_folder_becomes_a_case(tmp_path: Path):
    _jpg(tmp_path / "IMG_0002.jpg")
    _jpg(tmp_path / "IMG_0001.JPG")
    (tmp_path / "seller.txt").write_text("phone stand, not working\n")
    (tmp_path / "answers.yaml").write_text("weight_kg: 0.3\nworks: no\n")
    (tmp_path / "notes.docx").write_bytes(b"not an image")

    case = load_folder_case(tmp_path, asking=500)
    assert case.id == tmp_path.name
    assert [p.name for p in case.images] == ["IMG_0001.JPG", "IMG_0002.jpg"]
    assert case.seller_text == "phone stand, not working"
    assert case.answers == {"weight_kg": "0.3", "works": "no"}
    assert case.asking_price == 500.0
    assert case.truth == {}


def test_words_on_the_command_line_join_the_file(tmp_path: Path):
    _jpg(tmp_path / "a.png")
    (tmp_path / "seller.txt").write_text("old stand")
    case = load_folder_case(tmp_path, text="base is heavy")
    assert case.seller_text == "old stand\nbase is heavy"


def test_heic_is_converted_once_and_the_jpeg_is_used(tmp_path: Path):
    import pillow_heif

    pillow_heif.register_heif_opener()
    Image.new("RGB", (64, 48), (10, 200, 10)).save(tmp_path / "IMG_9.HEIC", format="HEIF")
    case = load_folder_case(tmp_path)
    assert [p.name for p in case.images] == ["IMG_9.jpg"]
    assert (tmp_path / "IMG_9.jpg").exists()
    again = load_folder_case(tmp_path)
    assert [p.name for p in again.images] == ["IMG_9.jpg"]


def test_empty_folder_is_a_loud_error(tmp_path: Path):
    import pytest

    with pytest.raises(FileNotFoundError, match="no photos"):
        load_folder_case(tmp_path)
