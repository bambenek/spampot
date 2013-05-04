"""
    Spampot Mail Handler Template
    Copyright (C) 2013 William A. Kennington III

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

class Msg:
    def __init__(self, to, sender, data):
        self.to = to
        self.sender = sender
        self.data = data

class BaseHandler:
    __name__ = 'Unnamed'
    def handle(self, msg):
        pass