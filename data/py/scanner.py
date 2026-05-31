from scapy.all import *
import io,sys,json,os
import threading
import time


acks = {}
prevAcks = [-1 for i in range(len(list(conf.ifaces.data.values())))];
existingIpIds = {}
existingTcpSeqs = {}
loads = {}

def try_buffer(key):
    buffers = acks[key];

    buffers = sorted(buffers, key=lambda x: x['seq'])
    finalBuffer = b''
    for i in buffers:
        finalBuffer += i['data']

    hexStr = ''
    try:
        hexStr = finalBuffer.hex();
    except:
        hexStr = ''.join(x.encode('hex') for x in finalBuffer);

    print(hexStr);
    print('&');

def check_packet(packet):
    if IP in packet:
        if Raw in packet and packet[Raw].load:
            # Key reassembly by the full TCP connection 4-tuple plus the
            # ack value, not by ack alone. Ack numbers are per-connection
            # and can collide across the many short-lived TCP connections
            # the game opens during a scan; keying on ack alone caused
            # unrelated streams to be concatenated, producing garbage
            # buffers the upstream parser drops. This shows up as item
            # counts going DOWN when more data is captured.
            key = (
                packet[IP].src, packet[TCP].sport,
                packet[IP].dst, packet[TCP].dport,
                packet.ack,
            )
            packet_bytes = bytes(packet[Raw].load)

            if packet_bytes.hex() in loads:
                return
            else:
                loads[packet_bytes.hex()] = True

            if key in acks:
                acks[key].append({'data': packet_bytes, 'seq': packet[TCP].seq})
            else:
                acks[key] = [{'data': packet_bytes, 'seq': packet[TCP].seq}]

def terminate():
    os._exit(0)

def _pickable_ifaces():
    # On Linux, multi-interface sniff() can include the same TCP stream
    # twice when a hotspot is active (once on the wifi iface from the
    # client and again on the upstream iface after NAT), which confuses
    # stream reassembly. Allow an override via env var; otherwise prefer
    # a single wireless interface if available, falling back to ethernet.
    override = os.environ.get('FRIBBELS_SCAN_IFACE')
    if override:
        return [override]

    skip_prefixes = ('lo', 'docker', 'br-', 'veth', 'virbr', 'tun', 'tap')
    names = []
    for i in get_working_ifaces():
        n = getattr(i, 'name', str(i))
        if n.startswith(skip_prefixes):
            continue
        names.append(n)

    # Prefer wireless (wl*, wlan*, wlp*) when present — that's the
    # hotspot interface where phone traffic shows up uniquely.
    wireless = [n for n in names if n.startswith(('wl', 'wlan', 'wlp'))]
    if wireless:
        return wireless[:1]

    return names or [get_working_ifaces()[0].name]

def thread_sniff():
    try:
        # EpicSeven traffic was confirmed to travel over tcp port 3333 via Wireshark.
        # Pass interface names (strings) and exclude virtual interfaces so Linux
        # hotspot setups capture phone traffic reliably.
        ifaces = _pickable_ifaces()
        print("scanner: sniffing on", ifaces, file=sys.stderr)
        sniff(iface=ifaces, prn=lambda x: check_packet(x), filter="tcp and ( port 5222 or port 3333 )", session=TCPSession)
    except Exception as e:
        print("scanner: sniff failed:", e, file=sys.stderr)

x = threading.Thread(target=thread_sniff)
x.daemon = True;
x.start()

t = threading.Timer(3600.0, terminate)
t.start()

loop = True
while loop:
    line = sys.stdin.readline()
    if "E" in line:
        for key in list(acks):
            try_buffer(key)
        loop = False
        print("DONE\n")
        sys.stdout.flush()