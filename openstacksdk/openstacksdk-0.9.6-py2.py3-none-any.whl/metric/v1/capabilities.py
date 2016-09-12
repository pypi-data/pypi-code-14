# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from openstack.metric import metric_service
from openstack import resource


class Capabilities(resource.Resource):
    base_path = '/capabilities'
    service = metric_service.MetricService()

    # Supported Operations
    allow_retrieve = True

    #: The supported methods of aggregation.
    aggregation_methods = resource.prop('aggregation_methods', type=list)
