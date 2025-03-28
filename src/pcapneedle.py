import argparse
import re
from scapy.all import rdpcap, Raw, IP
def main() :
    parser = argparse.ArgumentParser(description='Search for a pattern in a pcap file')
    parser.add_argument('pcap_file', help='path to pcap file')
    parser.add_argument('pattern', help='pattern to search for')
    parser.add_argument('-i','--ignore-case', action='store_true', help='Case insensitive search')
    parser.add_argument('-p','--protocol' ,help='Filter by protocol')
    args = parser.parse_args()
    
    try: 
        flags = re.IGNORECASE if args.ignore_case else 0
        regex = re.compile(args.pattern, flags)
        
        for packet in rdpcap(args.pcap_file):
            if args.protocol and not packet.haslayer(args.protocol):
                continue
            if packet.haslayer(Raw):
                payload = packet[Raw].load.decode(errors    ='ignore')
                if regex.search(payload):
                    print(f"[+] match pattern in pcap file {packet.number}")
                    print(f"    Source: {packet[IP].src}:{packet.sport}")
                    print(f"    Dest: {packet[IP].dst}:{packet.dport}")
                    print(f"    Payload: {payload[:100]}...\n")
                                
                                
    except Exception as e :
        print(f"Error: {e}")

if __name__ == "__main__" : 
    main()
        