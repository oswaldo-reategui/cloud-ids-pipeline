#!/usr/bin/env python3
"""
Continuously waits for Zeek’s conn.log (JSON lines), then tails it
and XADDs each record into the Redis stream “zeek:conn.”

We flatten each JSON object into a simple dict of strings so Redis can store it
as key/value pairs in the stream.
"""

import os
import time
import json
import redis

# Configuration – read Redis connection info from environment
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
STREAM_KEY = "zeek:conn"                        # name of the Redis Stream we will XADD into

# Inside the container, Zeek writes its JSON lines to /logs/conn.log
LOG_PATH = "/logs/conn.log"

def wait_for_file(path, timeout=60):
    """
    Wait up to `timeout` seconds for the given file to exist.
    Returns True if the file exists within the timeout; False otherwise.
    """
    start = time.time()
    while not os.path.exists(path):
        if time.time() - start > timeout:
            return False
        time.sleep(0.5)
    return True

def flatten_record(record):
    """
    Takes a JSON object (which include nested lists/dicts) and flattens it
    into a dict where each value is a string:
      - Strings, ints, floats become their own string form.
      - Booleans become "True"/"False".
      - Lists or dicts are dumped back to JSON text.
    """
    flat = {}
    for key, value in record.items():
        if isinstance(value, (str, int, float)):
            flat[key] = str(value)
        elif isinstance(value, bool):
            flat[key] = "True" if value else "False"
        else:
            # For lists, dicts, or anything else, JSON‐serialize it
            flat[key] = json.dumps(value)
    return flat

def tail_and_stream():
    """
    Main loop: connect to Redis, wait for Zeek’s conn.log file, then tail it.
    For each new line:
      1. Parse JSON
      2. Flatten record
      3. XADD into Redis stream
    """
    # Connect to Redis server
    client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    # Ensure conn.log exists before tailing
    print(f"Waiting for {LOG_PATH} …")
    if not wait_for_file(LOG_PATH, timeout=60):
        print(f"ERROR: {LOG_PATH} did not appear in 60s. Exiting.")
        return

    print(f"{LOG_PATH} found. Starting to tail …")

    # Open file and seek to end; we only want new appends
    with open(LOG_PATH, "r") as f:
        f.seek(0, os.SEEK_END)

        # Continuously loop, reading one line at a time
        while True:
            line = f.readline()
            if not line:
                # If no new line, sleep briefly and retry
                time.sleep(0.1)
                continue

            try:
                # Parse the JSON line into a Python dict
                record = json.loads(line)
            except json.JSONDecodeError:
                # Skip any invalid JSON line
                continue

            # Flatten nested structures and convert all values to strings
            safe_record = flatten_record(record)

            # Push the flattened record into the Redis stream
            msg_id = client.xadd(STREAM_KEY, safe_record)
            print(f"Pushed record {msg_id} to {STREAM_KEY}")

if __name__ == "__main__":
    # Entry point: start the tail & stream loop
    tail_and_stream()
