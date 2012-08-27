#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin
from socketio.sdjango import namespace
from dwitter.main.utils import redis_connection
import json

@namespace('/dwits')
class DwitsNamespace(BaseNamespace, RoomsMixin):

    def initialize(self):
        self.logger = logging.getLogger("socketio.dwits")
        self.log("Socketio session started")
        
    def log(self, message):
        self.logger.info("[{0}] {1}".format(self.socket.sessid, message))

    def listener(self, room):
        r = redis_connection().pubsub()
        r.subscribe('socketio_%s' % room)

        for m in r.listen():
            if m['type'] == 'message':
                data = json.loads(m['data'])
                self.process_event(data)
                    
    def on_join(self, room):
        self.room = room
        self.spawn(self.listener, room)
        self.join(room)
        return True

    def on_newdwit(self, *args):
        self.emit('newdwit', *args)

    def recv_disconnect(self):
        self.log('Disconnected')
        self.kill_local_jobs()
        self.disconnect(silent=True)
