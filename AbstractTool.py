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

it includes:
    AbstractTool:
        - a baseclass for all Tool classes
"""
import subprocess
import threading


class AbstractTool(threading.Thread):
    """
    AbstractTool Class

    Working with tool classes:
        If the tool you were working with was Nettacker,
        you would declare your Nettacker object and then call the run function.
        That should be it!

        scan = Nettacker(host='localhost')  # made up parameters, I dont know them yet
        scan.run()

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
            - String
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

        # Later this should be generated based off an ID in the database to ensure no duplicate containers
        self.ct_name = self.tool_name + '1'

        # Implementation Validation
        if self.tool_name is None:
            raise NotImplementedError("must define self.tool_name before calling init")
        if self.timeout is None:
            raise NotImplementedError("must define self.timeout before calling init")
        if self.run_command is None:
            raise NotImplementedError("must define self.run_command before calling init")

    def execute_cmd(self, cmd):
        """
        Executes a linux command
        :param cmd: a string of the command to be ran
        :raises: Timeout error, Tool Error
        """
        assert(type(cmd) == str)  # cmd must be string

        # splitting, this is required by subprocess
        cmd = cmd.split(' ')

        # creating process object
        sp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Executing
        stdout, stderr = sp.communicate(timeout=self.timeout)

        # decoding
        self.stdout = stdout.decode('utf-8')
        self.stderr = stderr.decode('utf-8')

        # validating. Could be an issue for some tools
        if self.stderr == '':
            raise self.ToolError("Command: %s \nReturned error: \n%s" % (cmd, stderr))

    def run(self):
        """
        If Python had public/private methods, this would be THE ONLY public one!

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
        self.execute_cmd(self.run_command)

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

