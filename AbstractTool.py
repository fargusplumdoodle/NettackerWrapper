"""
Abstract Tool V0.1
Isaac Thiessen 2019 April

This is a class I am using to figure out how to build the SST API.
This follows the idea of creating an abstract class that would be implemented
by each individual tool that will be integrated into the SST API.

But why?
    - all tools will be very similar. An abstract class would exercise
      the DRY principle of OOP
    - This could make adding new tools quick and hopefully easy

It includes:
    AbstractTool:
        - a baseclass for all Tool classes

Plans:
    Django database integration:
        - The run method should update the scan status in the database
    DummyTool
    Terminate Tool:
        - Stops container, Deletes container
    Position in queue?
"""
import subprocess
import threading


class AbstractTool(threading.Thread):
    """
    AbstractTool Class

    Public Methods:
        - run() -> runs the tool and parses output
        - terminate() -> destroys currently running tool

    Child Class Must Implement:
        - self.run_command:
            - String
            - Bash command that will be executed.
            - Recommended: Docker, not required.
            - Recommended for Docker: add the "--rm" parameter to the "docker run"
                                      command. This will delete the container on exit
                                      so we dont have a server full of docker containers
                                      that will never be used.

        - self.timeout:
            - Int
            - Number of seconds before tool times out
            - Upon tool timeout, self.run_tool will raise self.ToolError

        - self.tool_name:
            - String, lowercase alphabetic only
            - the name of the tool that is implementing the AbstractTool class

        - self.parse_output():
            - Method
            - Each tool provides output differently therefor each implementation
              of AbstractTool must override self.parse_output()
            - Must:
                1. Retrieve data from self.stdout
                2. Parse that data for meaningful information
                3. Put data in relevant place
            - Phases:
                1. Just put raw data into self.raw_output ( no parsing )
                2. Retrieve meaningful information from tool output and
                   put that information in the appropriate locations in
                   the database
    """
    def __init__(self):
        # calling threading's init
        super(AbstractTool, self).__init__()

        # Overwritten attributes
        self.tool_name = None
        self.timeout = None
        self.run_command = None

        # will be written by self.execute_tool()
        self.stdout = None
        self.stderr = None

        """
            The tools ACTIVE subprocess of type Popen
            this will be overwritten every time the execute command is ran
            this should be a member variable so we can kill the tool while running
            documentation: https://docs.python.org/3/library/subprocess.html#subprocess.Popen
        """
        self.sp = None

        # Later this should be generated based off an ID in the database to ensure no duplicate containers
        self.ct_name = self.tool_name + '1'

        # Implementation Validation
        if self.tool_name is None:
            raise NotImplementedError("must define self.tool_name before calling init")
        if self.timeout is None:
            raise NotImplementedError("must define self.timeout before calling init")
        if self.run_command is None:
            raise NotImplementedError("must define self.run_command before calling init")

    def terminate(self):
        """
        This kills the tool while running.
        """
        # killing subprocess
        self.sp.kill()

        stop_cmd = 'docker stop %s' % self.ct_name
        rm_cmd = 'docker stop %s' % self.ct_name

        # stopping/deleting container. If it doesnt exist this will fail and it wont matter
        try:
            self.__execute_cmd(stop_cmd)
        except self.ToolError:
            pass

        try:
            self.__execute_cmd(rm_cmd)
        except self.ToolError:
            pass

    def __execute_cmd(self, cmd):
        """
        Executes a linux command
        :param cmd: a string of the command to be ran
        :raises: Timeout error, Tool Error
        :returns stdout
        """
        assert(type(cmd) == str)  # cmd must be string

        # splitting, this is required by subprocess
        cmd = cmd.split(' ')

        # creating process object
        self.sp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Executing
        stdout, stderr = self.sp.communicate(timeout=self.timeout)

        # decoding
        stdout = stdout.decode('utf-8')
        stderr = stderr.decode('utf-8')

        # validating. Could be an issue for some tools
        if stderr == '':
            raise self.ToolError("Command: %s \nReturned error: \n%s" % (cmd, stderr))

        # clearing the subprocess
        self.sp = None

        return stdout

    def __execute_tool(self, cmd):
        """
        Executes a linux command, but use this specifically for running the tool
        This function populates the self.stdout member variable

        :param cmd: a string of the command to be ran
        :raises: Timeout error, Tool Error
        """
        assert(type(cmd) == str)  # cmd must be string

        # splitting, this is required by subprocess
        cmd = cmd.split(' ')

        # creating process object
        self.sp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Executing
        stdout, stderr = self.sp.communicate(timeout=self.timeout)

        # decoding
        self.stdout = stdout.decode('utf-8')
        self.stderr = stderr.decode('utf-8')

        # validating. Could be an issue for some tools
        if self.stderr == '':
            raise self.ToolError("Command: %s \nReturned error: \n%s" % (cmd, stderr))

        # clearing the subprocess
        self.sp = None

    def run(self):
        """
        Run method procedure:
            1. Starts new thread
            2. Executes self.run_tool command (implemented by child class)
                :raises Timeout error: if tool timed out
                :raises Tool Error: if stderr was not null
            3. Executes self.parse_output() (implemented by child class)

        Future functionality:
            - Put data in database
            - Update scan status as we progress through the procedure
        """
        # 2.
        self.__execute_tool(self.run_command)

        # 3.
        self.parse_output()

    def parse_output(self):
        """
        - self.parse_output():
            - Method
            - Each tool provides output differently therefor each implementation
              of AbstractTool must override self.parse_output()
            - Must:
                1. Retrieve data from self.stdout
                2. Parse that data for meaningful information
                3. Put data in relevant place
            - Phases:
                1. Just put raw data into self.raw_output ( no parsing )
                2. Retrieve meaningful information from tool output and
                   put that information in the appropriate locations in
                   the database
        """
        raise NotImplementedError("must override self.parse_output for your tool")

    class ToolError(Exception):
        # Exceptions dont require anything else
        pass


class DummyTool(AbstractTool):
    """
    This is a fake tool for testing purposes
    """
    def __init__(self):
        self.tool_name = "dummytool"
        self.timeout = 10  # it shouldn't take 10 seconds to do nothing
        self.run_command = "echo dummy tool output"  # doesn't matter

        super(DummyTool, self).__init__()

    def parse_output(self):
        print(self.stdout)

