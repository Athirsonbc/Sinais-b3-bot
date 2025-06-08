def calcular_gales(chance):
    if chance >= 90:
        entrada = 1.5
    elif chance >= 80:
        entrada = 2.0
    else:
        entrada = 2.5

    gale1 = round(entrada * 2, 2)
    gale2 = round(gale1 * 2, 2)

    return {
        "entrada": entrada,
        "gale1": gale1,
        "gale2": gale2,
        "total": round(entrada + gale1 + gale2, 2)
    }
