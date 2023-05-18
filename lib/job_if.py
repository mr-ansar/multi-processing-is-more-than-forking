# Author: Scott Woods <scott.suzuki@gmail.com>
# MIT License
#
# Copyright (c) 2017-2022
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""A component template.

Blah.
"""
import ansar.create as ar

__all__ = [
    'JobInput',
    'JobReturned',
]

#
#
class JobInput(object):
	def __init__(self, managers=1, management_levels=1, duties=None):
		self.managers = managers
		self.management_levels = management_levels
		self.duties = duties or ar.default_vector()

JOB_INPUT_SCHEMA = {
	"managers": ar.Integer8(),
	"management_levels": ar.Integer8(),
	"duties": ar.VectorOf(ar.Unicode()),
}

ar.bind(JobInput, object_schema=JOB_INPUT_SCHEMA)

#
#
class JobReturned(object):
	def __init__(self, processes=0):
		self.processes = processes

ar.bind(JobReturned)
