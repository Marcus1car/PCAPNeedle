import argparse
import re
import json
from scapy.all import rdpcap, Raw, IP

def main():
    parser = argparse.ArgumentParser(description='Search for a pattern in a pcap file')
    parser.add_argument("-o", "--output", default="output.json", help="Output JSON file (default: output.json)")
    parser.add_argument('pcap_file', help='path to pcap file')
    parser.add_argument('pattern', help='pattern to search for')
    parser.add_argument('-i','--ignore-case', action='store_true', help='Case insensitive search')
    parser.add_argument('-p','--protocol', help='Filter by protocol')
    args = parser.parse_args()
    matches = []
    
    try: 
        flags = re.IGNORECASE if args.ignore_case else 0
        regex = re.compile(args.pattern, flags)
        

        packet_number = 0
        for packet in rdpcap(args.pcap_file):
            packet_number += 1  
            
            if args.protocol and not packet.haslayer(args.protocol):
                continue
                
            if packet.haslayer(Raw):
                payload = packet[Raw].load.decode(errors='ignore')
                if regex.search(payload):
                    matches.append({
                        "packet_number": packet_number, 
                        "source_ip": packet[IP].src,
                        "source_port": packet.sport,
                        "destination_ip": packet[IP].dst,
                        "destination_port": packet.dport,
                        "matched_pattern": args.pattern,
                        "payload_snippet": payload[:100]  
                    })
                    
        with open(args.output, "w") as f:
            json.dump(matches, f, indent=2)
        print(f"[+] Results saved to {args.output}")
                
    except Exception as e:
        print(f"Error: {str(e)}")  

if __name__ == "__main__": 
    main()