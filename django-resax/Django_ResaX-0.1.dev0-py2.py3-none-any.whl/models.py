# coding: utf-8

from __future__ import unicode_literals

import collections
import pytz

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db import transaction
from django.db.models import Sum
from django.utils import six
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

#
# Footprint
#

@python_2_unicode_compatible
class Footprint(models.Model):
    add_date = models.DateTimeField(_("creation date"), auto_now_add=True)
    mod_date = models.DateTimeField(_("modification date"), auto_now=True)
    add_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("user who created"), related_name='+', null=True, editable=False)
    mod_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("user who modified"), related_name='+', null=True, editable=False)
    words = models.TextField(_("search words"), default="", editable=False)
    leafs = models.ManyToManyField('self', verbose_name=_("leafs"), related_name='roots', symmetrical=False, editable=False)
    object_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_("object type"), related_name='+', editable=False)

    words_list = []

    class Meta:
        verbose_name = _("footprint")
        verbose_name_plural = _("footprints")

    def __str__(self):
        if self.pk is None:
            return _("<Footprint*/%(object_type)s> created on %(date)s") % {
                'object_type': self.object_type,
                'date': self.add_date,
            }
        else:
            return _("<Footprint:%(id)s/%(object_type)s> modified on %(date)s") % {
                'object_type': self.object_type,
                'id': self.pk,
                'date': self.mod_date,
            }

    @transaction.atomic
    def save(self, *args, **kwargs):
        cur_user = get_current_user()
        if cur_user:
            self.mod_user = cur_user
            if self.pk is None:
                self.add_user = cur_user

        if self.pk is None:
            self.object_type = ContentType.objects.get_for_model(self.__class__)

        if 'update_fields' in kwargs:
            kwargs['update_fields'] = list(set(list(kwargs['update_fields']) + ['mod_date', 'mod_user', 'words']))

        self.set_words()

        res = super(Footprint, self).save(*args, **kwargs)

        self.update_roots()

        return res

    @transaction.atomic
    def delete(self, *args, **kwargs):
        roots = list(self.roots.all())

        res = super(Footprint, self).delete(*args, **kwargs)

        self.update_roots(roots)

        return res

    @transaction.atomic
    def addLeaf(self, leaf):
        self.leafs.add(leaf)
        self.save(update_fields = ['mod_date'])

    @transaction.atomic
    def update_roots(self, roots=None):
        if roots is None:
            if not hasattr(self, 'roots'):
                return
            roots = list(self.roots.all())

        for root in roots:
            obj = root.get_object()
            obj.full_clean()
            obj.save(update_fields = [])

    def get_object(self):
        """
        Returns, if possible, the object owning this footprint.
        """
        if self.pk and hasattr(self, 'related_%s' % self.object_type.model):
            return getattr(self, 'related_%s' % self.object_type.model)
        else:
            return None

    def set_words(self):
        """
        Constructs the ‘words’ attribute. This attribute is used by the search engine.
        """
        words_list = self.words_list[:]

        # makes typecasting from any iterable
        words_list = list(words_list)

        # adds owner info
        if self.add_user:
            words_list.append(self.add_user.get_full_name())
        if self.mod_user:
            words_list.append(self.mod_user.get_full_name())

        # adds log info
        for log in self.logs.all():
            if log.user:
                words_list.append(log.user.get_full_name())
            words_list.append(log.contents)
            words_list.append(log.attachment_name)

        # detects words and cleans whitespaces
        words = utils.split_words(' '.join(words_list))

        # saves changes
        self.words = words.lower()

    def pk_or_asterisk(self):
        """
        Returns an asterisk (*) if the object does not exist in the database (yet).
        Otherwise, returns an empty string.
        """
        if self.pk is None:
            return "*"
        else:
            return ":%d" % self.pk

class FootprintObject(Footprint):
    fp = models.OneToOneField(Footprint, on_delete=models.CASCADE, verbose_name=_("footprint"), related_name='related_%(class)s', parent_link=True)

    class Meta:
        abstract = True


#
# Domain-specific models
#

@python_2_unicode_compatible
class Organisation(models.Model):
    """
    Représente une organisation utilisatrice de l'API.
    """
    #: Nom de l'organisation
    name = models.CharField(_("name"), max_length=255, unique=True)
    #: Drapeau indiquant si l'organisation a été supprimée ou non
    deleted = models.BooleanField(_("deleted"), default=False)

    class Meta:
        verbose_name = _("organisation")
        verbose_name_plural = _("organisations")

    def __unicode__(self):
        return self.name

    @transaction.atomic
    def add_user(self):
        """
        Ajoute un nouveau membre (utilisateur) à l'organisation.

        :rtype: User
        """
        return self.users.create()

    @transaction.atomic
    def add_resource_type(self, name, resources=None):
        """
        Ajoute un nouveau type de ressource à l'organisation.
        Si l'argument *resources* est spécifié, il doit être
        un dictionnaire ayant pour clé le nom de la ressource
        et pour valeur sa quantité en stock.

        :param name:
            nom du type de ressource
        :type name: str
        :param resources:
            dictionnaire facultatif contenant les ressources à
            créer de ce type. Chaque clé doit correspondre au
            nom de la ressource, et chaque valeur doit indiquer
            la quantité disponible en stock
        :type resources: dict
        :rtype: ResourceType
        """
        if resources is None:
            resources = {}

        resource_type = ResourceType(name=name)
        resource_type.organisation = self
        resource_type.full_clean()
        resource_type.save(force_insert=True)

        for name, stock in resources.items():
            resource_type.add_resource(name, stock)

        return resource_type

    @transaction.atomic
    def add_activity(self, name, stock=1, resources=None):
        """
        Ajoute une activité à l'organisation.

        :param name:
            nom de l'activité
        :type name: str
        :param stock:
            nombre de places disponibles pour l'activité
        :type stock: int
        :param resources:
            dictionnaire facultatif contenant les ressources à
            ajouter à cette activité. Chaque clé doit correspondre
            à une ressource, et chaque valeur doit indiquer
            la quantité requise pour l'activité
        :type resources: dict
        :rtype: Activity
        """
        if resources is None:
            resources = {}

        activity = Activity(name=name, stock=stock)
        activity.organisation = self
        activity.full_clean()
        activity.save(force_insert=True)

        for resource, quantity in resources.items():
            if resource.organisation != self:
                raise ValidationError(_("Resource %s doesn't belong to this organisation.") % resource)

            activity.add_resource(resource, quantity)

        return activity

    @transaction.atomic
    def add_reservation_type(self, name, resources=None):
        """
        Ajoute un type de réservation à l'organisation.
        Si l'argument *resources* est spécifié, il doit être
        une liste contenant les ressources autorisées pour
        ce type de réservation.

        :param name:
            nom du type de réservation
        :type name: str
        :param resources:
            liste facultative contenant les ressources autorisées
            pour ce type de réservation
        :type resources: list
        :rtype: ReservationType
        """
        if resources is None:
            resources = []

        if not isinstance(resources, collections.Iterable):
            resources = [resources]

        reservation_type = ReservationType(name=name)
        reservation_type.organisation = self
        reservation_type.full_clean()
        reservation_type.save(force_insert=True)

        for resource in resources:
            if resource.organisation != self:
                raise ValidationError(_("Resource %s doesn't belong to this organisation.") % resource)

            reservation_type.add_resource(resource)

        return reservation_type


class User(models.Model):
    """
    Représente un utilisateur (membre) d'une organisation.
    """
    user_id = models.AutoField(primary_key=True)
    #: L'organisation à laquelle appartient l'utilisateur
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, verbose_name=_("organisation"), related_name='users')
    #: Liste des évènements réservés par l'utilisateur
    events = models.ManyToManyField('Event', through='Reservation', verbose_name=_("events"), related_name='users')

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __unicode__(self):
        return "User %s" % self.pk

    def check_reservation_params(self, reservation_object, date_start, date_stop):
        if date_start < timezone.now():
            raise ValidationError(_("The starting date must be greater than the current date"))
        if date_stop <= date_start:
            raise ValidationError(_("The ending date must be greater than the starting date"))
        if reservation_object.organisation != self.organisation:
            raise ValidationError(_("This doesn't belong to the organisation of the chosen reservation object"))

    @transaction.atomic
    def book_event(self, event, quantity=1):
        """
        Réserve *quantity* places pour l'évènement *event*.

        :param event:
            évènement à réserver
        :type event: Event
        :param quantity:
            nombre de places à réserver
        :type quantity: int
        :rtype: Reservation
        """
        return event.book(self, quantity)

    @transaction.atomic
    def book_resources(self, reservation_type, date_start, date_stop, resources=None):
        r"""
        Crée une réservation flexible.

        :param reservation_type:
            type de réservation
        :type reservation_type: ReservationType
        :param date_start:
            date de début de la réservation
        :param date_stop:
            date de fin de la réservation
        :param resources:
            dictionnaire facultatif contenant les ressources à réserver.
            Ce dictionnaire doit être composé d'un ensemble de clés et de valeurs, où chaque
            clé réprésente la ressource à réserver, et chaque valeur la quantité demandée
        :type resources: dict
        :rtype: FlexiReservation
        """
        if resources is None:
            resources = {}

        self.check_reservation_params(reservation_type, date_start, date_stop)

        allowed_resources = reservation_type.resources.filter(pk__in=[r.pk for r in resources.keys()]).only('pk')
        allowed_resources = allowed_resources.select_for_update()

        for resource, quantity in resources.items():
            if resource not in allowed_resources:
                raise ValidationError(_("Resource %s is not avaible for this reservation type") % resource)
            available_stock = resource.get_available_stock(date_start, date_stop)
            if available_stock < quantity:
                raise ValidationError(_("Not enough stock for resource %s") % resource)

        event = Event(date_start=date_start, date_stop=date_stop, stock=1)
        event.save(force_insert=True)
        reservation = FlexiReservation(reservation_type=reservation_type, user=self, event=event)
        reservation.save(force_insert=True)
        event.full_clean()
        reservation.full_clean()

        for resource, quantity in resources.items():
            reservation.add_resource(resource, quantity)

        return reservation


class ResourceType(models.Model):
    """
    Représente un type de ressource.
    """
    #: Organisation à laquelle appartient le type de ressource
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, verbose_name=_("organisation"), related_name='resource_types')
    #: Nom du type de ressource
    name = models.CharField(_("name"), max_length=255)
    #: Drapeau indiquant que le type de ressource est supprimé
    deleted = models.BooleanField(_("deleted"), default=False)

    class Meta:
        verbose_name = _("resource type")
        verbose_name_plural = _("resource types")
        unique_together = ('organisation', 'name')

    def __unicode__(self):
        return self.name

    @transaction.atomic
    def add_resource(self, name, stock=1):
        resource = Resource(name=name, stock=stock)
        resource.resource_type = self
        resource.full_clean()
        resource.save(force_insert=True)

        return resource


class Resource(models.Model):
    """
    Représente une ressource.
    """
    #: Type de la ressource
    resource_type = models.ForeignKey(ResourceType, on_delete=models.CASCADE, verbose_name=_("resource type"), related_name='resources')
    #: Nom de la ressource
    name = models.CharField(_("name"), max_length=255)
    #: Sotck disponible pour la ressource. 0 signifie que la stock est illimité.
    stock = models.PositiveIntegerField(_("stock"), default=0)
    #: Drapeau indiquant que la ressource est supprimée
    deleted = models.BooleanField(_("deleted"), default=False)

    class Meta:
        verbose_name = _("resource")
        verbose_name_plural = _("resources")
        unique_together = ('resource_type', 'name')

    def __unicode__(self):
        return "%s" % self.name

    @property
    def organisation(self):
        return self.resource_type.organisation

    def get_available_stock(self, date_start, date_stop, exclude_event=None):
        """
        Retour la quantité disponible de la ressource sur la période
        entre les dates *date_start* et *date_stop* spécifiées.

        Si *exclude_event* est spécifié, cet évènement n'est pas pris
        en compte dans les résultats.

        :param date_start:
            date de début de disponibilité recherchée pour la ressource
        :param date_stop:
            date de fin de disponibilité recherchée pour la ressource
        :param exclude_event:
            évènement facultatif à ne pas prendre en compte pour le
            caclul des résultats
        :type exclude_event: Event
        :rtype: int
        """
        if self.stock == 0:
            return 0

        flexi_stock = self.flexi_reservation_resources.filter(
            flexi_reservation__event__date_start__lt=date_stop,
            flexi_reservation__event__date_stop__gt=date_start,
        ).exclude(
            flexi_reservation__event__pk=(exclude_event.pk if exclude_event else None),
        ).aggregate(v=Sum('quantity'))['v'] or 0

        activity_stock = self.activity_resources.filter(
            activity__events__date_start__lt=date_stop,
            activity__events__date_stop__gt=date_start,
        ).exclude(
            activity__events__pk=(exclude_event.pk if exclude_event else None),
        ).aggregate(v=Sum('quantity'))['v'] or 0 # TODO: test this with multiple events per ActivityResource

        return self.stock - (flexi_stock + activity_stock)

    @transaction.atomic
    def lock(self):
        self.__class__.objects.select_for_update().filter(pk=self.pk).exists()

    @transaction.atomic
    def set_stock(self, new_stock):
        """
        Redéfinit la quantité en stock de la ressource.

        :param new_stock:
            quantité en stock de la ressource ; 0 si illimitée
        :type new_stock: int
        """
        if self.stock == new_stock:
            return

        self.lock() # preserves ActivityResource.quantity <= Resource.stock TODO: preserves other constraints too!

        self.stock = new_stock
        self.full_clean() # TODO: implement a clean() method that checks all constraints (for Activity, Event, etc)
        self.save(update_fields=['stock'])


class Event(models.Model):
    """
    Représentation d'un évènement dans le calendrier.
    """
    #: Activité associée à cet évènement (faculatif)
    activity = models.ForeignKey("Activity", on_delete=models.CASCADE, verbose_name=_("activity"), related_name='events', null=True, blank=True)
    #: Planning associé à cet évènement (facultatif)
    planning = models.ForeignKey("Planning", on_delete=models.CASCADE, verbose_name=_("planning"), related_name='events', null=True, blank=True)
    #: Date et heure de début de l'évènement
    date_start = models.DateTimeField(_("date_start"), db_index=True)
    #: Date et heure de fin de l'évènement
    date_stop = models.DateTimeField(_("date_stop"), db_index=True)
    #: Nombre de réservations possibles pour cet évènement. 0 signifie réservations illimitées
    stock = models.PositiveIntegerField(_("stock"), default=0)
    #: Date de création de l'évènement
    add_date = models.DateTimeField(_("creation date"), auto_now_add=True, editable=False)
    #: Date de modification de l'évènement
    mod_date = models.DateTimeField(_("modificationexit date"), auto_now=True, editable=False)

    class Meta:
        verbose_name = _("event")
        verbose_name_plural = _("events")

    def __unicode__(self):
        event_name = ""
        if self.activity:
            event_name = self.activity
        else:
            try:
                if self.flexi_reservation:
                    event_name = self.flexi_reservation.reservation_type.name
            except FlexiReservation.DoesNotExist:
                pass
        return "Event %s %s (%s to %s)" % (self.pk, event_name, self.date_start, self.date_stop)

    @property
    def duration(self):
        return self.date_stop - self.date_start

    @property
    def is_flexible(self):
        try:
            flexi_reservation = bool(self.flexi_reservation)
        except FlexiReservation.DoesNotExist:
            flexi_reservation = False

        if self.activity and not flexi_reservation:
            return False
        elif not self.activity and flexi_reservation:
            return True
        else:
            raise NotImplementedError

    @property
    def resources(self):
        if self.activity is None:
            try:
                return self.flexi_reservation.resources.all()
            except FlexiReservation.DoesNotExist:
                return Resource.objects.none()
        else:
            return self.activity.resources.all()

    @property
    def activity_resources(self):
        if self.activity is None:
            return ActivityResource.objects.none()
        else:
            return self.activity.activity_resources.all()

    @property
    def flexi_reservation_resources(self):
        try:
            return self.flexi_reservation.flexi_reservation_resources.all()
        except FlexiReservation.DoesNotExist:
            return FlexiReservationResource.objects.none()

    @property
    def used_resources(self):
        if self.activity is None:
            return self.flexi_reservation_resources
        else:
            return self.activity_resources

    def get_available_seats(self, exclude_event=None):
        excluded_pk = exclude_event.pk if exclude_event else None
        if self.stock > 0:
            taken_seats = self.reservations.exclude(pk=excluded_pk).aggregate(v=Sum('quantity'))['v'] or 0
            return self.stock - taken_seats
        else:
            return float('inf')

    def _clean_stock(self):
        if self.get_available_seats() < 0:
            raise ValidationError(_("Event's stock can not be inferior to the number of seats already reserved"))

    def clean(self):
        if self.date_stop <= self.date_start:
            raise ValidationError(_("Event's ending date must be greater than the starting date"))

        if self.planning and self.planning.activity is not self.activity:
            raise ValidationError(_("Specified planning isn't associated to the activity of this event"))

        self._clean_stock()

        try:
            if self.flexi_reservation and self.activity:
                raise ValidationError(_("An event can not simultaneously be linked to an activity and a flexible reservation"))
        except FlexiReservation.DoesNotExist:
            if not self.activity:
                raise ValidationError(_("An event has to be associated to an activity or to a flexible reservation"))

        for ur in self.used_resources.exclude(resource__stock=0):
            available_stock = ur.resource.get_available_stock(self.date_start, self.date_stop, self)
            if available_stock < ur.quantity:
                raise ValidationError(_("Stock of resource %s is overused") % ur.resource, code='stock')

    @transaction.atomic
    def lock(self):
        self.__class__.objects.select_for_update().filter(pk=self.pk).exists()

    @transaction.atomic
    def set_stock(self, new_stock):
        """
        Redéfinit le nombre de places disponibles pour l'évènement.

        :param new_stock:
            nombre de places disponibles pour l'évènement ; 0 si illimité
        :type new_stock: int
        """
        if self.stock == new_stock:
            return

        self.lock() # preserves self.stock >= self.reservations.aggregate(v=Sum('quantity'))['v']

        self.stock = new_stock
        self._clean_stock()
        self.save(update_fields=['stock'])

    @transaction.atomic
    def book(self, user, quantity=1):
        """
        Réserve cet évènement pour un utilisateur.

        :param user:
            utilisateur à associer à la réservation
        :type user: User
        :param quantity:
            nombre de places à réserver
        :type quantity: int
        :rtype: Reservation
        """
        self.lock()

        available_seats = self.get_available_seats()
        if available_seats < quantity:
            raise ValidationError(_("There are not enough seats left for this event"))

        reservation = Reservation(user=user, quantity=quantity)
        reservation.event = self
        reservation.full_clean()
        reservation.save(force_insert=True)

        return reservation


class Reservation(models.Model):
    """
    Représente une réservation pour un évènement.
    """
    #: L'évènement réservé
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name=_("event"), related_name='reservations')
    #: L'utilisateur ayant réservé l'évènement
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("user"), related_name='reservations')
    #: Nombre de places réservées
    quantity = models.IntegerField(_("quantity"), validators=[MinValueValidator(1)], default=0)

    class Meta:
        verbose_name = _("reservation")
        verbose_name_plural = _("reservations")

    def __unicode__(self):
        return "Reservation %s" % self.pk

    def clean(self):
        if self.event.get_available_seats(exclude_reservation=self) < self.quantity:
            raise ValidationError(_("Not enough seats left for this event"))


class ReservationType(models.Model):
    """
    Type de réservation. Un type de réservation permet à un utilisateur de réserver les ressources autorisées.
    """
    #: Liste des ressources autorisées pour ce type de réservation
    resources = models.ManyToManyField(Resource, verbose_name=_("resources"), related_name='reservation_type')
    #: L'organisation à laquelle appartient ce type de réservation
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, verbose_name=_("organisation"), related_name='reservation_types')
    #: Nom du type de réservation
    name = models.CharField(_("name"), max_length=255)

    class Meta:
        verbose_name = _("reservation type")
        verbose_name_plural = _("reservation types")
        unique_together = ('organisation', 'name')

    def __unicode__(self):
        return self.name

    @transaction.atomic
    def lock(self):
        self.__class__.objects.select_for_update().filter(pk=self.pk).exists()

    @transaction.atomic
    def add_resource(self, resource):
        self.lock() # preserves uniqueness of (ReservationTypeResource.resource_id, ReservationTypeResource.reservationtype_id)

        try:
            # if the resource is already associated, we don't do anything
            self.resources.get(pk=resource.pk)
        except Resource.DoesNotExist:
            self.resources.add(resource)


class FlexiReservation(models.Model):
    """
    Réservation flexible. Une réservation est dite “flexible” lorsqu'elle
    ne vient pas se greffer sur un évènement existant, mais lorsqu'elle crée
    elle-même un évènement. Cet évènement n'est alors pas associé à une
    activité ; les ressouces réservées sont directement spécifiées par l'utilisateur.
    """
    #: L'utilisateur ayant fait la réservation
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("user"), related_name='flexi_reservations')
    #: Type de réservation
    reservation_type = models.ForeignKey(ReservationType, on_delete=models.CASCADE, verbose_name=_("reservation type"), related_name='flexi_reservations')
    #: Ressources réservées, avec les quantités requises
    resources = models.ManyToManyField(Resource, through='FlexiReservationResource', verbose_name=_("resources"), related_name='flexi_reservations')
    #: L'évènement créé pour honorer cette réservation
    event = models.OneToOneField(Event, on_delete=models.CASCADE, verbose_name=_("event"), related_name='flexi_reservation')

    class Meta:
        verbose_name = _("flexible reservations")
        verbose_name_plural = _("flexible reservations")

    def __unicode__(self):
        return "Flexible reservation %s" % self.pk

    @transaction.atomic
    def lock(self):
        self.__class__.objects.select_for_update().filter(pk=self.pk).exists()

    @transaction.atomic
    def add_resource(self, resource, quantity):
        resource.lock() # preserves FlexiReservationResource.quantity <= Resource.stock
        self.lock() # preserves uniqueness of (FlexiReservationResource.resource, FlexiReservationResource.flexi_reservation)

        if quantity > resource.stock:
            raise ValidationError(_("Quantity can't be greater than the available stock"))

        try:
            # if the resource is already associated, we merge quantities
            ar = self.flexi_reservation_resources.get(resource=resource)
            ar.quantity += quantity
            ar.full_clean()
            ar.save(update_fields=['quantity'])
        except FlexiReservationResource.DoesNotExist:
            ar = self.flexi_reservation_resources.create(resource=resource, quantity=quantity)

        return ar


class FlexiReservationResource(models.Model):
    """
    Ressource réservée par une réservation dite “flexible”.
    """
    #: Réservation “flexible” associée
    flexi_reservation = models.ForeignKey(FlexiReservation, on_delete=models.CASCADE, verbose_name=_("reservation"), related_name='flexi_reservation_resources')
    #: Ressource réservée
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, verbose_name=_("resource"), related_name='flexi_reservation_resources')
    #: Quantité de la ressource requises
    quantity = models.IntegerField(_("quantity"), validators=[MinValueValidator(-1)], default=0)

    class Meta:
        verbose_name = _("flexible reservation resource")
        verbose_name_plural = _("flexible reservation resources")

    def __unicode__(self):
        return "Flexible reservation resource %s" % self.pk


class Activity(models.Model):
    """
    Activité de l'organisation.
    """
    #: Liste des ressources nécessaires pour l'activité
    resources = models.ManyToManyField(Resource, through='ActivityResource', verbose_name=_("resources"), related_name='activities')
    #: L'organisation à laquelle appartient l'activité
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, verbose_name=_("organisation"), related_name='activities')
    #: Nom de l'activité
    name = models.CharField(_("name"), max_length=255)
    #: Nombre de places disponibles pour cette activité
    stock = models.PositiveIntegerField(_("stock"), default=0)
    #: Drapeau indiquant que l'activité est supprimée
    deleted = models.BooleanField(_("deleted"), default=False)

    class Meta:
        verbose_name = _("activity")
        verbose_name_plural = _("activities")

    def __unicode__(self):
        return self.name

    def get_events_of_the_day(self, date=None):
        """
        Retourne tous les évènements correspondants à cette
        activité pour la date donnée, ou la date actuelle.

        :param date:
            date du jour
        :type date: datetime
        :rtype: QuerySet
        """
        if not date:
            date = timezone.now()
        return self.events.filter(date_start__day=date.day).order_by('date_start').all()

    @transaction.atomic
    def lock(self):
        self.__class__.objects.select_for_update().filter(pk=self.pk).exists()

    @transaction.atomic
    def lock_resources(self):
        self.resources.select_for_update().exists()

    @transaction.atomic
    def add_resource(self, resource, quantity):
        resource.lock() # preserves ActivityResource.quantity <= Resource.stock
        self.lock() # preserves uniqueness of (ActivityResource.resource, ActivityResource.activity)

        if quantity > resource.stock:
            raise ValidationError(_("Quantity can't be greater than the available stock"))

        try:
            # if the resource is already associated, we merge quantities
            ar = self.activity_resources.get(resource=resource)
            ar.quantity += quantity
            ar.full_clean()
            ar.save(update_fields=['quantity'])
        except ActivityResource.DoesNotExist:
            ar = self.activity_resources.create(resource=resource, quantity=quantity)

        return ar

    @transaction.atomic
    def add_event(self, date_start, date_stop, stock=None, planning=None):
        if stock is None:
            stock = self.stock

        self.lock_resources() # preserves Resource.get_available_stock(date_start, date_stop) >= ActivityResource.quantity

        event = Event(date_start=date_start, date_stop=date_stop, stock=stock, planning=planning)
        event.activity = self
        event.full_clean()
        event.save(force_insert=True)


class ActivityResource(models.Model):
    """
    Ressource d'activité.
    """
    #: Ressource requise
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, verbose_name=_("resource"), related_name='activity_resources')
    #: Activité correspondante
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, verbose_name=_("activity"), related_name='activity_resources')
    #: Quantité de la ressource requise pour l'activité ; la valeur spéciale -1 consomme la totalité de la ressource
    quantity = models.IntegerField(_("quantity"), validators=[MinValueValidator(-1)], default=0)

    class Meta:
        verbose_name = _("activity resource")
        verbose_name_plural = _("activity resources")
        unique_together = ('resource', 'activity')

    def __unicode__(self):
        return "Activity resource : (%s, %s, %s)" % (self.activity, self.resource, self.quantity)

    def clean(self):
        if self.quantity > self.resource.stock:
            raise ValidationError(_("Required quantity can't be greater than the available stock of the resource"))

    @transaction.atomic
    def set_quantity(self, new_quantity):
        self.resource.lock() # preserves ActivityResource.quantity <= Resource.stock

        if self.quantity == new_quantity:
            return

        self.quantity = new_quantity
        self.full_clean()
        self.save(update_fields=['quantity'])


class Planning(models.Model):
    """
    Planning de l'activité.
    """
    PERIODICITY_CHOICES = (
        (1, _("daily")),
        (2, _("weekly")),
        (3, _("monthly")),
    )

    #: Activité planifiée
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, verbose_name=_("activity"), related_name='plannings')
    #: Périodicité de l'activité planifiée
    periodicity = models.PositiveIntegerField(_("periodicity"), choices=PERIODICITY_CHOICES)
    #: Jours de la semaine programmés pour l'activité
    days_of_week = models.CharField(_("days of week"), max_length=7)
    #: Date et heure de début du premier évènement planifié
    time_start = models.DateTimeField(_("time start"))
    #: Date et heure de fin du premier évènement planifié
    time_stop = models.DateTimeField(_("time stop"))
    #: Date de fin de l'activité
    date_stop = models.DateTimeField(_("date stop"), null=True, blank=True)

    class Meta:
        verbose_name = _("planning")
        verbose_name_plural = _("plannings")

    def __unicode__(self):
        return "Planning %s" % self.pk
