# Security Log Normalizer (Syslog to ECS)

## 1. Visão Geral
Este motor de normalização transforma logs heterogéneos do padrão Syslog (RFC 5424) para o formato estruturado **Elastic Common Schema (ECS)**. A normalização é uma etapa crítica em arquiteturas de SIEM para permitir a correlação de eventos de diferentes fontes.

## 2. Especificações Técnicas
*   **Engine:** Python 3 com Expressões Regulares otimizadas.
*   **Standard Target:** ECS (Elastic Common Schema).
*   **Enriquecimento de Dados:** Conversão de Timestamps para ISO 8601 e classificação taxonómica de eventos (`event.action`).

## 3. Exemplo de Normalização (Output do Sistema)

### Input (Raw Log):
`Feb 10 08:23:15 servidor01 sshd[1234]: Failed password for admin from 10.0.0.50`

### Output (Normalizado):
- **@timestamp:** 2024-02-10T08:23:15Z
- **host.hostname:** servidor01
- **process.name:** sshd
- **event.action:** authentication_failure

## 4. Como Executar
```bash
python normalizador_syslog.py syslog_teste.log
```

---
*Projeto - Cibersegurança.*
