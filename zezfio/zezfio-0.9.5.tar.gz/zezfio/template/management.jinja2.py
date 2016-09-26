import irpy

from zezfio.io import zio,zscalar,zarray
from zezfio import babel
from zezfio.io.__init__ import build_path

d_instance = dict()
from ctypes import c_int
d_instance["zezfio_id"] = c_int(0)

def update_zezfio_id():
    d_instance["zezfio_id"] = c_int(d_instance["zezfio_id"].value + 1)

{% for category in json_config -%}

class {{ category|capitalize }}(object):

    {% for variable in json_config[category] -%}

    @irpy.lazy_property_mutable
    def {{ variable.name }}_shape(self):
        {% if variable.shape is defined %}
        return {{variable.shape}}
        {% else %}
        return [-1]
        {% endif %}

    @irpy.lazy_property
    def {{ variable.name }}_len(self):
        return babel.shape2len(self.{{ variable.name }}_shape)

    @irpy.lazy_property
    def {{ variable.name }}_path(self):
        return build_path('{{db_path}}','{{ category }}','{{ variable.name }}',
                          len_=self.{{ variable.name }}_len)

    @irpy.lazy_property_mutable
    def {{ variable.name }}_interface(self):
    
        {% if variable.default is defined %}

        data_py = {{ variable.default }}
        return babel.py2interface('{{ variable.type }}',data_py)

        {% else %}
        #IRPY Waring. Nele need to be in a separate variable cause zio can call a C function
        #who will break the genalogy machinery of IRPY
        nele = self.{{ variable.name }}_len
        return zio.db2interface(self.{{variable.name}}_path,'{{ variable.type }}', 
                                len_=nele)

        {% endif %}

    @irpy.lazy_property
    def {{ variable.name }}_len_interface(self):

        {% if variable.type != 'raw' %}

        return babel.len2bytes('{{ variable.type }}',
                               self.{{ variable.name }}_len)
        {% else %}
        return c_int(len(self.{{ variable.name }}_interface))
        {% endif %}

    #This value needs to depend of _interface            #
    #because it can be used to define the size of arrays #
    @irpy.lazy_property
    def {{ variable.name }}(self):
        return babel.interface2py(self.{{ variable.name }}_interface, 
                                  len_=self.{{ variable.name }}_len)

    def set_{{ variable.name }}(self,bytes):

        {% if variable.type != 'raw' %}
        sbytes = len(bytes)
        theobytes = self.{{ variable.name }}_len_interface.value

        if  sbytes != theobytes:
            raise IndexError("Conflic between the spec bytes of the array %i and the given one %i" % (sbytes, theobytes))       

        {% endif %}

        data_interface = babel.bytes2interface('{{ variable.type }}', bytes)
        self.{{ variable.name }}_interface = data_interface

        zio.interface2db(self.{{ variable.name }}_path,'{{ variable.type }}',
                             self.{{ variable.name }}_shape,data_interface)

        update_zezfio_id()

    @irpy.lazy_property
    def {{ variable.name }}_ascii(self):
        return babel.py2ascii(self.{{ variable.name }})

    @irpy.lazy_property
    def {{ variable.name }}_len_ascii(self):
        return c_int(len(self.{{ variable.name }}_ascii))

    def set_ascii_{{ variable.name }}(self,data_ascii):

        sbytes = len(data_ascii)
        theobytes = self.{{ variable.name }}_len_ascii.value

        if  sbytes != theobytes:
            raise IndexError("Conflic between the spec bytes of the array %i and the given one %i" % (sbytes, theobytes))       

        data_interface = babel.ascii2interface('{{ variable.type }}', data_ascii)
        self.{{ variable.name }}_interface = data_interface

        zio.interface2db(self.{{ variable.name }}_path,'{{ variable.type }}',
                             self.{{ variable.name }}_shape,data_interface)

        update_zezfio_id()


    {% endfor %}

#For allowing referance in shape
{{ category }} = {{ category|capitalize }}()
#Quicker than getattr
d_instance[ "{{ category }}" ] = {{ category }}

{%  endfor %}
