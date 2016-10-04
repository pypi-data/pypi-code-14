import requests
from pretty_cron import prettify_cron
from casepro.cases.models import Case
from casepro.contacts.models import Contact
from casepro.pods import Pod, PodConfig, PodPlugin
from confmodel import fields
from demands import HTTPServiceError
from django.conf import settings
from seed_services_client.stage_based_messaging \
    import StageBasedMessagingApiClient


class SubscriptionPodConfig(PodConfig):
    url = fields.ConfigText("URL to query for the registration data",
                            required=True)
    token = fields.ConfigText("Authentication token for registration endpoint",
                              required=True)


class SubscriptionPod(Pod):
    def __init__(self, pod_type, config):
        super(SubscriptionPod, self).__init__(pod_type, config)
        url = self.config.url
        token = self.config.token

        # Start a session with the StageBasedMessagingApiClient
        self.stage_based_messaging_api = StageBasedMessagingApiClient(
            token, url)

    def read_data(self, params):
        # Get contact idenity
        case_id = params["case_id"]
        case = Case.objects.get(pk=case_id)
        params = {
            'identity': case.contact.uuid
        }

        try:
            response = self.stage_based_messaging_api.get_subscriptions(params)
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
        active_sub_ids = []
        for subscription in data:
            subscription_data = {"rows": []}
            # Add the messageset
            message_set_id = subscription['messageset']
            message_set = self.stage_based_messaging_api.get_messageset(
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
            schedule = self.stage_based_messaging_api.get_schedule(schedule_id)
            subscription_data['rows'].append({
                "name": "Schedule",
                "value": self.format_schedule(schedule)})
            # Add the active flag
            subscription_data['rows'].append({
                "name": "Active",
                "value": subscription['active']})
            if subscription['active']:
                active_sub_ids.append(subscription['id'])
            # Add the completed flag
            subscription_data['rows'].append({
                "name": "Completed",
                "value": subscription['completed']})
            content['items'].append(subscription_data)

        actions = [{
            'type': 'full_opt_out',
            'name': 'Full Opt-Out',
            'confirm': True,
            'busy_text': 'Processing...',
            'payload': {
                'contact_id': case.contact.id,
                'subscription_ids': active_sub_ids
            }
        }]
        if len(active_sub_ids) > 0:
            cancel_action = {
                'type': 'cancel_subs',
                'name': 'Cancel All Subscriptions',
                'confirm': True,
                'busy_text': 'Cancelling...',
                'payload': {
                    'subscription_ids': active_sub_ids
                }
            }
            actions.append(cancel_action)

        content['actions'] = actions
        return content

    def format_schedule(self, schedule):
        cron_schedule = "%s %s %s %s %s" % (
            schedule['minute'], schedule['hour'], schedule['day_of_month'],
            schedule['month_of_year'], schedule['day_of_week'])
        return prettify_cron(cron_schedule)

    def cancel_subscriptions(self, subscription_ids):
        params = {'active': False}
        for subscription in subscription_ids:
            try:
                self.stage_based_messaging_api.update_subscription(
                    subscription, params)
            except HTTPServiceError:
                return False
        return True

    def full_opt_out(self, contact_id):
        contact = Contact.objects.get(pk=contact_id)
        identity = contact.uuid

        opt_out_url = settings.IDENTITY_API_ROOT + "api/v1/optout/"
        identity_token = settings.IDENTITY_AUTH_TOKEN
        headers = {
            'Authorization': "Token " + identity_token,
            'Content-Type': "application/json"
        }

        # Opt-outs have to have an address. This kinda sucks though
        if contact.urns:
            addr_type, address = contact.urns[0].split(':', 1)
            response = requests.post(
                opt_out_url, headers=headers,
                json={'identity': identity, 'optout_type': "forget",
                      'address_type': addr_type, 'address': address,
                      'request_source': 'casepro'},
            )
            if response.status_code == 201:
                return True
        return False

    def perform_action(self, type_, params):
        if type_ == "cancel_subs":
            subscription_ids = params.get("subscription_ids", [])
            success = self.cancel_subscriptions(subscription_ids)
            if not success:
                return (False,
                        {"message": "Failed to cancel some subscriptions"})
            return (True, {"message": "cancelled all subscriptions"})

        if type_ == "full_opt_out":
            opted_out = self.full_opt_out(params["contact_id"])
            subscription_ids = params.get("subscription_ids", [])
            subs_cancelled = self.cancel_subscriptions(subscription_ids)

            message = ""
            if opted_out:
                message = "Opt-Out completed."
            else:
                message = "An error occured while opting the user out."
            if subs_cancelled:
                message += " All subscriptions cancelled."
            else:
                message += " Failed to cancel some subscriptions"

            return ((opted_out and subs_cancelled), {"message": message})


class SubscriptionPlugin(PodPlugin):
    name = 'casepropods.family_connect_subscription'
    label = 'family_connect_subscription_pod'
    pod_class = SubscriptionPod
    config_class = SubscriptionPodConfig
    title = 'Subscription Pod'
    directive = 'subscription-pod'
    scripts = ['subscription_pod_directives.js']
    styles = ['subscription_pod.css']
