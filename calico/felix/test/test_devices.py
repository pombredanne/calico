# -*- coding: utf-8 -*-
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
"""
felix.test.test_devices
~~~~~~~~~~~

Test the interface handling code.
"""
import logging
import mock
import os
import sys
import unittest
import uuid

import calico.felix.devices as devices
import calico.felix.futils as futils
import calico.felix.test.stub_utils as stub_utils

# Logger
log = logging.getLogger(__name__)

class TestDevices(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_tap_exists(self):
        tap = "tap" + str(uuid.uuid4())[:11]

        with mock.patch('os.path.exists', return_value=True):
            self.assertTrue(devices.tap_exists(tap))
            os.path.exists.assert_called_with("/sys/class/net/" + tap)

        with mock.patch('os.path.exists', return_value=False):
            self.assertFalse(devices.tap_exists(tap))
            os.path.exists.assert_called_with("/sys/class/net/" + tap)

    def test_add_route(self):
        tap = "tap" + str(uuid.uuid4())[:11]
        mac = stub_utils.get_mac()
        retcode = futils.CommandOutput("", "")

        type = futils.IPV4
        ip = "1.2.3.4"
        with mock.patch('calico.felix.futils.check_call', return_value=retcode):
            devices.add_route(type, ip, tap, mac)
            futils.check_call.assert_any_call(['arp', '-s', ip, mac, '-i', tap])
            futils.check_call.assert_called_with(["ip", "route", "add", ip, "dev", tap])

        type = futils.IPV6
        ip = "2001::"
        with mock.patch('calico.felix.futils.check_call', return_value=retcode):
            devices.add_route(type, ip, tap, mac)
            futils.check_call.assert_called_with(["ip", "-6", "route", "add", ip, "dev", tap])

    def test_del_route(self):
        tap = "tap" + str(uuid.uuid4())[:11]
        retcode = futils.CommandOutput("", "")

        type = futils.IPV4
        ip = "1.2.3.4"
        with mock.patch('calico.felix.futils.check_call', return_value=retcode):
            devices.del_route(type, ip, tap)
            futils.check_call.assert_any_call(['arp', '-d', ip, '-i', tap])
            futils.check_call.assert_called_with(["ip", "route", "del", ip, "dev", tap])

        type = futils.IPV6
        ip = "2001::"
        with mock.patch('calico.felix.futils.check_call', return_value=retcode):
            devices.del_route(type, ip, tap)
            futils.check_call.assert_called_once_with(["ip", "-6", "route", "del", ip, "dev", tap])


    def test_list_tap_ips(self):
        type = futils.IPV4
        tap = "tap" + str(uuid.uuid4())[:11]

        retcode = futils.CommandOutput("", "")
        with mock.patch('calico.felix.futils.check_call', return_value=retcode):
            ips = devices.list_tap_ips(type, tap)
            futils.check_call.assert_called_once_with(["ip", "route", "list", "dev", tap])
            self.assertFalse(ips)
            
        stdout = "10.11.9.90  scope link"
        retcode = futils.CommandOutput(stdout, "")
        with mock.patch('calico.felix.futils.check_call', return_value=retcode):
            ips = devices.list_tap_ips(type, tap)
            futils.check_call.assert_called_once_with(["ip", "route", "list", "dev", tap])
            self.assertEqual(ips, set(["10.11.9.90"]))
            
        stdout = "10.11.9.90  scope link\nblah-di-blah not valid\nx\n"
        retcode = futils.CommandOutput(stdout, "")
        with mock.patch('calico.felix.futils.check_call', return_value=retcode):
            ips = devices.list_tap_ips(type, tap)
            futils.check_call.assert_called_once_with(["ip", "route", "list", "dev", tap])
            self.assertEqual(ips, set(["10.11.9.90"]))
            
        type = futils.IPV6
        stdout = "2001:: scope link\n"
        retcode = futils.CommandOutput(stdout, "")
        with mock.patch('calico.felix.futils.check_call', return_value=retcode):
            ips = devices.list_tap_ips(type, tap)
            futils.check_call.assert_called_once_with(["ip", "-6", "route", "list", "dev", tap])
            self.assertEqual(ips, set(["2001::"]))
            
        stdout = "2001:: scope link\n\n"
        retcode = futils.CommandOutput(stdout, "")
        with mock.patch('calico.felix.futils.check_call', return_value=retcode):
            ips = devices.list_tap_ips(type, tap)
            futils.check_call.assert_called_once_with(["ip", "-6", "route", "list", "dev", tap])
            self.assertEqual(ips, set(["2001::"]))

    def test_configure_tap2(self):
        tap = "tap" + str(uuid.uuid4())[:11]

        open_mock = mock.Mock()
        calls = [mock.call('/proc/sys/net/ipv4/conf/%s/route_localnet' % tap, 'wb'),
                 mock.call("/proc/sys/net/ipv4/conf/%s/proxy_arp" % tap, 'wb')]

        with mock.patch('__builtin__.open') as open_mock:
            # TODO: We don't test that the write calls happened, which is deeply annoying...
            devices.configure_tap(tap)
            open_mock.assert_has_calls(calls, any_order=True)