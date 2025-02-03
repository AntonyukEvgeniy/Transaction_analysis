from src.decorators import log_result_to_file


def test_log_result_to_file(tmp_path):
    @log_result_to_file(filename=str(tmp_path / "result.txt"))
    def test_func():
        return "test"

    result = test_func()
    assert result == "test"
    file_path = tmp_path / "result.txt"
    with open(file_path, "r") as f:
        assert f.read() == "test"
