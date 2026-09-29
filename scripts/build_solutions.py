"""Build static solution cards and detail pages from the supplied public brief."""
from pathlib import Path
from html import escape
import json
import argparse
from enterprise_page import render as render_enterprise

ROOT = Path(__file__).resolve().parents[1]
solutions = json.loads((ROOT/'content/solutions.json').read_text(encoding='utf-8'))
parser = argparse.ArgumentParser()
parser.add_argument('--only', choices=[p['id'] for p in solutions], help='Rebuild one detail page without changing the homepage or other detail pages.')
only = parser.parse_args().only

def portrait(cls='nav-ip', view='1380 70 330 280'):
    return f'<svg class="{cls}" viewBox="{view}" role="img" aria-label="小甜的个人 IP 形象"><image href="../assets/ip-character-sheet.png" width="2048" height="1152"/></svg>'

cards=[]
for i,p in enumerate(solutions):
    resource_label = "PPT" if p.get("primary_resource", {}).get("type") == "ppt" else "Demo"
    cards.append(f'''<article class="project-card{' is-active' if i==0 else ''}" data-project="{p['id']}">
      <img class="project-cover" src="assets/project-{p['id']}.svg" width="600" height="400" alt="{p['title']}方案示意" loading="lazy">
      <div class="project-kicker"><span>0{i+1} / SOLUTION</span><span class="project-year">方案示意</span></div>
      <button class="project-select" type="button" aria-label="展开{p['title']}简介" aria-expanded="{'true' if i==0 else 'false'}" aria-controls="summary-{p['id']}"></button>
      <div class="project-body"><p class="project-category">{p['category']}</p><h3 class="project-title">{p['title']}</h3>
      <p class="project-summary" id="summary-{p['id']}">{p['summary']}</p>
      <a class="project-open" href="projects/{p['id']}.html" aria-label="查看{p['title']}详情与 {resource_label}"><span class="open-label">方案详情 &amp; {resource_label}</span><span aria-hidden="true">↗</span></a></div>
    </article>''')
section='''<section class="section" id="projects"><div class="container">
  <p class="section-label">HIGH-VALUE SOLUTIONS · 高价值方案</p>
  <div class="folio-heading"><h2 class="section-title">让 AI 走进真实业务。</h2></div>
  <div class="project-accordion" aria-label="四类高价值方案">'''+''.join(cards)+'''</div>
  <p class="project-caption">四类高价值方案，从客户需求，到场景演示与实施。</p>
  </div></section>'''
path=ROOT/'index.html'
html=path.read_text(encoding='utf-8')
start=html.index('<section class="section" id="projects">');end=html.index('</section>',start)+len('</section>')
if not only:
    path.write_text(html[:start]+section+html[end:],encoding='utf-8')

for i,p in enumerate(solutions):
    if only and p['id'] != only:
        continue
    next_p=solutions[(i+1)%len(solutions)]
    page = render_enterprise(p, next_p, portrait)
    (ROOT/f'projects/{p["id"]}.html').write_text(page,encoding='utf-8')

# Reuse the existing original customer-service concept art, with the new solution name.
art=(ROOT/'assets/project-presales.svg').read_text(encoding='utf-8')
art=art.replace('售前知识助手','智能客服工作台').replace('企业知识库','客户需求').replace('这个场景适合什么解决方案？','想了解适合我的产品。').replace('需求澄清 → 知识检索 → 智能推荐','官网咨询 → 需求调研 → 服务协同')
(ROOT/'assets/project-customer-service.svg').write_text(art,encoding='utf-8')
art=(ROOT/'assets/project-investment.svg').read_text(encoding='utf-8')
art=art.replace('投资决策工作台','保险业务督导').replace('项目总览','业务总览').replace('机会研判','业绩问数').replace('尽调评估','签单分析').replace('专家评审','利润分析').replace('报告修订','客户洞察').replace('让每一个判断，都有依据。','让每一个业务问题，都有回应。').replace('信息聚合 / 智能评审 / 决策协同','经营问数 / 业务归因 / 找客户').replace('可追溯的决策材料','一线业务员管理').replace('财务 · 法务 · 税务 · 风控','绩效 · 利润 · 签单 · 归因')
(ROOT/'assets/project-insurance.svg').write_text(art,encoding='utf-8')
print(f'Built {only} detail page.' if only else 'Built 4 solution cards and 4 static detail pages.')
