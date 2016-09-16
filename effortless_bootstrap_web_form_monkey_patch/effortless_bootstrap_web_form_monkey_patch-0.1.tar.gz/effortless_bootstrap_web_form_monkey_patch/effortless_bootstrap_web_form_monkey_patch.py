"""
These are the rendering parts of the web/form.py. These are what need to get overwritten in order to make this thing extendable, bootstappable, yuiable, whatever.
"""

import copy
import web.form
import web.utils as utils, web.net as net

def patch():
  """monkey-patch class methods in web/form.py"""
  # update the render methods
  web.form.Form.render = Form.__dict__['render']
  web.form.Form.rendernote = Form.__dict__['rendernote']
  web.form.Input.render = Input.__dict__['render']
  web.form.File.render = File.__dict__['render']
  web.form.Textarea.render = Textarea.__dict__['render']
  web.form.Dropdown.render = Dropdown.__dict__['render']
  web.form.GroupedDropdown.render = GroupedDropdown.__dict__['render']
  web.form.Radio.render = Radio.__dict__['render']
  web.form.Checkbox.render = Checkbox.__dict__['render']
  web.form.Button.render = Button.__dict__['render']

  # add the new bootstrap-specific methods
  web.form.Input.group_start = Input.__dict__['group_start']
  web.form.Input.group_end = Input.__dict__['group_end']
  web.form.Input.group_title = Input.__dict__['group_title']
  web.form.Checkbox.group_start = Checkbox.__dict__['group_start']
  web.form.Checkbox.group_end = Checkbox.__dict__['group_end']
  web.form.Checkbox.group_title = Checkbox.__dict__['group_title']
  web.form.Radio.group_start = Radio.__dict__['group_start']
  web.form.Radio.group_end = Radio.__dict__['group_end']
  web.form.Radio.group_title = Radio.__dict__['group_title']

  web.form.Input.has_error = Input.__dict__['has_error']


class Form(web.form.Form):
  def render(self):
    out = ''
    out += self.rendernote(self.note)

    for i in self.inputs:
      if i.is_hidden():
        out += '%s\n' % i.render()
      else:
        out += i.group_start() + "\n"
        out += i.group_title() + "\n"
        if i.pre:
          out += '<p class="form-text text-muted">%s</p>' % utils.safeunicode(i.pre) 
        out += i.render() + "\n"
        if i.note:
          out += '<div class="form-control-feedback">%s</div>' % net.websafe(i.note)
        if i.post and len(i.post) > 60:
          out += '<p class="form-text text-muted">%s</p>' % utils.safeunicode(i.post) 
        elif i.post:
          out += '<small class="text-muted">%s</small>' % utils.safeunicode(i.post) 
        out += i.group_end() + "\n"

    return out

  def rendernote(self, note):
    if note:
      return '<strong class="wrong">%s</strong>' % net.websafe(note)
    else:
      return ""


class Input(web.form.Input):
  def render(self):
    attrs = self.attrs.copy()
    attrs['type'] = self.get_type()
    attrs['id'] = self.name
    attrs['name'] = self.name

    if 'class' in attrs:
      attrs['class'] += ' form-control'
    else:
      attrs['class'] = 'form-control'

    if self.has_error():
      attrs['class'] += ' form-control-danger'

    if self.value is not None:
      attrs['value'] = self.value

    return '<input %s>' % attrs

  # the next three methods are new, the handle containing the bootstrap fields in a nice box

  def group_start(self):
    """begin the container for an input"""
    if self.has_error():
      return '<div class="form-group has-danger">'
    else:
      return '<div class="form-group">'

  def group_title(self):
    """show the title of this group of inputs"""
    return '<label id="%s">%s</label>' % (self.id, net.websafe(self.description))

  def group_end(self):
    """end the container for an input"""
    return '</div>'

  def has_error(self):
    """a well-named shortcut for error-checking the web.form way"""
    if self.note: return True
    else: return False


class File(Input, web.form.File):
  def render(self):
    attrs = self.attrs.copy()
    attrs['type'] = self.get_type()
    attrs['id'] = self.name
    attrs['name'] = self.name

    if 'class' in attrs:
      attrs['class'] += ' form-control-file'
    else:
      attrs['class'] = 'form-control-file'

    if self.value is not None:
      attrs['value'] = self.value

    return '<input %s>' % attrs

class Textarea(Input, web.form.Textarea):
  def render(self):
    attrs = self.attrs.copy()
    attrs['id'] = self.name
    attrs['name'] = self.name

    if 'class' in attrs:
      attrs['class'] += ' form-control'
    else:
      attrs['class'] = 'form-control'

    if self.has_error():
      attrs['class'] += ' form-control-danger'

    value = net.websafe(self.value or '')

    return '<textarea %s>%s</textarea>' % (attrs, value)


class Dropdown(Input, web.form.Dropdown):
  def render(self):
    attrs = self.attrs.copy()
    attrs['id'] = self.name
    attrs['name'] = self.name

    if 'class' in attrs:
      attrs['class'] += ' form-control'
    else:
      attrs['class'] = 'form-control'

    if self.has_error():
      attrs['class'] += ' form-control-danger'

    out = '<select %s>\n' % attrs
    for arg in self.args:
      out += self._render_option(arg, '')
    out += '</select>\n'

    return out


class GroupedDropdown(Dropdown, web.form.GroupedDropdown):
  def render(self):
    attrs = self.attrs.copy()
    attrs['id'] = self.name
    attrs['name'] = self.name

    if 'class' in attrs:
      attrs['class'] += ' form-control'
    else:
      attrs['class'] = 'form-control'

    if self.has_error():
      attrs['class'] += ' form-control-danger'

    out = '<select %s>\n' % attrs

    for label, options in self.args:
      out += '  <optgroup label="%s">\n' % net.websafe(label)
      for arg in options:
        out += self._render_option(arg, indent = '    ')
      out +=  '  </optgroup>\n'

    out += '</select>\n'

    return out


class Radio(Input, web.form.Radio):
  def render(self):
    out = ''

    for arg in self.args:
      out += '<div class="form-check">'
      out += '<label class="form-check-label">'

      if isinstance(arg, (tuple, list)):
        value, desc= arg
      else:
        value, desc = arg, arg 

      attrs = self.attrs.copy()
      attrs['name'] = self.name
      attrs['id'] = self.name
      attrs['name'] = self.name
      attrs['type'] = 'radio'
      attrs['value'] = value

      if 'class' in attrs:
        attrs['class'] += ' form-check-input'
      else:
        attrs['class'] = 'form-check-input'

      if self.has_error():
        attrs['class'] += ' form-control-danger'

      if self.value == value:
        attrs['checked'] = 'checked'
      out += '<input %s> %s' % (attrs, net.websafe(desc))

      out += '</label></div>'

    return out

  # radio groups have specific container needs, the next three methods handle it

  def group_start(self):
    """begin the container for a group of radio selections"""
    if self.has_error():
      return '<fieldset class="form-group has-danger">'
    else:
      return '<fieldset class="form-group">'

  def group_title(self):
    """show the title of this group of radio selections"""
    return '<legend>%s</legend>' % (net.websafe(self.description))

  def group_end(self):
    """end the container for a radio selections"""
    return '</fieldset>'


class Checkbox(Input, web.form.Checkbox):
  def render(self):
    attrs = self.attrs.copy()
    attrs['type'] = 'checkbox'
    attrs['id'] = self.name
    attrs['name'] = self.name
    attrs['value'] = self.value

    if 'class' in attrs:
      attrs['class'] += ' form-check-input'
    else:
      attrs['class'] = 'form-check-input'

    if self.has_error():
      attrs['class'] += ' form-control-danger'

    if self.checked:
      attrs['checked'] = 'checked'
    return '<input %s> %s' % (attrs, net.websafe(self.description))

  # a checkbox has a specific container needs, the next three methods handle it

  def group_start(self):
    """begin the container for a checkbox"""
    if self.has_error():
      return '<div class="form-check has-danger"><label class="form-check-label">'
    else:
      return '<div class="form-check"><label class="form-check-label">'

  def group_title(self):
    """checkbox titles go to the right of the form element"""
    return ''

  def group_end(Self):
    """end the container for a checkbox"""
    return '</label></div>'


class Button(Input, web.form.Button):
  def render(self):
    attrs = self.attrs.copy()
    attrs['id'] = self.name
    attrs['name'] = self.name
    html = attrs.pop('html', None) or net.websafe(self.name)

    if 'class' in attrs:
      attrs['class'] += ' btn btn-primary'
    else:
      attrs['class'] = 'btn btn-primary'

    attrs['type'] = 'submit'

    if self.value is not None:
      attrs['value'] = self.value

    return '<button %s>%s</button>' % (attrs, html)

# classes we don't need to change at all
class Textbox(Input, web.form.Textbox): pass
class Password(Input, web.form.Password): pass
class Hidden(Input, web.form.Hidden): pass
class Validator(web.form.Validator): pass
class regexp(Validator): pass

