from gpio import *
from time import *

ledTopo = 0   # LED Vermelho
ledMeio = 1   # LED Verde
ledBaixo = 2  # LED Amarelo

def setup():
    pinMode(ledTopo, OUTPUT)
    pinMode(ledMeio, OUTPUT)
    pinMode(ledBaixo, OUTPUT)

def loop():
    digitalWrite(ledTopo, HIGH)   # LIGA Vermelho
    digitalWrite(ledMeio, LOW)    # Desliga Verde
    digitalWrite(ledBaixo, LOW)   # Desliga Amarelo
    delay(100)

if __name__ == "__main__":
    setup()
    while True:
        loop()
