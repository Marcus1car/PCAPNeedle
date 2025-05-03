Here's a polished, professional README.md for your PCAPNeedle tool:

```markdown
# PCAPNeedle 🧰

**Network Packet Analysis Made Simple**  
*Find needles in your packet haystacks*

[![Docker Build](https://img.shields.io/badge/Docker-ready-blue?logo=docker)](https://hub.docker.com/)
[![Python Version](https://img.shields.io/badge/Python-3.11%2B-green?logo=python)](https://www.python.org/)

PCAPNeedle is a command-line tool for fast pattern searching in network packet captures (PCAP files). Think `grep` for network traffic analysis, with protocol-aware filtering and JSON outputs.

---

## Features ✨

- 🔍 **Regex Pattern Matching** - Search payloads using regular expressions
- 🚦 **Protocol Filtering** - Focus on specific protocols (TCP/UDP/HTTP/DNS)
- 📦 **Docker Support** - Containerized deployment with single-command operation
- 📊 **Structured JSON Output** - Machine-readable results for easy processing
- ⚡ **Multiprocessing** - Optimized for large PCAP files
- 🛡️ **Error Resilience** - Skip malformed packets without crashing

## Quick Start 🚀

### Docker (Recommended)
```bash
# Build the image
docker build -t pcapneedle .

# Basic search (mount pcaps and output directories)
docker run -v $(pwd)/pcaps:/data -v $(pwd)/output:/app/output \
  pcapneedle /data/traffic.pcap "password" -o results.json

# Case-insensitive search with protocol filter
docker run -v $(pwd)/pcaps:/data -v $(pwd)/output:/app/output \
  pcapneedle /data/http.pcap "admin" -i -p HTTP
```

### Local Installation
```bash
# Install dependencies
pip install scapy tqdm

# Run directly
python pcapneedle.py traffic.pcap "secret" -o findings.json
```

## Usage Examples 📖

### Find API Keys in HTTP Traffic
```bash
docker run -v $(pwd)/pcaps:/data -v $(pwd)/output:/app/output \
  pcapneedle /data/prod_traffic.pcap "sk_live_[0-9a-zA-Z]{24}" -p HTTP
```

### Detect DNS Exfiltration
```bash
docker run -v $(pwd)/pcaps:/data -v $(pwd)/output:/app/output \
  pcapneedle /data/dns_logs.pcap "=[A-Za-z0-9+/]{40}=?" -p DNS
```

### Case-Insensitive Malware Pattern Search
```bash
docker run -v $(pwd)/pcaps:/data -v $(pwd)/output:/app/output \
  pcapneedle /data/suspicious.pcap "cmd.exe" -i -p TCP
```

## Output Format 📄
```json
[
  {
    "source_ip": "192.168.1.100",
    "source_port": 54321,
    "destination_ip": "10.0.0.5",
    "destination_port": 80,
    "matched_pattern": "secret",
    "payload_snippet": "GET /login?token=secret123 HTTP/1.1..."
  }
]
```

## Command Options ⚙️
| Option          | Description                          | Example               |
|-----------------|--------------------------------------|-----------------------|
| `-o`, `--output` | Output file path                     | `-o results.json`     |
| `-i`, `--ignore-case` | Case-insensitive search          | `-i "admin"`         |
| `-p`, `--protocol` | Filter by protocol layer          | `-p HTTP`            |

## Supported Protocols 🌐
`TCP`, `UDP`, `HTTP`, `DNS`, `ARP`, `ICMP`, `SSL/TLS`, and [all Scapy-supported layers](https://scapy.readthedocs.io/en/latest/layers.html)

## Troubleshooting 🔧

**No Matches Found?**  
✅ Verify your pattern works with:  
```bash
echo "testpayload" | grep -E "your_pattern"
```

**Protocol Filter Not Working?**  
✅ Use exact Scapy layer names:  
```bash
# Good
-p TCP

# Bad
-p tcp
-p HTTPRequest
```

**Permission Denied in Docker?**  
✅ Ensure volume mounts exist:  
```bash
mkdir -p pcaps output
chmod 755 pcaps output
```

## Development & Testing 🛠️
```bash
# Generate test PCAPs
python tests/generate_samples.py

# Run test suite
docker run -v $(pwd)/tests:/data pcapneedle /data/test_http.pcap "secret"

# Benchmark performance
hyperfine 'docker run pcapneedle large_capture.pcap "malware.com"'
```

## Roadmap 🗺️
- [ ] Hex pattern matching support
- [ ] Packet timestamp inclusion
- [ ] Live traffic analysis mode
- [ ] CSV output format
- [ ] Statistical summary reports

## License 📜
MIT License - See [LICENSE](LICENSE) for details
```

Key improvements:
1. Added visual hierarchy with emojis and badges
2. Structured troubleshooting section with common solutions
3. Clear development/testing instructions
4. Better organization of Docker vs local usage
5. Added real-world use case examples
6. Included protocol validation tips
7. Added performance benchmarking guidance

Would you like me to emphasize any particular aspect or adjust the tone?

# Host command
PCAP_FILE=/tests/fragmented.pcap \
PATTERN="Secret" \
PROTOCOL=TCP \
docker compose run --rm pcapneedle

# Results in output/results.json


\subsubsection{Choix du chiffrement AES-128 CBC} 

Dans les premières versions du projet, nous utilisions le chiffrement \textbf{AES-128 en mode ECB} pour sa simplicité. Ce choix a rapidement été abandonné au profit du \textbf{mode CBC} (Cipher Block Chaining), mieux adapté à nos exigences de sécurité.

Le mode CBC introduit une chaîne de dépendance entre les blocs : chaque bloc chiffré dépend du bloc précédent. Cette caractéristique permet de garantir qu’un même bloc en clair produira un résultat chiffré différent selon son contexte, empêchant ainsi toute répétition visible dans le fichier final. Un vecteur d’initialisation (IV) est utilisé pour sécuriser le chiffrement du premier bloc, assurant une bonne entropie dès le départ.

Ce fonctionnement rend l’analyse statique bien plus difficile pour un attaquant, notamment dans le cas d’un packer, où l’opacité des données est essentielle. De plus, le mode CBC reste performant et facilement intégrable dans notre pipeline de transformation.

Nous conservons l’utilisation d’une \textbf{clé symétrique de 128 bits}, qui offre un bon équilibre entre robustesse et rapidité d’exécution. L’AES-128 reste un standard éprouvé, largement utilisé dans l’industrie, et résistant aux attaques par force brute.

\begin{figure}[!h]
    \centering
    \includegraphics[width=1\linewidth]{Image/AES-CBC.png}
    \caption*{Illustration du chiffrement par blocs en mode CBC (Cipher Block Chaining)}
\end{figure}

