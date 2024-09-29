import psutil
import GPUtil
from ping3 import ping
import speedtest
import time

def monitor_cpu(threshold=80):
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_temp = None
    try:
        temps = psutil.sensors_temperatures()
        if 'coretemp' in temps:
            cpu_temp = temps['coretemp'][0].current
    except:
        pass

    if cpu_usage > threshold:
        print(f"ALERTA: Uso da CPU acima do limite! ({cpu_usage}%)")
    else:
        print(f"Uso da CPU: {cpu_usage}%")
    
    if cpu_temp:
        print(f"Temperatura da CPU: {cpu_temp}°C")
    
    return cpu_usage, cpu_temp

def monitor_memoria(threshold=80):
    mem = psutil.virtual_memory()
    mem_usage = mem.percent
    if mem_usage > threshold:
        print(f"ALERTA: Uso de memória acima do limite! ({mem_usage}%)")
    else:
        print(f"Uso de memória: {mem_usage}%")
    
    return mem_usage

def monitor_disco(threshold=80):
    disk_usage = psutil.disk_usage('/').percent
    if disk_usage > threshold:
        print(f"ALERTA: Uso do disco acima do limite! ({disk_usage}%)")
    else:
        print(f"Uso de disco: {disk_usage}%")
    
    return disk_usage

def monitor_gpu(threshold=80):
    gpus = GPUtil.getGPUs()
    for gpu in gpus:
        gpu_usage = gpu.load * 100
        gpu_temp = gpu.temperature
        if gpu_usage > threshold:
            print(f"ALERTA: Uso da GPU {gpu.name} acima do limite! ({gpu_usage}%)")
        else:
            print(f"Uso da GPU {gpu.name}: {gpu_usage}%")
        
        print(f"Temperatura da GPU {gpu.name}: {gpu_temp}°C")
    
    return [(gpu.name, gpu_usage, gpu_temp) for gpu in gpus]

def monitor_rede():
    st = speedtest.Speedtest()
    download_speed = st.download() / 1_000_000  # Mbps
    upload_speed = st.upload() / 1_000_000      # Mbps
    ping_latency = st.results.ping

    print(f"Velocidade de Download: {download_speed:.2f} Mbps")
    print(f"Velocidade de Upload: {upload_speed:.2f} Mbps")
    print(f"Latência (Ping): {ping_latency:.2f} ms")
    
    return download_speed, upload_speed, ping_latency

def monitor_trafego_rede(interface='eth0'):
    net_io = psutil.net_io_counters(pernic=True)
    if interface in net_io:
        traffic = net_io[interface]
        print(f"Trafego de rede {interface}:")
        print(f"Bytes enviados: {traffic.bytes_sent / 1_000_000:.2f} MB")
        print(f"Bytes recebidos: {traffic.bytes_recv / 1_000_000:.2f} MB")
    else:
        print(f"Interface {interface} não encontrada.")
    
    return net_io

def monitorar_em_tempo_real(intervalo=5):
    try:
        while True:
            print("\n--- Monitoramento em Tempo Real ---")
            monitor_cpu()
            monitor_memoria()
            monitor_disco()
            monitor_gpu()
            monitor_rede()
            print(f"Próxima atualização em {intervalo} segundos...")
            time.sleep(intervalo)
    except KeyboardInterrupt:
        print("\nMonitoramento interrompido pelo usuário.")
