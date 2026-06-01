# Mission Control AI - Global Solution 2026.1
# Disciplina: Prompt and Artificial Intelligence
# Projeto: monitoramento inteligente de uma missao espacial experimental

import random
import time
from datetime import datetime

try:
    import ollama
except Exception:
    ollama = None


def gerar_dados_missao(cenario="aleatorio"):
    """Gera dados simulados da missao espacial."""
    if cenario == "critico":
        return {
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "temperatura": random.randint(88, 105),
            "energia": random.randint(5, 19),
            "comunicacao": random.choice(["instavel", "offline"]),
            "geracao_solar": random.randint(0, 25),
            "oxigenio": random.randint(55, 72),
            "modulo": random.choice(["Habitat", "Energia", "Comunicacao", "Navegacao"]),
        }

    return {
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "temperatura": random.randint(18, 87),
        "energia": random.randint(20, 100),
        "comunicacao": random.choice(["estavel", "estavel", "instavel"]),
        "geracao_solar": random.randint(10, 95),
        "oxigenio": random.randint(73, 100),
        "modulo": random.choice(["Habitat", "Energia", "Comunicacao", "Navegacao"]),
    }


def gerar_alertas(dados):
    """Aplica regras de decisao para identificar alertas e acoes automaticas."""
    alertas = []
    acoes = []

    if dados["temperatura"] >= 85:
        alertas.append("Temperatura critica no modulo")
        acoes.append("Ativar resfriamento de emergencia")
    elif dados["temperatura"] >= 70:
        alertas.append("Temperatura elevada")
        acoes.append("Aumentar ventilacao e monitorar modulo")

    if dados["energia"] < 20:
        alertas.append("Energia abaixo do limite seguro")
        acoes.append("Ativar modo economia e desligar sistemas nao essenciais")
    elif dados["energia"] < 35:
        alertas.append("Energia em atencao")
        acoes.append("Reduzir consumo e priorizar suporte de vida")

    if dados["comunicacao"] == "offline":
        alertas.append("Comunicacao perdida")
        acoes.append("Reiniciar antena principal e ativar canal reserva")
    elif dados["comunicacao"] == "instavel":
        alertas.append("Sinal de comunicacao instavel")
        acoes.append("Ajustar antena e reenviar pacote de telemetria")

    if dados["oxigenio"] < 70:
        alertas.append("Nivel de oxigenio critico")
        acoes.append("Ativar protocolo de suporte de vida")

    if not alertas:
        alertas.append("Nenhum alerta critico identificado")
        acoes.append("Manter monitoramento padrao da missao")

    return alertas, acoes


def montar_prompt(dados, alertas, acoes):
    return f"""
Analise os dados de telemetria da missao espacial experimental.
Dados:
- Modulo: {dados['modulo']}
- Temperatura: {dados['temperatura']} graus Celsius
- Energia: {dados['energia']}%
- Comunicacao: {dados['comunicacao']}
- Geracao solar: {dados['geracao_solar']}%
- Oxigenio: {dados['oxigenio']}%

Alertas automaticos: {', '.join(alertas)}
Acoes recomendadas pelo sistema: {', '.join(acoes)}

Responda em portugues, de forma objetiva, com:
1. Status geral da missao
2. Risco principal
3. Acao imediata recomendada
""".strip()


def analisar_com_ia(dados, alertas, acoes):
    """Usa Llama via Ollama. Se nao estiver disponivel, usa fallback para manter a demonstracao funcional."""
    prompt_usuario = montar_prompt(dados, alertas, acoes)

    if ollama is not None:
        try:
            resposta = ollama.chat(
                model="llama3.2:1b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Voce e uma IA de controle de missao espacial. "
                            "Analise telemetria, identifique riscos e recomende acoes de seguranca."
                        ),
                    },
                    {"role": "user", "content": prompt_usuario},
                ],
            )
            return resposta["message"]["content"]
        except Exception as erro:
            return f"IA indisponivel no momento ({erro}). Analise local: {analise_local(dados, alertas, acoes)}"

    return analise_local(dados, alertas, acoes)


def analise_local(dados, alertas, acoes):
    """Fallback simples para testar o projeto sem Ollama instalado."""
    status = "CRITICO" if any(x in alertas for x in ["Temperatura critica no modulo", "Energia abaixo do limite seguro", "Comunicacao perdida", "Nivel de oxigenio critico"]) else "OPERACIONAL"
    return (
        f"Status geral: {status}. "
        f"Risco principal: {alertas[0]}. "
        f"Acao imediata: {acoes[0]}."
    )


def exibir_status(dados, alertas, acoes, analise_ia):
    print("=" * 60)
    print("MISSION CONTROL AI - STATUS ATUAL")
    print("=" * 60)
    print(f"Horario.........: {dados['timestamp']}")
    print(f"Modulo..........: {dados['modulo']}")
    print(f"Temperatura.....: {dados['temperatura']} C")
    print(f"Energia.........: {dados['energia']}%")
    print(f"Comunicacao.....: {dados['comunicacao']}")
    print(f"Geracao solar...: {dados['geracao_solar']}%")
    print(f"Oxigenio........: {dados['oxigenio']}%")
    print("-" * 60)
    print("ALERTAS AUTOMATICOS")
    for alerta in alertas:
        print(f"- {alerta}")
    print("-" * 60)
    print("ACOES AUTOMATIZADAS")
    for acao in acoes:
        print(f"- {acao}")
    print("-" * 60)
    print("ANALISE DA IA")
    print(analise_ia)
    print("=" * 60)


def executar_monitoramento(cenario="aleatorio", ciclos=3, intervalo=1):
    for ciclo in range(1, ciclos + 1):
        print(f"\nCICLO DE MONITORAMENTO {ciclo}/{ciclos}")
        dados = gerar_dados_missao(cenario if ciclo == ciclos else "aleatorio")
        alertas, acoes = gerar_alertas(dados)
        analise_ia = analisar_com_ia(dados, alertas, acoes)
        exibir_status(dados, alertas, acoes, analise_ia)
        time.sleep(intervalo)


if __name__ == "__main__":
    executar_monitoramento(cenario="critico", ciclos=3, intervalo=1)
