#!/usr/bin/env python
import socket
import settings
import connect_command
import threading
import ipaddress
import time
from sys import getsizeof

"""
يقوم بربط الخادم
ثم البحث عن خوادم عبر العميل
ثم إرسال الطلب من العميل لملف الرد (اوامر الإتصال) حسنا
يتم ارسال الطلب للخادم عبر دالة إرسال طلب من ملف اوامر الإتصال
"""

#status now
# shortcut for setting func
get_value_setting = settings.get_value_setting
prosses_manager = connect_command.prosses_messange

class lock():
    lock = 0

    def acquire(self):
        while self.locked():
            print("wait")
        #print("free")
        self.lock = 1

    def locked(self):
        return self.lock

    def release(self):
        self.lock = 0


class location():

    locations_list = []
    ip = None
    port = None
    access_location_list = lock()

    def set_ip_and_port(self, list_):
        self.ip , self.port = list_

    def set_ip_and_port_str(self, str_, split_char=":"):
        # linke "192.168.1.1:8080"
        self.ip , self.port = [(ip, int(port))
                               for ip, port in str_.split(split_char)]

    def get_ip_and_port(self):
        return (self.ip, self.port)

    def get_ip_and_port_str(self, split_char=":"):
        return self.ip+split_char+str(self.port)

    @staticmethod
    def get_ip_with_port_in_list(str_):
        a = str_.split(":")
        a[1] = int(a[1])
        return a

    @staticmethod
    def get_location_from_list_to_str(list_):
        list_[1]= str(list_[1])
        ":".join(list_)

    @staticmethod
    def get_locations_from_str_to_list(str_, split_char="/", split_ip=":"):
        list_ = [
            (ip, port)
                 for ip, port in item.split(split_ip)
                 for item in str_.split(split_char)
        ]


    @staticmethod
    def get_locations_from_list_to_str(list_):
        pass

#this is not important maybe num of it imoportant
#threads_run = {}

class server_class():

    #status = ["avalable", "busy", "not avalable", "progress"]
    # #clinet_send_to_servers_socket={}
    # setting var for connection
    start_port = get_value_setting("start_port")
    end_port = get_value_setting("end_port")
    # if bind the server_socket
    my_ip = socket.gethostbyname_ex( socket.getfqdn() )[2][0] \
                    if not get_value_setting("my_ip") else get_value_setting("my_ip")

    # use list becouse can do change with refreance only
    # but sring use less ram
    bind_socket = False
    my_port =    get_value_setting("start_port")
    # if not set in setting file get it

    #def create_socket():
    #    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # server_socket socket for receve requistes form clinet
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        print("start new server_socket")
        server_class.obj = self
        self.bind_my_server()
        #print(self.bind_socket)
        if self.bind_socket:
            self.server_listen_to_clinets()

    # getting own server_socket
    # if find port not available try with next port unless to end of ports num
    # if can bind create thread to connection with server_socket
    # else all besy port return messange cant connect

    def bind_my_server(self):
        print("my ip", self.my_ip)
        while self.bind_socket is False and self.my_port <= self.end_port:
            try:
                self.server_socket.bind((self.my_ip, self.my_port))
                print("connect with port {}".format(self.my_port))
                #skip_this_ids.append("{}:{}".format(my_ip, my_port))
                self.bind_socket = True
                #bind_the_socket[1] = time.time()
            except:
                #print("fail to connect with port {}".format(my_port))
                print("cant connect")
                self.my_port += 1

    # i prefer to do that with more than one func becose it easy to mantenas (devlop)
    # start listining to peers via socket
    def server_listen_to_clinets(self):
        listen_to_peers = get_value_setting("listening_peers")
        #print(" my id {}{}".format(my_ip, my_port))
        print("listing now to peer")
        self.server_socket.listen(5)
        clinet_socket, addr = self.server_socket.accept()
        # go final part
        #self.after_find_peer(clinet_socket, clinet_socket.recv(1024))
        threading.Thread(
            target=clinet_node,
            kwargs={"clinet socket":clinet_socket,
                    "location":clinet_socket.recv(1024)}
                         ).start()
        #clinet_node(clinet_socket=clinet_socket)
        #print("find clinet at {}".format(addr))

    def after_find_peer(self, clinet_socket, location):
        list_location = get_ip_with_port_in_list(location)
        new = clinet_node()
        clinet_socket.recv(1024)
        new.set_clinet_socket(clinet_socket)
        new.set_str_location(location)
        #threading.Thread(target=clinet_node, kwargs={"clinet_socket":clinet_socket})


class clinet_node ():

    # static var
    node_list = []

    # object var
    location = None
    clinet_socket = None
    server_socket = None
    access_node_list = lock()
    all_sockets_found = False
    #str_location = None
    #list_location = None

    @staticmethod
    def avalable_location():
        return [x.get_ip_with_port() for x in clinet_node.node_list]

    def __init__(self, *args ,**kwargs):
        if self.all_sockets_found:
            # clinet peer send to my = listen
            # server peer lister to my = send
            self.set_clinet_socket()
            self.set_server_socket()

            print("this clinet node")
            print(*args, *aargs)
            print(args, aargs)

            if self.is_in_list() == 0:
                clinet_node.access_node_list.acquire()
                clinet_node.node_list.append(self)
                clinet_node.access_node_list.release()


#    @staticmethod
#    def is_

    def set_str_location(self, str_location):
       self.str_location = str_location

    def set_clinet_socket(self, s):
        if s:
            self.clinet_socket = s

    def set_server_socket(self, s):
        if s:
            self.server_socket = s

    def get_ip_with_port(self):
        return (self.ip, self.port)


    def thread_server_connection_with_client(my_id, socket):
        # delete my_id not use
        print("now in a thread")
        #itr = 0

        try:
            global id_for_client
            id_for_client = socket.recv(1024)
            server_reseve_from_clinet_socket.append(id_for_client)
            while 1 :
                # send with connect_command return
                message = socket.recv(1024).decode()
                proseger = prosses_manager(message)
                socket.sendall(proseger)
            ##socket.sendall("{}".format(my_id).encode())
            #print("receve {} from ".format((socket.recv(1024))))
            # send list of ids to find peers quicly to peer
            #
        except Exception as err:
            #if err == "[Errno 106] Transport endpoint is already connected":
                #print("يووه مشكلة انه متصل فعلا !!! سبحان الله")
            #    pass
            #else:
            #print("there is \"{}\" ".format(err))
            #break
            # remove form avalable clinet
            print (f"oops {id_for_client} disconnected")
            server_reseve_from_clinet_socket.pop(id_for_client)

            pass


class search_auther_nodes():
    # find avoud locations
    # try connect
    # send connects to node to solve it
    #
    pass

# this is petter than nmap becose its fastest
# this work only on first time
def clinet_find_expected_servers():
    # generate ips and range port
    my_ip_zero = ".".join(my_ip.split(".")[0:3])+".0"
    all_ips = ipaddress.IPv4Network('{}/24'.format(my_ip_zero))
    num_of_all_ids = len(list(all_ips)) * (end_port - start_port)
    print(f"num of ids = {num_of_all_ids}")
    for ip in all_ips:
        for port in range(start_port, end_port+1):
                # skip avalabe location and localhost
                #print("skip this ids", skip_this_ids)
                if generate_id(ip, port) not in skip_this_ids:
                    #peers_client.append(clinet_socket())
                    threads_run[generate_id(ip , port)] = threading.Thread(target=clinet_connect_with_server,
                                         args=(str(ip), port, generate_id(ip, port)))

                    # to wait to system finsh from old try connect socket
                    while 1:
                        if len(threads_run) <= get_value_setting("max client search socket"):
                            #print("new inter")
                            threads_run[generate_id(ip, port)].start()
                            # stop after run
                            break
                    #t.join()
                        else :
                            #print(len(threads_run) , "run now ")
                            #time.sleep(.1)
                            pass

def clinet_connect_with_server(ip , port, id_server):
    # connect or skip this location
    # new socket for search
    # to easy delete it when not find or fail connection
    clinet_send_to_servers_socket[id_server] = create_socket()
    try:
            #clinet_send_to_servers_socket[id_server].settimeout(10)
            # [Errno 106] Transport endpoint is already connected
            ##print (ip, type (ip) , port,  type(port) , sep="\t")
            #print("send to {} with port {}".format(ip , port))
            clinet_send_to_servers_socket[id_server].connect((ip, port))
            clinet_send_to_servers_socket[id_server].sendall("{}".format(generate_id(my_ip , my_port)).encode())
            #id_for_peer = clinet_socket.recv()
            #print(id_for_peer, "--------------------------------------------------")

    except Exception as err:
        #print("_______________")
        if str(err) not in ["timed out1", "[Errno 113] No route to host", "[Errno 101] Network is unreachable"]  :
            #err = "غير موجود"
            print("id server_socket {} is \"{}\" ".format(id_server, str(err)))
        #print("server_socket id remove {}".format(id_server))
        clinet_send_to_servers_socket.pop(id_server)
        threads_run.pop(id_server)

    else:
        print("id server_socket {} is \"found :)\" ".format(id_server, end = "\t"))



def sent_to_server(ser_id, m):
    """snet to peer (n) message (m) """
    ## with try
    # and reconnect if fail connect

def set_to_all_list(lst, m):
    # send to all ist ids from own dectinary
    pass

def prints(x):
    print("-"*50)
    print(x)

def main():
    #main method
    # dict for save available player in network {id :ip}

    prints("binding server_socket now ...")
    bind_my_server()

    prints("start listening server_socket to clinet ...")
    threading.Thread(target=server_listen_to_clinets).start()
    #server_listen_to_clinets()

    prints("start search to auther servers (peers) ...")
    #hreading.Thread(target=clinet_find_expected_servers).start()
    t = time.time()
    clinet_find_expected_servers()



    while 1:
        if len(threads_run) == 0 :
            prints(f"finsh search auther servers (peers) with num {len(clinet_send_to_servers_socket)}\
                    \n thats take {time.time()-t} ")
            break
        else:
            time.sleep(5)
            print("this still in network search \n{}".format(len(threads_run)))

    return
def main_():
    server_class()

main_()
