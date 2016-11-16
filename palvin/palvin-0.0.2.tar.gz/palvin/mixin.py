# -*- coding:utf-8 -*-
from __future__ import division

import datetime

from sqlalchemy import Column, Integer, DateTime, Boolean

__all__ = ('CRUDMixin', 'IdMixin', 'TimestampMixin', 'VirtualDeleteMixin', 'ImageMixin')


class CRUDMixin(object):
    @classmethod
    def get_by(cls, **kwargs):
        try:
            return cls.query.filter_by(**kwargs).first()
        except Exception:
            return None

    @classmethod
    def get_or_create(cls, **kwargs):
        r = cls.get_by(**kwargs)
        if not r:
            r = cls(**kwargs).save()
        return r

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        cls.db.session.add(instance)
        return instance

    @classmethod
    def create_with_commit(cls, **kwargs):
        instance = cls.create(**kwargs)
        instance.save()
        return instance

    @classmethod
    def bulk_update_mappings(cls, mappings, commit=True):
        cls.db.session.bulk_update_mappings(cls, mappings)
        if commit:
            cls.commit()

    @classmethod
    def toggle(cls, **kwargs):
        r = cls.get_by(**kwargs)
        if r is None:
            cls.create_with_commit(**kwargs)
            return True
        r.delete()
        return False

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return self

    def update_with_commit(self, **kwargs):
        self.update(**kwargs)
        return self.save()

    def delete(self):
        self.db.session.delete(self)

    def delete_with_commit(self):
        self.delete()
        self.commit()

    def save(self):
        """
        Shortcut to add and save + rollback
        """
        try:
            self.db.add(self)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
        return self


class IdMixin(object):
    """
    Provides the :attr:`id` primary key column
    """
    #: Database identity for this model, used for foreign key
    #: references from other models
    id = Column(Integer, primary_key=True, autoincrement=True)

    @classmethod
    def get(cls, id_):
        try:
            id_ = int(id_)
        except ValueError:
            return None
        return cls.query.get(id_)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.id or '#')
IdMixin.id._creation_order = 0


class TimestampMixin(object):
    """
    Provides the :attr:`created_at` and :attr:`updated_at` audit timestamps
    """
    #: Timestamp for when this instance was created, in UTC
    created_at = Column(
        DateTime(timezone=True),
        default=datetime.datetime.utcnow,
        nullable=False
    )
    #: Timestamp for when this instance was last updated (via the app), in UTC
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False
    )
TimestampMixin.created_at._creation_order = 9998
TimestampMixin.updated_at._creation_order = 9999


class VirtualDeleteMixin(object):

    is_deleted = Column(Boolean, default=False, index=True)
    deleted_at = Column(DateTime, default=None)

    def delete(self, hard_delete=False):
        """
        Soft delete a record
        :param hard_delete: Bool - If true it will completely delete the record
        """
        # Hard delete
        if hard_delete:
            self.db.session.delete(self)
        else:
            self.is_deleted = True
            self.deleted_at = datetime.datetime.utcnow()
        return self

    def delete_with_commit(self, hard_delete=False):
        """
        Soft delete a record
        :param delete: Bool - To soft-delete/soft-undelete a record
        :param hard_delete: Bool - If true it will completely delete the record
        """
        self.delete(hard_delete)
        try:
            return self.db.commit()
        except Exception:
            self.db.rollback()
            raise

    def revoke(self):
        self.is_deleted = False
        self.deleted_at = None

    def revoke_with_commit(self):
        self.revoke()
        try:
            return self.db.commit()
        except Exception:
            self.db.rollback()
            raise
VirtualDeleteMixin.is_deleted._creation_order = 9994
VirtualDeleteMixin.deleted_at._creation_order = 9995
