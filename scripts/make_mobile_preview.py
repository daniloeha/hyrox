from pathlib import Path

root = Path(__file__).resolve().parents[1]
src = root / "index.html"
out = root / "mobile-preview.html"

html = src.read_text(encoding="utf-8")
marker = "/* Responsive hardening · mobile/tablet */"

responsive_css = r'''
/* Responsive hardening · mobile/tablet */
html,body{max-width:100%;overflow-x:hidden}
.layout,main,aside,section,.grid,.card{min-width:0}
main{min-width:0}
.table-scroll,.daily-table-wrap{max-width:100%;-webkit-overflow-scrolling:touch}
img,svg,video,canvas{max-width:100%}

@media(max-width:1100px){
  aside{position:sticky;top:0;z-index:100;height:auto;padding:12px 18px;border-right:0;border-bottom:1px solid var(--line);display:grid;grid-template-columns:auto 1fr;align-items:center;gap:4px 18px;background:rgba(3,3,3,.97);backdrop-filter:blur(10px);overflow:hidden}
  .brand{font-size:20px;white-space:nowrap}
  .sub{margin:0;text-align:right;font-size:9px;white-space:nowrap}
  nav{grid-column:1/-1;display:flex;gap:4px;overflow-x:auto;overscroll-behavior-x:contain;padding-top:7px;padding-bottom:1px;scrollbar-width:none}
  nav::-webkit-scrollbar{display:none}
  nav a{display:inline-flex;flex:0 0 auto;white-space:nowrap;padding:6px 9px;font-size:11px;background:#090909;border:1px solid #171717}
  main{padding:30px 28px 64px}
  section{scroll-margin-top:102px}
  .hero{padding:26px;margin-bottom:36px}
  h1{font-size:42px}
  .metric-top,.interactive-head,.channel-header{flex-wrap:wrap}
}

@media(max-width:650px){
  aside{padding:10px 12px;gap:3px 10px}
  .brand{font-size:18px}
  .sub{font-size:8px;overflow:hidden;text-overflow:ellipsis}
  nav{padding-top:6px}
  nav a{font-size:10px;padding:6px 8px}
  main{padding:18px 12px 44px}
  section{margin-bottom:48px;scroll-margin-top:94px}
  .hero{padding:18px 16px;margin-bottom:30px;border-radius:14px}
  .eyebrow{font-size:10px;letter-spacing:.1em}
  h1{font-size:32px;line-height:1.06}
  h2{font-size:23px;line-height:1.15}
  h3{line-height:1.25}
  .value{font-size:27px}
  .card{padding:14px}
  .metric-card-wide,.metric-card-simple2{padding:14px}
  .metric-inline-grid{grid-template-columns:1fr}
  .metric-top{align-items:flex-start;gap:6px;flex-direction:column}
  .daily-table{min-width:560px}
  .daily-table th,.daily-table td{padding:6px 7px}
  .format-dynamic-card,.interactive-chart-card{padding:14px}
  .format-tabs,.chart-tabs,.chart-tabs-css{flex-wrap:nowrap;overflow-x:auto;justify-content:flex-start;padding-bottom:3px;scrollbar-width:none}
  .format-tabs::-webkit-scrollbar,.chart-tabs::-webkit-scrollbar,.chart-tabs-css::-webkit-scrollbar{display:none}
  .format-tab,.chart-tab,.chart-tab-css{flex:0 0 auto}
  .format-chart{height:230px}
  .chart-panels{min-height:220px}
  .gallery{gap:10px}
  .thumb img{height:340px}
  .story-gallery{gap:10px}
  .earned-visual-card img,.coverage-card img{height:300px}
  .channel-header{align-items:flex-start;gap:8px}
  .amb2-rank-row{grid-template-columns:22px minmax(0,1fr)}
  .amb2-rank-row strong{grid-column:2;justify-self:start;white-space:normal}
  .amb2-table{min-width:900px}
  .amb2-best{min-width:150px}
  .ticket-big{font-size:36px}
  .acapulco-big{font-size:32px}
  .email-campaign h3{font-size:15px}
  .pill{font-size:10px;padding:5px 8px}
}

@media(max-width:420px){
  .sub{display:none}
  aside{grid-template-columns:1fr}
  nav{grid-column:1}
  .hero{padding:16px 14px}
  h1{font-size:29px}
  h2{font-size:21px}
  .thumb img{height:315px}
}
'''

if marker not in html:
    html = html.replace("</head>", f"<style>\n{responsive_css}\n</style>\n</head>", 1)

out.write_text(html, encoding="utf-8")
print(f"Wrote {out.name} from {src.name}")
