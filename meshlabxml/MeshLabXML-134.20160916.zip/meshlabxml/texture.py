""" MeshLabXML texture functions """

import math

from . import util


def flat_plane(script='TEMP3D_default.mlx', plane=0, aspect_ratio=False,
               current_layer=None, last_layer=None):
    """Flat plane parameterization 

    """
    script_file = open(script, 'a')
    script_file.write('  <filter name="Parametrization: Flat Plane ">\n')
    script_file.write(' '.join([
        '    <Param',
        'name="projectionPlane"',
        'value="%d"' % plane,
        'description="Projection plane"',
        'enum_val0="XY"',
        'enum_val1="XZ"',
        'enum_val2="YZ"',
        'enum_cardinality="3"',
        'type="RichEnum"',
        'tooltip="Choose the projection plane"',
        '/>\n']))
    script_file.write(' '.join([
        '    <Param',
        'name="aspectRatio"',
        'value="%s"' % str(aspect_ratio).lower(),
        'description="Preserve Ratio"',
        'type="RichBool"',
        'tooltip="If checked the resulting parametrization will preserve the original apsect ratio of the model otherwise it will fill up the whole 0..1 uv space"',
        '/>\n']))
    script_file.write('  </filter>\n')
    script_file.close()
    return current_layer, last_layer


def per_triangle(script='TEMP3D_default.mlx',
                 sidedim=0, textdim=1024, border=2, method=1,
                 current_layer=None, last_layer=None):
    """Trivial Per-Triangle parameterization 

    """
    script_file = open(script, 'a')
    script_file.write('  <filter name="Parametrization: Trivial Per-Triangle ">\n')
    script_file.write(' '.join([
        '    <Param',
        'name="sidedim"',
        'value="%d"' % sidedim,
        'description="Quads per line"',
        'type="RichInt"',
        'tooltip="Indicates how many triangles have to be put on each line (every quad contains two triangles). Leave 0 for automatic calculation"',
        '/>\n']))
    script_file.write(' '.join([
        '    <Param',
        'name="textdim"',
        'value="%d"' % textdim,
        'description="Texture Dimension (px)"',
        'type="RichInt"',
        'tooltip="Gives an indication on how big the texture is"',
        '/>\n']))
    script_file.write(' '.join([
        '    <Param',
        'name="border"',
        'value="%d"' % border,
        'description="Inter-Triangle border (px)"',
        'type="RichInt"',
        'tooltip="Specifies how many pixels to be left between triangles in parametrization domain"',
        '/>\n']))
    script_file.write(' '.join([
        '    <Param',
        'name="method"',
        'value="%d"' % method,
        'description="Method"',
        'enum_val0="Basic"',
        'enum_val1="Space-optimizing"',
        'enum_cardinality="2"',
        'type="RichEnum"',
        'tooltip="Choose space optimizing to map smaller faces into smaller triangles in parametrizazion domain"'
        '/>\n']))
    script_file.write('  </filter>\n')
    script_file.close()
    return current_layer, last_layer


def voronoi(script='TEMP3D_default.mlx',
            region_num=10, overlap=False,
            current_layer=None, last_layer=None):
    """Voronoi Atlas parameterization 

    """
    script_file = open(script, 'a')
    script_file.write('  <filter name="Parametrization: Voronoi Atlas">\n')
    script_file.write(' '.join([
        '    <Param',
        'name="regionNum"',
        'value="%d"' % region_num,
        'description="Approx. Region Num"',
        'type="RichInt"',
        'tooltip="An estimation of the number of regions that must be generated. Smaller regions could lead to parametrizations with smaller distortion."',
        '/>\n']))
    script_file.write(' '.join([
        '    <Param',
        'name="overlapFlag"',
        'value="%s"' % str(overlap).lower(),
        'description="Overlap"',
        'type="RichBool"',
        'tooltip="If checked the resulting parametrization will be composed by overlapping regions, e.g. the resulting mesh will have duplicated faces: each region will have a ring of ovelapping duplicate faces that will ensure that border regions will be parametrized in the atlas twice. This is quite useful for building mipmap robust atlases"',
        '/>\n']))
    script_file.write('  </filter>\n')
    script_file.close()
    return current_layer, last_layer


def isometric(script='TEMP3D_default.mlx',
              targetAbstractMinFaceNum=140, targetAbstractMaxFaceNum=180,
              stopCriteria=1, convergenceSpeed=1, DoubleStep=True,
              current_layer=None, last_layer=None):
    """Isometric parameterization 

    """
    script_file = open(script, 'a')
    script_file.write('  <filter name="Iso Parametrization">\n')
    script_file.write(' '.join([
        '    <Param',
        'name="targetAbstractMinFaceNum"',
        'value="%d"' % targetAbstractMinFaceNum,
        'description="Abstract Min Mesh Size"',
        'type="RichInt"',
        'tooltip="This number and the following one indicate the range face number of the abstract mesh that is used for the parametrization process. The algorithm will choose the best abstract mesh with the number of triangles within the specified interval. If the mesh has a very simple structure this range can be very low and strict; for a roughly spherical object if you can specify a range of [8,8] faces you get a octahedral abstract mesh, e.g. a geometry image. &lt;br>Large numbers (greater than 400) are usually not of practical use."',
        '/>\n']))
    script_file.write(' '.join([
        '    <Param',
        'name="overlapFlag"',
        'value="%s"' % str(overlap).lower(),
        'description="Overlap"',
        'type="RichBool"',
        'tooltip="If checked the resulting parametrization will be composed by overlapping regions, e.g. the resulting mesh will have duplicated faces: each region will have a ring of ovelapping duplicate faces that will ensure that border regions will be parametrized in the atlas twice. This is quite useful for building mipmap robust atlases"',
        '/>\n']))
    script_file.write('  </filter>\n')
    script_file.close()
    return current_layer, last_layer


