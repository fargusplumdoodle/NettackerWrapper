import threading


class AbstractTool(threading.Thread):
    """
    AbstractTool Class

    Child Class Must Implement:
        - self.run_command:
            - String
            - Bash command that will be executed.
            - Recommended: Docker, not required.

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
    """
    def __init__(self, tool_name):
        # calling threading's init
        super(AbstractTool, self).__init__()

        self.tool_name = tool_name

        # Later this should be generated based off an ID in the database
        self.ct_name = self.tool_name + '1'


    class ToolError(Exception):
        pass