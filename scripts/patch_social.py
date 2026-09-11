from pathlib import Path
import re, math, html

P = Path("index.html")
doc = P.read_text(encoding="utf-8")

def fmt_num(x):
    x=float(x)
    if abs(x)>=1_000_000: s=f"{x/1_000_000:.1f}M"
    elif abs(x)>=1000: s=f"{x/1000:.1f}K"
    else: s=f"{x:.0f}"
    return s.replace(".",",")

def fmt_int(x):
    return f"{int(round(float(x))):,}".replace(",",".")

def hbar(labels, values, width=820, height=None, left=180, suffix=""):
    values=[float(v) for v in values]
    n=len(values); height=height or max(250,38*n+55)
    top,bottom,right=18,34,70; cw=width-left-right; ch=height-top-bottom; rh=ch/max(n,1); mx=max(values) or 1
    o=[f'<svg class="native-svg" viewBox="0 0 {width} {height}" role="img">']
    for frac in [0,.25,.5,.75,1]:
        x=left+cw*frac
        o.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{height-bottom}" class="svg-grid"/>')
    for i,(lab,val) in enumerate(zip(labels,values)):
        y=top+i*rh+3; bh=max(13,rh-7); bw=cw*(val/mx)
        disp=(f"{val:.1f}".replace(".",",") if suffix else fmt_num(val))
        o += [f'<text x="{left-10}" y="{y+bh*.72:.1f}" text-anchor="end" class="svg-label">{html.escape(str(lab))}</text>',
              f'<rect x="{left}" y="{y:.1f}" width="{max(bw,2):.1f}" height="{bh:.1f}" rx="5" class="svg-bar"><title>{html.escape(str(lab))}: {disp}{suffix}</title></rect>',
              f'<text x="{left+bw+8:.1f}" y="{y+bh*.72:.1f}" class="svg-value">{disp}{suffix}</text>']
    return "".join(o)+"</svg>"

def line_chart(labels, values, width=900, height=290):
    vals=[float(v) for v in values]; n=len(vals); mx=max(vals) or 1
    left,right,top,bottom=55,18,25,48; cw=width-left-right; ch=height-top-bottom
    pts=[(left+cw*(i/(n-1)), top+ch*(1-v/mx)) for i,v in enumerate(vals)]
    o=[f'<svg class="native-svg" viewBox="0 0 {width} {height}" role="img">']
    x1=left+cw*(5.5/(n-1)); x2=left+cw*(8.5/(n-1))
    o += [f'<rect x="{x1:.1f}" y="{top}" width="{x2-x1:.1f}" height="{ch}" rx="8" fill="rgba(255,229,0,.05)"/>',
          f'<text x="{(x1+x2)/2:.1f}" y="15" text-anchor="middle" class="svg-axis" style="fill:#ffe500">EVENT · 04–06 SEP</text>']
    for frac in [0,.25,.5,.75,1]:
        y=top+ch*(1-frac)
        o += [f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" class="svg-grid"/>',
              f'<text x="{left-8}" y="{y+4:.1f}" text-anchor="end" class="svg-axis">{fmt_num(mx*frac)}</text>']
    path=" ".join(("M" if i==0 else "L")+f"{x:.1f},{y:.1f}" for i,(x,y) in enumerate(pts))
    area=path+f" L {pts[-1][0]:.1f},{top+ch:.1f} L {pts[0][0]:.1f},{top+ch:.1f} Z"
    o += [f'<path d="{area}" class="svg-area"/>', f'<path d="{path}" class="svg-line"/>']
    for i,(x,y) in enumerate(pts):
        o += [f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" class="svg-dot"><title>{labels[i]} · {fmt_num(vals[i])}</title></circle>',
              f'<text x="{x:.1f}" y="{height-20}" text-anchor="middle" class="svg-axis">{labels[i]}</text>']
    return "".join(o)+"</svg>"

def donut(parts, width=460, height=255):
    total=sum(v for _,v,_ in parts); cx,cy,r=120,125,72; circ=2*math.pi*r; off=0
    o=[f'<svg class="native-svg" viewBox="0 0 {width} {height}" role="img">',
       f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#252525" stroke-width="28"/>']
    for lab,val,col in parts:
        dash=circ*val/total
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="28" stroke-dasharray="{dash:.2f} {circ-dash:.2f}" stroke-dashoffset="{-off:.2f}" transform="rotate(-90 {cx} {cy})"><title>{lab} · {val}</title></circle>')
        off += dash
    o += [f'<text x="{cx}" y="{cy-2}" text-anchor="middle" class="donut-main">88,2%</text>',
          f'<text x="{cx}" y="{cy+19}" text-anchor="middle" class="svg-axis">positive</text>']
    for i,(lab,val,col) in enumerate(parts):
        y=75+i*38
        o += [f'<rect x="225" y="{y-10}" width="11" height="11" rx="2" fill="{col}"/>',
              f'<text x="243" y="{y}" class="svg-label">{lab}</text>',
              f'<text x="{width-20}" y="{y}" text-anchor="end" class="svg-value">{fmt_int(val)} · {val/total*100:.1f}%</text>']
    return "".join(o)+"</svg>"

dates=["29 Ago","30 Ago","31 Ago","01 Sep","02 Sep","03 Sep","04 Sep","05 Sep","06 Sep","07 Sep","08 Sep","09 Sep","10 Sep"]
mentions=[89,88,155,177,133,160,344,321,341,313,294,276,250]
eng=[10547,8791,12097,21009,13714,11817,34157,47328,190409,131650,37504,34415,22575]
platforms=["Instagram","TikTok","X / Twitter","YouTube","Web"]
platform_counts=[2556,222,65,43,55]
tags=[("#hyroxacapulco",1224),("#hyrox",1137),("#hyroxmexico",215),("#hyroxtraining",173),("#hyroxworld",159),("#acapulco",148),("#hyroxmx",124),("#fitness",100)]
sent=[("Positive",2593,"#50c878"),("Negative",150,"#ff5a5f"),("Neutral",63,"#ffe500"),("Unclassified",135,"#666")]
top=[
("Fer HM",74870,496700,88917,17.9,"https://www.tiktok.com/@soy.ferhm/video/7682599896540630289","Así me fue en mi primer HYROX"),
("Fer HM",75857,335200,47594,14.2,"https://www.tiktok.com/@soy.ferhm/video/7683001882180160769","Porra o hate?"),
("Lucía Romero",1614,286900,15092,5.3,"https://www.tiktok.com/@luciarromero/video/7682522447479934216","LAURA… humildemente con mis dos parches"),
("Marck",905,206590,2363,1.1,"https://www.tiktok.com/@marck_v/video/7681793745112567060","Metas · HYROX Acapulco"),
("Ana Lago",1096243,126500,9519,7.5,"https://www.tiktok.com/@analago95/video/7682533803637755156","HYROX ACAPULCO"),
("Rod Frias",7395,112300,502,0.4,"https://www.tiktok.com/@rodrigofrias422/video/7679648670987357461","Día 2 de 15 para completar HYROX Pro"),
("Roy Mata Paramedic",3866823,95200,9662,10.1,"https://www.tiktok.com/@roymata01/video/7682832912227536146","709 personas pasaron por nuestras manos"),
("Daniela Ragozzino",2303,90900,7571,8.3,"https://www.tiktok.com/@danielaragozzinoe/video/7682845808001125653","Espíritu competitivo"),
("Fer HM",74870,63300,8972,14.2,"https://www.tiktok.com/@soy.ferhm/video/7682501188406807825","Esto hice antes de mi primer HYROX Acapulco"),
("Megadiverti2",1943688,62100,2483,4.0,"https://www.tiktok.com/@megadiverti2/video/7682998870233632016","Gracias mami JAJAJA"),
]
eff=[("Marck",228.3),("Lucía Romero",177.8),("Daniela Ragozzino",39.5),("Rod Frias",15.2),("Fer HM",6.6)]
yt=[
("practicamente","HYROX Acapulco — por poco y no termino","3,4K","https://www.youtube.com/watch?v=GyiwHSqfF6Y"),
("Daria Sandoval","HYROX Acapulco","1,3K","https://www.youtube.com/watch?v=NOlNKsLfOiA"),
("RUN LIFT REPEAT","La 1ra batalla de los Doubles Mixtos","1,3K","https://www.youtube.com/watch?v=ipKhN4ecnjE"),
("Andres Ayala","HYROX Race Week","1,2K","https://www.youtube.com/watch?v=9dP4GZSuZqQ"),
]
web=[
("mex4you.net","Mundo Imperial conquista el reto HYROX Acapulco 2026","https://www.mex4you.net/articulo.php?n=39247"),
("docteur-fitness.com","HYROX 2026: Calendrier de toutes les courses","https://www.docteur-fitness.com/hyrox-2026-le-calendrier-complet-de-toutes-les-courses-dans-le-monde"),
("hoydiariodelmagdalena.com.co","Coverage mentioning HYROX Acapulco","https://hoydiariodelmagdalena.com.co/categoria/santa-marta/"),
("hybridathleteclub.com","2026 Acapulco Season 9 Race Results","https://hybridathleteclub.com/results/season_9_2026_Acapulco"),
]
xposts=[
("Hasvik","Vlog HYROX Acapulco · No siento las piernas","15,7K","https://www.twitter.com/HasvikMC/status/2097814483720925361"),
("Dr. Retrica","HYROX Acapulco en 6 días y ya me dio ansiedad","2,7K","https://www.twitter.com/_angelrd97/status/2094545230133420396"),
("Ziggy Starbucks","HYROX Acapulco 2026 · Pro Doubles Men","1,2K","https://www.twitter.com/EmilioCadernMne/status/2097735305088377191"),
("Emily Benítez Cortés","Acapulco como referente de turismo deportivo","365","https://www.twitter.com/emilybecor/status/2097679814769479994"),
]

rows="".join(f'<tr><td class="rank-cell">#{i}</td><td><div class="social-badge">TT</div></td><td><a class="report-link" href="{url}" target="_blank">{html.escape(name)}</a><div class="table-sub">{html.escape(title)}</div></td><td>TikTok</td><td>{fmt_num(fol)}</td><td><b>{fmt_num(view)}</b></td><td>{fmt_num(en)}</td><td>{er:.1f}%</td></tr>' for i,(name,fol,view,en,er,url,title) in enumerate(top,1))

def cards(items, kind):
    out=[]
    for item in items:
        if kind=="web":
            name,title,url=item; metric="Mention detected"; badge="WEB"; label="Coverage"
        else:
            name,title,metric,url=item; badge="YT" if kind=="yt" else "X"; label="Views" if kind=="yt" else "Impressions"
        out.append(f'<a class="coverage-card text-card" href="{url}" target="_blank"><div class="coverage-placeholder">{badge}</div><div class="coverage-body"><div class="coverage-source">{html.escape(name)}</div><div class="coverage-title">{html.escape(title)}</div><div class="coverage-kpi">{label}: <b>{metric}</b></div></div></a>')
    return "".join(out)

section=f'''
<section id="listening">
<div class="eyebrow">08 · Mentionlytics</div><h2>Social Listening & Earned Media</h2>
<p class="section-intro">Conversación pública detectada alrededor de HYROX Acapulco entre el 29 de agosto y el 10 de septiembre. Reach y engagement de cabecera provienen del dashboard de Mentionlytics; rankings y desgloses se reconstruyen desde el export individual de 2.941 menciones.</p>
<div class="grid listening-kpis">
<div class="card kpi"><div class="label">Total mentions</div><div class="value">2.941</div><div class="delta">29 Ago – 10 Sep</div></div>
<div class="card kpi"><div class="label">Unique social reach · estimated</div><div class="value">15,7 M</div><div class="delta">Mentionlytics estimate</div></div>
<div class="card kpi"><div class="label">Social engagement</div><div class="value">581,7 K</div><div class="delta">Dashboard aggregate</div></div>
<div class="card kpi"><div class="label">Positive sentiment</div><div class="value">88,2%</div><div class="delta">2.593 positive mentions</div></div>
</div>
<div class="insight-strip">
<div><span>Event window</span><b>1.006 mentions</b><small>34,2% · 04–06 Sep</small></div>
<div><span>Post-event sustained</span><b>1.133 mentions</b><small>38,5% · 07–10 Sep</small></div>
<div><span>Peak engagement</span><b>06 Sep</b><small>190,4K export interactions</small></div>
<div><span>Earned breakout</span><b>TikTok</b><small>Top 10 earned = 1,88M views</small></div>
</div>
<h3 class="subsection-title">Conversation timeline</h3>
<div class="grid"><div class="card half"><div class="mini-chart-head"><h3>Mentions by day</h3><span>Exact export count</span></div>{line_chart(dates,mentions)}</div><div class="card half"><div class="mini-chart-head"><h3>Engagement by day</h3><span>Export sum · directional</span></div>{line_chart(dates,eng)}</div></div>
<div class="note"><b>Momentum:</b> la conversación acelera con el evento y mantiene una cola fuerte después. El 07–10 Sep concentra 38,5% de las menciones del período.</div>
<h3 class="subsection-title">Platform & sentiment mix</h3>
<div class="grid"><div class="card half"><div class="mini-chart-head"><h3>Mentions by channel</h3><span>2.941 total</span></div>{hbar(platforms,platform_counts,width=760,height=285,left=130)}</div><div class="card half"><div class="mini-chart-head"><h3>Sentiment</h3><span>Export classification</span></div>{donut(sent)}</div></div>
<h3 class="subsection-title">Top hashtags</h3>
<div class="grid"><div class="card half">{hbar([x[0] for x in tags],[x[1] for x in tags],width=760,height=345,left=150)}</div><div class="card half hashtag-copy"><div class="callout-number">#hyroxacapulco</div><div class="callout-value">1.224 mentions</div><p>Seguido por <b>#hyrox</b> (1.137), <b>#hyroxmexico</b> (215), <b>#hyroxtraining</b> (173) y <b>#hyroxworld</b> (159).</p><div class="note compact-note"><b>Lectura:</b> el evento generó una identidad propia fuerte dentro de la conversación HYROX.</div></div></div>
<h3 class="subsection-title">Top Earned Content</h3>
<p class="section-intro">Piezas de terceros ordenadas por views/impressions disponibles. Se excluyen HYROX México y comentarios de Instagram.</p>
<div class="card full">{hbar([x[0] for x in top],[x[2] for x in top],width=900,height=420,left=175)}</div>
<div class="card full table-scroll"><table class="earned-table"><thead><tr><th>#</th><th>Platform</th><th>Creator / Content</th><th>Channel</th><th>Followers</th><th>Views</th><th>Engagement</th><th>Eng/View</th></tr></thead><tbody>{rows}</tbody></table></div>
<div class="note"><b>Earned signal:</b> los 10 contenidos externos líderes acumularon aproximadamente <b>1,88 M views</b> y <b>192,7 K engagements</b>. Los diez pertenecen a TikTok.</div>
<h3 class="subsection-title">Creator efficiency</h3>
<div class="grid"><div class="card half"><div class="mini-chart-head"><h3>Views vs follower base</h3><span>Best-performing post / followers</span></div>{hbar([x[0] for x in eff],[x[1] for x in eff],width=720,height=265,left=155,suffix="×")}</div><div class="card half"><div class="creator-insights"><div><b>Marck</b><span>206,6K views · 905 followers · ~228×</span></div><div><b>Lucía Romero</b><span>286,9K views · 1,6K followers · ~178×</span></div><div><b>Daniela Ragozzino</b><span>90,9K views · 2,3K followers · ~39×</span></div><div><b>Rod Frias</b><span>112,3K views · 7,4K followers · ~15×</span></div></div><div class="note compact-note"><b>Implication:</b> follower count alone hubiera subestimado varios de los amplificadores más eficientes.</div></div></div>
<h3 class="subsection-title">YouTube coverage</h3>
<div class="channel-header"><div><b>43 mentions/videos detected</b><span>34 unique profiles · 11,0K recorded views</span></div></div><div class="coverage-grid">{cards(yt,"yt")}</div>
<h3 class="subsection-title">Web & editorial coverage</h3>
<div class="channel-header"><div><b>55 web mentions</b><span>13 Threads posts + 42 editorial / website mentions across 33 non-Threads sources</span></div></div><div class="coverage-grid">{cards(web,"web")}</div>
<h3 class="subsection-title">X / Twitter conversation</h3>
<div class="channel-header"><div><b>65 posts detected</b><span>43 unique profiles · 26,4K recorded impressions</span></div></div><div class="coverage-grid">{cards(xposts,"x")}</div>
<div class="methodology-box"><h3>Methodology note</h3><p><b>Reach is estimated.</b> Mentionlytics social reach is not equivalent to first-party Meta reach and should not be added to Meta reach as if both represented the same unique audience.</p><p>The export sums to ~<b>576,0K</b> in <i>Total Engagement</i>, while the dashboard reports <b>581,7K</b>. We preserve the dashboard figure as the headline KPI and use export-level engagement directionally.</p></div>
</section>
<section id="pending"><div class="eyebrow">09</div><h2>Next Modules</h2><div class="grid"><div class="card third"><h3>GA4 / Web</h3><div class="placeholder">Traffic · acquisition · landing pages · conversions</div></div><div class="card third"><h3>Ambassadors</h3><div class="placeholder">50 profiles · compliance · content · performance</div></div><div class="card third"><h3>Tickets / Email</h3><div class="placeholder">Registrations · sales · email performance</div></div><div class="card full"><h3>Sponsor Intelligence</h3><div class="placeholder">Deliverables vs executed · share of voice · top content · brand moments · activations · insights</div></div></div></section>
'''

css='''/* Social Listening */.listening-kpis{margin-bottom:14px}.insight-strip{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:14px 0 22px}.insight-strip>div{background:#111;border:1px solid var(--line);border-radius:12px;padding:13px 14px}.insight-strip span{display:block;color:#808080;font-size:9px;text-transform:uppercase;letter-spacing:.07em}.insight-strip b{display:block;font-size:18px;margin:3px 0 2px}.insight-strip small{display:block;color:#999;font-size:10px}.hashtag-copy{display:flex;flex-direction:column;justify-content:center}.callout-number{font-size:30px;font-weight:900;color:var(--yellow);line-height:1.05}.callout-value{font-size:18px;font-weight:800;margin:5px 0 8px}.compact-note{margin:10px 0 0;font-size:11px}.table-scroll{overflow-x:auto}.earned-table{min-width:940px}.rank-cell{font-weight:900;color:var(--yellow)}.social-badge{width:46px;height:46px;border-radius:10px;background:#0e0e0e;border:1px solid #333;display:flex;align-items:center;justify-content:center;font-weight:900}.table-sub{font-size:10px;color:#777;max-width:380px;margin-top:3px}.report-link{color:#f1f1f1;text-decoration:none;font-weight:800}.report-link:hover{color:var(--yellow)}.creator-insights{display:flex;flex-direction:column;gap:8px}.creator-insights>div{background:#0f0f0f;border:1px solid #292929;border-radius:10px;padding:11px 12px}.creator-insights b{display:block;font-size:13px}.creator-insights span{display:block;color:#969696;font-size:10px;margin-top:2px}.channel-header{margin:6px 0 10px}.channel-header b{display:block;font-size:14px}.channel-header span{display:block;color:#888;font-size:10px;margin-top:2px}.coverage-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.coverage-card{display:block;background:#111;border:1px solid var(--line);border-radius:12px;overflow:hidden;text-decoration:none;color:#fff}.coverage-card:hover{border-color:#666}.coverage-placeholder{height:72px;display:flex;align-items:center;justify-content:center;background:#0b0b0b;color:var(--yellow);font-size:22px;font-weight:900;letter-spacing:.08em;border-bottom:1px solid #2b2b2b}.coverage-body{padding:11px 12px}.coverage-source{font-size:10px;color:var(--yellow);font-weight:800;text-transform:uppercase}.coverage-title{font-size:12px;font-weight:700;line-height:1.3;margin:5px 0 8px;min-height:31px}.coverage-kpi{font-size:10px;color:#989898}.methodology-box{margin-top:24px;border:1px solid #333;background:#0f0f0f;border-radius:14px;padding:16px 18px}.methodology-box h3{font-size:14px;margin-bottom:5px}.methodology-box p{font-size:10px;color:#999;margin:6px 0}@media(max-width:1100px){.insight-strip{grid-template-columns:repeat(2,1fr)}.coverage-grid{grid-template-columns:repeat(2,1fr)}}@media(max-width:650px){.insight-strip{grid-template-columns:1fr}.coverage-grid{grid-template-columns:1fr}}'''

if "/* Social Listening */" not in doc:
    doc=doc.replace("@media(max-width:1100px){.layout{grid-template-columns:1fr}",css+"\n@media(max-width:1100px){.layout{grid-template-columns:1fr}",1)
doc=doc.replace('<a href="#pending">08. Próximos módulos</a>','<a href="#listening">08. Social Listening</a>\n<a href="#pending">09. Next Modules</a>')
if 'id="listening"' in doc:
    doc=re.sub(r'<section id="listening">.*?</section>\s*<section id="pending">.*?</section>',section,doc,count=1,flags=re.S)
else:
    doc=re.sub(r'<section id="pending">.*?</section>',section,doc,count=1,flags=re.S)
doc=doc.replace("Working report · Meta block developed from first-party exports and screenshots supplied for HYROX Acapulco 2026.","Working report · Meta first-party + Mentionlytics social listening · HYROX Acapulco 2026.")
P.write_text(doc,encoding="utf-8")
