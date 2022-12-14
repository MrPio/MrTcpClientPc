import base64
import hashlib
import json
import os
import time
from typing import BinaryIO

import userpaths


class RecvHandler:
    def __init__(self):
        self.current_command:dict|None=None
        self.last_json:dict|None=None
        self.commands_queue:list[dict]=[]
        self.pkg_recv=0
        self.pkg_tot=0
        self.file_writer:BinaryIO|None=None
        self.handlers = {
            'FILE_SHARING': self.__recv_file,
        }

    def __recv_file(self, msg:bytes):
        if not self.__checksum_check(msg,self.last_json['md5']):
            print('!!!!!!!!!diversi!!!!!!!!!')
            return
        self.pkg_recv += 1

        self.file_writer.write(msg)
        percentage=round(100 * self.pkg_recv / self.pkg_tot, 2)
        print(f'{percentage} %')
        if percentage >= 100:
            self.pkg_recv,self.pkg_tot = 0,0
            print(f'File closed. took ---> {(time.time_ns() - self.file_sharing_start) / 1000000} ms')
            self.file_writer.close()
            self.current_command=None

    # ========== private ====================

    def __checksum_check(self,msg: bytes,checksum:str):
        my_base64 = base64.b64encode(msg)
        my_md5 = hashlib.md5(my_base64).hexdigest()
        return my_md5 == checksum

    def __process_json(self,msg: dict):
        self.last_json=msg
        if msg['type'] == 'command':
            # If I am already handling a command, I store the new one in the queue
            if self.current_command is not None:
                self.commands_queue.append(msg)
                return

            self.current_command=msg
            if msg['command_name'] == 'FILE_SHARING':
                # global file_tot_packets, file_name, io, start
                file_name = msg['file_name']
                self.pkg_tot = int(msg['file_packets'])
                if os.path.exists(userpaths.get_desktop() + '\\' + file_name):
                    os.remove(userpaths.get_desktop() + '\\' + file_name)
                self.file_writer = open(userpaths.get_desktop() + '\\' + file_name, 'ab')
                self.file_sharing_start = time.time_ns()

    def __process_bytes(self,msg: bytes):
        if self.current_command is None:
            return
        self.handlers[self.current_command['command_name']](msg)


    def __process_string(self,msg:str):
        print(msg)

    #========== public ======================

    def on_message(self,msg:bytes):
        # try to convert to json
        try:
            self.__process_json(json.loads(msg))
            return
        except:
            pass

        # if I am not handling a command
        '''
        Example:
        START_RECV_WEBCAM ---> incoming frames pkgs ---> STOP_RECV_WEBCAM
        START_SEND_WEBCAM --->  sending frames pkgs ---> STOP_SEND_WEBCAM
        '''
        if self.current_command is None:
            # try to convert to string
            try:
                self.__process_string(msg.decode())
                return
            except:
                pass

        # use as binary
        self.__process_bytes(msg)
        pass