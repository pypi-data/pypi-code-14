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
from box0.property import Ref, I2cVersion, Label, Buffer
import numpy as np

class Slave(object):
	def __init__(self, addr, mod):
		self.addr = addr
		self.mod = mod

	def detect(self):
		return self.mod.detectSlave(self.addr)

	def read(self, read):
		return self.mod.read(self.addr, read)

	def write(self, write):
		return self.mod.read(self.addr, write)

	def write8_read(self, write_byte, read):
		return self.mod.write8_read(self, self.addr, write_byte, read)

	def write_read(self, write, read):
		return self.mod.write_read(self, self.addr, write, read)

	def __str__(self):
		return "Slave Address: " + hex(self.addr)

def _task_cflags(task):
	"""
	Convert the task flags to C flags
	"""
	_flags = 0

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
		if flag.lower() is 'last':
			raise Exception("LAST flag is automatically infered")

		_flag = {
			'write': libbox0.B0_I2C_TASK_WRITE,
			'w': libbox0.B0_I2C_TASK_WRITE,
			'read': libbox0.B0_I2C_TASK_READ,
			'r': libbox0.B0_I2C_TASK_READ
		}.get(flag.lower())

		if _flag is None: raise Exception("Invalid flag %s" % flag)
		_flags |= _flag

	return _flags

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
		_tasks.append({
			'flags': _task_cflags(task),
			'addr': task['addr'],
			'data': ffi.cast("void *", task['data'].ctypes.data),
			'count': task['data'].nbytes
		})

	_tasks[-1]['flags'] |= libbox0.B0_I2C_TASK_LAST
	return ffi.new("b0_i2c_task []", _tasks)

class I2c(ModuleInstance):
	_info = libbox0.b0_i2c_info
	_open = libbox0.b0_i2c_open
	_close = libbox0.b0_i2c_close
	_cache_flush = libbox0.b0_i2c_cache_flush

	_read = libbox0.b0_i2c_read
	_write = libbox0.b0_i2c_write
	_write8_read = libbox0.b0_i2c_write8_read
	_write_read = libbox0.b0_i2c_write_read
	_slave_id = libbox0.b0_i2c_slave_id
	_slave_detect = libbox0.b0_i2c_slave_detect
	_start = libbox0.b0_i2c_start
	_stop = libbox0.b0_i2c_stop

	def __init__(self, dev, index):
		ModuleInstance.__init__(self, dev, index, "b0_i2c**")
		self.ref = Ref(self._pointer.ref)
		self.version = I2cVersion(self._pointer.version)
		self.label = Label(self._pointer.label)
		self.buffer = Buffer(self._pointer.buffer)

	def slave_id(self, addr):
		"""
		return (manufacturer, part, revision)
		"""
		manuf = ffi.new("uint16_t*")
		part = ffi.new("uint16_t*")
		rev = ffi.new("uint8_t*")
		ResultException.act(self._slave_id(self._pointer, addr, manuf, part, rev))
		return manuf[0], part[0], rev[0]

	def start(self, tasks):
		"""
		tasks to execute
		"""
		failed_task_index = ffi.new("int *")
		failed_task_ack = ffi.new("int *")
		ResultException.act(self._start(self._pointer, _to_ctasks(tasks), \
			failed_task_index, failed_task_ack))
		return failed_task_index[0], failed_task_ack[0]

	def stop(self):
		ResultException.act(self._stop(self._pointer))

	def slaveDetect(self, addr):
		detected = ffi.new("bool*")
		ResultException.act(self._slave_detect(self._pointer, addr, detected))
		return (detected[0] != 0)

	def write8_read(self, addr, write_byte, read):
		"""
		read can be a number [no of bytes to read]
		or a numpy array, that contain no of bytes to read

		return the readed array
		"""
		if not isinstance(read, np.ndarray):
			read = int(read)
			assert (read > 0)
			read = np.empty(read, dtype=np.uint8)

		read_buf = ffi.cast("void *", read.ctypes.data)
		ResultException.act(self._write8_read(self._pointer, addr, write_byte, \
					read_buf, read.nbytes))
		return read

	def write_read(self, addr, write, read):
		"""
		first write buffer and then read
		return the readed array
		"""
		if not isinstance(read, np.ndarray):
			read = int(read)
			assert (read > 0)
			read = np.empty(read, dtype=np.uint8)

		write_buf = ffi.cast("void *", write.ctypes.data)
		read_buf = ffi.cast("void *", read.ctypes.data)
		ResultException.act(self._write8_read(self._pointer, addr, write_buf, \
				write.nbytes, read_buf, read.nbytes))
		return read

	def write(self, addr, write):
		"""
		`write' is assumed to be a numpy array
		"""
		write_ptr = ffi.cast("void *", write.ctypes.data)
		result = self._write(self._pointer, addr, write_ptr, write.nbytes)
		ResultException.act(result)

	def read(self, addr, read):
		"""
		`read' can be a number [no of bytes to read]
		or a numpy array
		"""
		if not isinstance(read, np.ndarray):
			read = int(read)
			assert (read > 0)
			read = np.empty(read, dtype=np.uint8)

		data_ptr = ffi.cast("void *", read.ctypes.data)
		result = self._read(self._pointer, addr, data_ptr, read.nbytes)
		ResultException.act(result)
		return read

	def slave(self, addr):
		"""
		construct a Slave Object
		modX.slave(addr) => Slave(addr, modX)
		"""
		return Slave(addr, self)
