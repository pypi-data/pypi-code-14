"""volume.py contains the Volume composite resource for steno3d"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from json import dumps
from numpy import ndarray
from six import string_types
from traitlets import validate

from .base import BaseMesh
from .base import CompositeResource
from .data import DataArray
from .options import ColorOptions
from .options import MeshOptions
from .traits import (Array, HasSteno3DTraits, KeywordInstance, Repeated,
                     String, Vector)


class _Mesh3DOptions(MeshOptions):
    pass


class _VolumeOptions(ColorOptions):
    pass


class Mesh3DGrid(BaseMesh):
    """Contains spatial information of a 3D grid volume."""

    h1 = Array(
        help='Tensor cell widths, x-direction',
        shape=('*',),
        dtype=(float, int)
    )
    h2 = Array(
        help='Tensor cell widths, y-direction',
        shape=('*',),
        dtype=(float, int)
    )
    h3 = Array(
        help='Tensor cell widths, z-direction',
        shape=('*',),
        dtype=(float, int)
    )
    x0 = Vector(
        help='Origin vector',
        default_value=[0., 0., 0.]
    )
    opts = KeywordInstance(
        help='Mesh3D Options',
        klass=_Mesh3DOptions,
        allow_none=True
    )

    @property
    def nN(self):
        """ get number of nodes """
        return (len(self.h1)+1) * (len(self.h2)+1) * (len(self.h3)+1)

    @property
    def nC(self):
        """ get number of cells """
        return len(self.h1) * len(self.h2) * len(self.h3)

    def _nbytes(self, arr=None):
        filenames = ('h1', 'h2', 'h3', 'x0')
        if arr is None:
            return sum(self._nbytes(fn) for fn in filenames)
        if isinstance(arr, string_types) and arr in filenames:
            if getattr(self, arr, None) is None:
                return 0
            arr = getattr(self, arr)
        if isinstance(arr, ndarray):
            return arr.astype('f4').nbytes
        raise ValueError('Mesh3DGrid cannot calculate the number of '
                         'bytes of {}'.format(arr))

    def _get_dirty_data(self, force=False):
        datadict = super(Mesh3DGrid, self)._get_dirty_data(force)
        dirty = self._dirty_traits
        if force or ('h1' in dirty or 'h2' in dirty or 'h3' in dirty):
            datadict['tensors'] = dumps(dict(
                h1=self.h1.tolist(),
                h2=self.h2.tolist(),
                h3=self.h3.tolist()
            ))
        if force or ('h1' in dirty or 'h2' in dirty or 'h3' in dirty or
                     'x0' in dirty):
            datadict['OUVZ'] = dumps(dict(
                O=self.x0.tolist(),
                U=[self.h1.sum().astype(float), 0, 0],
                V=[0, self.h2.sum().astype(float), 0],
                Z=[0, 0, self.h3.sum().astype(float)]
            ))
        return datadict

    @classmethod
    def _build_from_json(cls, json, **kwargs):
        mesh = Mesh3DGrid(
            title=kwargs['title'],
            description=kwargs['description'],
            h1=json['tensors']['h1'],
            h2=json['tensors']['h2'],
            h3=json['tensors']['h3'],
            x0=json['OUVZ']['O'],
            opts=json['meta']
        )
        return mesh


class _VolumeBinder(HasSteno3DTraits):
    """Contains the data on a 3D volume with location information"""
    location = String(
        help='Location of the data on mesh',
        choices={
            'CC': ('CELLCENTER'),
            # 'N': ('NODE', 'VERTEX', 'CORNER')
        }
    )
    data = KeywordInstance(
        help='Data',
        klass=DataArray
    )


class Volume(CompositeResource):
    """Contains all the information about a 3D volume"""
    mesh = KeywordInstance(
        help='Mesh',
        klass=Mesh3DGrid,
    )
    data = Repeated(
        help='Data',
        trait=KeywordInstance(klass=_VolumeBinder)
    )
    opts = KeywordInstance(
        help='Options',
        klass=_VolumeOptions,
        allow_none=True
    )

    def _nbytes(self):
        return self.mesh._nbytes() + sum(d.data._nbytes() for d in self.data)

    @validate('data')
    def _validate_data(self, proposal):
        """Check if resource is built correctly"""
        for ii, dat in enumerate(proposal['value']):
            assert dat.location == 'CC'  # in ('N', 'CC')
            valid_length = (
                proposal['owner'].mesh.nC if dat.location == 'CC'
                else proposal['owner'].mesh.nN
            )
            if len(dat.data.array) != valid_length:
                raise ValueError(
                    'volume.data[{index}] length {datalen} does not match '
                    '{loc} length {meshlen}'.format(
                        index=ii,
                        datalen=len(dat.data.array),
                        loc=dat.location,
                        meshlen=valid_length
                    )
                )
        return proposal['value']


__all__ = ['Volume', 'Mesh3DGrid']
