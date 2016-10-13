import wx

import collections
import os
from PIL import Image

import color_cycler
import image_processor
import ppu_memory
import view_renderer
import file_modify_watcher
from constants import *


APP_WIDTH = 1024
APP_HEIGHT = 704
APP_TITLE = 'Makechr'


MousePos = collections.namedtuple('MousePos',
                                  ['clear', 'y', 'x', 'size', 'reuse'])


class ComponentView(object):
  """A component of NES graphics, drawable to a bitmap.

  Wraps a bitmap, which displays a single component of NES graphics. Handles
  both drawing the bitmap, and processing mouseover events.
  """
  def __init__(self, parent, pos, size):
    self.bitmap = wx.EmptyBitmap(size[0], size[1])
    self.ctrl = wx.StaticBitmap(parent, wx.ID_ANY, self.bitmap, pos=pos,
                                size=size)
    self.manager = None
    self.StartMouseListener()

  def load(self, bitmap):
    self.bitmap = bitmap
    wx.CallAfter(self.ctrl.SetBitmap, self.bitmap)

  def StartMouseListener(self):
    self.ctrl.Bind(wx.EVT_ENTER_WINDOW, lambda e:self.OnMouseEvent('enter', e))
    self.ctrl.Bind(wx.EVT_MOTION,       lambda e:self.OnMouseEvent('move', e))
    self.ctrl.Bind(wx.EVT_LEAVE_WINDOW, lambda e:self.OnMouseEvent('leave', e))

  def SetManager(self, manager):
    self.manager = manager

  def OnMouseEvent(self, type, e):
    y = x = clear = None
    if type == 'leave' or type == 'move':
      clear = True
    if type == 'enter' or type == 'move':
      y = e.GetY()
      x = e.GetX()
    self.emitMouse(clear, y, x)

  def drawBox(self, clear, y, x, size, color):
    dc = wx.ClientDC(self.ctrl)
    dc.BeginDrawing()
    if clear:
      dc.DrawBitmap(self.bitmap, 0, 0, True)
    if y is None or x is None or size is None:
      return
    dc.SetPen(wx.Pen(color, style=wx.SOLID))
    dc.SetBrush(wx.Brush(color, wx.TRANSPARENT))
    dc.DrawRectangle(x * size, y * size, size, size)
    dc.EndDrawing()

  def emitMouse(self, clear, y, x):
    raise NotImplementedError()


class TileBasedComponentView(ComponentView):
  """A component that works with tiles."""

  def emitMouse(self, clear, y, x):
    if self.manager:
      y = y / 8 if y else None
      x = x / 8 if x else None
      self.manager.MouseEvent(MousePos(clear, y, x, 8, False))


class BlockBasedComponentView(ComponentView):
  """A component that works with blocks."""

  def emitMouse(self, clear, y, x):
    if self.manager:
      y = y / 16 if y else None
      x = x / 16 if x else None
      self.manager.MouseEvent(MousePos(clear, y, x, 16, False))

  def drawBox(self, clear, y, x, size, color):
    if y is None or x is None or size is None:
      new_y = new_x = new_size = None
    else:
      new_size = 16
      new_y = (y * size) / new_size
      new_x = (x * size) / new_size
    ComponentView.drawBox(self, clear, new_y, new_x, new_size, color)


class ReuseBasedComponentView(ComponentView):
  """A component that represents tile reuse."""

  def emitMouse(self, clear, y, x):
    if self.manager:
      y = y / 8 if y else None
      x = x / 8 if x else None
      self.manager.MouseEvent(MousePos(clear, y, x, 8, True))


class ChrBasedComponentView(ComponentView):
  """A component that works with chr."""

  def emitMouse(self, clear, y, x):
    if self.manager:
      y = y / 17 if y else None
      x = x / 17 if x else None
      self.manager.ChrMouseEvent(MousePos(clear, y, x, 17, False))


class Cursor(object):
  """Dumb object that represents a cursor with position, size, and color."""

  def __init__(self):
    self.y = None
    self.x = None
    self.size = None
    self.cycler = color_cycler.ColorCycler()
    self.enabled = False

  def nextColor(self):
    self.cycler.next()

  def getColor(self):
    return self.cycler.getColor()

  def set(self, y, x, size):
    self.y = y
    self.x = x
    self.size = size


class DrawCursorManager(object):
  """Manager that routes mouse movement events and draw commands.

  The manager holds references to the cursor, and a list of components.
  Mediates mouse movement, telling each component how to draw the current
  cursor. Also handles cursor animation.
  """
  def __init__(self, parent, processor):
    self.cursor = None
    self.components = []
    self.timer = None
    self.tileSet = False
    self.reusableCursor = Cursor()
    self.parent = parent
    self.processor = processor
    self.CreateTimer()

  def addCursor(self, cursor):
    self.cursor = cursor
    # Alias the cycler, so that cursor and reusableCursor share the same one.
    self.reusableCursor.cycler = self.cursor.cycler

  def addComponent(self, component):
    self.components.append(component)
    component.SetManager(self)

  def getChrTilePosition(self):
    nt = self.processor.ppu_memory().get_nametable(0)
    if self.cursor.y is None or self.cursor.x is None:
      return (None, None)
    try:
      tile = nt[self.cursor.y][self.cursor.x]
    except IndexError:
      # Sometimes, x == size of array.
      return (None, None)
    chr_y = tile / 16
    chr_x = tile % 16
    return chr_y, chr_x

  def CreateTimer(self):
    self.timer = wx.Timer(self.parent, wx.ID_ANY)
    self.parent.Bind(wx.EVT_TIMER, self.OnTimer)
    self.timer.Start(30)

  def OnTimer(self, e):
    if not self.cursor.enabled:
      return
    self.cursor.nextColor()
    self.OnCursor(False)

  def MouseEvent(self, pos):
    if not self.cursor.enabled:
      return
    self.tileSet = None
    clear, y, x, size, reuse = (pos.clear, pos.y, pos.x, pos.size, pos.reuse)
    if clear:
      self.cursor.set(None, None, None)
    if not y is None and not x is None and not size is None:
      self.cursor.set(y, x, size)
    if reuse:
      nt = self.processor.ppu_memory().get_nametable(0)
      try:
        self.tileSet = nt[self.cursor.y][self.cursor.x]
      except TypeError:
        self.tileSet = None
    self.OnCursor(clear)

  def ChrMouseEvent(self, pos):
    if not self.cursor.enabled:
      return
    clear, y, x, size, reuse = (pos.clear, pos.y, pos.x, pos.size, pos.reuse)
    if x is None or y is None:
      return
    self.tileSet = y * 16 + x
    try:
      elems = self.processor.nt_lookup[self.tileSet]
    except KeyError:
      elems = None
    if elems:
      (y,x) = elems[0]
      self.cursor.set(y, x, 8)
    self.OnCursor(clear)

  def OnCursor(self, clear):
    if self.tileSet:
      self.DrawCursorToComponents(clear, self.cursor)
      try:
        elems = self.processor.nt_lookup[self.tileSet]
      except KeyError:
        elems = None
      if elems and len(elems) < TILE_REUSE_LIMIT:
        for y,x in elems:
          self.reusableCursor.set(y, x, 8)
          self.DrawCursorToComponents(False, self.reusableCursor)
        return
    self.DrawCursorToComponents(clear, self.cursor)

  def DrawCursorToComponents(self, clear, cursor):
    color = cursor.getColor()
    for comp in self.components:
      if isinstance(comp, ChrBasedComponentView):
        (chr_y, chr_x) = self.getChrTilePosition()
        chr_size = 17
        if not chr_y is None and not chr_x is None:
          comp.drawBox(clear, chr_y, chr_x, chr_size, color)
      else:
        comp.drawBox(clear, cursor.y, cursor.x, cursor.size, color)


class MakechrGui(wx.Frame):
  """MakechrGui main application."""

  def __init__(self, *args, **kwargs):
    super(MakechrGui, self).__init__(*args, **kwargs)
    self.processor = image_processor.ImageProcessor()
    self.renderer = view_renderer.ViewRenderer(future_views=True, scale=1)
    self.inputImagePath = None
    self.cursor = None
    self.manager = None
    self.watcher = file_modify_watcher.FileModifyWatcher()
    self.Create()

  def Create(self):
    self.panel = wx.Panel(self, -1)
    self.CreateApp()
    self.CreateMenu()
    self.CreateImages()
    self.CreateLabels()
    self.CreateReloadTimer()
    self.CreateCursorManager()

  def CreateApp(self):
    self.SetSize((APP_WIDTH, APP_HEIGHT))
    self.SetTitle(APP_TITLE)
    self.SetPosition((200, 30))

  def CreateMenu(self):
    menubar = wx.MenuBar()
    # File
    fileMenu = wx.Menu()
    openItem = fileMenu.Append(wx.ID_ANY, '&Open')
    saveItem = fileMenu.Append(wx.ID_ANY, '&Save')
    quitItem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
    self.Bind(wx.EVT_MENU, self.OnOpen, openItem)
    self.Bind(wx.EVT_MENU, self.OnSave, saveItem)
    self.Bind(wx.EVT_MENU, self.OnQuit, quitItem)
    menubar.Append(fileMenu, '&File')
    # Tools
    toolsMenu = wx.Menu()
    importItem = toolsMenu.Append(wx.ID_ANY, '&Import RAM')
    exportItem = toolsMenu.Append(wx.ID_ANY, '&Export Binaries')
    self.Bind(wx.EVT_MENU, self.OnImportRam, importItem)
    self.Bind(wx.EVT_MENU, self.OnExportBinaries, exportItem)
    menubar.Append(toolsMenu, '&Tools')
    self.SetMenuBar(menubar)

  def CreateImages(self):
    # Component views.
    self.inputComp = TileBasedComponentView(self.panel,
                                            pos=(0x20,0x30), size=(0x100,0xf0))
    self.ntComp = TileBasedComponentView(self.panel,
                                         pos=(0x170,0x30), size=(0x100,0xf0))
    self.colorsComp = BlockBasedComponentView(self.panel,
                                              pos=(0x170,0x140),
                                              size=(0x100,0xf0))
    self.reuseComp = ReuseBasedComponentView(self.panel,
                                            pos=(0x290,0x30), size=(0x100,0xf0))
    self.chrComp = ChrBasedComponentView(self.panel,
                                         pos=(0x290,0x140), size=(0x10f,0x10f))
    # Palette.
    img = wx.EmptyImage(104, 32)
    self.paletteCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                       wx.BitmapFromImage(img),
                                       pos=(0x170,0x250), size=(0x68, 0x20))
    # System colors.
    img = wx.EmptyImage(252, 72)
    self.sysColorCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                        wx.BitmapFromImage(img),
                                        pos=(0x20,0x170), size=(0xfc,0x48))
    view = Image.open('res/systemcolors.png')
    wx.CallAfter(self.sysColorCtrl.SetBitmap, self.PilImgToBitmap(view))
    # Key for reuse.
    img = wx.EmptyImage(42, 144)
    self.rKeyCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                    wx.BitmapFromImage(img),
                                    pos=(0x3a0,0x30), size=(42,144))
    view = Image.open('res/reuse-key.png')
    wx.CallAfter(self.rKeyCtrl.SetBitmap, self.PilImgToBitmap(view))

  def CreateLabels(self):
    wx.StaticText(self.panel, wx.ID_ANY, label='Pixel art', pos=(0x20, 0x1c))
    wx.StaticText(self.panel, wx.ID_ANY, label='System colors',
                  pos=(0x20, 0x15c))
    wx.StaticText(self.panel, wx.ID_ANY, label='Nametable', pos=(0x170, 0x1c))
    wx.StaticText(self.panel, wx.ID_ANY, label='CHR', pos=(0x290, 0x12c))
    wx.StaticText(self.panel, wx.ID_ANY, label='Attribute', pos=(0x170, 0x12c))
    wx.StaticText(self.panel, wx.ID_ANY, label='Reuse', pos=(0x290, 0x1c))
    wx.StaticText(self.panel, wx.ID_ANY, label='Palette', pos=(0x170, 0x23c))
    wx.StaticText(self.panel, wx.ID_ANY, label='Key', pos=(0x3a0, 0x1c))
    self.numTileCtrl = wx.StaticText(self.panel, wx.ID_ANY,
                                     label='Number of tiles: 0  Hex: $00',
                                     pos=(0x290, 0x258))

  def CreateCursorManager(self):
    self.cursor = Cursor()
    self.manager = DrawCursorManager(self, self.processor)
    self.manager.addCursor(self.cursor)
    self.manager.addComponent(self.inputComp)
    self.manager.addComponent(self.ntComp)
    self.manager.addComponent(self.reuseComp)
    self.manager.addComponent(self.colorsComp)
    self.manager.addComponent(self.chrComp)

  def CreateReloadTimer(self):
    self.reloadTimer = wx.Timer(self, wx.ID_ANY)
    self.Bind(wx.EVT_TIMER, self.OnReloadTimer, self.reloadTimer)

  def IdentifyFileKind(self, path):
    golden = '(VALIANT)'
    fp = open(path, 'rb')
    bytes = fp.read(len(golden))
    fp.close()
    if bytes == golden:
      return 'valiant'
    return 'image'

  def LoadImage(self):
    kind = self.IdentifyFileKind(self.inputImagePath)
    if kind == 'image':
      self.ReassignImage()
      self.ProcessMakechr()
      self.CreateViews()
      self.cursor.enabled = True
      # TODO: Unwatch when something else is opened.
      self.watcher.watch(self.inputImagePath, self.OnModify)
    elif kind == 'valiant':
      self.LoadPpuMemory()
      self.CreateViews()
      self.cursor.enabled = True

  def LoadPpuMemory(self):
    # TODO: Implement
    self.inputImagePath

  def ReassignImage(self):
    img = wx.Image(self.inputImagePath, wx.BITMAP_TYPE_ANY)
    bitmap = wx.BitmapFromImage(img)
    self.inputComp.load(bitmap)

  def ProcessMakechr(self):
    input = Image.open(self.inputImagePath)
    self.processor.process_image(input, '', None, 'horizontal', False, False)

  def CreateViews(self):
    renderer = self.renderer
    if self.processor.err().has():
      # Errors.
      view = renderer.create_error_view(None, input, self.processor.err().get(),
                                        has_grid=False)
      self.inputComp.load(self.PilImgToBitmap(view))
      return
    self.processor.build_nt_lookup()
    # Colorization.
    view = renderer.create_colorization_view(None, self.processor.ppu_memory(),
        self.processor.artifacts(), self.processor.color_manifest())
    self.colorsComp.load(self.PilImgToBitmap(view))
    # Nametable.
    view = renderer.create_nametable_view(None, self.processor.ppu_memory())
    self.ntComp.load(self.PilImgToBitmap(view))
    # Reuse.
    view = renderer.create_reuse_view(None, self.processor.ppu_memory(),
        self.processor.nt_count())
    self.reuseComp.load(self.PilImgToBitmap(view))
    # Palette.
    view = renderer.create_palette_view(None, self.processor.ppu_memory())
    wx.CallAfter(self.paletteCtrl.SetBitmap, self.PilImgToBitmap(view))
    # Chr.
    view = renderer.create_chr_view(None, self.processor.ppu_memory())
    self.chrComp.load(self.PilImgToBitmap(view))
    # Num tiles.
    num = len(self.processor.ppu_memory().chr_data)
    self.numTileCtrl.SetLabel('Number of tiles: %d  Hex: $%02x' % (num, num))

  def PilImgToBitmap(self, pilImg):
    img = wx.EmptyImage(*pilImg.size)
    img.SetData(pilImg.convert('RGB').tobytes())
    img.SetAlphaData(pilImg.convert('RGBA').tobytes()[3::4])
    return wx.BitmapFromImage(img)

  def OnOpen(self, e):
    dlg = wx.FileDialog(self, 'Choose a file', '', '',
                        '*.bmp;*.png;*.gif;*.mchr', wx.OPEN)
    if dlg.ShowModal() == wx.ID_OK:
      self.inputImagePath = dlg.GetPath()
    dlg.Destroy()
    if not self.inputImagePath is None:
      self.LoadImage()

  def OnSave(self, e):
    dlg = wx.FileDialog(self, 'Save project as...', '', '',
                        '*.mchr', wx.SAVE|wx.OVERWRITE_PROMPT)
    if dlg.ShowModal() != wx.ID_OK:
      return
    path = dlg.GetPath()
    dlg.Destroy()
    if not path is None:
      config = ppu_memory.PpuMemoryConfig()
      self.processor.ppu_memory().save_valiant(path, config)

  def OnImportRam(self, e):
    # TODO: Implement RAM importer
    print 'import'

  def OnExportBinaries(self, e):
    # TODO: Implement binary exporter
    print 'export'

  def ReloadFile(self):
    self.ReassignImage()
    self.MakechrViews()

  def OnReloadTimer(self, e):
    self.reloadTimer.Stop()
    self.ReloadFile()

  def OnModify(self, e):
    wx.CallAfter(self.reloadTimer.Start, 1000)

  def OnQuit(self, e):
    self.watcher.stop()
    self.Close()


class MakechrGuiApp(wx.App):
  def OnInit(self):
    self.SetAppName('Makechr')
    mainframe = MakechrGui(None)
    self.SetTopWindow(mainframe)
    mainframe.Show(True)
    return 1


if __name__ == '__main__':
  app = MakechrGuiApp()
  app.MainLoop()
