from pathlib import Path
import re, html

P=Path('index.html')
doc=P.read_text(encoding='utf-8')

def fmt_num(x):
    x=float(x)
    if abs(x)>=1_000_000: s=f'{x/1_000_000:.1f}M'
    elif abs(x)>=1000: s=f'{x/1000:.1f}K'
    else: s=f'{x:.0f}'
    return s.replace('.',',')

def hbar(labels, values, width=820, height=None, left=180, formatter=None, barclass='svg-bar'):
    values=[float(v) for v in values]; n=len(values); height=height or max(250,38*n+55)
    top,bottom,right=18,34,78; cw=width-left-right; ch=height-top-bottom; rh=ch/max(n,1); mx=max(values) or 1
    o=[f'<svg class="native-svg" viewBox="0 0 {width} {height}" role="img">']
    for frac in [0,.25,.5,.75,1]:
        x=left+cw*frac
        o.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{height-bottom}" class="svg-grid"/>')
    for i,(lab,val) in enumerate(zip(labels,values)):
        y=top+i*rh+3; bh=max(13,rh-7); bw=cw*(val/mx)
        disp=formatter(val) if formatter else fmt_num(val)
        o += [f'<text x="{left-10}" y="{y+bh*.72:.1f}" text-anchor="end" class="svg-label">{html.escape(str(lab))}</text>',
              f'<rect x="{left}" y="{y:.1f}" width="{max(bw,2):.1f}" height="{bh:.1f}" rx="5" class="{barclass}"><title>{html.escape(str(lab))}: {html.escape(disp)}</title></rect>',
              f'<text x="{left+bw+8:.1f}" y="{y+bh*.72:.1f}" class="svg-value">{html.escape(disp)}</text>']
    return ''.join(o)+'</svg>'

channels=['Organic Search','Direct','Referral','Cross-network','Email','Organic Social','AI Assistant']
channel_new=[6400,2400,1300,1200,960,651,276]
source_labels=['google','(not set)','brevo','hyrox.com','l.instagram.com','mexico.hyrox.com','bing','chatgpt.com']
source_active=[7298,4474,1245,1188,629,369,372,307]
source_sessions=[12844,5643,2604,1785,730,570,472,378]
source_eng_rate=[59.45,26.19,59.45,63.92,40.55,68.60,76.06,59.26]
pages=['Home','Acapulco event','Mexico City event','/eventos/','FAQs','The Fitness Race']
page_views=[12188,11923,5343,3327,1955,823]
page_users=[7184,5386,3466,2443,1317,548]
page_time=[18,31,18,13,46,47]
cities=['Mexico City','Puebla','Acapulco','Santiago de Querétaro','Guadalajara','Cuernavaca','Monterrey']
city_users=[3513,950,636,598,540,443,443]
city_eng=[52.2,55.61,64.38,55.25,58.3,60.11,55.08]

source_rows=''.join(
    f'<tr><td>{html.escape(s)}</td><td>{a:,}</td><td>{ss:,}</td><td>{er:.2f}%</td></tr>'.replace(',', '.')
    for s,a,ss,er in zip(source_labels,source_active,source_sessions,source_eng_rate)
)
page_rows=''.join(
    f'<tr><td>{html.escape(p)}</td><td>{v:,}</td><td>{u:,}</td><td>{t}s</td></tr>'.replace(',', '.')
    for p,v,u,t in zip(pages,page_views,page_users,page_time)
)

section=f'''
<section id="ga4">
<div class="eyebrow">09 · Google Analytics 4</div>
<h2>Web Performance</h2>
<p class="section-intro">Ventana 29 Ago – 10 Sep 2026. El sitio concentra una parte importante de la demanda alrededor de la página de Acapulco, pero GA4 no tiene eventos clave configurados en el período, por lo que tráfico y engagement web no pueden conectarse todavía con registros o ventas.</p>
<div class="grid ga4-kpis">
  <div class="card kpi"><div class="label">Active users</div><div class="value">15.169</div><div class="delta">GA4</div></div>
  <div class="card kpi"><div class="label">New users</div><div class="value">13.167</div><div class="delta">≈86,8% of active users</div></div>
  <div class="card kpi"><div class="label">Sessions</div><div class="value">24.874</div><div class="delta">53,29% engagement rate</div></div>
  <div class="card kpi"><div class="label">Page views</div><div class="value">39.969</div><div class="delta">2,63 views / active user</div></div>
</div>
<div class="insight-strip ga4-strip">
  <div><span>Avg engagement time</span><b>36 s</b><small>per active user</small></div>
  <div><span>Engaged sessions</span><b>13.255</b><small>53,29% of sessions</small></div>
  <div><span>Acapulco page views</span><b>11.923</b><small>29,83% of all views</small></div>
  <div class="warning-insight"><span>Key events</span><b>0</b><small>conversion tracking gap</small></div>
</div>

<h3 class="subsection-title">Acquisition mix</h3>
<div class="grid">
  <div class="card half"><div class="mini-chart-head"><h3>New users by channel</h3><span>GA4 overview</span></div>{hbar(channels,channel_new,width=760,height=330,left=155)}</div>
  <div class="card half ga4-copy">
    <div class="callout-number">6,4K</div><div class="callout-value">new users from Organic Search</div>
    <p>Organic Search is the largest new-user acquisition channel, followed by Direct (2,4K), Referral (1,3K), Cross-network (1,2K) and Email (960).</p>
    <div class="note compact-note"><b>AI discovery:</b> GA4 attributes <b>276 new users</b> to “AI Assistant”, while <b>chatgpt.com</b> appears separately as a source with 307 active users.</div>
  </div>
</div>

<h3 class="subsection-title">Traffic sources</h3>
<div class="grid">
  <div class="card half"><div class="mini-chart-head"><h3>Active users by source</h3><span>Top sources</span></div>{hbar(source_labels,source_active,width=760,height=350,left=150)}</div>
  <div class="card half"><div class="mini-chart-head"><h3>Engagement rate by source</h3><span>Quality signal</span></div>{hbar(source_labels,source_eng_rate,width=760,height=350,left=150,formatter=lambda v:f'{v:.1f}%'.replace('.',','),barclass='svg-bar')}</div>
  <div class="card full table-scroll"><table><thead><tr><th>Source</th><th>Active users</th><th>Sessions</th><th>Engagement rate</th></tr></thead><tbody>{source_rows}</tbody></table></div>
</div>
<div class="note"><b>Traffic quality:</b> Search is not only the largest source; Bing (76,06%), mexico.hyrox.com (68,60%), hyrox.com (63,92%) and Google (59,45%) show materially stronger engagement rates than Instagram referral traffic (40,55%).</div>

<h3 class="subsection-title">Page performance</h3>
<div class="grid">
  <div class="card half"><div class="mini-chart-head"><h3>Top pages by views</h3><span>39.969 total views</span></div>{hbar(pages,page_views,width=760,height=300,left=160)}</div>
  <div class="card half acapulco-page-card">
    <div class="label">Acapulco event page</div>
    <div class="acapulco-big">11.923 <span>views</span></div>
    <div class="acapulco-metrics"><div><b>5.386</b><span>active users</span></div><div><b>2,21</b><span>views / user</span></div><div><b>31 s</b><span>avg engagement</span></div><div><b>34.876</b><span>events</span></div></div>
    <div class="note compact-note"><b>Share of site activity:</b> the Acapulco event page generated <b>29,83% of all page views</b> and reached <b>35,51% of active users</b> during the reporting window.</div>
  </div>
  <div class="card full table-scroll"><table><thead><tr><th>Page</th><th>Views</th><th>Active users</th><th>Avg engagement</th></tr></thead><tbody>{page_rows}</tbody></table></div>
</div>

<h3 class="subsection-title">Geographic signal</h3>
<div class="grid">
  <div class="card half"><div class="mini-chart-head"><h3>Active users by city</h3><span>Top markets</span></div>{hbar(cities,city_users,width=760,height=330,left=175)}</div>
  <div class="card half"><div class="mini-chart-head"><h3>Engagement rate by city</h3><span>Selected top cities</span></div>{hbar(cities,city_eng,width=760,height=330,left=175,formatter=lambda v:f'{v:.1f}%'.replace('.',','))}</div>
</div>
<div class="note"><b>Acapulco users show stronger intent:</b> Acapulco represents 636 active users (4,19% of total) but records a <b>64,38% engagement rate</b> and <b>48 s average engagement time</b>, both above the overall site averages of 53,29% and 36 s.</div>

<div class="methodology-box ga4-warning"><h3>Measurement gap · conversion tracking</h3><p>GA4 reports <b>0 key events</b> throughout the period. That means the current analytics implementation cannot reliably attribute registrations, ticket purchases or qualified leads to acquisition sources, campaigns or landing pages.</p><p><b>Recommendation:</b> define and validate key events for outbound ticket clicks, registration start, checkout/purchase where technically available, and any lead-generation action before the next HYROX event.</p></div>
</section>
<section id="pending"><div class="eyebrow">10</div><h2>Next Modules</h2><div class="grid"><div class="card third"><h3>Ambassadors</h3><div class="placeholder">50 profiles · compliance · content · performance</div></div><div class="card third"><h3>Tickets / Registrations</h3><div class="placeholder">Registrations · sales · funnel performance</div></div><div class="card third"><h3>Email</h3><div class="placeholder">Sends · opens · clicks · traffic contribution</div></div><div class="card full"><h3>Sponsor Intelligence</h3><div class="placeholder">Deliverables vs executed · share of voice · top content · brand moments · activations · insights</div></div></div></section>
'''

css='''/* GA4 */.ga4-kpis{margin-bottom:14px}.ga4-copy{display:flex;flex-direction:column;justify-content:center}.ga4-strip .warning-insight{border-color:#634b00;background:rgba(255,229,0,.035)}.acapulco-page-card{display:flex;flex-direction:column;justify-content:center}.acapulco-big{font-size:40px;font-weight:900;line-height:1.05;margin:8px 0 14px;color:var(--yellow)}.acapulco-big span{font-size:13px;color:#aaa;font-weight:700}.acapulco-metrics{display:grid;grid-template-columns:repeat(2,1fr);gap:8px}.acapulco-metrics>div{background:#0f0f0f;border:1px solid #292929;border-radius:10px;padding:10px}.acapulco-metrics b{display:block;font-size:16px}.acapulco-metrics span{display:block;color:#858585;font-size:9px;text-transform:uppercase;letter-spacing:.05em;margin-top:2px}.ga4-warning{border-color:#5a4f18;background:rgba(255,229,0,.025)}@media(max-width:650px){.acapulco-metrics{grid-template-columns:1fr}}'''

if '/* GA4 */' not in doc:
    doc=doc.replace('/* Social Listening */',css+'\n/* Social Listening */',1)
if '<a href="#ga4">09. GA4 / Web</a>' not in doc:
    doc=doc.replace('<a href="#listening">08. Social Listening</a>\n<a href="#pending">09. Next Modules</a>', '<a href="#listening">08. Social Listening</a>\n<a href="#ga4">09. GA4 / Web</a>\n<a href="#pending">10. Next Modules</a>')
if 'id="ga4"' in doc:
    doc=re.sub(r'<section id="ga4">.*?</section>\s*<section id="pending">.*?</section>',section,doc,count=1,flags=re.S)
else:
    doc=re.sub(r'<section id="pending">.*?</section>',section,doc,count=1,flags=re.S)

doc=doc.replace('Working report · Meta first-party + Mentionlytics social listening · HYROX Acapulco 2026.','Working report · Meta first-party + Mentionlytics social listening + GA4 web analytics · HYROX Acapulco 2026.')
P.write_text(doc,encoding='utf-8')
