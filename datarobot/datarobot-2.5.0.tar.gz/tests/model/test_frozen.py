import pytest
import responses

from datarobot import FrozenModel


@responses.activate
@pytest.mark.usefixtures('client')
def test_frozen_model_get_returns_valid_data(frozen_json, one_frozen):
    url = 'https://host_name.com/projects/p-id/frozenModels/{}/'.format(one_frozen.id)
    responses.add(responses.GET,
                  url,
                  body=frozen_json,
                  status=200,
                  content_type='application/json')
    frozen = FrozenModel.get('p-id', one_frozen.id)
    assert isinstance(frozen, FrozenModel)
    assert frozen.id == one_frozen.id
    assert frozen.parent_model_id == one_frozen.parent_model_id


@responses.activate
@pytest.mark.usefixtures('client')
def test_request_frozen_model(one_model, project_url, frozen_model_job_completed_server_data):
    frozen_models_url = '{}frozenModels/'.format(project_url)
    job_url = '{}modelJobs/{}/'.format(project_url, frozen_model_job_completed_server_data['id'])
    finished_freeze_url = '{}/12344321beefcafe43211234/'.format(frozen_models_url)

    responses.add(responses.POST, frozen_models_url, body='', status=202,
                  content_type='application/json', adding_headers={'Location': job_url})
    responses.add(responses.GET, job_url, json=frozen_model_job_completed_server_data,
                  status=303,
                  adding_headers={'Location': finished_freeze_url})

    model_job = one_model.request_frozen_model(sample_pct=98.98)
    assert model_job.id == int(frozen_model_job_completed_server_data['id'])
