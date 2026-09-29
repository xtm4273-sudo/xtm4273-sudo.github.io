"""Build static solution cards and detail pages from the supplied public brief."""
from pathlib import Path
from html import escape
from urllib.parse import quote
import json
import re

ROOT = Path(__file__).resolve().parents[1]
solutions = json.loads((ROOT/'content/solutions.json').read_text(encoding='utf-8'))

def portrait(cls='nav-ip', view='1380 70 330 280'):
    return f'<svg class="{cls}" viewBox="{view}" role="img" aria-label="小甜的个人 IP 形象"><image href="../assets/ip-character-sheet.png" width="2048" height="1152"/></svg>'

def demo_markup(demo):
    title = escape(demo['label'])
    inner = f'<span class="resource-type">{demo["type"]}</span><h3>{title}</h3><p>{escape(demo["description"])}</p><span class="resource-action">{escape(demo["action"])} <span aria-hidden="true">{"↗" if demo["url"] else "—"}</span></span>'
    if demo['url']:
        return f'<a class="demo-resource" href="{escape(demo["url"],quote=True)}" target="_blank" rel="noopener noreferrer">{inner}</a>'
    return f'<article class="demo-resource resource-pending" aria-label="{title}，链接待补充">{inner}</article>'

def document_markup(p):
    doc = p.get('document')
    if not doc:
        return '<section class="document-section" id="documents"><div><p class="detail-eyebrow">04 / SOLUTION DOCUMENTS</p><h2>产品方案文档</h2><p>详细方案资料待补充，欢迎联系我了解。</p></div><span class="document-status">待补充</span></section>'
    headline = ''.join('<span>'+escape(part)+('</span>' if i == len(doc['headline'].split('，'))-1 else '，</span>') for i, part in enumerate(doc['headline'].split('，')))
    roles = ''.join(f'<div><h3>{escape(item["title"])}</h3><p>{escape(item["text"])}</p></div>' for item in doc['roles'])
    flow = ''.join(f'<li><span class="flow-number">0{i+1}</span><h4>{escape(item["title"])}</h4><p>{escape(item["text"])}</p></li>' for i, item in enumerate(doc['flow']))
    cases = []
    for i, item in enumerate(doc['cases']):
        points = ''.join(f'<li>{escape(point)}</li>' for point in item['points'])
        cases.append(f'<details class="case-chapter"{" open" if i == 0 else ""}><summary><span class="case-number">0{i+1}</span><h4>{escape(item["title"])}</h4><span class="case-toggle" aria-hidden="true"></span></summary><div class="case-content"><blockquote>{escape(item["question"])}</blockquote><p>{escape(item["text"])}</p><ul>{points}</ul><p class="case-outcome"><span>场景产出</span>{escape(item["outcome"])}</p></div></details>')
    architecture = ''.join(f'<div><dt>{escape(item["title"])}</dt><dd>{escape(item["text"])}</dd></div>' for item in doc['architecture'])
    return f'''<section class="solution-document" id="documents" aria-labelledby="document-title">
    <header class="document-heading"><p class="detail-eyebrow">04 / SOLUTION IN DEPTH</p><span class="document-name">{escape(doc['name'])}</span><h2 id="document-title">{headline}</h2><p class="document-intro">{escape(doc['intro'])}</p></header>
    <div class="document-roles">{roles}</div>
    <section class="document-flow" aria-labelledby="flow-title"><p class="detail-eyebrow">THE WORKFLOW</p><h3 id="flow-title">{escape(doc['flow_title'])}</h3><ol>{flow}</ol></section>
    <section class="document-cases" aria-labelledby="cases-title"><div class="chapter-heading"><h3 id="cases-title">展开一个场景，看看如何落地。</h3><span>点击展开 / 收起</span></div>{''.join(cases)}</section>
    <details class="architecture-chapter"><summary>方案架构与实施能力<span aria-hidden="true">↗</span></summary><dl>{architecture}</dl></details>
    <p class="document-note">{escape(doc['note'])}</p></section>'''

cards=[]
for i,p in enumerate(solutions):
    cards.append(f'''<article class="project-card{' is-active' if i==0 else ''}" data-project="{p['id']}">
      <img class="project-cover" src="assets/project-{p['id']}.svg" width="600" height="400" alt="{p['title']}方案示意" loading="lazy">
      <div class="project-kicker"><span>0{i+1} / SOLUTION</span><span class="project-year">方案示意</span></div>
      <button class="project-select" type="button" aria-label="展开{p['title']}简介" aria-expanded="{'true' if i==0 else 'false'}" aria-controls="summary-{p['id']}"></button>
      <div class="project-body"><p class="project-category">{p['category']}</p><h3 class="project-title">{p['title']}</h3>
      <p class="project-summary" id="summary-{p['id']}">{p['summary']}</p>
      <a class="project-open" href="projects/{p['id']}.html" aria-label="查看{p['title']}详情与 Demo"><span class="open-label">方案详情 &amp; Demo</span><span aria-hidden="true">↗</span></a></div>
    </article>''')
section='''<section class="section" id="projects"><div class="container">
  <p class="section-label">HIGH-VALUE SOLUTIONS · 高价值方案</p>
  <div class="folio-heading"><h2 class="section-title">让 AI 走进真实业务。</h2><p class="folio-intro">四类高价值方案，<br>从客户需求，到场景演示与实施。</p></div>
  <div class="project-accordion" aria-label="四类高价值方案">'''+''.join(cards)+'''</div>
  <div class="project-footer"><span class="folio-counter">04 SOLUTIONS / REAL-WORLD PRACTICE</span><span>需要客户展示或定制方案，欢迎联系我。</span></div>
  <div class="solution-service-note"><span>需求沟通 / Demo / 方案 / 实施</span><p>可协助客户方案展示、AI 项目定制开发，以及 Dora、Wufan 等平台实施。</p><a href="#contact">聊聊你的需求 ↗</a></div>
  </div></section>'''
path=ROOT/'index.html'
html=path.read_text(encoding='utf-8')
start=html.index('<section class="section" id="projects">');end=html.index('</section>',start)+len('</section>')
path.write_text(html[:start]+section+html[end:],encoding='utf-8')

for i,p in enumerate(solutions):
    next_p=solutions[(i+1)%len(solutions)]
    tags=''.join(f'<span>{escape(tag)}</span>' for tag in p['tags'])
    scenes=''.join(f'<li><span class="scenario-number">0{j+1}</span><p>{escape(scene)}</p></li>' for j,scene in enumerate(p['scenes']))
    proof=''
    if p['validation']:
        proof='<div class="solution-proof">'+''.join(f'<div><strong>{escape(v["value"])}</strong><span>{escape(v["label"])}</span></div>' for v in p['validation'])+'<small>商机验证 · 当前方案进展</small></div>'
    resources=''.join(demo_markup(demo) for demo in p['demos'])
    mail='mailto:18098028372@163.com?subject='+quote(p['title']+'方案咨询')
    page=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{p['title']} · 马晓甜的高价值方案</title><meta name="description" content="{escape(p['summary'],quote=True)}">
    <script src="../assets/theme.js"></script><link rel="stylesheet" href="../assets/detail.css"><link rel="stylesheet" href="../assets/projects.css"><link rel="stylesheet" href="../assets/solutions.css">
    </head><body class="detail-page" data-project="{p['id']}">
    <header class="detail-nav"><a class="nav-logo" href="../index.html#projects">{portrait()}<span class="brand-word">马晓甜<small>PRODUCT &amp; POSSIBILITY</small></span></a><a class="back-link" href="../index.html#projects">← 返回全部方案</a></header>
    <main class="detail-main solution-main">
    <div class="solution-hero"><div class="solution-title"><p class="detail-eyebrow">HIGH-VALUE SOLUTIONS / 0{i+1}</p><h1>{p['title']}</h1><p class="detail-lead">{p['summary']}</p><div class="solution-tags">{tags}</div><div class="solution-hero-actions"><a class="solution-primary" href="#demo">查看 Demo 入口 <span aria-hidden="true">↗</span></a><a class="solution-secondary" href="{mail}">咨询定制方案</a></div></div>
    <div class="solution-visual"><span class="visual-number">0{i+1}</span><img src="../assets/project-{p['id']}.svg" width="600" height="400" alt="{p['title']}方案示意"><span class="visual-caption">PRODUCT CONCEPT · 方案示意</span></div></div>
    {proof}
    <nav class="solution-tabs" aria-label="方案章节"><a href="#audience">适用客户</a><a href="#scenarios">业务场景</a><a href="#demo">Demo 入口</a><a href="#documents">方案资料</a></nav>
    <section class="detail-section" id="audience"><div><p class="detail-eyebrow">01 / WHO IT'S FOR</p><h2>什么样的客户适合？</h2></div><div><p class="audience-copy">{p['audience']}</p><div class="solution-tags">{tags}</div></div></section>
    <section class="detail-section" id="scenarios"><div><p class="detail-eyebrow">02 / USE CASES</p><h2>从真实业务切入</h2></div><ol class="scenario-list">{scenes}</ol></section>
    <section class="solution-resources" id="demo"><div class="resource-heading"><div><p class="detail-eyebrow">03 / EXPLORE THE SOLUTION</p><h2>先看看方案如何运作。</h2></div><span>演示与场景体验</span></div><div class="resource-grid">{resources}</div></section>
    {document_markup(p)}
    <section class="demo-section solution-contact"><div><p class="detail-eyebrow">LET'S MAKE IT WORK</p><h2>把方案，带进你的业务。</h2><p>客户方案展示、AI 项目定制、需求沟通、Demo 与实施，欢迎随时联系我。</p><div class="demo-actions"><a href="{mail}">联系小甜聊需求 ↗</a><a href="../index.html#contact">更多联系方式</a></div></div>{portrait('detail-persona','1225 862 173 230')}</section>
    <a class="next-project" href="{next_p['id']}.html"><span>下一个方案</span><strong>{next_p['title']}</strong><span>↗</span></a></main>
    <footer class="detail-footer">马晓甜 · 把想象，做成真实的产品。</footer></body></html>'''
    (ROOT/f'projects/{p["id"]}.html').write_text(page,encoding='utf-8')

# Reuse the existing original customer-service concept art, with the new solution name.
art=(ROOT/'assets/project-presales.svg').read_text(encoding='utf-8')
art=art.replace('售前知识助手','智能客服工作台').replace('企业知识库','客户需求').replace('这个场景适合什么解决方案？','想了解适合我的产品。').replace('需求澄清 → 知识检索 → 智能推荐','官网咨询 → 需求调研 → 服务协同')
(ROOT/'assets/project-customer-service.svg').write_text(art,encoding='utf-8')
art=(ROOT/'assets/project-investment.svg').read_text(encoding='utf-8')
art=art.replace('投资决策工作台','保险业务督导').replace('项目总览','业务总览').replace('机会研判','业绩问数').replace('尽调评估','签单分析').replace('专家评审','利润分析').replace('报告修订','客户洞察').replace('让每一个判断，都有依据。','让每一个业务问题，都有回应。').replace('信息聚合 / 智能评审 / 决策协同','经营问数 / 业务归因 / 找客户').replace('可追溯的决策材料','一线业务员管理').replace('财务 · 法务 · 税务 · 风控','绩效 · 利润 · 签单 · 归因')
(ROOT/'assets/project-insurance.svg').write_text(art,encoding='utf-8')
print('Built 4 solution cards and 4 static detail pages.')
