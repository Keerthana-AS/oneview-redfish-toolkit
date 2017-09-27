# -*- coding: utf-8 -*-

# Copyright (2017) Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# Python libs
import json
import unittest
from unittest import mock

# 3rd party libs
from flask import Flask
from flask_api import status
from hpOneView.exceptions import HPOneViewException
from oneview_redfish_toolkit import util

# Module libs
from oneview_redfish_toolkit.blueprints.manager \
    import manager


class TestManager(unittest.TestCase):
    """Tests for Managers blueprint

        Tests:
            - enclosures
                - know value
                - not found error
                - unexpected error
            - blades
    """

    @mock.patch.object(util, 'OneViewClient')
    def setUp(self, ov_mock):
        """Tests preparation"""

        # Load config on util
        util.load_config('redfish.conf')

        # creates a test client
        self.app = Flask(__name__)

        self.app.register_blueprint(manager)

        self.app = self.app.test_client()

        # propagate the exceptions to the test client
        self.app.testing = True

    #############
    # Enclosure #
    #############
    @mock.patch.object(util, 'get_oneview_client')
    def test_get_enclosure_manager(
            self, mock_get_ov_client):
        """"Tests EnclosureManager with a known Enclosure"""

        # Loading ov_enclosure mockup value
        with open(
                'oneview_redfish_toolkit/mockups/Enclosure.json'
        ) as f:
            ov_enclosure = json.load(f)

        # Loading rf_enclosure mockup result
        with open(
                'oneview_redfish_toolkit/mockups/EnclosureManager.json'
        ) as f:
            rf_enclosure_manager = f.read()

        ov = mock_get_ov_client()

        ov.index_resources.get_all.return_value = [{"category": "enclosures"}]
        ov.enclosures.get.return_value = ov_enclosure
        ov. appliance_node_information.get_version.return_value = \
            {"softwareVersion": "3.00.07-0288219"}

        # Get EnclosureManager
        response = self.app.get(
            "/redfish/v1/Managers/0000000000A66101"
        )

        json_str = response.data.decode("utf-8")

        # Tests response
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual("application/json", response.mimetype)
        self.assertEqual(rf_enclosure_manager, json_str)

    @mock.patch.object(util, 'get_oneview_client')
    def test_get_enclosure_not_found(self, mock_get_ov_client):
        """Tests EnclosureManager with Enclosure not found"""

        ov = mock_get_ov_client()

        ov.index_resources.get_all.return_value = [{"category": "enclosures"}]
        ov.enclosures.get.return_value = \
            {'enclosureUri': 'invalidUri'}
        e = HPOneViewException({
            'errorCode': 'RESOURCE_NOT_FOUND',
            'message': 'enclosure not found',
        })

        ov.enclosures.get.side_effect = e

        response = self.app.get(
            "/redfish/v1/Managers/0000000000A66101"
        )

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual("application/json", response.mimetype)

    @mock.patch.object(util, 'get_oneview_client')
    def test_enclosure_unexpected_error(self, mock_get_ov_client):
        """Tests EnclosureManager with an unexpected error"""

        ov = mock_get_ov_client()

        ov.index_resources.get_all.return_value = [{"category": "enclosures"}]
        ov.enclosures.get.side_effect = Exception()

        response = self.app.get(
            "/redfish/v1/Managers/0000000000A66101"
        )

        self.assertEqual(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            response.status_code)
        self.assertEqual("application/json", response.mimetype)

    #############
    # Blade     #
    #############
    @mock.patch.object(util, 'get_oneview_client')
    def test_get_blade_manager(
            self, mock_get_ov_client):
        """"Tests BladeManager with a known Server Hardware"""

        # Loading ov_serverhardware mockup value
        with open(
                'oneview_redfish_toolkit/mockups/ServerHardware.json'
        ) as f:
            ov_serverhardware = json.load(f)

        # Loading rf_serverhardware mockup result
        with open(
                'oneview_redfish_toolkit/mockups/BladeManager.json'
        ) as f:
            rf_blade_manager = f.read()

        ov = mock_get_ov_client()

        ov.index_resources.get_all.return_value = \
            [{"category": "server-hardware"}]
        ov.server_hardware.get.return_value = ov_serverhardware
        ov. appliance_node_information.get_version.return_value = \
            {"softwareVersion": "3.00.07-0288219"}

        # Get BladeManager
        response = self.app.get(
            "/redfish/v1/Managers/30303437-3034-4D32-3230-313133364752"
        )

        json_str = response.data.decode("utf-8")

        # Tests response
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual("application/json", response.mimetype)
        self.assertEqual(rf_blade_manager, json_str)

    @mock.patch.object(util, 'get_oneview_client')
    def test_get_server_hardware_not_found(self, mock_get_ov_client):
        """Tests BladeManager with Server Hardware not found"""

        ov = mock_get_ov_client()

        ov.index_resources.get_all.return_value = [
            {"category": "server-hardware"}]
        ov.server_hardware.get.return_value =\
            {'serverHardwareUri': 'invalidUri'}
        e = HPOneViewException({
            'errorCode': 'RESOURCE_NOT_FOUND',
            'message': 'server hardware not found',
        })

        ov.server_hardware.get.side_effect = e

        response = self.app.get(
            "/redfish/v1/Managers/30303437-3034-4D32-3230-313133364752"
        )

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual("application/json", response.mimetype)

    @mock.patch.object(util, 'get_oneview_client')
    def test_server_hardware_unexpected_error(self, mock_get_ov_client):
        """Tests BladeManager with an unexpected error"""

        ov = mock_get_ov_client()

        ov.index_resources.get_all.return_value = [
            {"category": "server-hardware"}]
        ov.server_hardware.get.side_effect = Exception()

        response = self.app.get(
            "/redfish/v1/Managers/30303437-3034-4D32-3230-313133364752"
        )

        self.assertEqual(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            response.status_code)
        self.assertEqual("application/json", response.mimetype)
