# This class tends to draw objects in matplotlib but finally we use web plotting
# # define the graphic related objects
# from matplotlib import pyplot as plt
# from matplotlib import patches
# from matplotlib.path import Path
# import matplotlib
# import math
#
#
# class GlyphClassesEnum:
#     def __init__(self):
#         pass
#
#
# # the config of display object
# class DisplayConfig:
#     def __init__(self, line_color="black", fill_color="none", edge_width=0.5, font_size=12, assist_font_size=6):
#         self.line_color = line_color
#         self.fill_color = fill_color
#         self.edge_width = edge_width
#         self.font_size = font_size
#         self.assist_font_size = assist_font_size
#
#
# # root graphic object
# class GraphicObject:
#     def __init__(self):
#         pass
#
#     def draw(self, ax):
#         raise NotImplementedError
#
#
# # basic objects: Line, Rect, RoundRect, HalfRoundRect, Circle, Triangle, RidingRect(perturbing agent),
# # PolygonRect(Complex), RectWithTriangle(tag), ExtrudeRect(phenotype), Ellipse
#
# class Line(GraphicObject):
#     def __init__(self, start, end, config):
#         GraphicObject.__init__(self)
#         self.start, self.end, self.config = start, end, config
#
#     def draw(self, ax):
#         line = plt.Line2D([self.start[0], self.end[0]], [self.start[1], self.end[1]],
#                           linewidth=self.config.edge_width, color=self.config.line_color)
#         ax.add_line(line)
#
#
# class Rect(GraphicObject):
#     def __init__(self, x, y, height, width, config, label=None):
#         GraphicObject.__init__(self)
#         self.x, self.y, self.height, self.width, self.config, self.label = x, y, height, width, config, label
#
#     def draw(self, ax):
#         rect = plt.Rectangle((self.x, self.y), self.width, self.height,
#                              fc=self.config.fill_color, ec=self.config.line_color, lw=self.config.edge_width)
#         if self.label:
#             ax.text(self.x + self.width / 2.0, self.y + self.height / 2.0, self.label,
#                     horizontalalignment='center', verticalalignment='center', fontsize=self.config.font_size)
#         ax.add_patch(rect)
#
#
# class RoundRect(GraphicObject):
#     def __init__(self, x, y, height, width, radius, config, label=None):
#         GraphicObject.__init__(self)
#         self.x, self.y, self.height, self.width, self.radius, self.config = x, y, height, width, radius, config
#         self.label = label
#
#     def draw(self, ax):
#         f = patches.FancyBboxPatch((self.x + self.radius, self.y + self.radius), self.width - self.radius * 2, self.height - self.radius * 2,
#                                    boxstyle=patches.BoxStyle("Round", pad=self.radius),
#                                    fc=self.config.fill_color, ec=self.config.line_color, lw=self.config.edge_width)
#         if self.label:
#             ax.text(self.x + self.width / 2.0, self.y + self.height / 2.0, self.label,
#                     horizontalalignment='center', verticalalignment='center', fontsize=25)
#         ax.add_patch(f)
#
#
# class HalfRoundRect(GraphicObject):
#     def __init__(self, x, y, height, width, radius, config, label=None):
#         GraphicObject.__init__(self)
#         self.x, self.y, self.height, self.width, self.radius, self.config = x, y, height, width, radius, config
#         self.label = label
#
#     def draw(self, ax):
#         # start @ left up
#         verts = [(self.x, self.y + self.height),    # Upper Left
#                  (self.x, self.y + self.radius),  # arc start
#                  (self.x, self.y),   # point rect should be
#                  (self.x + self.radius, self.y),    # arc start
#                  (self.x + self.width - self.radius, self.y),   # another arc start
#                  (self.x + self.width, self.y),     # another point rect should be
#                  (self.x + self.width, self.y + self.radius),   # another arc end
#                  (self.x + self.width, self.y + self.height),   # Top right
#                  (self.x + self.width, self.y + self.height),   # end it
#                  ]
#         codes = [Path.MOVETO, Path.LINETO, Path.CURVE3, Path.CURVE3, Path.LINETO, Path.CURVE3,
#                  Path.CURVE3, Path.LINETO, Path.CLOSEPOLY]
#         path = Path(verts, codes)
#         patch = patches.PathPatch(path, fc=self.config.fill_color, ec=self.config.line_color, lw=self.config.edge_width)
#         if self.label:
#             ax.text(self.x + self.width / 2.0, self.y + self.height / 2.0, self.label,
#                     horizontalalignment='center', verticalalignment='center', fontsize=25)
#         ax.add_patch(patch)
#
#
# class Circle(GraphicObject):
#     def __init__(self, x, y, radius, config, label=None):
#         GraphicObject.__init__(self)
#         self.x, self.y, self.radius, self.config, self.label = x, y, radius, config, label
#
#     def draw(self, ax):
#         c = plt.Circle((self.x, self.y), self.radius,
#                        fc=self.config.fill_color, ec=self.config.line_color, lw=self.config.edge_width)
#         if self.label:
#             ax.text(self.x, self.y, self.label,
#                     horizontalalignment='center', verticalalignment='center', fontsize=25)
#         ax.add_patch(c)
#
#
# class TriAngle(GraphicObject):
#     def __init__(self, p1, p2, p3, config):
#         GraphicObject.__init__(self)
#         self.p1, self.p2, self.p3, self.config = p1, p2, p3, config
#
#     def draw(self, ax):
#         points = [self.p1, self.p2, self.p3, self.p3]
#         codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
#         path = Path(points, codes)
#         patch = patches.PathPatch(path, fc=self.config.fill_color, ec=self.config.line_color, lw=self.config.edge_width)
#         ax.add_patch(patch)
#
#     def get_patch(self):
#         points = [self.p1, self.p2, self.p3, self.p3]
#         codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
#         path = Path(points, codes)
#         patch = patches.PathPatch(path, fc=self.config.fill_color, ec=self.config.line_color, lw=self.config.edge_width)
#         return patch
#
#
# class RidingRect(GraphicObject):
#     def __init__(self, x, y, width, height, inner, config, label=None):
#         GraphicObject.__init__(self)
#         self.x, self.y, self.width, self.height, self.inner, self.config = x, y, width, height, inner, config
#         self.label = label
#
#     def draw(self, ax):
#         points = [(self.x, self.y + self.height),   # Upper Left
#                   (self.x + self.inner, self.y + self.height / 2.0),     # Mid Inner Left
#                   (self.x, self.y),     # Lower Left
#                   (self.x + self.width, self.y),    # Lower Right
#                   (self.x + self.width - self.inner, self.y + self.height / 2.0),   # Mid Inner Right
#                   (self.x + self.width, self.y + self.height),  # Upper Right
#                   (self.x + self.width, self.y + self.height),  # Close
#                   ]
#         codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
#         path = Path(points, codes)
#         patch = patches.PathPatch(path, fc=self.config.fill_color, ec=self.config.line_color, lw=self.config.edge_width)
#         if self.label:
#             ax.text(self.x, self.y, self.label,
#                     horizontalalignment='center', verticalalignment='center', fontsize=25)
#         ax.add_patch(patch)
#
#
# class PolygonRect(GraphicObject):
#     def __init__(self, x, y, width, height, length, config, label=None):
#         GraphicObject.__init__(self)
#         self.x, self.y, self.width, self.height, self.length, self.config = x, y, width, height, length, config
#         self.label = label
#
#     def draw(self, ax):
#         points = [(self.x + self.length, self.y + self.height),     # Upper Left 1
#                   (self.x, self.y + self.height - self.length),     # Upper Left 2
#                   (self.x, self.y + self.length),   # Lower Left 1
#                   (self.x + self.length, self.y),   # Lower Left 2
#                   (self.x + self.width - self.length, self.y),  # Lower Right 1
#                   (self.x + self.width, self.y + self.length),  # Lower Right 2
#                   (self.x + self.width, self.y + self.height - self.length),    # Upper Right 1
#                   (self.x + self.width - self.length, self.y + self.height),    # Upper Right 2
#                   (self.x + self.width - self.length, self.y + self.height),    # Close
#         ]
#         codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.LINETO,
#                  Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
#         path = Path(points, codes)
#         patch = patches.PathPatch(path, fc=self.config.fill_color, ec=self.config.line_color, lw=self.config.edge_width)
#         if self.label:
#             ax.text(self.x + self.width / 2.0, self.y + self.height / 2.0, self.label,
#                     horizontalalignment='center', verticalalignment='center', fontsize=25)
#         ax.add_patch(patch)
#
#
# class RectWithTriangle(GraphicObject):
#     def __init__(self, x, y, width, height, config, side, length=None, label=None):
#         GraphicObject.__init__(self)
#         self.x, self.y, self.width, self.height, self.length, self.config = x, y, width, height, length, config
#         if self.length is None:
#             self.length = self.height / 2.0
#         self.label, self.side = label, side
#
#     def draw(self, ax):
#         if self.side == 0:
#             # right
#             points = [(self.x, self.y + self.height), (self.x, self.y), (self.x + self.width - self.length, self.y),
#                       (self.x + self.width, self.y + self.height / 2),
#                       (self.x + self.width - self.length, self.y + self.height),
#                       (self.x + self.width - self.length, self.y + self.height)]
#         else:
#             # left
#             points = [(self.x + self.length, self.y + self.height), (self.x, self.y + self.height / 2.0),
#                       (self.x + self.length, self.y), (self.x + self.width, self.y),
#                       (self.x + self.width, self.y + self.height), (self.x + self.width, self.y + self.height)]
#         codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
#         path = Path(points, codes)
#         patch = patches.PathPatch(path, fc=self.config.fill_color, ec=self.config.line_color, lw=self.config.edge_width)
#         if self.label:
#             ax.text(self.x + self.width / 2.0 - self.length / 2, self.y + self.height / 2.0, self.label,
#                     horizontalalignment='center', verticalalignment='center', fontsize=25)
#         ax.add_patch(patch)
#
#
# class ExtrudePolygon(GraphicObject):
#     def __init__(self, x, y, width, height, inner, config, label=None):
#         GraphicObject.__init__(self)
#         self.x, self.y, self.width, self.height, self.inner, self.config = x, y, width, height, inner, config
#         self.label = label
#
#     def draw(self, ax):
#         points = [(self.x + self.inner, self.y + self.height),   # Upper Left
#                   (self.x, self.y + self.height / 2.0),     # Mid Inner Left
#                   (self.x + self.inner, self.y),     # Lower Left
#                   (self.x + self.width - self.inner, self.y),    # Lower Right
#                   (self.x + self.width, self.y + self.height / 2.0),   # Mid Inner Right
#                   (self.x + self.width - self.inner, self.y + self.height),  # Upper Right
#                   (self.x + self.width - self.inner, self.y + self.height),  # Close
#                   ]
#         codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
#         path = Path(points, codes)
#         patch = patches.PathPatch(path, fc=self.config.fill_color, ec=self.config.line_color, lw=self.config.edge_width)
#         if self.label:
#             ax.text(self.x + self.width / 2.0, self.y + self.height / 2.0, self.label,
#                     horizontalalignment='center', verticalalignment='center', fontsize=25)
#         ax.add_patch(patch)
#
#
# class Ellipse(GraphicObject):
#     def __init__(self, x, y, width, height, config, label):
#         GraphicObject.__init__(self)
#         self.x, self.y, self.width, self.height, self.config, self.label = x, y, width, height, config, label
#
#     def draw(self, ax):
#         e = patches.Ellipse((self.x, self.y), self.width, self.height,
#                             fc=self.config.fill_color, ec=self.config.line_color, lw=self.config.edge_width)
#         if self.label:
#             ax.text(self.x, self.y, self.label,
#                     horizontalalignment='center', verticalalignment='center', fontsize=25)
#         ax.add_patch(e)
#
#
# class Polygon(GraphicObject):
#     def __init__(self, points, config):
#         GraphicObject.__init__(self)
#         self.points = points
#         self.config = config
#
#     def draw(self, ax):
#         code = [Path.MOVETO]
#         for x in self.points[1:]:
#             code.append(Path.LINETO)
#         code.append(Path.CLOSEPOLY)
#         self.points.append(self.points[-1])
#         path = Path(self.points, code)
#         patch = patches.PathPatch(path, fc=self.config.fill_color, ec=self.config.line_color, lw=self.config.edge_width)
#         ax.add_patch(patch)
#
#
# # Visualizer for glyph, arc:
# class Visualizer:
#     def __init__(self, plt, fig, ax):
#         self.plt, self.fig, self.ax = plt, fig, ax
#         self.glyph_funcs = {"unspecificed entity": self._unspecified_entity, "simple chemical": self._simple_chemical,
#                             "macromolecule": self._mocromolecule, "nucleic_acid_feature": self._nucleic_acid_feature,
#                             "perturbing agent": self._perturbing_agent, "source sink": self._source_sink,
#                             "complex": self._complex, "multimers": self._multimers,
#                             "uint of information": self._uint_of_information, "state variable": self._state_variable,
#                             "submap": self._sub_map, "tag": self._tag, "process": self._process,
#                             "ommited process": self._omitted_process, "uncertain process": self._uncertain_process,
#                             "association": self._association, "dissociation": self._dissociation,
#                             "phenotype": self._phenotype}
#
#         self.arc_funcs = {"consumption": self._consumption, "production": self._production,
#                           "modulation": self._modulation, "stimulation": self._stimulation,
#                           "inhibition": self._inhibition, "necessary stimulation": self._necessary_stimulation,
#                           "logic arc": self._logic_arc, "equivalence arc": self._equivalence_arc,
#                           "catalysis": self._catalysis}
#
#     def _rotate_patch(self, patch, point):
#         t_start = self.ax.transData
#         coords = t_start.transform(point)
#         print(coords)
#         t = matplotlib.transforms.Affine2D().rotate_deg_around(point[0], point[1], 60)
#         t_end = t_start + t
#         patch.set_transform(t_end)
#         return patch
#
#     def rotation_point(self, end, start, d, degree):
#         theta = math.atan2(end[1] - start[1], end[0] - start[0])
#         print(theta)
#         # theta = 0
#         alpha, beta = math.pi - degree / 2, math.pi + degree / 2
#         return (d * math.cos(alpha + theta) + end[0], d * math.sin(alpha + theta) + end[1]),\
#                (d * math.cos(beta + theta) + end[0], d * math.sin(beta + theta) + end[1])
#
#     def arc(self, type, start, next, *args):
#         print("draw arc {}".format(type))
#         if type not in self.arc_funcs:
#             return
#         self.arc_funcs[type](start, next, args)
#
#     def _consumption(self, start, next, *args):
#         self._curve_between(start, next)
#
#     def _production(self, start, next, *args):
#         self._curve_between(start, next)
#         # draw triagale
#         end_point = (next[-1].x, next[-1].y)
#         point = self.rotation_point(end_point, (start.x, start.y), 10, math.pi / 3)
#         ta = TriAngle(end_point, point[0], point[1],
#                       DisplayConfig(fill_color="black"))
#         ta.draw(self.ax)
#         # print(end_point)
#         # self.ax.add_patch(self._rotate_patch(ta.get_patch(), end_point))
#
#     # not tested
#     def _modulation(self, start, next, *args):
#         self._curve_between(start, next)
#         end_point = (next[-1].x, next[-1].y)
#         point = self.rotation_point(end_point, (start.x, start.y), 20, math.pi / 2)
#         p2 = self.rotation_point(end_point, (start.x, start.y), 20 * math.sqrt(2), 0)
#         Polygon([end_point, point[0], p2, point[1]], DisplayConfig(fill_color="white")).draw(self.ax)
#
#     def _stimulation(self, start, next, *args):
#         self._curve_between(start, next)
#         # draw triagale
#         end_point = (next[-1].x, next[-1].y)
#         point = self.rotation_point(end_point, (start.x, start.y), 10, math.pi / 3)
#         ta = TriAngle(end_point, point[0], point[1], DisplayConfig(fill_color="white"))
#         ta.draw(self.ax)
#
#     def _catalysis(self, start, next, *args):
#         self._curve_between(start, next)
#         # draw triagale
#         end_point = (next[-1].x, next[-1].y)
#         point = self.rotation_point(end_point, (start.x, start.y), 8, 0)
#         Circle(point[0][0], point[0][1], 8, DisplayConfig(fill_color="white"), None).draw(self.ax)
#
#     def _inhibition(self, start, next, *args):
#         self._curve_between(start, next)
#         # draw triagale
#         end_point = (next[-1].x, next[-1].y)
#         point = self.rotation_point(end_point, (start.x, start.y), 16, math.pi)
#         Line(point[0], point[1], DisplayConfig()).draw(self.ax)
#
#     def _necessary_stimulation(self, start, next, *args):
#         self._curve_between(start, next)
#         # draw triagale
#         end_point = (next[-1].x, next[-1].y)
#         point = self.rotation_point(end_point, (start.x, start.y), 10, math.pi / 3)
#         ta = TriAngle(end_point, point[0], point[1], DisplayConfig(fill_color="white"))
#         ta.draw(self.ax)
#         point = self.rotation_point(end_point, (start.x, start.y), 12, math.pi)
#         Line(point[0], point[1], DisplayConfig()).draw(self.ax)
#
#     def _logic_arc(self, start, next, *args):
#         self._curve_between(start, next)
#
#     def _equivalence_arc(self, start, next, *args):
#         self._curve_between(start, next)
#
#     # draw curve from start to nexts to end
#     def _curve_between(self, start, next, *args):
#         points = [(start.x, start.y)]
#         code = [Path.MOVETO]
#         for x in next:
#             if x.type == 0:
#                 # line to
#                 points.append((x.x, x.y))
#                 code.append(Path.LINETO)
#             elif x.type == 1:
#                 points.append(x.hepler[0])
#                 points.append((x.x, x.y))
#                 code.extend([Path.CURVE3, Path.CURVE3])
#             elif x.type == 2:
#                 points.extend([x.hepler[0], x.hepler[1], (x.x, x.y)])
#                 code.extend([Path.CURVE4, Path.CURVE4, Path.CURVE4])
#         path = Path(points, code)
#         patch = patches.PathPatch(path, fc='none',
#                                   ec=DisplayConfig().line_color, lw=DisplayConfig().edge_width)
#         self.ax.add_patch(patch)
#
#     def clear(self):
#         self.plt.clf()
#
#     # draw a clone with masking father
#     def clone(self, father, label, font_size):
#         pass
#
#     # draw a label:
#     def label(self, bbox, txt, font_size=6):
#         print("label: {}".format(txt))
#         self.ax.text(bbox.x + bbox.w / 2.0, bbox.y + bbox.h / 2.0, txt,
#                      horizontalalignment='center', verticalalignment='center', fontsize=font_size)
#
#     # draw a graph type, aka class,
#     def glyph(self, type, bbox):
#         if type not in self.glyph_funcs:
#             return
#         self.glyph_funcs[type](bbox)
#
#     # glyph related function start, Entity Pool, Node
#     def _unspecified_entity(self, bbox):
#         Ellipse(bbox.x, bbox.y, bbox.w, bbox.h, DisplayConfig(), None).draw(self.ax)
#
#     def _simple_chemical(self, bbox):
#         Circle(bbox.x + bbox.w / 2.0, bbox.y + bbox.h / 2.0, bbox.w / 2.0, DisplayConfig(), None).draw(self.ax)
#
#     def _mocromolecule(self, bbox):
#         RoundRect(bbox.x, bbox.y, bbox.h, bbox.w, min(bbox.w, bbox.h) / 6.0, DisplayConfig(), None).draw(self.ax)
#
#     def _nucleic_acid_feature(self, bbox):
#         HalfRoundRect(bbox.x, bbox.y, bbox.h, bbox.w, min(bbox.w, bbox.h) / 4.0, DisplayConfig(), None).draw(self.ax)
#
#     def _perturbing_agent(self, bbox):
#         RidingRect(bbox.x, bbox.y, bbox.w, bbox.h, bbox.h / 3.0, DisplayConfig(), None).draw(self.ax)
#
#     def _source_sink(self, bbox):
#         Line((bbox.x, bbox.y), (bbox.x + bbox.w, bbox.y + bbox.h), DisplayConfig()).draw(self.ax)
#         Circle(bbox.x + bbox.w / 2.0, bbox.y + bbox.h / 2.0, bbox.w / 2.0, DisplayConfig(), None).draw(self.ax)
#
#     def _complex(self, bbox):
#         PolygonRect(bbox.x - 16, bbox.y - 16, bbox.w + 32, bbox.h + 32, 16, DisplayConfig(), None).draw(self.ax)
#
#     def _multimers(self, bbox):
#         pass
#
#     # Auxiliary Uints
#     def _uint_of_information(self, bbox):
#         Rect(bbox.x, bbox.y, bbox.h, bbox.w, DisplayConfig(), None).draw(self.ax)
#
#     def _state_variable(self, bbox):
#         Ellipse(bbox.x + bbox.w / 2.0, bbox.y + bbox.h / 2.0, bbox.w, bbox.h,
#                 DisplayConfig(fill_color="white"), None).draw(self.ax)
#
#     # Sub map
#     def _sub_map(self, bbox):
#         pass
#
#     def _tag(self, bbox, side=0):
#         RectWithTriangle(bbox.x, bbox.y, bbox.w, bbox.h, DisplayConfig(), side).draw(self.ax)
#
#     # process node
#     def _process(self, bbox):
#         Rect(bbox.x, bbox.y, bbox.w, bbox.h, DisplayConfig()).draw(self.ax)
#
#     def _omitted_process(self, bbox):
#         Rect(bbox.x, bbox.y, bbox.w, bbox.h, DisplayConfig()).draw(self.ax)
#         self.label(bbox, "\\")
#
#     def _uncertain_process(self, bbox):
#         Rect(bbox.x, bbox.y, bbox.w, bbox.h, DisplayConfig()).draw(self.ax)
#         self.label(bbox, "?")
#
#     def _association(self, bbox, fill="black"):
#         Circle(bbox.x + bbox.w / 2.0, bbox.y + bbox.h / 2.0, bbox.w / 2.0, DisplayConfig(fill_color=fill)).draw(self.ax)
#
#     def _dissociation(self, bbox):
#         Circle(bbox.x + bbox.w / 2.0, bbox.y + bbox.h / 2.0, bbox.w / 2.0, DisplayConfig()).draw(self.ax)
#         Circle(bbox.x + bbox.w / 2.0, bbox.y + bbox.h / 2.0, 0.75 * bbox.w / 2.0, DisplayConfig()).draw(self.ax)
#
#     def _phenotype(self, bbox):
#         ExtrudePolygon(bbox.x, bbox.y, bbox.w, bbox.h, bbox.h / 2.0, DisplayConfig()).draw(self.ax)
#
#     # so the arc start
#
# if __name__ == '__main__':
#     fig = plt.figure()
#     ax = fig.gca()
#     ax.set_aspect("equal")
#     plt.xlim([0, 30])
#     plt.ylim([0, 30])
#     plt.show()
