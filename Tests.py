import time
from AbstractTool import DummyTool
from NettackerTool import NettackerTool


# abstract tool
def test_regular_conditions():
    cmd = "echo -n foo"  # -n means no newline
    to = 10
    x = DummyTool(run_command=cmd, timeout=to)
    x.start()
    while not x.finished:
        time.sleep(0.1)

    assert x.raw_output == "foo"  # regular conditions failed


# abstract tool
def test_timeout():
    # timeout is 1, command waits for longer than that
    cmd = "sleep 4"
    to = 1
    x = DummyTool(run_command=cmd, timeout=to)
    x.start()

    while not x.finished:
        time.sleep(0.1)

    assert x.failed  # tool did not timeout


# abstract tool
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


# abstract tool
def test_dummy_abstract_tool():
    # Execute Tool tests
    test_regular_conditions()
    test_timeout()

    # terminate tests
    test_terminate()
    print("\nAbstractTool Tests Completed Successfully\n")


# nettacker
def test_regular_conditions_nettacker():
    x = NettackerTool()
    x.start()
    while not x.finished:
        time.sleep(0.1)

    assert x.raw_output is not None  # I dont know what it should be, but it should not be None


# nettacker
def test_nettacker_tool():
    test_regular_conditions_nettacker()

    print("\nNettackerTool Tests Completed Successfully\n")


if __name__ == '__main__':
    test_dummy_abstract_tool()
    test_nettacker_tool()
