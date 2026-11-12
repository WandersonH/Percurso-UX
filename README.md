# Percurso UX

Landing page de um curso online fictício de UX, feita como avaliação do 2º bimestre da disciplina **Experiência do Usuário (UX)**, do curso de Análise e Desenvolvimento de Sistemas da **Fatec Franca**.

- **Docente:** Carlos Alberto Lucas
- **Autoria:** Wanderson Honorio Roberto da Silva
- **Apresentação:** 12/11/2026

> O curso, o preço e a inscrição são fictícios. O formulário é uma simulação: nenhum dado é enviado e nada é cobrado.

## Como abrir

Abra o arquivo `index.html` em qualquer navegador. Não há instalação nem servidor.

Com o GitHub Pages ativado neste repositório (Settings › Pages › branch `main`), o site fica em `https://wandersonh.github.io/Percurso-UX/`.

## Onde está a documentação

A documentação pedida no enunciado fica dentro da própria página: clique em **"Ver como este projeto foi feito"**, no topo ou no rodapé, ou abra `index.html#processo`. Ela mostra:

1. Resumo do projeto: objetivo, público, problema de UX.
2. As quatro fases do Duplo Diamante e onde cada uma aparece na página.
3. As dez heurísticas de Nielsen, com o local de aplicação e como verificar cada uma.
4. Arquitetura da informação: três pilares e quatro sistemas.
5. Limitações e validações pendentes.
6. Anexos: matriz CSD, pesquisa de mesa, roteiro de entrevista, proto-persona, mapa de empatia, jornada, fluxo de inscrição, rascunho de baixa fidelidade, design system, acessibilidade e plano de teste de usabilidade.

Cada afirmação sobre o usuário está marcada como **evidência**, **hipótese** ou **não verificado**. Nenhuma entrevista ou teste com usuários foi realizado.

## Como demonstrar as heurísticas

| Para ver | Faça |
|---|---|
| Visibilidade do status | Role a página e observe o menu; envie o formulário preenchido |
| Prevenção de erros | Digite `nome@gmial.com` no e-mail; digite só números no celular |
| Recuperação de erros | Envie o formulário vazio; depois use um e-mail terminado em `@erro.teste` para simular falha de envio |
| Controle e liberdade | Preencha, clique em "Limpar formulário" e depois em "Desfazer" |
| Flexibilidade | Clique em "Abrir todos os módulos"; abra "Acessibilidade" no topo |

## Estrutura

```
index.html                  página do curso e documentação (HTML, CSS e JavaScript em um arquivo)
testes/auditoria_axe.py     roteiro da auditoria automática de acessibilidade
testes/relatorio_axe.json   resultado da auditoria de 12/11/2026
```

## Acessibilidade

- Painel "Acessibilidade" com tamanho do texto, contraste reforçado, espaçamento de leitura e animações desligadas.
- Navegação completa por teclado, link "Pular para o conteúdo" e estados anunciados para leitores de tela.
- Auditoria com axe-core 4.14.0 (regras WCAG 2.0, 2.1 e 2.2, níveis A e AA): nenhuma violação em 12 cenários.

Limites: ferramentas automáticas encontram só parte dos problemas. Não houve teste com leitor de tela nem com pessoas com deficiência, e a página não tem tradução em Libras.

Para repetir a auditoria:

```
npm install axe-core
pip install playwright
python3 testes/auditoria_axe.py index.html
```

## Tecnologia

HTML, CSS e JavaScript sem framework. O enunciado não pontua tecnologia; um único arquivo abre em qualquer navegador e publica em qualquer hospedagem estática.
