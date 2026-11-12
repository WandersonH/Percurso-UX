"""Auditoria automática de acessibilidade do Percurso UX com axe-core.

Uso:  python3 auditoria_axe.py caminho/para/index.html
Requer: Python 3, playwright (pip install playwright), Google Chrome e
        axe-core (npm install axe-core) na pasta atual.
Gera:   relatorio_axe.json com o resultado de cada cenário.
"""
import json, sys, datetime, pathlib
from playwright.sync_api import sync_playwright

ARQUIVO = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "index.html").resolve()
AXE = pathlib.Path("node_modules/axe-core/axe.min.js").resolve()
REGRAS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"]
CENARIOS = []

def auditar(pg, nome, largura, modo):
    pg.add_script_tag(path=str(AXE))
    r = pg.evaluate("(tags) => axe.run(document, {runOnly: {type: 'tag', values: tags}})", REGRAS)
    CENARIOS.append({
        "cenario": nome, "largura_px": largura, "modo": modo,
        "regras_aprovadas": len(r["passes"]),
        "violacoes": [{"regra": v["id"], "impacto": v["impact"], "descricao": v["help"], "elementos": [n["target"] for n in v["nodes"]]} for v in r["violations"]],
        "revisao_manual": [{"regra": i["id"], "elementos": len(i["nodes"])} for i in r["incomplete"]],
    })
    return r["testEngine"]["version"]

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    versao_chrome = b.version
    for modo in ("padrão", "contraste reforçado"):
        for largura in (1280, 390):
            pg = b.new_page(viewport={"width": largura, "height": 800})
            pg.goto(ARQUIVO.as_uri()); pg.wait_for_timeout(800)
            if modo != "padrão":
                pg.evaluate("document.documentElement.setAttribute('data-contrast', 'alto')")
            abrir = "document.querySelectorAll('details').forEach(d => d.open = true)"
            pg.evaluate(abrir)
            versao_axe = auditar(pg, "Página do curso, tudo expandido", largura, modo)
            pg.click("#submit-btn"); pg.wait_for_timeout(200)
            auditar(pg, "Formulário enviado vazio (estado de erro)", largura, modo)
            pg.evaluate("location.hash = 'processo'"); pg.wait_for_timeout(400); pg.evaluate(abrir)
            auditar(pg, "Documentação, anexos abertos", largura, modo)
            pg.close()
    b.close()

relatorio = {
    "projeto": "Percurso UX", "arquivo": ARQUIVO.name,
    "data": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
    "ferramenta": f"axe-core {versao_axe}", "navegador": f"Google Chrome {versao_chrome} (headless)",
    "regras": REGRAS,
    "limitacoes": "Ferramentas automáticas detectam só parte dos problemas de acessibilidade. Itens em 'revisao_manual' são casos que o axe-core não consegue decidir sozinho (por exemplo, contraste de texto sobre fundo composto). Não substitui teste com leitor de tela nem com pessoas com deficiência. Executado com as fontes de reserva do sistema, sem acesso ao Google Fonts.",
    "total_cenarios": len(CENARIOS), "total_violacoes": sum(len(c["violacoes"]) for c in CENARIOS),
    "cenarios": CENARIOS,
}
pathlib.Path("relatorio_axe.json").write_text(json.dumps(relatorio, ensure_ascii=False, indent=2), encoding="utf-8")
print(relatorio["ferramenta"], "|", relatorio["navegador"])
for c in CENARIOS:
    print(f'{c["largura_px"]:>5} px | {c["modo"]:<20} | {c["cenario"]:<42} | aprovadas {c["regras_aprovadas"]:>2} | violações {len(c["violacoes"])} | revisão manual {sum(i["elementos"] for i in c["revisao_manual"])}')
print("Total de violações:", relatorio["total_violacoes"])
