from pretty_cron import prettify_cron
from casepro.cases.models import Case
from casepro.pods import Pod, PodConfig, PodPlugin
from confmodel import fields
from demands import HTTPServiceError
from seed_services_client.stage_based_messaging \
    import StageBasedMessagingApiClient


class SubscriptionPodConfig(PodConfig):
    url = fields.ConfigText("URL to query for the registration data",
                            required=True)
    token = fields.ConfigText("Authentication token for registration endpoint",
                              required=True)


class SubscriptionPod(Pod):
    def read_data(self, params):
        url = self.config.url
        token = self.config.token

        # Get contact idenity
        case_id = params["case_id"]
        case = Case.objects.get(pk=case_id)
        params = {
            'identity': case.contact.uuid
        }

        # Start a session with the StageBasedMessagingApiClient
        stage_based_messaging_api = StageBasedMessagingApiClient(token, url)
        try:
            response = stage_based_messaging_api.get_subscriptions(params)
        except HTTPServiceError as e:
            return {"items": [{"name": "Error", "value": e.details["detail"]}]}

        # Format and return data
        if response['count'] < 1:
            return {"items": [{
                "rows": [{
                    "name": "No subscriptions", "value": ""
                }]
            }]}
        data = response["results"]
        content = {"items": []}
        for subscription in data:
            subscription_data = {"rows": []}
            # Add the messageset
            message_set_id = subscription['messageset']
            message_set = stage_based_messaging_api.get_messageset(
                message_set_id)
            if message_set:
                subscription_data['rows'].append({
                    "name": "Message Set", "value": message_set["short_name"]})
            # Add the sequence number
            subscription_data['rows'].append({
                "name": "Next Sequence Number",
                "value": subscription['next_sequence_number']})
            # Add the schedule
            schedule_id = subscription['schedule']
            schedule = stage_based_messaging_api.get_schedule(schedule_id)
            subscription_data['rows'].append({
                "name": "Schedule",
                "value": self.format_schedule(schedule)})
            # Add the active flag
            subscription_data['rows'].append({
                "name": "Active",
                "value": subscription['active']})
            # Add the completed flag
            subscription_data['rows'].append({
                "name": "Completed",
                "value": subscription['completed']})
            content['items'].append(subscription_data)
        return content

    def format_schedule(self, schedule):
        cron_schedule = "%s %s %s %s %s" % (
            schedule['minute'], schedule['hour'], schedule['day_of_month'],
            schedule['month_of_year'], schedule['day_of_week'])
        return prettify_cron(cron_schedule)


class SubscriptionPlugin(PodPlugin):
    name = 'casepropods.family_connect_subscription'
    label = 'family_connect_subscription_pod'
    pod_class = SubscriptionPod
    config_class = SubscriptionPodConfig
    title = 'Subscription Pod'
    directive = 'subscription-pod'
    scripts = ['subscription_pod_directives.js']
    styles = ['subscription_pod.css']
