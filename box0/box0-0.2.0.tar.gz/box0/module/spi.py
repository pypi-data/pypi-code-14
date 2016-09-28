#
# This file is part of pyBox0.
# Copyright (C) 2014-2016 Kuldeep Singh Dhaka <kuldeepdhaka9@gmail.com>
#
# pyBox0 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyBox0 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyBox0.  If not, see <http://www.gnu.org/licenses/>.
#

from box0._binding import ffi, libbox0
from box0.exceptions import ResultException
from box0.module import ModuleInstance
from box0.property import Speed, Count, Ref, Buffer, Capab, Bitsize
import numpy as np

class Slave(object):
	def __init__(self, addr, mod):
		self.addr = addr
		self.mod = mod

	def hd_write(self, data):
		self.mod.hd_write(self.addr, data)

	def hd_read(self, data):
		return self.mod.hd_read(self.addr, data)

	def fd(self, write, read):
		return self.mod.fd(self.addr, write, read)

	@property
	def active_state(self):
		return self.mod.active_state(self.addr)

	@active_state.setter
	def active_state(self, value):
		self.mod.active_state(self.addr, value)

	def __str__(self):
		return "Slave Address: " + hex(self.addr)

def _to_cflags(mode, lsb_first, cpol, cpha):
	"""
	Convert value to mode flags
	"""
	_flags = 0

	if mode is not None:
		if cpol is not None:
			raise Exception("cpol and mode cannot exists together")
		if cpha is not None:
			raise Exception("cpha and mode cannot exists together")
		_mode = {
			0: libbox0.B0_SPI_TASK_MODE0,
			1: libbox0.B0_SPI_TASK_MODE1,
			2: libbox0.B0_SPI_TASK_MODE2,
			3: libbox0.B0_SPI_TASK_MODE3,
		}.get(mode)
		if _mode is None: raise Exception("Invalid SPI mode %i" % mode)
		_flags |= _mode
	else:
		if cpol: _flags |= libbox0.B0_SPI_TASK_CPOL
		if cpha: _flags |= libbox0.B0_SPI_TASK_CPHA

	if lsb_first:
		_flags |= libbox0.B0_SPI_TASK_LSB_FIRST

	return _flags

def _task_cflags(task):
	"""
	Convert the task flags to C flags
	"""

	_flags = 0

	if 'write' in task and 'read' in task:
		_flags |= libbox0.B0_SPI_TASK_FD
	elif 'write' in task:
		_flags |= libbox0.B0_SPI_TASK_HD_WRITE
	elif 'read' in task:
		_flags |= libbox0.B0_SPI_TASK_HD_READ
	else:
		raise Exception("Provide something to do (read, write or both)")

	flags = []

	for name in ('flag', 'flags'):
		if name not in task:
			continue
		data = task[name]
		if type(data) in (list, tuple):
			flags.extend(data)
		else:
			flags.append(data)

	for flag in flags:
		if flag.lower() in ('hd_write', 'hd_read', 'hd'):
			raise Exception("Library automatically infer transfer (%s)" % flag)

		if flag.lower() is 'last':
			raise Exception("LAST flag is automatically inferred")

		# FIXME: check if the two flags that modify same bit is provided
		_flag = {
			'mode0': libbox0.B0_SPI_TASK_MODE0,
			'mode1': libbox0.B0_SPI_TASK_MODE1,
			'mode2': libbox0.B0_SPI_TASK_MODE2,
			'mode3': libbox0.B0_SPI_TASK_MODE3,
			'lsb_first': libbox0.B0_SPI_TASK_LSB_FIRST,
			'msb_first': libbox0.B0_SPI_TASK_MSB_FIRST,
			'cpol': libbox0.B0_SPI_TASK_CPOL,
			'cpha': libbox0.B0_SPI_TASK_CPHA
		}.get(flag.lower())

		if _flag is None: raise Exception("Unknown flag %s" % flag)
		_flags |= _flag

	return _flags

def _to_sugar_arg(addr, bitsize, lsb_first, mode, cpha, cpol):
	return ffi.new("b0_spi_sugar_arg *", {
		'flags': _to_cflags(mode, lsb_first, cpha, cpol),
		'addr': addr,
		'bitsize': bitsize
	})

def _bitsize_heuristic(data1, data2=None):
	dtype = None
	if data1 is None or data2 is None:
		data = data1 if data2 is None else data2
		dtype = data.dtype
	else:
		if data1.dtype == data2.dtype:
			dtype = data1.dtype

	if dtype is not None and dtype.itemsize > 0:
		return dtype.itemsize

	raise Exception("Please specify bitsize")

def _count_heuristic(data1, data2=None):
	if data1 is None or data2 is None:
		data = data1 if data2 is None else data2
		return len(data)
	else:
		if data1.dtype == data2.dtype:
			return min(len(data1), len(data2))

	raise Exception("Please specify count")

def _to_ctasks(tasks):
	"""
	Convert the python style task to C task
	"""

	if type(tasks) not in (list, tuple):
		# make it an iterable object
		tasks = [tasks]

	if not len(tasks): raise Exception("Tasks cannot be empty")

	_tasks = []
	for task in tasks:
		write = task['write']
		read = task['read']

		count = task['count'] \
			if 'count' in task else _count_heuristic(write, read)

		bitsize = task['bitsize'] \
			if 'bitsize' in task else _bitsize_heuristic(write, read)

		write_buf = ffi.cast("void *", write.ctypes.data) \
				if write is not None else ffi.NULL
		read_buf = ffi.cast("void *", read.ctypes.data) \
				if read is not None else ffi.NULL

		# check for overflow
		_bytes = np.floor(count * bitsize / 8.0)
		if write is not None: assert(write.nbytes >= _bytes)
		if read is not None: assert(read.nbytes >= _bytes)
		_tasks.append({
			'flags': _task_cflags(task),
			'bitsize': bitsize,
			'addr': task['addr'],
			'wdata': write_buf,
			'rdata': read_buf,
			'count': count
		})

	_tasks[-1]['flags'] |= libbox0.B0_SPI_TASK_LAST
	return ffi.new("b0_spi_task []", _tasks)

class Spi(ModuleInstance):
	_info = libbox0.b0_spi_info
	_open = libbox0.b0_spi_open
	_close = libbox0.b0_spi_close
	_cache_flush = libbox0.b0_spi_cache_flush

	_active_state_get = libbox0.b0_spi_active_state_get
	_active_state_set = libbox0.b0_spi_active_state_set

	_start = libbox0.b0_spi_start
	_stop = libbox0.b0_spi_stop

	_hd_write = libbox0.b0_spi_hd_write
	_hd_read = libbox0.b0_spi_hd_read
	_fd = libbox0.b0_spi_fd

	def __init__(self, dev, index):
		ModuleInstance.__init__(self, dev, index, "b0_spi**")
		self.speed = Speed(self._pointer.speed)
		self.count = Count(self._pointer.count)
		self.ref = Ref(self._pointer.ref)
		self.buffer = Buffer(self._pointer.buffer)
		self.capab = Capab(self._pointer.capab)
		self.bitsize = Bitsize(self._pointer.bitsize)

	def __active_state_set(self, ss, value):
		ResultException.act(self._active_state_set(self._pointer, ss, value))

	def __active_state_get(self, ss):
		value = ffi.new("bool")
		ResultException.act(self._active_state_get(self._pointer, ss, value))
		return (value[0] != 0)

	def active_state(self, ss, value=None):
		if value is None:
			self.__active_state_get(ss)
		else:
			self.__active_state_set(ss, value)

	def start(self, tasks):
		failed_task_index = ffi.new("int *")
		failed_task_count = ffi.new("int *")
		ResultException.act(self._start(self._pointer, _to_ctasks(tasks), \
			failed_task_index, failed_task_count))
		return failed_task_index[0], failed_task_count[0]

	def stop(self):
		ResultException.act(self._stop(self._pointer))

	def hd_write(self, addr, data, bitsize=None, lsb_first=False, \
					mode=None, cpha=None, cpol=None):
		if bitsize is None:
			bitsize = _bitsize_heuristic(bitsize, data)

		arg = _to_sugar_arg(addr, bitsize, lsb_first, mode, cpha, cpol)
		data_buf = ffi.cast("void *", data.ctypes.data)
		ResultException.act(self._hd_write(self._pointer, arg, data_buf, \
			len(data)))

	def hd_read(self, addr, data, bitsize=None, lsb_first=False, \
					mode=None, cpha=None, cpol=None):

		if bitsize is None: bitsize = _bitsize_heuristic(bitsize, data)
		arg = _to_sugar_arg(addr, bitsize, lsb_first, mode, cpha, cpol)
		data_buf = ffi.cast("void *", data.ctypes.data)
		ResultException.act(self._hd_read(self._pointer, arg, data_buf, \
			len(data)))

	def fd(self, addr, write, read=None, count=None, bitsize=None, \
					lsb_first=False, mode=None, cpha=None, cpol=None):
		"""
		write and write buffer
		"""
		if bitsize is None: bitsize = _bitsize_heuristic(write, read)
		if count is None: count = _count_heuristic(write, read)
		if read is None: read = np.empty(len(write), dtype=write.dtype)
		arg = _to_sugar_arg(addr, bitsize, lsb_first, mode, cpha, cpol)
		write_buf = ffi.cast("void *", write.ctypes.data)
		read_buf = ffi.cast("void *", read.ctypes.data)
		ResultException.act(self._fd(self._pointer, arg, \
					write_buf, read_buf, count))
		return read

	def slave(self, addr):
		"""
		construct a Slave Object
		modX.slave(addr) => Slave(addr, modX)
		"""
		return Slave(addr, self)
