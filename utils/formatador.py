def formatar_mensagem(sinal):
    if sinal["duracao"] == "longo prazo":
        return f"""
🏗 INVESTIMENTO DE LONGO PRAZO DETECTADO

Ativo: {sinal['ativo']}
Tipo: {sinal['tipo']}
Chance de Valorização: {sinal['chance']}%
Duração estimada: {sinal['duracao']}

💸 Estratégia sugerida:
Entrada mínima: {sinal['estrategia']['minimo']}
Sugestão: {sinal['estrategia']['entrada']}
"""
    else:
        return f"""
📊 SINAL DETECTADO
Ativo: {sinal['ativo']}
Tipo: {sinal['tipo']}
Entrada: imediata
Duração: {sinal['duracao']} minutos
Chance de Green: {sinal['chance']}%

💸 Estratégia sugerida:
1ª entrada: {sinal['estrategia']['entrada']}%
Gale 1: {sinal['estrategia']['gale1']}%
Gale 2: {sinal['estrategia']['gale2']}%
Total do ciclo: {sinal['estrategia']['total']}%
"""

def mensagem_monitoramento():
    return "📡 Estamos analisando o mercado em tempo real. Em breve traremos novas oportunidades!"
