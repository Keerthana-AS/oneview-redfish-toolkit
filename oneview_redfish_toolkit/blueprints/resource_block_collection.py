# -*- coding: utf-8 -*-

# Copyright (2018) Hewlett Packard Enterprise Development LP
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

from flask import Blueprint
from flask import g

from oneview_redfish_toolkit.api.resource_block_collection \
    import ResourceBlockCollection
from oneview_redfish_toolkit.blueprints.util.response_builder import \
    ResponseBuilder

resource_block_collection = Blueprint("resource_block_collection", __name__)


@resource_block_collection.route(
    "/redfish/v1/CompositionService/ResourceBlocks/", methods=["GET"])
def get_resource_block_collection():
    """Get the Redfish ResourceBlock Collection.

        Return ResourceBlockCollection redfish JSON.
        Logs exception of any error and return
        Internal Server Error or Not Found.

        Returns:
            JSON: Redfish json with ResourceBlockCollection.
    """

    # Gets all server hardware
    server_hardware_list = g.oneview_client.server_hardware.get_all()
    server_profile_template_list = g.oneview_client.\
        server_profile_templates.get_all()
    drives_list = g.oneview_client.index_resources \
        .get_all(category="drives", count=10000)
    volume_list = g.oneview_client.volumes.get_all()
    filter_volume_list = [volume for volume in volume_list
                          if volume["isShareable"]]
    #print("server_hardware_list = " + str(len(server_hardware_list)))
    #print(server_hardware_list)
    #print("server_profile_template_list = " + str(len(server_profile_template_list)))
    #print(server_profile_template_list)
    #print("drives_list = " + str(len(drives_list)))
    #print(drives_list)
    #print("volume_list = " + str(len(volume_list)))
    #print(volume_list)
    # Emptying volume list to suppress external storage changes for
    # current release.
    # In future, remove this line to enable external storage support
    filter_volume_list = []

    # Build ResourceBlockCollection object and validates it
    cc = ResourceBlockCollection(server_hardware_list,
                                 server_profile_template_list,
                                 drives_list, filter_volume_list)

    return ResponseBuilder.success(cc)
