    
    
import argparse
import re
import json
from scapy.all import PcapReader, Raw, IP
from scapy.config import conf
from multiprocessing import Pool, cpu_count

def validate_protocol(protocol):
    valid_layers = [layer.__name__ for layer in conf.layers]
    if protocol not in valid_layers:
        raise ValueError(f"Invalid protocol. Valid: {', '.join(valid_layers)}")

def process_packet(packet, args):
    try:
        if args.protocol and not packet.haslayer(args.protocol):
            return None
        
        if packet.haslayer(Raw):
            payload = packet[Raw].load.decode(errors='ignore')
            if args.regex.search(payload):
                return {
                    "source_ip": packet[IP].src if packet.haslayer(IP) else "N/A",
                    "source_port": packet.sport if hasattr(packet, 'sport') else 0,
                    "destination_ip": packet[IP].dst if packet.haslayer(IP) else "N/A",
                    "destination_port": packet.dport if hasattr(packet, 'dport') else 0,
                    "matched_pattern": args.pattern,
                    "payload_snippet": payload[:100]
                }
        return None
    except Exception as e:
        print(f"Skipping packet: {str(e)}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Search for patterns in PCAP files')
    parser.add_argument("-o", "--output", default="output.json", help="Output JSON file")
    parser.add_argument('pcap_file', help='Path to pcap file')
    parser.add_argument('pattern', help='Pattern to search for')
    parser.add_argument('-i', '--ignore-case', action='store_true', help='Case-insensitive search')
    parser.add_argument('-p', '--protocol', help='Filter by protocol')
    args = parser.parse_args()

    try:
        
        # compile regex and validate protocol
        flags = re.IGNORECASE if args.ignore_case else 0
        args.regex = re.compile(args.pattern, flags)
        if args.protocol:
            validate_protocol(args.protocol)
        # Process packets
        packets = PcapReader(args.pcap_file)
        with Pool(cpu_count()) as pool:
            results = pool.starmap(process_packet, [(pkt, args) for pkt in packets])
        # save to result.json
        matches = [res for res in results if res]
        with open(args.output, "w") as f:
            json.dump(matches, f, indent=2)
        print(f"[+] Results saved to {args.output}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__": 
    main()