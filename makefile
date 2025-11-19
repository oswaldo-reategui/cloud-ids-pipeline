# ────────────────────────────────────────────────────
# Makefile shortcuts for common operations
# ────────────────────────────────────────────────────

# Start the core services (Redis & Zeek) in detached mode
up:
	docker compose up -d redis zeek

# Replay the PCAP once through the Zeek container,
# then exit and remove the temporary replayer container
replay:
	docker compose run --rm replayer

# Follow Zeek’s primary connection log in real time
logs:
	tail -f data/zeek/conn.log

# Start the Python Consumer in detached mode
consumer:
	docker compose up -d consumer

# ────────────────────────────────────────────────────
# Kubernetes cluster management via Minikube
# ────────────────────────────────────────────────────

# Start Minikube cluster on Docker
minikube-up:
	minikube start --driver=docker --kubernetes-version=v1.29.0

# Stops and deletes the Minikube cluster, freeing resources
minikube-down:
	minikube delete