# Copyright 2014 Metaswitch Networks
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from multiprocessing import Process
import unittest

import calico.acl_manager.acl_manager as acl_manager

# Default configuration file path.
default_config = "calico/acl_manager/test/data/default.cfg"

class TestMainline(unittest.TestCase):
    """
    Mainline tests for the whole of ACL Manager.

    These tests run the whole of ACL Manager in a separate process, and verify
    its mainline function.
    """

    def set_command_line_args(self, config_path):
        """Set the command line arguments that ACL Manager will use"""
        del sys.argv[1:]
        sys.argv.extend(["-c", config_path])

    def start_acl_manager(self):
        self.acl_manager_process = Process(target = acl_manager.main)
        self.acl_manager_process.start()

    def stop_acl_manager(self):
        self.acl_manager_process.terminate()

    def setUp(self):
        self.acl_manager_process = None

    def tearDown(self):
        if (self.acl_manager_process and self.acl_manager_process.is_alive()):
            self.stop_acl_manager()

    def test_case1(self):
        self.assertEqual(1, 1)

    def test_case2(self):
        self.set_command_line_args(default_config)
        self.start_acl_manager()

if __name__ == '__main__':
    unittest.main()
