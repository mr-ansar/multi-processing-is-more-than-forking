# Author: Scott Woods <scott.suzuki@gmail.com>
# MIT License
#
# Copyright (c) 2022
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

"""A complete no-op.

Called with no settings and returns immediately, by falling
through the end of the main function.
"""

import uuid
import ansar.create as ar

# Do nothing. Terminate.
def noop(self):
	v = ar.command_variables()
	assert isinstance(v.session_id, uuid.UUID)
	return ar.Ack()

ar.bind(noop)


class CommandEnvironment(object):
	def __init__(self, session_id=None, sequence=None):
		self.session_id = session_id
		self.sequence = sequence or ar.default_vector()

command_variables_SCHEMA = {
	"session_id": ar.UUID(),
	"sequence": ar.VectorOf(ar.Float8()),
}

ar.bind(CommandEnvironment, object_schema=command_variables_SCHEMA)


default_environment = CommandEnvironment()

if __name__ == '__main__':
	ar.create_object(noop, factory_variables=default_environment)

