# ==============================================================================
# PARTE 1: AS FERRAMENTAS (IMPORTS)
# Aqui o Python busca caixas de ferramentas prontas para nos ajudar na construção.
# ==============================================================================

# O 'asyncio' é o nosso Cronômetro de Precisão. Ele permite que o computador
# conte o tempo (esperar segundos) sem travar as outras tarefas do programa.
import asyncio

# O 'os' (Operating System) serve para o programa conversar com o seu computador.
# Nós vamos usar ele exclusivamente para limpar a lousa do terminal (tela).
import os

# O 'sys' (System) dá acesso a comandos profundos do sistema, como fazer o
# alto-falante do computador dar um "bipe" ou fechar o programa imediatamente.
import sys

# O 'threading' é o segredo do trabalho em equipe. Ele cria uma "Thread" (uma
# linha de pensamento paralela). É como se o computador ganhasse um ajudante.
import threading

# Do 'colorama', nós pegamos as ferramentas Fore (cor do texto), Style (estilo)
# e init (preparador). Elas servem para pintar as palavras de verde, amarelo e vermelho.
from colorama import Fore, Style, init

# ==============================================================================
# PARTE 2: PREPARAÇÃO E VALIDAÇÃO
# Aqui o programa faz os testes iniciais para ter certeza de que tudo vai funcionar.
# ==============================================================================

# O 'init()' prepara o seu terminal de comando para aceitar as cores do colorama.
# Sem isso, as cores poderiam virar códigos estranhos em computadores diferentes.
init()

# O bloco 'try/except' é uma rede de segurança contra erros.
try:
    # O programa tenta ligar o "sensor do teclado" chamado 'readchar'.
    import readchar
except ImportError:
    # Se você esqueceu de instalar o 'readchar', o programa cai aqui, avisa o que
    # está faltando com uma mensagem bem clara e fecha o simulador para não dar erro.
    print("Por favor, instale a biblioteca readchar usando: pip install readchar")
    sys.exit(1)

# ==============================================================================
# PARTE 3: O MANUAL DE REGRAS E A MEMÓRIA (CONSTANTES E VARIÁVEIS)
# Aqui guardamos as regras que nunca mudam e as informações que mudam toda hora.
# ==============================================================================

# --- REGRAS DE TEMPO (Valores fixos que o semáforo usa para contar) ---
# Nota: No Python usamos números quebrados (ex: 15.0) para representar os segundos.
TEMPO_VERDE_CARROS = 15.0  # Os carros têm direito a 15 segundos de sinal verde.
TEMPO_AMARELO_CARROS = 3.0  # O sinal amarelo de atenção dura exatamente 3 segundos.
TEMPO_VERMELHO_CICLO = (
    6.0  # Se não houver pedestre, os carros esperam 6 segundos no vermelho.
)

# --- QUADRO DE MEMÓRIA (Coisas que o computador precisa lembrar enquanto roda) ---
estado_semaforo = 0  # Guarda a fase atual: 0 = Verde, 1 = Amarelo, 2 = Vermelho.
pedestre_solicitou = False  # Guarda se alguém apertou o botão. Começa como Falso.
rodando = True  # É a tomada do programa. Se virar Falso, o semáforo desliga.


# ==============================================================================
# PARTE 4: OS OPERÁRIOS ESPECIALIZADOS (FUNÇÕES DE SUPORTE)
# Cada bloco 'def' abaixo é um trabalhador treinado para fazer apenas uma coisa.
# ==============================================================================


def configurar_cor_console(estado: str):
    """OPERÁRIO 1: O Trocador de Tintas.

    Ele lê o nome do estado e escolhe a cor do texto que vai sair na tela.
    """
    if "VERDE" in estado:
        print(Fore.GREEN, end="")  # Se a palavra tem 'VERDE', use tinta verde.
    elif "AMARELO" in estado:
        print(
            Fore.YELLOW, end=""
        )  # Se a palavra tem 'AMARELO', use tinta amarela.
    elif "VERMELHO" in estado:
        print(Fore.RED, end="")  # Se a palavra tem 'VERMELHO', use tinta vermelha.
    else:
        print(# ==============================================================================
            Fore.LIGHTBLACK_EX, end=""
        )  # Se for outra coisa (como os traços), pinte de cinza escuro.


def atualizar_painel(cor_carros: str, cor_pedestres: str):
    """OPERÁRIO 2: O Desenhista do Painel.

    Ele limpa o que estava na tela e desenha o semáforo atualizado com as cores certas.
    """
    # Limpa o console. Se for Windows (nt) usa 'cls', se for Linux/Mac usa 'clear'.
    # Isso faz a tela parecer estática em vez de ficar criando texto para baixo sem parar.
    os.system("cls" if os.name == "nt" else "clear")

    # Desenha o cabeçalho do nosso painel visual
    print("=====================================================")
    print("        STATUS ATUAL DO SISTEMA DE SEMÁFOROS          ")
    print("=====================================================")

    # Desenha a linha do Semáforo dos Carros
    print(" SEMÁFORO X (Carros):    [ ", end="")
    configurar_cor_console(cor_carros)  # Ativa a cor certa para os carros
    # Imprime o nome da cor alinhado em um espaço de 10 letras e depois limpa a tinta (Style.RESET_ALL)
    print(f"{cor_carros.ljust(10)}{Style.RESET_ALL} ]")

    # Desenha a linha do Semáforo dos Pedestres
    print(" SEMÁFORO Y (Pedestres): [ ", end="")
    configurar_cor_console(cor_pedestres)  # Ativa a cor certa para os pedestres
    print(f"{cor_pedestres.ljust(10)}{Style.RESET_ALL} ]")

    print("=====================================================")

    # Checa a memória para ver se o botão está apertado e mostra o aviso luminoso na tela
    if pedestre_solicitou:
        print(
            f"{Fore.YELLOW} [!] PEDESTRE AGUARDANDO TRAVESSIA (Botão Pressionado){Style.RESET_ALL}"
        )
    else:
        print(" [-] Nenhuma solicitação de pedestre ativa.")
    print("=====================================================")


# ==============================================================================
# PARTE 5: OS PROCESSOS ASSÍNCRONOS (GERENCIAMENTO DE TEMPO REATIVO)
# As funções que têm 'async' conseguem trabalhar com o tempo de forma inteligente.
# ==============================================================================


async def aguardar_ou_interromper(segundos: float):
    """OPERÁRIO 3: O Guarda Vigilante.

    Em vez de dormir 15 segundos direto, ele divide o tempo em fatias de 0,1s e
    fica checando se o botão foi pressionado.
    """
    global pedestre_solicitou  # Pede permissão para mexer na variável global do botão
    tempo_passado = 0.0  # Começa marcando zero segundos passados

    # Enquanto o tempo que passou for menor que o tempo total que temos que esperar...
    while tempo_passado < segundos:
        # Se o pedestre apertou o botão E o semáforo ainda está verde para os carros (estado 0)...
        if pedestre_solicitou and estado_semaforo == 0:
            # Mostra na tela que o sistema entendeu o pedido e vai adiantar o fechamento
            print(
                f"{Fore.CYAN} [*] Solicitação aceita! Adiantando transição para amarelo...{Style.RESET_ALL}"
            )
            await asyncio.sleep(
                1.0
            )  # Espera apenas 1 segundo por segurança dos carros
            return  # Sai da função IMEDIATAMENTE (cancela o resto dos 15 segundos)

        # Se ninguém apertou o botão, ele tira uma soneca bem curta de 0,1 segundo...
        await asyncio.sleep(0.1)
        tempo_passado += (
            0.1  # ...e anota no caderno que já se passaram mais 0,1 segundos
        )


async def executar_rotina_pedestre():
    """OPERÁRIO 4: O Cronograma do Pedestre.

    Este bloco cuida exclusivamente do momento em que o pedestre ganha o direito de passar.
    """
    global pedestre_solicitou
    await asyncio.sleep(1.0)  # Espera 1 segundo com tudo no vermelho por segurança

    # Abre o sinal para o pedestre caminhar
    atualizar_painel(
        "VERMELHO", "VERDE 🚶‍♂️"
    )  # Carros param no vermelho, pedestre vê verde
    await asyncio.sleep(5.0)  # Garante 5 segundos para o pedestre andar com calma

    # Um ciclo de repetição (for) que vai rodar 3 vezes para fazer o sinal de texto piscar
    for _ in range(3):
        atualizar_painel(
            "VERMELHO", "--- (PISCANDO)"
        )  # Apaga o sinal do pedestre
        await asyncio.sleep(0.4)  # Espera quase meio segundo
        atualizar_painel(
            "VERMELHO", "VERMELHO (PISCANDO)"
        )  # Acende o vermelho do pedestre
        await asyncio.sleep(0.4)  # Espera quase meio segundo

    await asyncio.sleep(1.0)  # Espera 1 segundo de calmaria antes do fluxo voltar


def monitorar_botao(loop):
    """OPERÁRIO 5: O Vigia do Botão (A Thread Ajudante).

    Esta função roda em uma guarita separada (Thread). O único objetivo dela na vida
    é ficar espiando o teclado do computador sem parar para ver se você apertou algo.
    """
    global pedestre_solicitou, rodando

    # Enquanto o sistema estiver ligado...
    while rodando:
        try:
            # O 'readkey()' trava aqui e fica esperando você encostar o dedo em qualquer tecla
            key = readchar.readkey()

            # Se a tecla pressionada foi o 'ESC' do teclado:
            if key == readchar.key.ESC:
                rodando = False  # Avisa que o programa deve parar
                print("\nEncerrando o simulador...")
                os._exit(
                    0
                )  # Força o fechamento de todas as janelas e desliga tudo

            # Se a tecla foi 'Espaço' ou se foi o 'Enter':
            elif key in (
                readchar.key.SPACE,
                readchar.key.ENTER,
                "\r",
                "\n",
                " ",
            ):
                # Se o botão já não tiver sido apertado antes:
                if not pedestre_solicitou:
                    pedestre_solicitou = (
                        True  # Ativa o aviso de que há pedestre esperando
                    )
                    sys.stdout.write(
                        "\a"
                    )  # Envia o comando ASCII especial que faz a placa-mãe dar um "Bipe"
                    sys.stdout.flush()  # Força o som a sair na mesma hora
        except Exception:
            pass  # Se der qualquer erro na leitura do teclado, ignore para o programa não cair


# ==============================================================================
# PARTE 6: O MAESTRO DO TRÂNSITO (LOOP PRINCIPAL DE ESTADOS)
# Aqui fica o coração do semáforo, alternando entre as fases de forma eterna.
# ==============================================================================


async def main_async():
    """OPERÁRIO 6: O Gerente Geral do Fluxo.

    Ele coordena a mudança das fases (Verde -> Amarelo -> Vermelho -> Verde).
    """
    global estado_semaforo, pedestre_solicitou, rodando

    # Pega o controle do relógio atual do Python
    loop = asyncio.get_event_loop()
    # Cria o ajudante em paralelo (Thread), liga ele na função 'monitorar_botao' e dá a partida!
    threading.Thread(target=monitorar_botao, args=(loop,), daemon=True).start()

    # Este loop 'while rodando' cria o ciclo eterno do semáforo da rua
    while rodando:

        # --- FASE 0: VERDE PARA OS CARROS ---
        if estado_semaforo == 0:
            atualizar_painel(
                "VERDE", "VERMELHO"
            )  # Liga o painel: Verde para Carros, Vermelho para Pedestres
            # Entra na espera inteligente de 15s (que pode ser cortada se apertarem o botão)
            await aguardar_ou_interromper(TEMPO_VERDE_CARROS)
            estado_semaforo = 1  # Quando o tempo acaba ou é cortado, diz que a próxima fase é a 1

        # --- FASE 1: AMARELO PARA OS CARROS ---
        elif estado_semaforo == 1:
            atualizar_painel(
                "AMARELO", "VERMELHO"
            )  # Liga o painel de atenção para os motoristas
            await asyncio.sleep(
                TEMPO_AMARELO_CARROS
            )  # Espera os 3 segundos obrigatórios sem interrupção
            estado_semaforo = 2  # Avisa que a próxima fase é a 2

        # --- FASE 2: VERMELHO PARA OS CARROS (HORA DE DECIDIR) ---
        elif estado_semaforo == 2:
            atualizar_painel(
                "VERMELHO", "VERMELHO"
            )  # Tudo fechado por um breve instante de segurança

            # O gerente olha para a variável do botão para decidir o que fazer:
            if pedestre_solicitou:
                # Se o botão está apertado (True), ele chama a rotina especial de travessia do pedestre
                await executar_rotina_pedestre()
                pedestre_solicitou = (
                    False  # Depois que o pedestre passou, zera o botão para Falso
                )
            else:
                # Se ninguém apertou o botão, faz o ciclo automático comum de carros (espera 6s no vermelho)
                atualizar_painel("VERMELHO", "VERMELHO (Ciclo Auto)")
                await asyncio.sleep(TEMPO_VERMELHO_CICLO)

            estado_semaforo = (
                0  # Reinicia a máquina! Joga o estado para 0 (Verde dos carros)
            )


# ==============================================================================
# PARTE 7: A IGNIÇÃO (O PONTO DE PARTIDA DO PROGRAMA)
# É aqui que o Python bate a chave do motor quando você aperta o "Play".
# ==============================================================================


def main():
    """OPERÁRIO 7: O Recepcionista.

    Ele mostra as boas-vindas e inicia o sistema assíncrono.
    """
    # Imprime as instruções iniciais na tela para o usuário saber o que fazer
    print("=====================================================")
    print("       SIMULADOR DE SEMÁFORO INTERTRAVADO            ")
    print("=====================================================")
    print(" Pressione [Espaço] ou [Enter] para simular o Botão  ")
    print(" Pressione [ESC] para fechar o programa              ")
    print("=====================================================\n")

    import time

    time.sleep(
        2
    )  # Dá uma pausa de 2 segundos para o humano conseguir ler o menu acima

    try:
        # Dá a partida oficial no sistema assíncrono rodando o Gerente Geral (main_async)
        asyncio.run(main_async())
    except KeyboardInterrupt:
        # Se o usuário apertar CTRL+C no teclado, fecha o programa educadamente
        print("\nPrograma finalizado pelo usuário.")




# Esta linha abaixo é padrão do Python. Ela significa: "Se este arquivo estiver sendo
# executado diretamente pelo usuário, comece chamando a função main() ali de cima".
if __name__ == "__main__":
    main()
