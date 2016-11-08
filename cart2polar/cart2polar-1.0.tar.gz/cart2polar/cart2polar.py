from h5py import File
from math import pi, cos, sin, atan2, ceil, floor
from numpy import sin as npsin, cos as npcos, \
				  minimum, maximum, ravel_multi_index, \
				  arange, empty, hstack, fliplr
from scipy.integrate import quad
from scipy.sparse import csr_matrix
from .quadrant import foldQuadrant, resizeFolded

class PolarRebin:

	def __init__(self, cbins=None, rbins=None, thbins=None, file=None):

		if isinstance(cbins, str) or isinstance(cbins, File):
			file = cbins
			rbins, thbins = None, None

		if cbins and rbins and thbins:
			self.cbins  = cbins
			self.rbins  = rbins
			self.thbins = thbins
			rs, ths, xs, ys, vals = self.get_overlap_values(cbins, rbins, thbins)
			self.overlap_values = self.make_matrix(rs, ths, xs, ys, vals)
			self.save(rs, ths, xs, ys, vals, file=file)
		elif isinstance(file, str):
			with File(file, 'r') as file:
				return self.__init__(file=file)
		elif isinstance(file, File):
			self.cbins  = file['cbins'].value
			self.rbins  = file['rbins'].value
			self.thbins = file['thbins'].value
			rs = file['rs'].value
			ths = file['ths'].value
			xs = file['xs'].value
			ys = file['ys'].value
			vals = file['vals'].value
			self.overlap_values = self.make_matrix(rs, ths, xs, ys, vals)
		else:
			raise ValueError("PolarRebin constructor needs a filename or bin values")

	def R(self):
		return (arange(self.rbins) + 0.5) * (self.cbins - 0.5) / self.rbins

	def TH(self, full=False):
		return (arange(self.thbins + 3*self.thbins*(full==True)) + 0.5) * (pi / 2) / self.thbins

	def rebin(self, cart, x0=None, y0=None):

		if x0 and y0:
			return hstack((fliplr(self.rebin(resizeFolded(foldQuadrant(cart, x0, y0, [1,0,0,0]), self.cbins))),
								  self.rebin(resizeFolded(foldQuadrant(cart, x0, y0, [0,1,0,0]), self.cbins)),
						   fliplr(self.rebin(resizeFolded(foldQuadrant(cart, x0, y0, [0,0,1,0]), self.cbins))),
								  self.rebin(resizeFolded(foldQuadrant(cart, x0, y0, [0,0,0,1]), self.cbins))))
		else:
			return self.overlap_values.dot(cart.reshape(self.cbins**2, -1)).reshape(self.rbins, self.thbins, -1).squeeze()

	def save(self, rs, ths, xs, ys, vals, file=None):

		if file is None:
			file = 'PR_c%d_r%d_th%d.h5' % (self.cbins, self.rbins, self.thbins)

		with File(file, 'w') as file:
			file.create_dataset('cbins' , data=self.cbins)
			file.create_dataset('rbins' , data=self.rbins)
			file.create_dataset('thbins', data=self.thbins)
			file.create_dataset('rs'    , data=rs)
			file.create_dataset('ths'   , data=ths)
			file.create_dataset('xs'    , data=xs)
			file.create_dataset('ys'    , data=ys)
			file.create_dataset('vals'  , data=vals)

	def get_overlap_values(self, cbins, rbins, thbins):

		dr = (cbins - 0.5) / rbins
		dth = (pi / 2) / thbins
		thbins_reduced = ceil(thbins / 2)

		def overlap_value(x, y, r, th):

			thmin = max(th - dth/2, atan2(y - 0.5, x + 0.5))
			thmax = min(th + dth/2, atan2(y + 0.5, x - 0.5))

			rin  = lambda theta: maximum(r - dr/2, maximum((x - 0.5) / npcos(theta), (y - 0.5) / npsin(theta)))
			rout = lambda theta: minimum(r + dr/2, minimum((x + 0.5) / npcos(theta), (y + 0.5) / npsin(theta)))

			integrand = lambda theta: maximum(rout(theta)**2 - rin(theta)**2, 0)

			return 0.5 * quad(integrand, thmin, thmax)[0]

		expected = int(pi*rbins**2)
		rs = empty(expected, dtype=int)
		ths = empty(expected, dtype=int)
		xs = empty(expected, dtype=int)
		ys = empty(expected, dtype=int)
		vals = empty(expected, dtype=float)
		found = 0

		for thi in range(thbins_reduced):
			th = (thi + 0.5) * dth
			for ri in range(rbins):
				r = (ri + 0.5) * dr
				for x in range(round((r - dr/2) * cos(th + dth/2)), min(cbins, round((r + dr/2) * cos(th - dth/2)) + 1)):
					for y in range(round((r - dr/2) * sin(th - dth/2)), min(cbins, round((r + dr/2) * sin(th + dth/2)) + 1)):
						if ((x - 0.5)**2 + (y - 0.5)**2 < (r + dr/2)**2) and \
						   ((x + 0.5)**2 + (y + 0.5)**2 > (r - dr/2)**2) and \
						   (atan2(y + 0.5, x - 0.5) > th - dth/2) and \
						   (atan2(y - 0.5, x + 0.5) < th + dth/2):
						   area = overlap_value(x, y, r, th)
						   if area > 0:
						   	rs[found] = ri
						   	ths[found] = thi
						   	xs[found] = x
						   	ys[found] = y
						   	vals[found] = area
						   	found+=1

		return rs[:found], ths[:found], xs[:found], ys[:found], vals[:found]

	def make_matrix(self, rs, ths, xs, ys, vals):

		ps = ravel_multi_index((hstack((rs, rs)), hstack((ths, self.thbins - ths - 1))), (self.rbins, self.thbins))
		cs = ravel_multi_index((hstack((xs, ys)), hstack((ys, xs))), (self.cbins, self.cbins))

		return csr_matrix((hstack((vals, vals)), (ps, cs)), (self.rbins*self.thbins, self.cbins**2))