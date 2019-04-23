import time
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
    x.start()

    while not x.finished:
        time.sleep(0.1)

    assert x.failed  # tool did not timeout


def test_terminate():
    # timeout is 1, command waits for longer than that
    cmd = "sleep 9"
    to = 10
    x = DummyTool(run_command=cmd, timeout=to)
    x.start()

    time.sleep(1)  # giving time for internal gears to turn
    x.terminate()
    assert x.failed  # we do want it to have failed
    assert x.stderr == "terminated"  # insert schwarzenegger reference here


if __name__ == '__main__':
    # Execute Tool tests
    test_regular_conditions()
    test_timeout()

    # terminate tests
    test_terminate()
    print("\nTests Completed Successfully\n")
