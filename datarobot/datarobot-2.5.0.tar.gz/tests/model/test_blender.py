import pytest
import responses

from datarobot import BlenderModel


@responses.activate
@pytest.mark.usefixtures('client')
def test_blender_model_get_return_valid_data(blender_json, one_blender):
    url = 'https://host_name.com/projects/p-id/blenderModels/{}/'.format(one_blender.id)
    responses.add(responses.GET,
                  url,
                  body=blender_json,
                  status=200,
                  content_type='application/json')
    blender = BlenderModel.get('p-id', one_blender.id)
    assert isinstance(blender, BlenderModel)
    assert blender.id == one_blender.id
    assert blender.model_ids == one_blender.model_ids
    assert blender.blender_method == one_blender.blender_method
