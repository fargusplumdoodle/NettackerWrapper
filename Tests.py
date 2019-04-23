import time
import subprocess
from AbstractTool import DummyTool


def test_regular_conditions():
    cmd = "echo -n foo"  # -n means no newline
    to = 10
    x = DummyTool(run_command=cmd, timeout=to)
    x.start()
    while not x.finished:
        time.sleep(0.1)

    assert x.raw_output == "foo"  # regular conditions failed


def test_timeout():
    # timeout is 1, command waits for longer than that
    cmd = "sleep 4"
    to = 1
    x = DummyTool(run_command=cmd, timeout=to)
    passed = False
    try:
        x.start()
    except subprocess.TimeoutExpired:
        passed = True

    assert passed  # tool did not timeout


if __name__ == '__main__':
    test_regular_conditions()
    test_timeout()

    print("\nTests Completed Successfully\n")
