def calculate_nps(pesquisa):
    """
    Calcula o score NPS e outras métricas para uma dada pesquisa.
    Retorna um dicionário com os resultados.
    """
    respostas = pesquisa.respostas
    if not respostas:
        return {
            'nps_score': 0,
            'total_respostas': 0,
            'promotores': 0,
            'passivos': 0,
            'detratores': 0
        }

    total_respostas = len(respostas)
    promotores = sum(1 for r in respostas if r.nota >= 9)
    passivos = sum(1 for r in respostas if r.nota in [7, 8])
    detratores = sum(1 for r in respostas if r.nota <= 6)

    # A fórmula do NPS é a porcentagem de promotores menos a porcentagem de detratores.
    nps_score = round(((promotores / total_respostas) * 100) - ((detratores / total_respostas) * 100))

    return {
        'nps_score': nps_score,
        'total_respostas': total_respostas,
        'promotores': promotores,
        'passivos': passivos,
        'detratores': detratores
    }
