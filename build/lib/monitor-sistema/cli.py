import argparse
from monitor import (
    monitor_cpu,
    monitor_memoria,
    monitor_disco,
    monitor_gpu,
    monitor_rede,
    monitor_trafego_rede,
    monitorar_em_tempo_real
)

def main():
    parser = argparse.ArgumentParser(description="Monitor de Sistema em Tempo Real")
    parser.add_argument('--tempo-real', action='store_true', help="Monitorar em tempo real")
    parser.add_argument('--intervalo', type=int, default=5, help="Intervalo de atualização em segundos (default: 5s)")
    parser.add_argument('--cpu', action='store_true', help="Monitorar uso da CPU")
    parser.add_argument('--memoria', action='store_true', help="Monitorar uso da memória")
    parser.add_argument('--disco', action='store_true', help="Monitorar uso do disco")
    parser.add_argument('--gpu', action='store_true', help="Monitorar uso da GPU")
    parser.add_argument('--rede', action='store_true', help="Monitorar velocidade de rede")
    parser.add_argument('--trafego-rede', action='store_true', help="Monitorar tráfego de rede")
    parser.add_argument('--interface', type=str, default='eth0', help="Interface de rede (default: eth0)")

    args = parser.parse_args()

    if args.tempo_real:
        monitorar_em_tempo_real(intervalo=args.intervalo)

    if args.cpu:
        monitor_cpu()
    
    if args.memoria:
        monitor_memoria()

    if args.disco:
        monitor_disco()

    if args.gpu:
        monitor_gpu()

    if args.rede:
        monitor_rede()

    if args.trafego_rede:
        monitor_trafego_rede(args.interface)

if __name__ == '__main__':
    main()
