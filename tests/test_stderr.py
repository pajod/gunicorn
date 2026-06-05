import sys

def test_stdout(capsys):
    print("hello")
    print("world", file=sys.stderr)
    captured = capsys.readouterr()
    assert captured.out == "hello\n"
    assert captured.err == "world\n"
