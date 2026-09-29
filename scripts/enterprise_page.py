"""Render the approved enterprise solution layout from the existing source content."""
from html import escape as e


def render(p, next_p, portrait):
    doc = p.get('document')
    demo = p.get('primary_resource') or next((d for d in p['demos'] if d.get('url')), None)
    demo_label = demo.get('button_label') if demo else None
    demo_label = demo_label or ('查看排班 Demo' if p['id'] == 'scheduling' else '立即体验 Demo')
    hint = (demo or {}).get('hint') or ('腾讯文档演示资料 · 新窗口打开' if p['id']=='scheduling' else '在线产品体验 · 新窗口打开')
    def cta(extra=''):
        if not demo:
            return '<span class="demo-disabled" aria-disabled="true">Demo 待补充</span>'
        download = f' download="{e(demo["download"], quote=True)}"' if demo.get('download') else ' target="_blank" rel="noopener noreferrer"'
        icon = '↓' if demo.get('download') else '↗'
        return f'<a class="demo-cta {extra}" href="{e(demo["url"], quote=True)}"{download}>{e(demo_label)}<span aria-hidden="true">{icon}</span></a>'

    title = doc['name'] if doc else p['title']
    flow = doc['flow'] if doc else [
        {'title': '明确业务需求', 'text': '结合客户实际的排班、派单或排产流程沟通需求。'},
        {'title': '定制场景方案', 'text': '按制造业或零售业的具体业务设计方案。'},
        {'title': '展示与验证', 'text': '通过 Demo 展示业务流程，进一步确认实施需求。'}]
    preview = ''.join(f'<li><span>0{i+1}</span><div><strong>{e(item["title"])}</strong><p>{e(item["text"])}</p></div></li>' for i, item in enumerate(flow))
    proof = ''.join(f'<span><strong>{e(v["value"])}</strong>{e(v["label"])}</span>' for v in p['validation'])
    proof = f'<div class="proof"><span class="proof-label">商机验证</span>{proof}</div>' if proof else ''
    intro = doc['intro'] if doc else '制造与零售业务中的人员安排、任务派发和生产调度，各有不同的实际流程。方案围绕客户的排班、派单或排产需求展开，结合业务场景定制，并通过 Demo 沟通和验证。'
    roles = ''
    if doc:
        role_rows = ''.join(f'<div><dt>{e(r["title"])}</dt><dd>{e(r["text"])}</dd></div>' for r in doc['roles'])
        roles = f'<details class="more-details"><summary>查看不同角色的使用价值<span aria-hidden="true">＋</span></summary><dl>{role_rows}</dl></details>'
    cases = doc['cases'] if doc else [
        {'title':'零售业人员排班', 'question':'以奶茶店为例，如何安排具体时间段与人员？', 'text':p['scenes'][0], 'points':['通过已提供的零售排班 Demo 查看场景。','结合客户的实际业务进一步沟通定制需求。'], 'outcome':'零售排班场景演示'},
        {'title':'制造业派单与排产', 'question':'如何把方案应用到具体制造业务？', 'text':p['scenes'][1], 'points':['围绕实际的派单与排产需求沟通方案。','制造业 Demo 尚待补充，可联系我了解。'], 'outcome':'按业务需求定制的方案'}]
    case_html = ''
    for i, c in enumerate(cases):
        points = ''.join(f'<li>{e(s)}</li>' for s in c['points'])
        case_html += f'''<details class="case-chapter" {'open' if i == 0 else ''}><summary><span class="case-index">0{i+1}</span><h3>{e(c['title'])}</h3><span class="expand-mark" aria-hidden="true"></span></summary><div class="case-content"><p class="case-question">{e(c['question'])}</p><p>{e(c['text'])}</p><ul>{points}</ul><p class="case-result"><span>交付结果</span>{e(c['outcome'])}</p></div></details>'''
    flow_html = ''.join(f'<li><span>0{i+1}</span><h3>{e(x["title"])}</h3><p>{e(x["text"])}</p></li>' for i,x in enumerate(flow))
    architecture = ''
    if doc:
        rows = ''.join(f'<div><dt>{e(x["title"])}</dt><dd>{e(x["text"])}</dd></div>' for x in doc['architecture'])
        architecture = f'<details class="more-details architecture-chapter"><summary>技术架构与实施能力<span aria-hidden="true">＋</span></summary><dl>{rows}</dl></details><p class="source-note">{e(doc["note"])}</p>'
    else:
        architecture = '<p class="source-note">详细产品方案与制造业 Demo 待补充。当前可查看零售排班演示，或联系我沟通定制需求。</p>'
    return f'''<!doctype html><html lang="zh-CN" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(p['title'])} · 马晓甜</title><meta name="description" content="{e(p['summary'],quote=True)}"><script src="../assets/theme.js?v=20260929"></script><link rel="stylesheet" href="../assets/enterprise.css"><link rel="stylesheet" href="../assets/solution-layout.css"><link rel="stylesheet" href="../assets/site-design.css?v=20260929"></head>
    <body data-project="{p['id']}"><a class="skip-link" href="#overview">跳转到方案正文</a>
    <header class="site-header"><a class="brand" href="../index.html">{portrait()}<span>马晓甜<small>产品方案 / Portfolio</small></span></a><a class="back-link" href="../index.html#projects">← 全部方案</a></header>
    <main><section class="hero wrap" aria-labelledby="page-title"><div class="hero-copy"><p class="eyebrow">{e(p['category'])}</p><h1 id="page-title">{e(title)}</h1><p class="hero-summary">{e(p['summary'])}</p><div class="hero-actions">{cta('hero-demo')}<a class="text-link" href="#overview">了解方案 <span aria-hidden="true">↓</span></a></div><p class="demo-hint">{e(hint)}</p>{proof}</div>
    <aside class="hero-outline" aria-label="方案流程概览"><div class="outline-heading"><span>方案如何运作</span><span aria-hidden="true">↘</span></div><ol>{preview}</ol></aside></section>
    <nav class="chapter-nav" aria-label="方案章节"><div class="wrap chapter-inner"><div class="chapter-links"><a href="#overview">业务问题</a><a href="#scenarios">核心场景</a><a href="#implementation">实施方式</a></div>{cta('nav-demo')}</div></nav>
    <div class="design-main"><section class="content-section" id="overview"><div class="section-heading"><span>01</span><h2>解决什么问题</h2></div><div class="section-body"><p class="intro">{e(intro)}</p><div class="audience"><h3>适用客户</h3><p>{e(p['audience'])}</p></div>{roles}</div></section>
    <section class="content-section" id="scenarios"><div class="section-heading"><span>02</span><h2>核心业务场景</h2><p>按需展开，查看方案如何落地。</p></div><div class="section-body case-list">{case_html}</div></section>
    <section class="implementation" id="implementation"><div class="section-heading"><span>03</span><h2>从需求到落地</h2></div><ol class="workflow">{flow_html}</ol>{architecture}</section>
    <a class="next-project" href="{next_p['id']}.html"><span>继续了解</span><strong>{e(next_p['title'])}</strong><span aria-hidden="true">→</span></a></div></main>
    <footer class="site-footer">马晓甜 · 把想象，做成真实的产品。</footer><div class="mobile-demo"><span>{e(p['title'])}</span>{cta('mobile-demo-link')}</div>
    <script src="../assets/enterprise.js"></script></body></html>'''
