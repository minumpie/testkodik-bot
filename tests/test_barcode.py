import pytest
from bot import generate_barcode_png
from io import BytesIO

def test_generate_barcode_returns_bytesio():
    buffer = generate_barcode_png("123456")
    assert isinstance(buffer, BytesIO)
    assert buffer.getbuffer().nbytes > 0  # файл не пустой

def test_generate_barcode_with_invalid_input():
    with pytest.raises(Exception):
        generate_barcode_png("")  # пустой номер невалидный
