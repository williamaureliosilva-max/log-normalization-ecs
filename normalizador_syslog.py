#!/usr/bin/env python3
"""
normalizador_syslog.py
Normaliza linhas de Syslog para um formato padrao com campos fixos.
UC01482 - Atividade 3-4
"""

import re
import json
import sys
from datetime import datetime

PADRAO_SYSLOG = re.compile(
    r'^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+(\S+?)(?:\[(\d+)\])?:\s+(.*)'
)

# Mapeamento de nomes de mes para numero
MESES = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
    "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
    "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
}

def normalizar_timestamp(ts_raw):
    """Converte 'Feb 10 08:23:15' para '2024-02-10T08:23:15Z'"""
    partes = ts_raw.split()
    mes = MESES.get(partes[0], 1)
    dia = int(partes[1])
    hora = partes[2]
    return "2024-{:02d}-{:02d}T{}Z".format(mes, dia, hora)

def classificar_evento(mensagem):
    """Classifica o tipo de evento com base na mensagem."""
    msg = mensagem.lower()
    if "failed password" in msg or "authentication failure" in msg:
        return "authentication_failure"
    elif "accepted password" in msg or "session opened" in msg:
        return "authentication_success"
    elif "connection closed" in msg or "disconnected" in msg:
        return "connection_closed"
    elif "cmd" in msg or "command" in msg:
        return "command_execution"
    else:
        return "unknown"

def normalizar_linha(linha_raw):
    """Transforma uma linha Syslog num dicionario normalizado."""
    linha = linha_raw.strip()
    m = PADRAO_SYSLOG.match(linha)
    if not m:
        return None

    timestamp_raw = m.group(1)
    hostname = m.group(2)
    programa = m.group(3)
    pid = m.group(4) or "N/A"
    mensagem = m.group(5)

    return {
        "@timestamp": normalizar_timestamp(timestamp_raw),
        "timestamp_original": timestamp_raw,
        "host.hostname": hostname,
        "process.name": programa,
        "process.pid": pid,
        "message": mensagem,
        "event.action": classificar_evento(mensagem),
        "log.source": "syslog"
    }

def processar_ficheiro(caminho):
    """Le e normaliza todas as linhas do ficheiro."""
    try:
        with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
            linhas = f.readlines()
    except FileNotFoundError:
        print("ERRO: Ficheiro '" + caminho + "' nao encontrado.")
        sys.exit(1)

    print("=== NORMALIZADOR SYSLOG ===")
    print("Ficheiro: " + caminho)
    print("Total de linhas: " + str(len(linhas)))
    print("=" * 50)

    normalizados = 0
    falhados = 0

    for i, linha in enumerate(linhas):
        linha = linha.strip()
        if not linha:
            continue

        resultado = normalizar_linha(linha)

        print("\n--- Linha " + str(i+1) + " ---")
        print("ORIGINAL : " + linha[:90])
        if resultado:
            print("RESULTADO:")
            for campo, valor in resultado.items():
                print("  " + campo + ": " + str(valor))
            normalizados += 1
        else:
            print("RESULTADO: [LINHA NAO RECONHECIDA - ignorada]")
            falhados += 1

    print("\n" + "=" * 50)
    print("Linhas normalizadas: " + str(normalizados))
    print("Linhas nao reconhecidas: " + str(falhados))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python normalizador_syslog.py <ficheiro.log>")
        sys.exit(1)
    processar_ficheiro(sys.argv[1])