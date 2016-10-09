"""API calls for RingPlus."""

from __future__ import print_function

from ringplus.parsers import ModelParser
from ringplus.binder import bind_api


class API(object):
    """A python wrapper for the RingPlus API.

    :reference: https://docs.ringplus.net/
    """

    def __init__(self, auth_handler=None,
                 host='api.ringplus.net', cache=None,
                 parser=None, version='1', retry_count=0, retry_delay=0,
                 retry_errors=None, timeout=60,
                 wait_on_rate_limit=False, wait_on_rate_limit_notify=False,
                 proxy=''):
        """API instance constructor.

        Args:
            auth_handler: The OAutherHandler from to use to retreive the
                authorization token.
            host:  url of the server of the rest api.
                default:'api.ringplus.net'
            cache: Cache to query if a GET method is used.
                default:None
            parser: ModelParser instance to parse the responses.
                default:None
            version: Major version number to include in header.
                default 1
            retry_count: number of allowed retries, default:0
            retry_errors: default:None
            timeout: delay before to consider the request as timed out in
                seconds. default:60
            wait_on_rate_limit: If the api wait when it hits the rate limit.
                default:False
            wait_on_rate_limit_notify: If the api print a notification when
                the rate limit is hit. default:False
            proxy: Url to use as proxy during the HTTP request. default:''
        """

        self.auth = auth_handler
        self.host = host
        self.cache = cache
        self.parser = parser or ModelParser()
        self.version = version
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.retry_errors = retry_errors
        self.timeout = 60
        self.wait_on_rate_limit = wait_on_rate_limit
        self.wait_on_rate_limit_notify = wait_on_rate_limit_notify
        self.proxy = proxy

    # Accounts
    @property
    def user_accounts(self):
        """A list of accounts belonging to a specific user.

        scope: public

        Args:
            user_id: User ID
            name (optional): The name of the account to filter by.
                Currently does not partial or full text search.
            email_address (optional): The email_address of the account to
                filter by. Currently does not partial or full text search.
            phone_number (optional): The phone_number of the account to
                filter by. Currently does not partial or full text search.
            device_esn (optional): The active device_esn of the account to
                filter by. Currently does not partial or full text search.
            device_iccid (optional): The active device_iccid of the account to
                filter by. Currently does not partial or full text search.
            page (optional): Which page of the paged results to return.
                Default to 1.
            per_page (optional): How many results to return per page.
                Defaults to 25.

        Returns
            list: List of Account objects
        """
        return bind_api(
            api=self,
            path='/users/{user_id}/accounts',
            payload_type='account',
            payload_list=True,
            allowed_param=['user_id', 'name', 'email_address',
                           'phone_number', 'device_esn', 'device_iccid',
                           'page', 'per_page'])

    @property
    def accounts(self):
        """List all accounts the user has access to.

        scope: public

        Args:
            name (optional): The name of the account to filter by.
                Currently does not partial or full text search.
            email_address (optional): The email_address of the account to
                filter by. Currently does not partial or full text search.
            phone_number (optional): The phone_number of the account to
                filter by. Currently does not partial or full text search.
            ddevice_esn (optional): The active device_esn of the account to
                filter by. Currently does not partial or full text search.
            device_iccid (optional): The active device_iccid of the account to
                filter by. Currently does not partial or full text search.
            page (optional): Which page of the paged results to return.
                Default to 1.
            per_page (optional): How many results to return per page.
                Defaults to 25.

        Returns
            list: List of Account objects
        """
        return bind_api(
            api=self,
            path='/accounts',
            payload_type='account',
            payload_list=True,
            allowed_param=['name', 'email_address', 'phone_number',
                           'device_esn', 'device_iccid', 'page',
                           'per_page'])

    @property
    def get_account(self):
        """Get a specific account.

        This returns a more detailed account object than those returned in
        API.user_accounts and API.accounts.

        scope: public

        Args:
            account_id: Account ID

        Returns:
            Detailed Account object.
        """
        return bind_api(
            api=self,
            path='/accounts/{account_id}',
            payload_type='account',
            allowed_param=['account_id'])

    @property
    def update_account(self):
        """Update an accounts information.

        scope: manage

        Args:
            account_id: Account ID
            name (optional): Update the name of an account.
        """
        return bind_api(
            api=self,
            path='/accounts/{account_id}',
            method='PUT',
            post_container='account',
            allowed_param=['account_id', 'name'])

    # Account Registration
    @property
    def register_account(self):
        """Create a registration request to associate a user with a device.

        scope: request

        Args:
            user_id: User ID
            name: A name for this account.
            billing_plan_id: The ID of the billing plan to use for this
                account.
            device_esn: The mobile device's ESN numbers, usually an
                alphanumeric string.
            credit_card_id: An ID of a credit card already associated with the
                User.
            device_iccid (optional): The mobile device's ICCID, or SIM card
                serial number.

        Returns:
            Account Registration Request Status object.
        """
        return bind_api(
            api=self,
            path='/users/{user_id}/account_registration_requests',
            method='POST',
            post_container='account_registration_request',
            payload_type='request',
            allowed_param=['user_id', 'name', 'billing_plan_id',
                           'device_esn', 'device_iccid', 'credit_card_id'])

    @property
    def register_account_status(self):
        """Get the status on an account registration request.

        scope: public

        Args:
            request_id: The ID of the register account request.

        Returns:
            list: List of Account Registration Status objects.
        """
        return bind_api(
            api=self,
            path='/account_registration_requests/{request_id}',
            payload_type='request',
            payload_list=True,
            allowed_param=['request_id'])

    # Change Device
    @property
    def change_device(self):
        """Create a change device request to change physical device.

        Registering new devices can take time depending on the device and
        network conditions. The request route provide a non-blocking way of
        sending the request. Requests that pass initial validation will return
        with with a request ID which can be queried to find out the status of
        the request. The status of the request will display whether the
        request has been completed and whether it was successful.

        scope: request

        Args:
            account_id: Account ID
            device_esn: ESN of new device.
            device_iccid (optional): The mobile device's ICCID, or SIM card
                serial number. This is optional, only if the device does not
                have an ICCID. If the device has an ICCID and it is not
                included in the request, the request will likely fail.

        Returns:
            Change Device Request Status object.
        """
        return bind_api(
            api=self,
            path='/accounts/{account_id}/device_change_requests',
            method='POST',
            post_container='device_change_request',
            payload_type='request',
            allowed_param=['account_id', 'device_esn', 'device_iccid'])

    @property
    def change_device_status(self):
        """Get the status of a device change request.

        scope: public

        Args:
            request_id: The ID of the change device request.

        Returns:
            list: List of Device Request Status objects.
        """
        return bind_api(
            api=self,
            path='/device_change_requests/{request_id}',
            payload_type='request',
            payload_list=True,
            allowed_param=['request_id'])

    # Change Phone Number
    @property
    def change_phone_number(self):
        """Creates a request to change the phone number of an Account.

        Change phone number requsts allow you to change the phone number on an
        account. Change Phone Number requests do not allow you choose your new
        phone number, you will be assigned an available number.

        The request route provide a non-blocking way of sending the request.
        Requests that pass initial validation will return with with a request
        ID which can be queried to find out the status of the request. The
        status of the request will display whether the request has been
        completed and whether it was successful.

        scope: request

        Args:
            account_id: Account ID

        Returns:
            Change Phone Number Request Status object.
        """
        return bind_api(
            api=self,
            path='/accounts/{account_id}/phone_number_change_requests',
            method='POST',
            payload_type='request',
            allowed_param=['account_id'])

    @property
    def change_phone_number_status(self):
        """Get the status of a phone number change request.

        scope: public

        Args:
            request_id:

        Returns:
            list: List of Change Phone Number Request Status objects.
        """
        return bind_api(
            api=self,
            path='/phone_number_change_requests/{request_id}',
            payload_type='request',
            payload_list=True,
            allowed_param=['request_id'])

    # Enforced Carrier Services
    @property
    def enforced_carrier_services(self):
        """List the applied enforced carrier services of an Account.

        Enforced Carrier Services are services offered at the carrier level
        that have been enforced on an account. These are not the only services
        that may be active on a given account, but are sure to override any
        other policies.

        scope: public

        Args:
            account_id: Account ID
            page (optional): Which page of the paged results to return.
                Default to 1.
            per_page (optional): How many results to return per page.
                Defaults to 25.

        Returns:
            list: List of Carrier Service objects.
        """
        return bind_api(
            api=self,
            path='/accounts/{account_id}/enforced_carrier_services',
            payload_type='carrier_service',
            payload_list=True,
            allowed_param=['account_id', 'page', 'per_page'])

    # Fluid Call
    @property
    def fluid_call_credentials(self):
        """Get the list of FluidCall credentials.

        FluidCall allows any VoIP phone to act as an additional handset
        attached to an account. Currently, any number of additional FluidCall
        connections can be made to a single account. Those connections will be
        rung along with the primary handset, and can make calls using standard
        SIP/RTP VoIP protocols.

        scope: public

        Args:
            account_id: Account ID
            page (optional): Which page of the paged results to return.
                Default to 1.
            per_page (optional): How many results to return per page.
                Defaults to 25.

        Returns:
            list: List of Fluid Call objects.
        """
        return bind_api(
            api=self,
            path='/accounts/{account_id}/fluidcall_credentials',
            payload_type='fluidcall',
            payload_list=True,
            allowed_param=['account_id', 'page', 'per_page'])

    # Phone Calls
    @property
    def calls(self):
        """Returns an account's paged phone call details.

        scope: public

        Args:
            account_id: Account ID
            start_date (datetime, optional): Return only records occurring
                after this date.
            end_date (datetime, optional): Return only records occurring
                before this date.
            per_page (optional): How many results to return per page.
                Defaults to 25.
            page (optional): Which page of the paged results to return.
                Default to 1.

        Returns:
            list: List of Call objects.
        """
        return bind_api(
            api=self,
            path='/accounts/{account_id}/phone_calls',
            payload_type='call',
            payload_list=True,
            allowed_param=['account_id', 'start_date',
                           'end_date', 'per_page', 'page'])

    # Phone Texts
    @property
    def texts(self):
        """Returns an account's paged phone text details.

        scope: public

        Args:
            account_id: Account ID
            start_date (datetime, optional): Return only records occurring
                after this date.
            end_date (datetime, optional): Return only records occurring
                before this date.
            per_page (optional): How many results to return per page.
                Defaults to 25.
            page (optional): Which page of the paged results to return.
                Default to 1.

        Returns:
            list: List of Text objects.
        """
        return bind_api(
            api=self,
            path='/accounts/{account_id}/phone_texts',
            payload_type='text',
            payload_list=True,
            allowed_param=['account_id', 'start_date',
                           'end_date', 'per_page', 'page'])

    # Phone Data
    @property
    def data(self):
        """Return an account's paged phone data details.

        scope: public

        Args:
            account_id: Account ID
            start_date (datetime, optional): Return only records occurring
                after this date.
            end_date (datetime, optional): Return only records occurring
                before this date.
            per_page (optional): How many results to return per page.
                Defaults to 25.
            page (optional): Which page of the paged results to return.
                Default to 1.

        Returns:
            list: List of Data objects.
        """
        return bind_api(
            api=self,
            path='/accounts/{account_id}/phone_data',
            payload_type='data',
            payload_list=True,
            allowed_param=['account_id', 'start_date',
                           'end_date', 'per_page', 'page'])

    # Users
    @property
    def get_user(self):
        """Return a specific user's details.

        scope: public

        Args:
            user_id: User ID

        Returns:
            User object.
        """
        return bind_api(
            api=self,
            path='/users/{user_id}',
            payload_type='user',
            allowed_param=['user_id'])

    @property
    def users(self):
        """Return all Users you have access to.

        scope: public

        Args:
            email_address (optional): The email_address of the account to
                filter by. Currently does not partial or full text search.
            per_page (optional): How many results to return per page.
                Defaults to 25.
            page (optional): Which page of the paged results to return.
                Default to 1.

        Returns:
            list: List of User objects.
        """
        return bind_api(
            api=self,
            path='/users',
            payload_type='user',
            payload_list=True,
            allowed_param=['email_address', 'per_page', 'page'])

    @property
    def update_user(self):
        """Update a User's account.

        scope: manage

        Args:
            user_id: User ID
            email (optional): New email.
            password (optional): New password.
        """
        return bind_api(
            api=self,
            path='/users/{user_id}',
            method='PUT',
            post_container='user',
            allowed_param=['user_id', 'email', 'password'])

    # Voicemail Messages
    @property
    def voicemail(self):
        """Return an Account's paged voicemail messages.

        scope: voicemail

        Args:
            voicemail_box_id: ID of the voicemail box.
            only_new (optional):
            per_page (optional): How many results to return per page.
                Defaults to 25.
            page (optional): Which page of the paged results to return.
                Default to 1.

        Returns:
            list: Paged list of voicemail message objects.
        """
        return bind_api(
            api=self,
            path='/voicemail_boxes/{voicemail_box_id}/voicemail_messages',
            payload_type='voicemail',
            payload_list=True,
            allowed_param=['voicemail_box_id', 'only_new', 'per_page', 'page'])

    @property
    def delete_voicemail(self):
        """Deletes a voicemail message.

        scope: voicemail

        Args:
            voicemail_message_id:
        """
        return bind_api(
            api=self,
            path='/voicemail_messages/{voicemail_message_id}',
            allowed_param=['voicemail_message_id'],
            method='DELETE')
