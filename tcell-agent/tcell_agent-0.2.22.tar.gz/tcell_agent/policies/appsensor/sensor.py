import tcell_agent.agent

from tcell_agent.sensor_events import AppSensorEvent

def sendEvent(
        appsensor_meta,
        detection_point,
        parameter,
        meta,
        payload=None,
        pattern=None):
    tcell_agent.agent.TCellAgent.send(AppSensorEvent(
        detection_point,
        parameter,
        appsensor_meta.location,
        appsensor_meta.remote_address,
        appsensor_meta.route_id,
        meta,
        appsensor_meta.method,
        payload=payload,
        user_id=appsensor_meta.user_id,
        hmacd_session_id=appsensor_meta.session_id,
        pattern=pattern
    ))
