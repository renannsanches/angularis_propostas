from pathlib import Path
import re,html,json
root=Path(__file__).parent
def inline(s):
 s=html.escape(s.replace('\\.','.'))
 s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
 return re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<em>\1</em>',s)
def md(text):
 lines=text.splitlines();out=[];i=0
 while i<len(lines):
  s=lines[i].strip();i+=1
  if not s or s=='---':continue
  if s.startswith('|'):
   rows=[s]
   while i<len(lines) and lines[i].strip().startswith('|'):rows.append(lines[i].strip());i+=1
   rows=[r for r in rows if not re.match(r'^\|[\s:|\-]+\|$',r)]
   out.append('<table><tbody>'+''.join('<tr>'+''.join('<td>'+inline(c.strip())+'</td>' for c in r.strip('|').split('|'))+'</tr>' for r in rows)+'</tbody></table>');continue
  m=re.match(r'^(#{1,6})\s+(.*)',s)
  if m:
   level=min(len(m[1])+1,5);out.append(f'<h{level}>'+inline(m[2])+f'</h{level}>');continue
  if re.match(r'^(?:[-*]|\d+\.)\s',s):
   items=[re.sub(r'^(?:[-*]|\d+\.)\s+','',s)]
   while i<len(lines) and re.match(r'^(?:[-*]|\d+\.)\s',lines[i].strip()):items.append(re.sub(r'^(?:[-*]|\d+\.)\s+','',lines[i].strip()));i+=1
   out.append('<ul>'+''.join('<li>'+inline(x)+'</li>' for x in items)+'</ul>');continue
  out.append('<p>'+inline(s)+'</p>')
 return ''.join(out)
content=(root/'template.html').read_text(encoding='utf-8')
content=content.replace('MONTHLY_DOCUMENT',md((root/'content/Proposta_Comercial_NewPlay.md').read_text(encoding='utf-8-sig'))).replace('DIGITAL_DOCUMENT',md((root/'content/Proposta_NewPlay_Sites_e_Tracking.md').read_text(encoding='utf-8-sig')))
content=content.replace('<h2><strong>Para a operação funcionar</strong></h2>','<h2 id="responsabilidades">Para a operação funcionar</h2>').replace('<h2><strong>Investimento e contratação</strong></h2>','<h2 id="contratacao">Investimento e contratação</h2>')
(root/'dist/index.html').write_text(content,encoding='utf-8')
manifest=root/'.openai/hosting.json'
data=json.loads(manifest.read_text(encoding='utf-8-sig'));data['static']={'directory':'dist'};manifest.write_text(json.dumps(data,indent=2),encoding='utf-8')
print('Site completo gerado; ambos os documentos incorporados.')

