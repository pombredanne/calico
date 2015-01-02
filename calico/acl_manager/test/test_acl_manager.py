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

import unittest
import calico.acl_manager.acl_manager

# Default config path.
config_path = "calico/acl_manager/test/data/default.cfg"

class TestMainline(unittest.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_case1(self):
        self.assertEqual(1, 1)
        
    def test_case2(self):
        calico.acl_manager.acl_manager.main()

if __name__ == '__main__':
    unittest.main()
