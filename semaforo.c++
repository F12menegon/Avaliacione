// =====================================================================
// DEFINIÇÃO DOS PINOS DO HARDWARE (Onde os fios estão ligados)
// =====================================================================
// Semáforo da Avenida Principal
const int LED_PRINCIPAL_VERDE = 2;
const int LED_PRINCIPAL_AMARELO = 3;
const int LED_PRINCIPAL_VERMELHO = 4;

// Semáforo da Rua Secundária
const int LED_SECUNDARIO_VERDE = 5;
const int LED_SECUNDARIO_AMARELO = 6;
const int LED_SECUNDARIO_VERMELHO = 7;

// Sensores IoT (Entradas)
const int PINO_BOTAO_PEDESTRE = 8;
const int PINO_SENSOR_CARRO = 9; // Simula um sensor de presença/asfalto

// Constantes de Tempo (em milissegundos)
const unsigned long TEMPO_AMARELO = 3000;       // 3 segundos
const unsigned long TEMPO_MINIMO_VERDE = 5000;   // Garante 5s aberto para a avenida

// CONFIGURAÇÃO INICIAL DO MICROCONTROLADOR
void setup() {
  // Configura os pinos dos LEDs como SAÍDA de energia
  pinMode(LED_PRINCIPAL_VERDE, OUTPUT);
  pinMode(LED_PRINCIPAL_AMARELO, OUTPUT);
  pinMode(LED_PRINCIPAL_VERMELHO, OUTPUT);
  
  pinMode(LED_SECUNDARIO_VERDE, OUTPUT);
  pinMode(LED_SECUNDARIO_AMARELO, OUTPUT);
  pinMode(LED_SECUNDARIO_VERMELHO, OUTPUT);
  
  // Configura os pinos dos sensores como ENTRADA de sinal
  pinMode(PINO_BOTAO_PEDESTRE, INPUT_PULLUP); // Usa resistor interno do chip
  pinMode(PINO_SENSOR_CARRO, INPUT_PULLUP);
  
  // Estado Inicial: Avenida Principal Aberta, Rua Secundária Fechada
  abrirViaPrincipal();
}


// LOOP PRINCIPAL (Roda infinitamente no chip do semáforo)
void loop() {
  // O semáforo inteligente fica lendo os sensores em tempo real
  bool pedestreChamou = (digitalRead(PINO_BOTAO_PEDESTRE) == LOW); // LOW significa pressionado
  bool carroEsperando = (digitalRead(PINO_SENSOR_CARRO) == LOW);   // Carro detectado pelo sensor
  
  // Se houver demanda na via secundária ou pedestre querendo atravessar
  if (pedestreChamou || carroEsperando) {
    
    // 1. Mantém o verde da avenida por um tempo mínimo de segurança
    delay(TEMPO_MINIMO_VERDE);
    
    // 2. Transição: Avenida Principal vai para Amarelo
    digitalWrite(LED_PRINCIPAL_VERDE, LOW);
    digitalWrite(LED_PRINCIPAL_AMARELO, HIGH);
    delay(TEMPO_AMARELO);
    
    // 3. Fecha Avenida Principal, Abre Rua Secundária
    digitalWrite(LED_PRINCIPAL_AMARELO, LOW);
    digitalWrite(LED_PRINCIPAL_VERMELHO, HIGH);
    
    digitalWrite(LED_SECUNDARIO_VERMELHO, LOW);
    digitalWrite(LED_SECUNDARIO_VERDE, HIGH);
    
    // 4. Tempo que o sinal fica aberto para a rua secundária/pedestre
    delay(6000); // 6 segundos de fluxo
    
    // 5. Transição: Rua Secundária vai para Amarelo
    digitalWrite(LED_SECUNDARIO_VERDE, LOW);
    digitalWrite(LED_SECUNDARIO_AMARELO, HIGH);
    delay(TEMPO_AMARELO);
    
    // 6. Fecha Rua Secundária e reabre a Avenida Principal
    digitalWrite(LED_SECUNDARIO_AMARELO, LOW);
    digitalWrite(LED_SECUNDARIO_VERMELHO, HIGH);
    
    abrirViaPrincipal();
  }
  
  delay(150); // Pequena pausa para estabilizar as leituras dos sensores
}

// =====================================================================
// FUNÇÕES AUXILIARES
// =====================================================================
void abrirViaPrincipal() {
  // Garante o estado seguro de prioridade da avenida
  digitalWrite(LED_PRINCIPAL_VERMELHO, LOW);
  digitalWrite(LED_PRINCIPAL_AMARELO, LOW);
  digitalWrite(LED_PRINCIPAL_VERDE, HIGH);
  
  digitalWrite(LED_SECUNDARIO_VERDE, LOW);
  digitalWrite(LED_SECUNDARIO_AMARELO, LOW);
  digitalWrite(LED_SECUNDARIO_VERMELHO, HIGH);
}