
RESOURCE_MAPPING = {
    'user': {
        'resource': 'me',
        'docs': 'https://circleci.com/docs/api/#user',
        'methods': ['GET'],
    },
    'projects': {
        'resource': 'projects',
        'docs': 'https://circleci.com/docs/api/#projects',
        'methods': ['GET'],
    },
    'project': {
        'resource': 'project/{vcs_type}/{username}/{project}',
        'docs': 'https://circleci.com/docs/api/#recent-builds-project',
        'methods': ['GET', 'POST'],
    },
    'follow_project': {
        'resource': 'project/{vcs_type}/{username}/{project}/follow',
        'docs': 'https://circleci.com/docs/api/#follow-project',
        'methods': ['POST'],
    },
    'project_build': {
        'resource': 'project/{vcs_type}/{username}/{project}/{build_num}',
        'docs': 'https://circleci.com/docs/api/#build',
        'methods': ['GET'],
    },
    'retry_project_build': {
        'resource': 'project/{vcs_type}/{username}/{project}/{build_num}/retry',
        'docs': 'https://circleci.com/docs/api/#retry-build',
        'methods': ['POST'],
    },
    'cancel_project_build': {
        'resource': 'project/{vcs_type}/{username}/{project}/{build_num}/cancel',
        'docs': 'https://circleci.com/docs/api/#cancel-build',
        'methods': ['POST'],
    },
    'project_builds_for_branch': {
        'resource': 'project/{vcs_type}/{username}/{project}/tree/{branch}',
        'docs': 'https://circleci.com/docs/api/#recent-builds-project-branch',
        'methods': ['GET', 'POST'],
    },
    'build_artifacts': {
        'resource': 'project/{vcs_type}/{username}/{project}/{build_num}/artifacts',
        'docs': 'https://circleci.com/docs/api/#build-artifacts',
        'methods': ['GET'],
    },
    'latest_build_artifacts': {
        'resource': 'project/{vcs_type}/{username}/{project}/latest/artifacts',
        'docs': 'https://circleci.com/docs/api/#build-artifacts-latest',
        'methods': ['GET'],
    },
    'recent_builds': {
        'resource': 'recent-builds',
        'docs': 'https://circleci.com/docs/api/#recent-builds',
        'methods': ['GET'],
    },
    'clear_cache': {
        'resource': 'project/{vcs_type}/{username}/{project}/build-cache',
        'docs': 'https://circleci.com/docs/api/#clear-cache',
        'methods': ['DELETE'],
    },
}
