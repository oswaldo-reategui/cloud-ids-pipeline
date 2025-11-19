# **Cloud IDS Pipeline: Zeek + Redis Streams + tcpreplay**

**Author:** Oswaldo Reategui Garcia  
**University:** University of London

## **1. Overview**

This repository contains the **network telemetry ingestion pipeline** developed as part of my MSc thesis on cloud-native intrusion detection.

It provides a containerised environment that replays PCAP traffic, parses it through Zeek, converts logs to JSON, and streams them into Redis for downstream processing:

```
tcpreplay → Zeek 7.1 (JSON logs) → Redis Streams → Python Consumer
```

The goal is to provide a **low-latency, modular, and reproducible environment** for real-time inspection of network flows and integration with security analytics systems.

The complete thesis package (report, datasets, analytical notebooks, and figures) is private and available on request.

## **2. Architecture**

```
          +-------------------+
          |   example.pcap    |
          +---------+---------+
                    |
                    v
        +-----------+-----------+
        |      tcpreplay        |
        |   (replayer container)|
        +-----------+-----------+
                    |
                    v
          +---------+---------+
          |       Zeek        |
          |  JSON log output  |
          |   (IDS engine)    |
          +---------+---------+
                    |
                    v
        +-----------+-----------+
        |      Redis Streams     |
        |     stream: zeek:conn  |
        +-----------+-----------+
                    |
                    v
          +---------+---------+
          |   Python Consumer |
          |  (flatten & XADD) |
          +-------------------+
```

## **3. Repository Structure**

```
cloud-ids-pipeline/
├─ consumer/
│  ├─ Dockerfile
│  ├─ requirements.txt
│  └─ zeek_to_redis.py        # Tails Zeek logs and XADDs records to Redis
│
├─ replayer/
│  └─ Dockerfile              # tcpreplay container to inject PCAP traffic
│
├─ data/
│  ├─ pcap/
│  │  └─ example.pcap         # Included for standalone demo
│  ├─ zeek/                   # Zeek writes JSON logs here at runtime
│  │  └─ .gitkeep             # Folder kept empty in repo
│  ├─ TrafficCSV/             # Empty; user provides CICIDS2017 CSV files
│
├─ docker-compose.yml         # Orchestration for Redis, Zeek, Consumer, Replay
├─ makefile                   # Convenience commands
└─ README.md                  # This file
```

## **4. Quickstart Demo (using example.pcap)**

This requires **Docker Desktop**.

### **1) Start Redis and Zeek**

```bash
make up
```

### **2) Start the Python consumer**

```bash
make consumer
```

### **3) Replay the sample PCAP**

```bash
make replay
```

### **4) View Zeek logs**

```bash
make logs
```

### **5) Inspect Redis stream**

```bash
docker exec -it ids_redis redis-cli
XREAD STREAMS zeek:conn 0
```

### **Shutdown**

```bash
docker compose down
```

## **5. CICIDS2017 Dataset (Optional)**

To reproduce full experiments, download CICIDS2017 from:

[https://www.unb.ca/cic/datasets/ids-2017.html](https://www.unb.ca/cic/datasets/ids-2017.html)

Place the CSV files into:

```
data/TrafficCSV/
```

This dataset is **not included** in the repository. The code should be modified for this dataset.

---

## **6. Make Commands**

| Command         | Description                      |
| --------------- | -------------------------------- |
| `make up`       | Start Redis and Zeek containers  |
| `make consumer` | Start the Python consumer        |
| `make replay`   | Replay example.pcap through Zeek |
| `make logs`     | Follow Zeek’s connection log     |

## **7. License**

MIT © 2025 Oswaldo Reategui Garcia