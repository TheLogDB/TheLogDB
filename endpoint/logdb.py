#!/usr/bin/env python3

import argparse
import subprocess
import sys
import os
import json
import yaml
import requests
import logging
from datetime import datetime
from pathlib import Path

# Optional: If implementing file monitoring in Live Mode
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler

# Configure internal logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("logdb_endpoint.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def load_config(config_path):
    """
    Load configuration from a YAML or JSON file.
    """
    if not os.path.exists(config_path):
        logging.error(f"Configuration file {config_path} not found.")
        sys.exit(1)
    
    with open(config_path, 'r') as f:
        if config_path.endswith('.yaml') or config_path.endswith('.yml'):
            config = yaml.safe_load(f)
        elif config_path.endswith('.json'):
            config = json.load(f)
        else:
            logging.error("Unsupported configuration file format. Use YAML or JSON.")
            sys.exit(1)
    
    return config

def send_log(server_address, api_key, log_entry):
    """
    Send a single log entry to the LogDB server.
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    try:
        response = requests.post(server_address, headers=headers, json=log_entry)
        if response.status_code in [200, 201]:
            logging.info("Log sent successfully.")
        else:
            logging.error(f"Failed to send log. Status Code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        logging.error(f"Error sending log: {e}")

def parse_live_mode(pipe_input, server_address, api_key):
    """
    Handle Live Mode: Read from stdin and send logs in real-time.
    Usage: /some/exec | logdb_endpoint.py --live
    """
    logging.info("Running in Live Mode.")
    for line in sys.stdin:
        log_entry = {
            "logLevel": "INFO",  # Default level; can be enhanced to parse levels
            "message": line.strip(),
            "module": "Live Mode",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        send_log(server_address, api_key, log_entry)

def parse_archive_mode(path, recursive, date_format, server_address, api_key):
    """
    Handle Archive Mode: Read log files and send them to the server.
    Usage: logdb_endpoint.py --archive /path/to/log --recursive --date-format "yyyy-MM-dd HH:mm:ss Z"
    """
    logging.info("Running in Archive Mode.")
    path = Path(path)
    if not path.exists():
        logging.error(f"Path {path} does not exist.")
        sys.exit(1)
    
    if path.is_file():
        files = [path]
    elif path.is_dir():
        if recursive:
            files = list(path.rglob("*.log"))  # Assuming log files have .log extension
        else:
            files = list(path.glob("*.log"))
    else:
        logging.error(f"Path {path} is neither a file nor a directory.")
        sys.exit(1)
    
    for file in files:
        logging.info(f"Processing file: {file}")
        try:
            with open(file, 'r') as f:
                for line in f:
                    timestamp = None
                    message = line.strip()
                    if date_format:
                        try:
                            # Example format: yyyy-MM-dd HH:mm:ss Z
                            # Python equivalent: %Y-%m-%d %H:%M:%S %z
                            # Adjust based on the provided date_format
                            # Here, we assume the timestamp is at the start of the line
                            # e.g., "2024-12-05 04:54:20 +0800 Log message"
                            # Split the line into timestamp and message
                            parts = line.split(' ', 2)
                            if len(parts) >= 3:
                                timestamp_str = ' '.join(parts[:3])
                                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S %z").isoformat()
                                message = parts[3] if len(parts) > 3 else ""
                        except Exception as e:
                            logging.warning(f"Failed to parse timestamp: {e}")
                            timestamp = datetime.utcnow().isoformat() + "Z"
                    
                    log_entry = {
                        "logLevel": "INFO",  # Default level; can be enhanced to parse levels
                        "message": message,
                        "module": "Archive Mode",
                        "timestamp": timestamp if timestamp else datetime.utcnow().isoformat() + "Z"
                    }
                    send_log(server_address, api_key, log_entry)
        except Exception as e:
            logging.error(f"Error processing file {file}: {e}")

def main():
    parser = argparse.ArgumentParser(description="LogDB Endpoint Client")
    subparsers = parser.add_subparsers(dest='mode', help='Mode of operation')
    
    # Live Mode
    live_parser = subparsers.add_parser('live', help='Run in Live Mode')
    
    # Archive Mode
    archive_parser = subparsers.add_parser('archive', help='Run in Archive Mode')
    archive_parser.add_argument('path', type=str, help='Path to log file or directory')
    archive_parser.add_argument('-r', '--recursive', action='store_true', help='Recursively process directories')
    archive_parser.add_argument('--date-format', type=str, help='Date format of log entries (Unicode Technical Standard #35)')
    
    # Common argument for configuration file
    parser.add_argument('--config', type=str, default='config.yaml', help='Path to configuration file (YAML or JSON)')
    
    args = parser.parse_args()
    
    if not args.mode:
        parser.print_help()
        sys.exit(1)
    
    config = load_config(args.config)
    server_address = config.get('server', {}).get('address')
    api_key = config.get('server', {}).get('api_key') or config.get('auth', {}).get('token')
    
    if not server_address or not api_key:
        logging.error("Server address and API key/token must be provided in the configuration file.")
        sys.exit(1)
    
    if args.mode == 'live':
        parse_live_mode(sys.stdin, server_address, api_key)
    elif args.mode == 'archive':
        parse_archive_mode(args.path, args.recursive, args.date_format, server_address, api_key)
    else:
        logging.error("Unknown mode selected.")
        sys.exit(1)

if __name__ == '__main__':
    main()
