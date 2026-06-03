using System;
using System.Threading.Tasks;

namespace SimuladorSemaforo
{
    class Program
    {
        private const int TEMPO_VERDE_CARROS   = 15000;
        private const int TEMPO_AMARELO_CARROS = 3000;
        private const int TEMPO_VERMELHO_CICLO = 6000;

        private static int estadoSemaforo = 0;
        private static bool pedestreSolicitou = false;
        private static bool rodando = true;

        static void Main(string[] args)
        {
            Console.WriteLine("=====================================================");
            Console.WriteLine("       SIMULADOR DE SEMÁFORO INTERTRAVADO            ");
            Console.WriteLine("=====================================================");
            Console.WriteLine(" Pressione [Espaço] ou [Enter] para simular o Botão  ");
            Console.WriteLine(" Pressione [ESC] para fechar o programa              ");
            Console.WriteLine("=====================================================\n");

            MainAsync().GetAwaiter().GetResult();
        }

        private static async Task MainAsync()
        {
            _ = Task.Run(() => MonitorarBotao());

            while (rodando)
            {
                switch (estadoSemaforo)
                {
                    case 0:
                        AtualizarPainel("VERDE", "VERMELHO");
                        await AguardarOuInterromper(TEMPO_VERDE_CARROS);
                        estadoSemaforo = 1; 
                        break;

                    case 1:
                        AtualizarPainel("AMARELO", "VERMELHO");
                        await Task.Delay(TEMPO_AMARELO_CARROS);
                        estadoSemaforo = 2; 
                        break;

                    case 2:
                        AtualizarPainel("VERMELHO", "VERMELHO"); 

                        if (pedestreSolicitou)
                        {
                            await ExecutarRotinaPedestre();
                            pedestreSolicitou = false;
                        }
                        else
                        {
                            AtualizarPainel("VERMELHO", "VERMELHO (Ciclo Auto)");
                            await Task.Delay(TEMPO_VERMELHO_CICLO);
                        }

                        estadoSemaforo = 0; 
                        break;
                }
            }
        }

        private static async Task ExecutarRotinaPedestre()
        {
            await Task.Delay(1000);

            AtualizarPainel("VERMED_VERMELHO", "VERDE 🚶‍♂️"); // Mantém carros fechados
            AtualizarPainel("VERMELHO", "VERDE 🚶‍♂️");
            await Task.Delay(5000);

            for (int i = 0; i < 3; i++)
            {
                AtualizarPainel("VERMELHO", "--- (PISCANDO)");
                await Task.Delay(400);
                AtualizarPainel("VERMELHO", "VERMELHO (PISCANDO)");
                await Task.Delay(400);
            }

            await Task.Delay(1000);
        }

        private static async Task AguardarOuInterromper(int milissegundos)
        {
            int tempoPassado = 0;
            while (tempoPassado < milissegundos)
            {
                if (pedestreSolicitou && estadoSemaforo == 0)
                {
                    Console.ForegroundColor = ConsoleColor.Cyan;
                    Console.WriteLine(" [*] Solicitação aceita! Adiantando transição para amarelo...");
                    Console.ResetColor();
                    await Task.Delay(1000); 
                    return;
                }
                await Task.Delay(100);
                tempoPassado += 100;
            }
        }

        private static void MonitorarBotao()
        {
            while (rodando)
            {
                if (Console.KeyAvailable)
                {
                    ConsoleKeyInfo tecla = Console.ReadKey(true);
                    if (tecla.Key == ConsoleKey.Escape)
                    {
                        rodando = false;
                        Environment.Exit(0);
                    }
                    else if (!pedestreSolicitou)
                    {
                        pedestreSolicitou = true;
                        try { Console.Beep(800, 150); } catch { }
                    }
                }
                Task.Delay(50).Wait();
            }
        }

        private static void AtualizarPainel(string corCarros, string corPedestres)
        {
            Console.Clear();
            Console.WriteLine("=====================================================");
            Console.WriteLine("       STATUS ATUAL DO SISTEMA DE SEMÁFOROS          ");
            Console.WriteLine("=====================================================");
            
            Console.Write(" SEMÁFORO X (Carros):    [ ");
            ConfigurarCorConsole(corCarros);
            Console.Write(corCarros.PadRight(10));
            Console.ForegroundColor = ConsoleColor.Gray;
            Console.WriteLine(" ]");

            Console.Write(" SEMÁFORO Y (Pedestres): [ ");
            ConfigurarCorConsole(corPedestres);
            Console.Write(corPedestres.PadRight(10));
            Console.ForegroundColor = ConsoleColor.Gray;
            Console.WriteLine(" ]");

            Console.WriteLine("=====================================================");
            if (pedestreSolicitou)
            {
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine(" [!] PEDESTRE AGUARDANDO TRAVESSIA (Botão Pressionado)");
                Console.ResetColor();
            }
            else
            {
                Console.WriteLine(" [-] Nenhuma solicitação de pedestre ativa.");
            }
            Console.WriteLine("=====================================================");
        }

        private static void ConfigurarCorConsole(string estado)
        {
            if (estado.Contains("VERDE")) Console.ForegroundColor = ConsoleColor.Green;
            else if (estado.Contains("AMARELO")) Console.ForegroundColor = ConsoleColor.Yellow;
            else if (estado.Contains("VERMELHO")) Console.ForegroundColor = ConsoleColor.Red;
            else Console.ForegroundColor = ConsoleColor.DarkGray;
        }
    }
}
