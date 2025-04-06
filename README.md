# PCAPNeedle     

Forensic tool for PCAP file analysis and pattern matching.

CLI tool for fast pattern searching in network packet captures (PCAP files).     
A `grep` for network traffic analysis, with protocol-aware filtering and JSON out puts. 


## Key Features 🔒
- **Regex Pattern Hunting**: Advanced pattern matching in packet payloads
- **Protocol-Aware Filtering**: Layer 3-7 protocol isolation
- **Performance Optimized**: Multiprocessing for faster analysis of large captures
- **Docker Sandboxing**: Containerized execution for portability
- **Structured Output**: JSON results for automated processing and integration
- **Case Sensitivity Control**: Configurable case-sensitive or insensitive searching with the addition of `-i`


## File Structure 🏗  
```
.
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
├── src/
│   └── pcapneedle.py  
├── pcaps/                 # Add your PCAP's files here
├── output/                # Results are stored here
├── tests/                 # Sample PCAP's files for testing
│   ├── http_login.pcap
│   └── test_http.pcap
└── README.md
```

## Quick Start 

**1. Build your container**  

```bash
mkdir -p pcaps output
docker compose build
```    

**2. Basic Pattern Search with a custom output**     
```bash
docker compose run --rm pcapneedle \
  /tests/http_login.pcap "password" -o findings.json
```

**3. Protocol-Filtered Analysis**      
```bash
docker compose run --rm pcapneedle \
  /data/dns_logs.pcap "malware.com" -p DNS
```

**4. Case-Insensitive Search**
```bash
docker compose run --rm pcapneedle \
  /data/http_traffic.pcap "login" -i
```

**Direct Python Usage**     
For local execution without Docker:    
```bash
python src/pcapneedle.py /path/to/capture.pcap "pattern" -p HTTP -i -o output/results.json
```

## Configuration and Usage 🔧 

**Command Options**     
| Option          | Description                          | Example               |
|-----------------|--------------------------------------|-----------------------|
| `-o`, `--output` | Output file path                     | `-o results.json`     |
| `-i`, `--ignore-case` | Case-insensitive search          | `-i "admin"`         |
| `-p`, `--protocol` | Filter by protocol layer          | `-p HTTP`            |

**Supported Protocols 🌐**    
`TCP`, `UDP`, `HTTP`, `DNS`, `ARP`, `ICMP`, `SSL/TLS`, and [all Scapy-supported layers](https://scapy.readthedocs.io/en/latest/layers.html)


**Environment Variables**

Configure the tool using environment variables in the docker-compose.yaml file:

```yaml
environment:
  - PCAP_FILE=${PCAP_FILE:-/data/sample.pcap}
  - PATTERN=${PATTERN:-secret}
  - PROTOCOL=${PROTOCOL:-}
  - IGNORE_CASE=${IGNORE_CASE:-false}
  - OUTPUT_FILE=${OUTPUT_FILE:-/app/output/results.json}
```

**Output Format**     
The tool generates structured JSON output with the following fields:     
```json
[
  {
    "source_ip": "192.168.1.100",
    "source_port": 52123,
    "destination_ip": "93.184.216.34",
    "destination_port": 80,
    "matched_pattern": "password",
    "payload_snippet": "username=admin&password=SecretPassword123"
  }
]
```

## Examples

**Finding Login Credentials**

```bash
docker compose run --rm pcapneedle \
  /data/http_traffic.pcap "username|password" -p HTTP
```

**Detecting API Keys**

```bash
docker compose run --rm pcapneedle \
  /data/api_traffic.pcap "api[-_]?key" -i
```

**Scanning for Email Addresses**

```bash
docker compose run --rm pcapneedle \
  /data/smtp_traffic.pcap "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
```