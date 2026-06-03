import time
import random

# =====================================================================
# CONFIGURAÇÕES INICIAIS E ESTADOS DO SISTEMA
# =====================================================================
# Estados possíveis para os semáforos: "VERDE", "AMARELO", "VERMELHO"
semaforo_principal = "VERDE"
semaforo_secundario = "VERMELHO"

# Tempos de transição (em segundos)
TEMPO_AMARELO = 2
TEMPO_ABERTO_SECUNDARIO = 5
TEMPO_MINIMO_PRINCIPAL = 3

# =====================================================================
# FUNÇÕES DE LEITURA DOS DISPOSITIVOS IoT (SIMULAÇÃO)
# =====================================================================
def ler_sensores_trafego():
    """
    Simula a leitura dos sensores IoT nas vias.
    Retorna True se houver demanda na via secundária ou pedestre esperando.
    """
    # Na vida real, aqui leríamos os pinos de entrada do hardware (Ex: Arduino/Raspberry Pi)
    carro_via_secundaria = random.choice([True, False])
    pedestre_botao = random.choice([True, False])
    
    return carro_via_secundaria, pedestre_botao

def verificar_integridade_sistema():
    """
    Simula a checagem de falhas do sistema (lâmpadas queimadas ou cabos furtados).
    Retorna True se o sistema estiver operando normalmente.
    """
    # Simula uma chance muito pequena de falha física no dispositivo IoT
    falha_detectada = random.choices([False, True], weights=[95, 5])[0]
    return not falha_detectada

# =====================================================================
# ALGORITMO PRINCIPAL DE GERENCIAMENTO DE TRÁFEGO
# =====================================================================
def executar_gerenciador_iot():
    global semaforo_principal, semaforo_secundario
    
    print("\n==================================================")
    print("      INICIANDO SISTEMA DE TRÁFEGO INTELIGENTE    ")
    print("==================================================")
    
    # Loop contínuo de funcionamento do semáforo
    for ciclo in range(1, 4):  # Simula 3 ciclos de funcionamento
        print(f"\n[CICLO N° {ciclo}]")
        
        # 1. Checagem de Segurança (IoT Remoto)
        if not verificar_integridade_sistema():
            print("[ALERTA CRÍTICO] Falha física ou furto de cabos detectado!")
            print("Ação de Emergência: Ativando AMARELO PISCANTE em ambas as vias.")
            semaforo_principal = "AMARELO PISCANTE"
            semaforo_secundario = "AMARELO PISCANTE"
            print(f"Status - Principal: {semaforo_principal} | Secundária: {semaforo_secundario}")
            print("Notificação enviada remotamente para a CET.")
            break # Interrompe para manutenção
            
        # 2. Estado Padrão: Prioridade para a Via Principal Flow
        semaforo_principal = "VERDE"
        semaforo_secundario = "VERMELHO"
        print(f"Status Atual -> Via Principal: {semaforo_principal} | Via Secundária: {semaforo_secundario}")
        print("-> Fluxo normal na avenida principal. Aguardando dados dos sensores...")
        time.sleep(TEMPO_MINIMO_PRINCIPAL)
        
        # 3. Leitura inteligente dos sensores IoT
        carro_esperando, pedestre_esperando = ler_sensores_trafego()
        
        # 4. Tomada de Decisão com base nos dados
        if carro_esperando or pedestre_esperando:
            if carro_esperando:
                print("[SENSÓR] Carro detectado aguardando na via secundária.")
            if pedestre_esperando:
                print("[BOTÃO] Pedestre solicitou travessia segura.")
                
            print("\nModificando tráfego de forma inteligente...")
            
            # Transição: Principal vai para Amarelo
            semaforo_principal = "AMARELO"
            print(f"Mudança -> Via Principal: {semaforo_principal} | Via Secundária: {semaforo_secundario}")
            time.sleep(TEMPO_AMARELO)
            
            # Libera a Via Secundária / Pedestre
            semaforo_principal = "VERMELHO"
            semaforo_secundario = "VERDE"
            print(f"Mudança -> Via Principal: {semaforo_principal} | Via Secundária: {semaforo_secundario}")
            print(f"-> Tráfego fluindo na via secundária por {TEMPO_ABERTO_SECUNDARIO} segundos.")
            time.sleep(TEMPO_ABERTO_SECUNDARIO)
            
            # Retorna a prioridade para a via principal
            print("\nEncerrando tempo da via secundária. Retornando prioridade...")
            semaforo_secundario = "AMARELO"
            print(f"Mudança -> Via Principal: {semaforo_principal} | Via Secundária: {semaforo_secundario}")
            time.sleep(TEMPO_AMARELO)
            
        else:
            print("-> Nenhum carro ou pedestre detectado nas vias secundárias.")
            print("-> Mantendo sinal VERDE na via principal para evitar congestionamentos.")
            time.sleep(2)

# Executa o programa
if __name__ == "__main__":
    executar_gerenciador_iot()
