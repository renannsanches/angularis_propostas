from pathlib import Path
import re, shutil

root=Path(__file__).parent
builder=root/'build.py'
source=builder.read_text(encoding='utf-8')
start=source.index("content='''")
end=source.index("'''\ncontent=",start)
template=source[start+11:end]
template=template.replace('<link rel="stylesheet" href="style.css">','<link rel="preload" href="assets/geist-latin.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="style.css"><script src="assets/gsap.min.js" defer></script><script src="assets/ScrollTrigger.min.js" defer></script>')
template=template.replace('<body>','<body><a class="skip-link" href="#planos">Ir para os planos e valores</a>')
nav='''<header><div class="wrap nav"><a class="brand-link" href="#inicio" aria-label="Angularis, início"><img class="brand" src="assets/angularis.png" alt="Agência Angularis" width="170" height="65"></a><span class="nav-context">Proposta comercial <span>para NewPlay</span></span><nav class="navlinks" aria-label="Navegação principal"><a href="#planos">Planos</a><a href="#digital">Implantação</a><a href="#processo">Etapas</a><a href="#condicoes">Condições</a></nav></div></header>'''
template=re.sub(r'<header>.*?</header>',nav,template,flags=re.S)
template=template.replace('<div class="eyebrow">Angularis × NewPlay · Proposta comercial</div>','')
template=template.replace('<div class="reveal">','<div class="hero-copy">')
template=template.replace('<a class="button" href="#planos">Explorar a proposta <span aria-hidden="true">↗</span></a>','<div class="hero-actions"><a class="button" href="#planos">Comparar planos <img src="assets/arrow-right.svg" alt="" width="20" height="20"></a><a class="text-link" href="#digital">Ver implantação digital <img src="assets/arrow-down.svg" alt="" width="18" height="18"></a></div>')
template=re.sub(r'<div class="summary-strip">.*?</div></section>', '</section>',template,count=1,flags=re.S)
# Move strategic context after the offers, bringing the decision path forward.
strategy=re.search(r'<section id="estrategia">.*?</section>',template,re.S).group()
template=template.replace(strategy,'')
template=template.replace('<section id="processo">',strategy+'\n<section id="processo">')
template=template.replace('<div class="eyebrow" style="margin-bottom:18px">Conteúdo + mídia de performance</div>','')
template=template.replace('<h2>Escolha o ritmo do crescimento.</h2>','<div class="section-heading"><h2>Escolha o ritmo<br>do crescimento.</h2><p class="section-context">Gestão mensal de conteúdo e mídia</p></div>')
template=template.replace('<div class="badge">Estrutura para crescer</div>','<div class="plan-top"><h3>NewPlay Growth</h3><span class="plan-tier">Essencial</span></div>')
template=template.replace('<h3>NewPlay Growth</h3><p class="plan-description">','<p class="plan-description">')
template=template.replace('<div class="badge">Recomendado para o lançamento</div><h3>NewPlay Scale</h3>','<div class="plan-top"><h3>NewPlay Scale</h3><span class="recommendation">Recomendado</span></div>')
template=template.replace('<a href="#escopo-mensal" class="button secondary" data-scope>Ver escopo completo <span aria-hidden="true">↗</span></a>','<a href="#escopo-growth" class="button secondary" data-scope>Conhecer o Growth <img src="assets/arrow-right-light.svg" alt="" width="20" height="20"></a>')
template=template.replace('<a href="#proximos-passos" class="button">Próximos passos <span aria-hidden="true">↗</span></a>','<a href="#escopo-scale" class="button" data-scope>Conhecer o Scale <img src="assets/arrow-right.svg" alt="" width="20" height="20"></a>')
template=template.replace('<div class="compare"><table><caption>O que muda entre os planos</caption>', '<details class="comparison-disclosure"><summary>Comparar os planos em detalhe<span class="summary-end">Escopo lado a lado <img class="disclosure-icon" src="assets/plus.svg" alt="" width="20" height="20"></span></summary><div class="compare" role="region" aria-label="Comparação dos planos" tabindex="0"><table><caption class="sr-only">O que muda entre os planos</caption>')
template=template.replace('</tbody></table></div></section>','</tbody></table></div></details></section>',1)
template=template.replace('<span class="number">01</span>','<img class="deliverable-icon" src="assets/browser.svg" alt="" width="24" height="24">').replace('<span class="number">02</span>','<img class="deliverable-icon" src="assets/target-arrow.svg" alt="" width="24" height="24">').replace('<span class="number">03</span>','<img class="deliverable-icon" src="assets/chart-dots.svg" alt="" width="24" height="24">')
template=template.replace('<div class="badge">Pacote Implantação Digital</div><h3>Três entregas.<br>Uma base integrada.</h3>','<h3>Implantação Digital</h3><p class="package-subtitle">Site + landing page + tracking</p>')
template=template.replace('<div class="price"><small>R$</small> 6.900</div>','<div class="price"><small>R$</small> 6.900<span>/projeto</span></div>')
template=template.replace('Pagamento por projeto, separado da gestão mensal. Economia de R$ 3.600 na contratação conjunta.','<span class="saving">Economia de R$ 3.600</span> na contratação conjunta. Investimento separado da gestão mensal.')
template=template.replace('<p class="note" style="margin-top:26px">','<p class="note package-deadline">')
template=template.replace('</p></aside></div><p class="note">','</p><a class="text-link" href="#escopo-digital" data-scope>Consultar escopo da implantação <img src="assets/arrow-down.svg" alt="" width="18" height="18"></a></aside></div><p class="note">')
template=template.replace('<p class="note" style="margin-top:32px">','<p class="note strategy-note">')
template=template.replace('<summary>Escopo completo · Conteúdo e performance</summary>','<summary><span>Conteúdo e performance<span class="summary-description">Entregas, responsabilidades e limites dos planos</span></span><img class="disclosure-icon" src="assets/plus.svg" alt="" width="24" height="24"></summary>')
template=template.replace('<summary>Escopo completo · Site, landing page e tracking</summary>','<summary><span>Implantação digital<span class="summary-description">Páginas, integrações, tracking e suporte</span></span><img class="disclosure-icon" src="assets/plus.svg" alt="" width="24" height="24"></summary>')
template=template.replace('<div class="document">MONTHLY_DOCUMENT</div>','<div class="document"><nav class="document-nav" aria-label="Atalhos do escopo mensal"><a href="#escopo-growth">Growth</a><a href="#escopo-scale">Scale</a><a href="#responsabilidades">Responsabilidades</a><a href="#contratacao">Contratação</a></nav>MONTHLY_DOCUMENT<button class="collapse-document" type="button">Recolher escopo <img src="assets/chevron-up.svg" alt="" width="18" height="18"></button></div>')
template=template.replace('<div class="document">DIGITAL_DOCUMENT</div>','<div class="document">DIGITAL_DOCUMENT<button class="collapse-document" type="button">Recolher escopo <img src="assets/chevron-up.svg" alt="" width="18" height="18"></button></div>')
template=template.replace('<p>Após a escolha do plano e dos serviços, a Angularis prepara o início da operação.</p>','<p>Após a escolha do plano e dos serviços, a Angularis prepara o início da operação.</p><a class="text-link" href="#planos">Voltar aos planos <img src="assets/arrow-up-right.svg" alt="" width="20" height="20"></a>')
template=template.replace('<footer class="wrap"><span>Agência Angularis<br>Estratégia, conteúdo e performance.</span><span>Proposta preparada para NewPlay</span></footer>','<footer class="wrap"><span>Agência Angularis<span class="footer-secondary">Estratégia, conteúdo e performance.</span></span><span>Preparado para <strong>NewPlay</strong></span><a href="#inicio">Voltar ao início <img src="assets/chevron-up.svg" alt="" width="18" height="18"></a></footer>')
(root/'template.html').write_text(template,encoding='utf-8')
source=source[:start]+"content=(root/'template.html').read_text(encoding='utf-8')\n"+source[end+4:]
source=source.replace("(root/'dist/index.html').write_text(content,encoding='utf-8')",'''content=content.replace('<p><strong>PLANO UM</strong></p>','<h3 id="escopo-growth" tabindex="-1">NewPlay Growth</h3>').replace('<p><strong>PLANO DOIS RECOMENDADO PARA O LANÇAMENTO</strong></p>','<h3 id="escopo-scale" tabindex="-1">NewPlay Scale</h3>').replace('<h2><strong>Para a operação funcionar</strong></h2>','<h2 id="responsabilidades">Para a operação funcionar</h2>').replace('<h2><strong>Investimento e contratação</strong></h2>','<h2 id="contratacao">Investimento e contratação</h2>')
(root/'dist/index.html').write_text(content,encoding='utf-8')''')
builder.write_text(source,encoding='utf-8')
assets=root/'dist/assets'
shutil.copyfile(root/'node_modules/@fontsource-variable/geist/files/geist-latin-wght-normal.woff2',assets/'geist-latin.woff2')
for file in ['gsap.min.js','ScrollTrigger.min.js']:
 shutil.copyfile(root/'node_modules/gsap/dist'/file,assets/file)
for name in ['arrow-right','arrow-down','arrow-up-right','plus','chevron-up','check','browser','target-arrow','chart-dots']:
 svg=(root/'node_modules/@tabler/icons/icons/outline'/f'{name}.svg').read_text()
 svg=svg.replace('stroke="currentColor"','stroke="#ede9ef"').replace('stroke-width="2"','stroke-width="1.5"')
 (assets/f'{name}.svg').write_text(svg)
svg=(assets/'arrow-right.svg').read_text()
(assets/'arrow-right-light.svg').write_text(svg)
(assets/'arrow-right.svg').write_text(svg.replace('#ede9ef','#1e1018'))
for name in ['check','browser','target-arrow','chart-dots']:
 p=assets/f'{name}.svg';p.write_text(p.read_text().replace('#ede9ef','#f47fad'))
print('Template, fonte, animações e ícones preparados.')
