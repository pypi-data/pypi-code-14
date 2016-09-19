
from . import _VDAPIService, _VDAPIResponse

class _DomainListResponse(_VDAPIResponse):
    """
    Override to give you access to the actual domains
    """

    def get_domains(self, **kwargs):
        """
        Get the list of domains that are in this domain list

            d = springserve.domain_list.get(id)
            domains = d.get_domains()

            for domain in domains:
                print domain.name

        """
        return self._service.get("{}/domains".format(self.id), **kwargs)
    
    def _to_list(self, input_list):
        """
        The api needs a list, and you can't serialize sets, or Series
        """
        if isinstance(input_list, list):
            return input_list

        return [x for x in input_list]

    def add_domains(self, domains):
        """
        Add a list of domains to this domain list

            d = springserve.domain_list.get(id)
            d.add_domains(['blah.com', 'blah2.com'])

        domains: List of domains you would like to add 
        """
        payload = {'names':self._to_list(domains)}
        resp = self._service.post(payload,
                                  path_param='{}/domains/bulk_create'.format(self.id)
                                 )
        return resp

    def remove_domains(self, domains):
        """
        Add a list of domains to this domain list

            d = springserve.domain_list.get(id)
            d.remove_domains(['blah.com', 'blah2.com'])

        domains: List of domains you would like to add 
        """
        payload = {'names':self._to_list(domains)}
        resp = self._service.bulk_delete(payload,
                                  path_param='{}/domains/bulk_delete'.format(self.id)
                                 )
        return resp



class _DomainListAPI(_VDAPIService):

    __API__ = "domain_lists"
    __RESPONSE_OBJECT__ = _DomainListResponse

    
