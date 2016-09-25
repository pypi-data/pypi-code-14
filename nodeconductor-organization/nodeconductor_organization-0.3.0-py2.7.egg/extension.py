from nodeconductor.core import NodeConductorExtension


class OrganizationExtension(NodeConductorExtension):

    @staticmethod
    def django_app():
        return 'nodeconductor_organization'

    @staticmethod
    def rest_urls():
        from .urls import register_in
        return register_in
