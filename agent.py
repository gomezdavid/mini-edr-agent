from datetime import datetime
import psutil


def get_timestamp():
    return datetime.now().isoformat()


def collect_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
        try:
            processes.append({
                "pid": proc.info['pid'],
                "name": proc.info['name'],
                "username": proc.info['username'],
                "cpu": proc.info['cpu_percent'],
                "memory": proc.info['memory_percent'],
                "timestamp": get_timestamp()
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return processes


def collect_connections():
    connections = []
    for conn in psutil.net_connections():
        try:
            connections.append({
                "local_ip": conn.laddr.ip if conn.laddr else None,
                "local_port": conn.laddr.port if conn.laddr else None,
                "remote_ip": conn.raddr.ip if conn.raddr else None,
                "remote_port": conn.raddr.port if conn.raddr else None,
                "status": conn.status,
                "timestamp": get_timestamp()
            })
        except Exception:
            continue
    return connections
