# copyright 2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.
"""cubicweb-oaipmh views for OAI-PMH export

Set hierarchy specification
---------------------------

Sets_ are optional construct for selective harvesting. The scheme used to
define the syntax of sets is usually specific to the community using the
OAI-PMH exchange protocol. This OAI-PMH implementation exposes the following
set hierarchy.

- The first level of hierarchy refers to the entity type to perform the
  selective request on, e.g. for a `ListIdentifiers` verb:

      <baseurl>/oai?verb=ListIdentifiers&set=agent

  would return the identifiers of entities of type Agent found in the repository.

- The second level of hierarchy refers to a filtering criterion on selected
  entity type, usually an attribute with respect to the application schema,
  and is tight to a value of this criterion (attribute) to filter entities on.
  For instance:

      <baseurl>/oai?verb=ListIdentifiers&set=agent:kind:person

  would return the identifiers of entities of type Agent of kind 'person'.

.. _Set:
.. _Sets: http://www.openarchives.org/OAI/openarchivesprotocol.html#Set
"""

from datetime import datetime, timedelta

from isodate import datetime_isoformat
import dateutil.parser
from lxml import etree
from lxml.builder import E, ElementMaker
import pytz

from logilab.common.registry import objectify_predicate

from cubicweb.predicates import ExpectedValuePredicate, match_form_params
from cubicweb.view import View
from cubicweb.web.views import urlrewrite

from cubes.oaipmh import utcnow, ResumptionToken


def utcparse(timestr):
    """Parse a date/time string as an UTC datetime."""
    date = dateutil.parser.parse(timestr)
    if date.tzinfo is None:
        if 'T' in timestr:
            raise ValueError('cannot parse a date with time but no timezone')
        else:
            # No time, assume UTC.
            return date.replace(tzinfo=pytz.utc)
    else:
        # Convert to UTC.
        return date.astimezone(pytz.utc)


class match_verb(ExpectedValuePredicate):
    """Predicate checking `verb` request form parameter presence and value.

    Return 2 in case of match, for precedence over
    ``match_form_params('verb')``.
    """

    def __call__(self, cls, req, rset=None, **kwargs):
        verb = req.form.get('verb')
        if verb is None:
            return 0
        return 2 * int(verb in self.expected)


def filter_none(mapping):
    """Return a dict from `mapping` with None values filtered out."""
    out = {}
    for key, val in mapping.iteritems():
        if val is not None:
            out[key] = val
    return out


def oai_records(rset):
    """Yield OAIRecord items from a result set."""
    for entity in rset.entities():
        record = entity.cw_adapt_to('IOAIPMHRecord')
        if not record:
            continue
        yield OAIRecord(record)


def xml_metadataformat(prefix, mformat):
    """Return the XML representation of a MetadataFormat object."""
    return E.metadataFormat(
        E.metadataPrefix(prefix),
        E.schema(mformat.schema),
        E.metadataNamespace(mformat.namespace),
    )


class OAIError(Exception):
    """Error in OAI-PMH request."""

    def __init__(self, errors):
        super(OAIError, self).__init__()
        self.errors = errors


class IdDoesNotExist(OAIError):
    """The value of the identifier argument is unknown or illegal in this
    repository.
    """

    def __init__(self, identifier):
        msg = 'no entity with OAI identifier {0} in repository'.format(
            identifier)
        errors = {'idDoesNotExist': msg}
        super(IdDoesNotExist, self).__init__(errors)


class OAIRequest(object):
    """Represent an OAI-PMH request."""

    @classmethod
    def from_request(cls, baseurl, request):
        form = request.form
        return cls(
            baseurl,
            setspec=form.get('set'),
            verb=form.get('verb'),
            identifier=form.get('identifier'),
            from_date=form.get('from'),
            until_date=form.get('until'),
            resumption_token=form.get('resumptionToken'),
            metadata_prefix=form.get('metadataPrefix'),
        )

    def __init__(self, baseurl, verb=None, setspec=None, identifier=None,
                 from_date=None, until_date=None, resumption_token=None,
                 metadata_prefix=None):
        self.baseurl = baseurl
        self.verb = verb
        self.setspec = setspec
        self.identifier = identifier
        self.errors = {}
        self.resumption_token = ResumptionToken.parse(resumption_token)
        # Parse "from" and "until" dates, which are, by specification
        # expressed in UTC.
        from_date = self.resumption_token.from_date or from_date
        if from_date is not None:
            from_date = utcparse(from_date)
        until_date = self.resumption_token.until_date or until_date
        if until_date is not None:
            until_date = utcparse(until_date)
        if (from_date is not None and until_date is not None and
                from_date > until_date):
            msg = 'the from argument must be less than or equal to the until argument'
            self.errors['badArgument'] = msg
        self.from_date = from_date
        self.until_date = until_date
        self.metadata_prefix = self.resumption_token.metadata_prefix or metadata_prefix

    def __repr__(self):
        return etree.tostring(self.to_xml())

    def rset_from_identifier(self, cnx):
        """Return a ResultSet corresponding to request identifier."""
        oai = cnx.vreg['components'].select('oai', cnx)
        return oai.match_identifier(self.identifier)

    def rset(self, cnx):
        """Return a result set with a resumptionToken information from OAI-PMH
        request by using any provided set specifier, from/until dates and
        previous token.
        """
        dates = {'from_date': self.from_date,
                 'until_date': self.until_date}
        oai = cnx.vreg['components'].select('oai', cnx)
        try:
            rset, next_eid = oai.match(
                self.setspec, metadata_prefix=self.metadata_prefix,
                from_eid=self.resumption_token.eid, **dates)
        except ValueError:
            raise OAIError(
                {'noRecordsMatch': 'invalid set specifier {0}'.format(self.setspec)})
        if not rset:
            if self.resumption_token:
                raise OAIError(
                    {'badResumptionToken': ('The value of the resumptionToken '
                                            'argument is invalid or expired.')})
            raise OAIError(
                {'noRecordsMatch': ('The combination of the values of the '
                                    'from, until, and set arguments results '
                                    'in an empty list.')})
        return rset, next_eid

    def new_token(self, eid):
        """Return a resumptionToken XML element or None built from request
        parameters and the `eid` of the next entity to return upon
        continuation of the request.

        * return a resumptionToken with a value if there are more result to be
        fetched;
        * return an empty resumptionToken if this response completes and the
        request contains a resumptionToken;
        * None otherwise.
        """
        if eid is not None:
            if self.resumption_token:
                # Reuse previous token, just updating "eid" field.
                token = self.resumption_token
                token.eid = eid
            else:
                token = ResumptionToken(eid, self.setspec, self.from_date,
                                        self.until_date, self.metadata_prefix)
            expire = datetime_isoformat(
                datetime.now(pytz.utc) + timedelta(hours=1))
            return E.resumptionToken(token.encode(), expirationDate=expire)
        elif self.resumption_token:
            return E.resumptionToken()

    def to_xml(self, errors=None):
        if not errors:
            # In cases where the request that generated this response resulted
            # in a badVerb or badArgument error condition, the repository must
            # return the base URL of the protocol request only. Attributes
            # must not be provided in these cases.
            attributes = {
                'verb': self.verb,
                'identifier': self.identifier,
                'set': self.setspec,
            }
            if self.from_date:
                attributes['from'] = datetime_isoformat(self.from_date)
            if self.until_date:
                attributes['until'] = datetime_isoformat(self.until_date)
            if self.metadata_prefix:
                attributes['metadataPrefix'] = self.metadata_prefix
            if self.resumption_token:
                attributes['resumptionToken'] = self.resumption_token.encode()
        else:
            attributes = {}
        attributes = filter_none(attributes)
        return E.request(self.baseurl, **attributes)


class OAIResponse(object):
    """Represent an OAI-PMH response."""

    def __init__(self, oai_request):
        self.oai_request = oai_request

    @staticmethod
    def _build_errors(errors):
        """Return a list of <error> tag from `errors` dict."""
        return [E.error(msg, code=code)
                for code, msg in errors.iteritems()]

    def body(self, content=None, errors=None):
        """Return a list of body items of the OAI-PMH response."""
        def check_content(content):
            assert content is not None, (
                'unexpected empty content while no error got reported')

        oai_request = self.oai_request
        if errors:
            return self._build_errors(errors)
        check_content(content)
        try:
            return [E(oai_request.verb, *content)]
        except OAIError as exc:
            return self._build_errors(exc.errors)
        except TypeError:
            # Usually something wrong with `content` generator, try to unpack
            # it to get a meaningful error.
            content = list(content)
            check_content(content)
            return [E(oai_request.verb, *content)]

    def to_xml(self, content=None, errors=()):
        date = E.responseDate(datetime_isoformat(utcnow()))
        request = self.oai_request.to_xml(errors)
        body_elems = self.body(content, errors=errors)
        nsmap = {None: 'http://www.openarchives.org/OAI/2.0/',
                 'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
        maker = ElementMaker(nsmap=nsmap)
        attributes = {
            '{%s}schemaLocation' % nsmap['xsi']: ' '.join([
                'http://www.openarchives.org/OAI/2.0/',
                'http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd'
            ])
        }
        return maker('OAI-PMH', date, request, *body_elems, **attributes)


class OAIRecord(object):
    """Represent an OAI record built from an entity adapted as IOAIPMHRecord.
    """

    def __init__(self, record):
        self.record = record

    def header(self, prefix):
        """The <header> part of an OAI-PMH record.

        See http://www.openarchives.org/OAI/openarchivesprotocol.html#header
        for a description of elements of a "header".
        """
        if prefix not in self.record.metadata_formats:
            raise OAIError(
                {'noRecordsMatch': 'unsupported metadata prefix "{0}"'.format(prefix)})
        # TODO: add setSpec tag for each record.
        tags = []
        for tag in ('identifier', 'datestamp'):
            value = getattr(self.record, tag)
            if value:
                tags.append(E(tag, value))
        attrs = {}
        if self.record.deleted:
            attrs['status'] = 'deleted'
        return E.header(*tags, **attrs)

    def metadata(self, prefix):
        """The <metadata> part of an OAI-PMH record."""
        if self.record.deleted:
            return None
        try:
            metadata = self.record.metadata(prefix)
        except ValueError as exc:
            raise OAIError({'noRecordsMatch': str(exc)})
        if metadata:
            return E.metadata(etree.XML(metadata))
        return None

    def metadata_formats(self):
        for prefix, (fmt, _) in self.record.metadata_formats.iteritems():
            yield xml_metadataformat(prefix, fmt)

    def to_xml(self, prefix):
        """Return the <record> XML element."""
        elems = [self.header(prefix)]
        metadata = self.metadata(prefix)
        if metadata is not None:  # deleted record
            elems.append(metadata)
        return E.record(*elems)


class OAIPMHRewriter(urlrewrite.SimpleReqRewriter):
    rules = [('/oai', dict(vid='oai'))]


class OAIView(View):
    """Base class for any OAI view, subclasses should either implement
    `errors` or `verb_content` methods.
    """
    __regid__ = 'oai'
    __abstract__ = True
    templatable = False
    content_type = 'text/xml'
    binary = True

    @staticmethod
    def verb_content():
        return

    @staticmethod
    def errors():
        """Return the errors of the OAI-PMH request."""
        return {}

    def __init__(self, *args, **kwargs):
        super(OAIView, self).__init__(*args, **kwargs)
        self.oai_request = OAIRequest.from_request(
            self._cw.build_url('oai'), self._cw)

    def call(self):
        encoding = self._cw.encoding
        assert encoding == 'UTF-8', 'unexpected encoding {0}'.format(encoding)
        self.w('<?xml version="1.0" encoding="%s"?>\n' % encoding)
        oai_response = OAIResponse(self.oai_request)
        # combine errors coming from view selection with those of request
        # processing.
        errors = self.errors()
        errors.update(self.oai_request.errors)
        response_elem = oai_response.to_xml(self.verb_content(), errors=errors)
        self.w(etree.tostring(response_elem, encoding='utf-8'))


class OAIBaseView(OAIView):
    """Base view for OAI-PMH request with no "verb" specified.

    `verb` request parameter is necessary in our implementation.
    """

    def errors(self):
        return {'badVerb': 'no verb specified'}


class OAIWithVerbView(OAIView):
    """Base view for OAI-PMH request with a "verb" specified.

    This view generated an error as the implementation relies on explicit view
    to handle supported verbs.
    """
    __select__ = match_form_params('verb')

    def errors(self):
        """Return the errors of the OAI-PMH request."""
        return {'badVerb': 'illegal verb "{0}"'.format(self.oai_request.verb)}


class OAIIdentifyView(OAIView):
    """View handling verb="Identify" requests."""
    __select__ = match_verb('Identify')

    def verb_content(self):
        oai = self._cw.vreg['components'].select('oai', self._cw)
        yield E('repositoryName', self._cw.property_value('ui.site-title'))
        # XXX Should match the URL rewrite rule.
        yield E('baseURL', self._cw.build_url('oai'))
        yield E('protocolVersion', '2.0')
        try:
            admin_email = self._cw.vreg.config['admin-email']
        except KeyError:
            pass
        else:
            yield E('adminEmail', admin_email)
        oldest = self._cw.execute(
            'Any D WHERE X creation_date D, X identity MX'
            ' WITH MX BEING (Any MIN(X))')[0][0]
        yield E('earliestDatestamp', datetime_isoformat(oldest))
        yield E('deletedRecord', oai.deleted_handling)
        yield E('granularity', 'YYYY-MM-DDThh:mm:ssZ')


@objectify_predicate
def no_params_in_form(cls, req, **kwargs):
    """Return 1 if req.form only has "verb" (and "vid") parameters."""
    extra = set(req.form) - set(['verb', 'vid'])
    return 0 if extra else 1


class OAIIdentifyBadArgumentsView(OAIView):
    """View handling verb="Identify" requests but with bad arguments"""
    __select__ = match_verb('Identify') & ~no_params_in_form()

    def errors(self):
        return {
            'badArgument': 'Identify accepts no argument'}


class OAIListMetadatFormatsView(OAIView):
    """View handling verb="ListMetadataFormats" requests for the whole
    repository.
    """
    __select__ = match_verb('ListMetadataFormats')

    def verb_content(self):
        oai = self._cw.vreg['components'].select('oai', self._cw)
        for prefix, fmt in oai.metadata_formats():
            yield xml_metadataformat(prefix, fmt)


class OAIListMetadatFormatsByIdentifierView(OAIView):
    """View handling verb="ListMetadataFormats" requests."""
    __select__ = (match_verb('ListMetadataFormats')
                  & match_form_params('identifier'))

    def verb_content(self):
        rset = self.oai_request.rset_from_identifier(self._cw)
        if not rset:
            raise IdDoesNotExist(self.oai_request.identifier)
        for record in oai_records(rset):
            for fmt in record.metadata_formats():
                yield fmt


class OAIListSetsView(OAIView):
    """View handling verb="ListSets" requests."""
    __select__ = match_verb('ListSets')

    @staticmethod
    def build_set(spec, name=u''):
        """Return a "set" element"""
        return E('set', E.setSpec(spec), E.setName(name))

    def verb_content(self):
        oai = self._cw.vreg['components'].select('oai', self._cw)
        for spec, description in oai.setspecs():
            yield self.build_set(spec, name=self._cw._(description))


class OAIListIdentifiersView(OAIView):
    """View handling verb="ListIdentifiers" requests.

    This view returns an error as it handles cases where no "set" selection is
    specified.
    """
    __select__ = match_verb('ListIdentifiers')

    def errors(self):
        return {
            'badArgument': 'ListIdentifiers verb requires a "metadataPrefix" restriction'}


class OAIListIdentifiersWithSetView(OAIView):
    """View handling verb="ListIdentifiers" requests with "set" selection."""
    __select__ = match_verb('ListIdentifiers') & match_form_params('metadataPrefix')

    def verb_content(self):
        rset, token = self.oai_request.rset(self._cw)
        for record in oai_records(rset):
            yield record.header(self.oai_request.metadata_prefix)
        new_token = self.oai_request.new_token(token)
        if new_token is not None:
            yield new_token


class OAIListRecordsErrorView(OAIView):
    """View handling verb="ListRecords" requests when arguments are missing."""
    __select__ = match_verb('ListRecords')

    def errors(self):
        return {
            'badArgument': 'ListRecords verb requires a "metadataPrefix" restriction'}


class OAIListRecordsView(OAIView):
    """View handling verb="ListRecords"."""
    __select__ = (match_verb('ListRecords')
                  & (match_form_params('metadataPrefix')
                     | match_form_params('resumptionToken')))

    def verb_content(self):
        rset, token = self.oai_request.rset(self._cw)
        for record in oai_records(rset):
            yield record.to_xml(self.oai_request.metadata_prefix)
        new_token = self.oai_request.new_token(token)
        if new_token is not None:
            yield new_token


class OAIGetRecordErrorView(OAIView):
    """View handling verb="GetRecord" requests when arguments are missing."""
    __select__ = match_verb('GetRecord')

    def errors(self):
        return {'badArgument': ('GetRecord verb requires "identifier" and '
                                '"metadataPrefix" arguments')}


class OAIGetRecordMissingIdentifierView(OAIView):
    """View handling verb="GetRecord" requests when "identifier" is missing.
    """
    __select__ = match_verb('GetRecord') & match_form_params('metadataPrefix')

    def errors(self):
        return {'badArgument': 'GetRecord verb requires "identifier" restriction'}


class OAIGetRecordMissingMetadataPrefixView(OAIView):
    """View handling verb="GetRecord" requests when metadataPrefix argument is
    missing.
    """
    __select__ = match_verb('GetRecord') & match_form_params('identifier')

    def errors(self):
        return {'badArgument': 'GetRecord verb requires "metadataPrefix" restriction'}


class OAIGetRecordView(OAIView):
    """View handling verb="GetRecord" with proper arguments."""
    __select__ = (match_verb('GetRecord')
                  & match_form_params('identifier', 'metadataPrefix'))

    def verb_content(self):
        rset = self.oai_request.rset_from_identifier(self._cw)
        for record in oai_records(rset):
            if record is not None:
                yield record.to_xml(self.oai_request.metadata_prefix)
                break
        else:
            raise IdDoesNotExist(self.oai_request.identifier)
