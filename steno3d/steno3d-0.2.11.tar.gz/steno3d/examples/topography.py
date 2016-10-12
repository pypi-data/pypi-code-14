from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from json import loads

from numpy import array, mean

from .base import BaseExample, exampleproperty
from ..data import DataArray
from ..project import Project
from ..surface import Mesh2D, Surface
from ..texture import Texture2DImage


class Topography(BaseExample):
    """Topography example

    This module provides example data for a topography surface.
    """

    @exampleproperty
    def filenames(self):
        return ['topography.json', 'topography.png']

    @exampleproperty
    def _data(self):
        """topography data from json"""
        if getattr(self, '__data', None) is None:
            json_file = Topography.fetch_data(filename='topography.json',
                                              download_if_missing=False,
                                              verbose=False)
            with open(json_file, 'r') as f:
                self.__data = loads(f.read())
        return self.__data

    @exampleproperty
    def vertices(self):
        """n x 3 topography vertices"""
        return array(self._data['vertices'])

    @exampleproperty
    def triangles(self):
        """n x 3 topography triangles"""
        return array(self._data['triangles'])

    @exampleproperty
    def topo_image(self):
        """surface image"""
        return Topography.fetch_data(filename='topography.png',
                                     download_if_missing=False,
                                     verbose=False)

    @exampleproperty
    def topo_image_orientation(self):
        """surface image O, U, and V"""
        return dict(
            O=[443200., 491750, 0],
            U=[4425., 0, 0],
            V=[0., 3690, 0]
        )

    @classmethod
    def get_project(self):
        """return topography project"""
        elev = self.vertices[:, 2]
        proj = Project(
            title='Topography'
        )
        Surface(
            project=proj,
            mesh=Mesh2D(
                vertices=self.vertices,
                triangles=self.triangles
            ),
            data=[
                dict(
                    location='N',
                    data=DataArray(
                        array=elev,
                        title='Elevation, vertices'
                    )
                ),
                dict(
                    location='CC',
                    data=DataArray(
                        array=mean(elev[self.triangles], axis=1),
                        title='Elevation, faces'
                    )
                )
            ],
            textures=[
                Texture2DImage(
                    image=self.topo_image,
                    **self.topo_image_orientation
                )
            ],
            title='Topography Surface',
            description=('This surface has face and vertex elevation '
                         'data as well as surface imagery')
        )
        return proj
