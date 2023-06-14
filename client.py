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

"""A demo-only network client.

Initiates a connection to (host, port). Sessions expect a basic "echo" behaviour
from the server.

This is not a recommended approach to production network messaging.
"""

import socket
import errno
import ansar.create as ar
from client_server import ServerAddress

#
#
def client(self, settings):
    """A client-side session."""
    address = (settings.host, settings.port)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(address)
            self.console(f'Connected to {address}')

            word, expect = b'fervent', b'eager'
            s.sendall(word)
            reply = s.recv(1024)
            self.test(reply == expect, f"Expected {expect} for {word}, got {reply}")

            word, expect = b'explain', b'define'
            s.sendall(word)
            reply = s.recv(1024)
            self.test(reply == expect, f"Expected {expect} for {word}, got {reply}")

            word, expect = b'fly', b'droll'
            s.sendall(word)
            reply = s.recv(1024)
            self.test(reply == expect, f"Expected {expect} for {word}, got {reply}")

    except OSError as e:
        s = str(e)
        self.warning(f'Session error - "{s}"')
        if e.errno == errno.ECONNREFUSED:
            return ar.Maybe()
        self.test(False, f"errno.ECONNREFUSED accepted ({s})")

    # Acquire the pass/fail report.
    ar.test_enquiry(self)
    report = self.select(ar.TestReport)
    return report

ar.bind(client)

#
#
settings = ServerAddress('127.0.0.1', 65432)

if __name__ == '__main__':
    ar.create_object(client, factory_settings=settings)
