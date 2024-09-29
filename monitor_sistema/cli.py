import argparse
import psutil
import GPUtil
import speedtest
from ping3 import ping


# Função para monitorar CPU
def monitor_cpu():
    print(f"Uso da CPU: {psutil.cpu_percent(interval=1)}%")

# Função para monitorar Memória
def monitor_memoria():
    memoria = psutil.virtual_memory()
    print(f"Uso de Memória: {memoria.percent}%")

# Função para monitorar o uso do Disco
def monitor_disco(limite_alerta=90):
    discos = psutil.disk_partitions()
    for disco in discos:
        uso_disco = psutil.disk_usage(disco.mountpoint)
        print(f"Uso do Disco ({disco.device}): {uso_disco.percent}%")
        if uso_disco.percent > limite_alerta:
            print(f"ALERTA: Uso de disco acima de {limite_alerta}% no {disco.device}")

# Função para monitorar a GPU
def monitor_gpu():
    gpus = GPUtil.getGPUs()
    if gpus:
        for gpu in gpus:
            print(f"Uso da GPU ({gpu.name}): {gpu.load * 100}%")
            print(f"Temperatura da GPU ({gpu.name}): {gpu.temperature}°C")
    else:
        print("Nenhuma GPU detectada.")

# Função para monitorar Rede (velocidade de conexão e tráfego de dados)
def monitor_rede():
    st = speedtest.Speedtest()
    st.get_best_server()

    # Medir a velocidade de download e upload
    velocidade_download = st.download() / 1_000_000  # Convertido para Mbps
    velocidade_upload = st.upload() / 1_000_000  # Convertido para Mbps
    print(f"Velocidade de Download: {velocidade_download:.2f} Mbps")
    print(f"Velocidade de Upload: {velocidade_upload:.2f} Mbps")

    # Tráfego de dados (total de bytes enviados e recebidos)
    io_rede = psutil.net_io_counters()
    print(f"Total Enviado: {io_rede.bytes_sent / 1_000_000:.2f} MB")
    print(f"Total Recebido: {io_rede.bytes_recv / 1_000_000:.2f} MB")

# Função para monitorar Latência de Rede (Ping)
def monitor_ping(host='8.8.8.8', limite_alerta=100):
    latencia = ping(host) * 1000  # Convertido para ms
    if latencia is None:
        print(f"Falha ao conectar ao servidor {host}")
    else:
        print(f"Ping para {host}: {latencia:.2f} ms")
        if latencia > limite_alerta:
            print(f"ALERTA: Latência alta (>{limite_alerta} ms) para o servidor {host}")


# Função principal do CLI
def main():
    parser = argparse.ArgumentParser(description="Monitor de Sistema via CLI")
    
    # Adicionar opções de linha de comando
    parser.add_argument('--cpu', action='store_true', help="Monitora o uso de CPU")
    parser.add_argument('--memoria', action='store_true', help="Monitora o uso de memória")
    parser.add_argument('--disco', action='store_true', help="Monitora o uso de Disco")
    parser.add_argument('--gpu', action='store_true', help="Monitora o uso da GPU")
    parser.add_argument('--rede', action='store_true', help="Monitora a velocidade e tráfego de Rede")
    parser.add_argument('--ping', action='store_true', help="Verifica a latência de rede (Ping)")
    
    # Parse dos argumentos
    args = parser.parse_args()

    # Verifique qual argumento foi passado e execute a função correspondente
    if args.cpu:
        monitor_cpu()
    elif args.memoria:
        monitor_memoria()
    elif args.disco:
        monitor_disco()
    elif args.gpu:
        monitor_gpu()
    elif args.rede:
        monitor_rede()
    elif args.ping:
        monitor_ping()
    else:
        print("Por favor, use uma das opções: --cpu, --memoria, --disco, --gpu, --rede, --ping")

if __name__ == "__main__":
    main()
