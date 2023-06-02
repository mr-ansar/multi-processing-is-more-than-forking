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

"""A demo-only network server.

Establishes a listen at (host, port) and accepts inbound connections. Sessions
implement a basic "word-mapping" behaviour where the inbound word is mapped
to a synonym. If no match is found, the word is simply echoed back to the
client.

This is not a recommended approach to production network messaging.
"""

import socket
import ansar.create as ar
from client_server import ServerAddress

#
#
def accepted(self, conn, addr, word_map):
    """A server-side session."""
    try:
        with conn:
            self.console(f"Accepted on {addr}")
            while True:
                word = conn.recv(1024)
                if not word:          # EOF.
                    break             # Shutdown.
                try:
                    word = word_map[word]
                except KeyError:
                    pass
                conn.sendall(word)    # Echo data back to client.
    except OSError as e:
        self.warning('Session error - "{e}"'.format(e=str(e)))
        return ar.Nak()
    return ar.Ack()

ar.bind(accepted)

def listen(self, address):
    """Listening at an address."""

    word_map = {}
    model = ar.model_folder()
    if model:
        f = model.file('word-map', ar.MapOf(ar.String, ar.String))
        try:
            word_map, _ = f.recover()
        except ar.FileNotFound:
            pass

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(address)
            s.listen()
            # Established. Wait for inbound clients.
            while not self.halted:
                conn, addr = s.accept()
                a = self.create(accepted, conn, addr, word_map)
                self.assign(a, conn)
            # Halted. Shutdown active sessions.
            for conn, _ in self.running():
                conn.close()
            # Wait for accepted objects.
            while self.working():
                self.select(ar.Completed)
                self.debrief()
    except OSError as e:
        self.warning('Listen error - "{e}"'.format(e=str(e)))
        return ar.Nak()
    return ar.Ack()

ar.bind(listen)

def server(self, settings):
    address = (settings.host, settings.port)

    a = self.create(listen, address)
    m = self.select(ar.Stop, ar.Completed)
    if isinstance(m, ar.Stop):
        # Need to honour termination protocol. Mark the listen
        # instance and initiate a connection, to force the
        # listen object out of its blocking call.
        ar.halt(a)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(address)
            # Fall through and close.
        self.select(ar.Completed)
        return ar.Aborted()
    return ar.Ack()
    
ar.bind(server)

#
#
settings = ServerAddress('127.0.0.1', 65432)

if __name__ == '__main__':
    ar.create_object(server, compiled_settings=settings)