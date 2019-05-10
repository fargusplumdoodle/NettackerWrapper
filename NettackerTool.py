import os
import random
from AbstractTool import AbstractTool


class NettackerTool(AbstractTool):
    """
    Nettacker Implementation for AbstractTool

    REQUIRES A PREBUILT IMAGE FOR NETTACKER

    AbstractTool docs:
    Public Methods:
        - run() -> runs the tool and parses output
            - raises a FileNotFoundError when provided a bad run_command
        - terminate() -> destroys currently running tool

    Implements:
        - self.run_command:
        - self.timeout:
        - self.tool_name:
        - self.parse_output():
    """
    def __init__(self, target='127.0.0.1', scan_options='icmp_scan', exclude_options="viewdns_reverse_ip_lookup_scan", timeout=60):
        super(NettackerTool, self).__init__(timeout=timeout, tool_name="nettacker")
        # TODO:change scan_options to "all"

        # to prevent any clashes with simultaneous scans, later probably will be replaced with some
        # unique value from database
        self.scan_no = str(random.choice(range(100)))

        # may need to be fixed later
        self.output_fl = 'nettacker_scan' + self.scan_no + '.json'

        # the target to scan
        self.target = target

        # container name
        self.ct_name = self.tool_name + "_" + self.scan_no

        # the options, by default is icmp_scan because its fast
        self.scan_options = scan_options

        # the location of the results folder in the container
        self.docker_results = '/root/.owasp-nettacker/results/'

        self.docker_image = 'nettacker'

        # options not to include when scanning
        self.exclude_options = exclude_options

        # local results config
        self.local_results = '/tmp/nettacker/scan' + self.scan_no + '/'
        os.makedirs(self.local_results)  # making local results directory

        self.results_file_path_docker = os.path.join(self.docker_results, self.output_fl)
        self.results_file_path_local = os.path.join(self.local_results, self.output_fl)

        # docker simplifies things... trust me...
        # --rm deletes the container after its done running
        self.run_command = 'docker run ' \
                           '-v %s:%s ' \
                           '--rm ' \
                           '--name %s %s ' \
                           '-i %s ' \
                           '-m %s ' \
                           '-o %s ' \
                           '-x %s ' \
                           % (
                               self.local_results,
                               self.docker_results,
                               self.ct_name,
                               self.docker_image,
                               self.target,
                               self.scan_options,
                               self.results_file_path_docker,
                               self.exclude_options
                           )

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
        with open(self.results_file_path_local, 'r') as f:
            try:
                self.raw_output = f.read()
            except IOError:
                print("Error opening file")
                exit(-3)

