from core.utils import file_utils


# ========== compute_checksum ==========

def test_compute_checksum_from_str():
    text = "hello world"
    checksum = file_utils.compute_checksum(text)
    assert isinstance(checksum, str)
    assert checksum == "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"  # SHA256


def test_compute_checksum_from_bytes():
    b = b"hello world"
    result = file_utils.compute_checksum(b, algo="md5")
    assert result == "5eb63bbbe01eeed093cb22bb8f5acdc3"


# ========== write_text / read_text_lines ==========

def test_write_and_read_text_lines(tmp_path):
    test_file = tmp_path / "test.txt"
    text = "linha 1\nlinha 2\nlinha 3"
    file_utils.write_text(test_file, text)

    lines = file_utils.read_text_lines(test_file)
    assert lines == ["linha 1", "linha 2", "linha 3"]


# ========== save_json / load_json ==========

def test_save_and_load_json(tmp_path):
    data = {"nome": "Ye Hong", "nivel": 10}
    path = tmp_path / "data" / "user.json"
    file_utils.save_json(path, data)

    loaded = file_utils.load_json(path)
    assert isinstance(loaded, dict)
    assert loaded["nome"] == "Ye Hong"
    assert loaded["nivel"] == 10


# ========== write_text with auto mkdir ==========

def test_write_text_creates_directories(tmp_path):
    nested_file = tmp_path / "a" / "b" / "c.txt"
    file_utils.write_text(nested_file, "teste")
    assert nested_file.exists()
    assert nested_file.read_text(encoding="utf-8") == "teste"
