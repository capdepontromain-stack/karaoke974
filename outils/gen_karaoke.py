# -*- coding: utf-8 -*-
"""Générateur du microsite karaoke974.re (Pull Up Événements)."""
import os, re, json, subprocess, uuid, datetime
from html import escape

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # racine du dépôt
DOM = 'https://karaoke974.re'
TEL = '06 93 49 19 02'; TELH = '+262693491902'; MAIL = 'contact@pullup.re'  # Ketsia gère le karaoké
NOTE = '4,9'; NB = '144'
TODAY = datetime.date.today()
TODAY_FR = TODAY.strftime('%-d ') + ['janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre'][TODAY.month-1] + TODAY.strftime(' %Y')

def img_size(name):
    p = os.path.join(OUT, 'images', name)
    o = subprocess.run(['sips','-g','pixelWidth','-g','pixelHeight',p],capture_output=True,text=True).stdout
    w = re.search(r'pixelWidth: (\d+)',o).group(1); h = re.search(r'pixelHeight: (\d+)',o).group(1)
    return w, h

def IMG(name, alt, pre='', cls='', lazy=True, w=None, h=None):
    W,H = img_size(name)
    return f'<img src="{pre}images/{name}" alt="{escape(alt)}" width="{W}" height="{H}"{" loading=\"lazy\" decoding=\"async\"" if lazy else " fetchpriority=\"high\""}{f" class=\"{cls}\"" if cls else ""}>'

# ───────────────────────── CSS ─────────────────────────
CSS = r"""
:root{--nuit:#070b1c;--encre:#0f1733;--carte:#151e3f;--bord:#243058;--blanc:#f7f5ff;--gris:#aab1d2;--rose:#ff2e88;--cyan:#1fe0ff;--jaune:#ffe347;--violet:#7c5cff}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:"Outfit",-apple-system,sans-serif;background:var(--nuit);color:var(--blanc);line-height:1.7;font-size:17px;overflow-x:hidden}
img{max-width:100%;display:block}
img[width]{height:auto}
h1,h2,h3,.disp{font-family:"Righteous",cursive;font-weight:400;line-height:1.05;letter-spacing:.3px}
h2{font-size:clamp(30px,4.4vw,46px);margin-bottom:14px}
h3{font-size:22px;margin-bottom:8px}
p{margin-bottom:12px}
a{color:var(--cyan);text-decoration:none}
.wrap{max-width:1140px;margin:0 auto;padding:0 22px}
section{padding:70px 0}
.sur{display:inline-block;font-size:12.5px;letter-spacing:3px;text-transform:uppercase;color:var(--jaune);font-weight:700;margin-bottom:10px}
.lead{font-size:19px;color:#dcd9ef;max-width:760px}
.reveal{opacity:0;transform:translateY(26px);transition:opacity .7s ease,transform .7s ease}
.reveal.on{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){.reveal{opacity:1;transform:none;transition:none}}
/* bandeau confiance */
.pu-trust{background:linear-gradient(90deg,#1a1030,#03050f 50%,#1a1030);color:#f3efff;font:700 15.5px/1.4 "Outfit",system-ui,sans-serif;padding:11px 16px;display:flex;align-items:center;justify-content:center;gap:16px;flex-wrap:wrap;position:relative;z-index:60;border-bottom:1px solid rgba(255,227,71,.35)}
.pu-trust a{color:inherit;display:inline-flex;align-items:center;gap:6px}
.pu-trust .pu-et{color:var(--jaune);letter-spacing:2px;font-size:16px;text-shadow:0 0 10px rgba(255,227,71,.6)}
.pu-trust b{color:#fff;font-weight:800}
@media(max-width:760px){.pu-trust{font-size:13px;gap:8px;padding:8px 8px}.pu-trust .pu-opt{display:none}}
/* header */
.top{position:sticky;top:0;z-index:50;background:rgba(7,11,28,.86);backdrop-filter:blur(12px);border-bottom:1px solid var(--bord)}
.top .in{max-width:1140px;margin:0 auto;padding:12px 22px;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}
.logo{font-family:"Righteous",cursive;font-size:24px;color:#fff;display:flex;align-items:center;gap:10px}
.logo .mic{width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,var(--rose),var(--violet));display:grid;place-items:center;font-size:18px;box-shadow:0 0 18px rgba(255,46,136,.55)}
.logo small{display:block;font-family:"Outfit";font-size:11px;letter-spacing:2.5px;color:var(--gris);text-transform:uppercase;line-height:1}
.top nav{display:flex;gap:4px 18px;flex-wrap:wrap;align-items:center}
.top nav a{color:var(--gris);font-weight:600;font-size:14px}
.top nav a:hover{color:#fff}
.top nav a.tel{background:var(--jaune);color:var(--nuit);padding:9px 16px;border-radius:40px;font-weight:800;white-space:nowrap}
@media(max-width:760px){.top nav a:not(.tel):not(.dv){display:none}.top nav a.dv{font-size:13px}}
/* boutons */
.btn{display:inline-block;font-weight:800;padding:15px 30px;border-radius:44px;font-size:15.5px;letter-spacing:.2px;transition:transform .15s}
.btn:hover{transform:translateY(-2px)}
.btn.rose{background:var(--rose);color:#fff;box-shadow:0 10px 32px -8px var(--rose)}
.btn.jaune{background:var(--jaune);color:var(--nuit)}
.btn.ghost{border:2px solid var(--bord);color:#fff}
/* héros */
.hero{position:relative;min-height:min(88vh,820px);display:flex;align-items:center;padding:70px 0;overflow:hidden}
.hero .bg{position:absolute;inset:0}
.hero .bg img{width:100%;height:100%;object-fit:cover;filter:brightness(.38) saturate(1.2)}
.hero .bg::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(7,11,28,.92) 0%,rgba(7,11,28,.55) 55%,rgba(7,11,28,.35) 100%),linear-gradient(180deg,transparent 60%,var(--nuit) 100%)}
.hero .glow{position:absolute;width:560px;height:560px;border-radius:50%;filter:blur(110px);opacity:.45;pointer-events:none}
.hero .glow.a{background:var(--rose);left:-180px;top:-120px;animation:flot 10s ease-in-out infinite}
.hero .glow.b{background:var(--cyan);right:-200px;bottom:-200px;animation:flot 13s ease-in-out infinite reverse}
@keyframes flot{50%{transform:translate(40px,30px)}}
.hero .in{position:relative;z-index:2;max-width:1140px;margin:0 auto;padding:0 22px;width:100%}
.badge{display:inline-flex;align-items:center;gap:8px;border:1px solid rgba(255,227,71,.45);background:rgba(15,23,51,.8);padding:9px 18px;border-radius:40px;font-size:14px;font-weight:800;letter-spacing:1px;text-transform:uppercase;color:var(--jaune);box-shadow:0 0 22px rgba(255,227,71,.18)}
.hero h1{font-size:clamp(44px,8vw,104px);margin:20px 0 10px;max-width:900px}
.hero h1 .neon{color:#fff;text-shadow:0 0 12px rgba(255,46,136,.9),0 0 38px rgba(255,46,136,.6),0 0 80px rgba(255,46,136,.35)}
.hero h1 .l2{display:block;color:var(--cyan);text-shadow:0 0 14px rgba(31,224,255,.6)}
.hero p.lead{margin:12px 0 26px;font-size:19.5px}
.hero .cta{display:flex;gap:14px;flex-wrap:wrap;align-items:center}
.hero .cta .note{font-size:14px;color:var(--gris)}
/* barre paroles karaoké : signature du site */
.lyrics{margin-top:40px;max-width:720px;background:rgba(3,5,15,.65);border:1px solid var(--bord);border-radius:14px;padding:16px 20px;font-family:"Righteous",cursive;font-size:clamp(17px,2.4vw,24px);line-height:1.35}
.lyrics .tag{display:block;font-family:"Outfit";font-size:11px;letter-spacing:3px;color:var(--gris);text-transform:uppercase;margin-bottom:6px}
.lyrics .w{color:rgba(247,245,255,.38);transition:color .25s,text-shadow .25s}
.lyrics .w.on{color:var(--jaune);text-shadow:0 0 14px rgba(255,227,71,.6)}
/* égaliseur */
.eq{display:inline-flex;gap:3px;align-items:flex-end;height:18px;margin-left:8px;vertical-align:middle}
.eq i{width:3px;background:var(--cyan);border-radius:2px;animation:eq 1s ease-in-out infinite}
.eq i:nth-child(2){animation-delay:.15s;background:var(--rose)}.eq i:nth-child(3){animation-delay:.3s;background:var(--jaune)}.eq i:nth-child(4){animation-delay:.45s}.eq i:nth-child(5){animation-delay:.6s;background:var(--rose)}
@keyframes eq{0%,100%{height:4px}50%{height:18px}}
@media(prefers-reduced-motion:reduce){.eq i{animation:none;height:10px}.hero .glow{animation:none}}
/* marquee */
.mq{background:linear-gradient(90deg,var(--rose),var(--violet),var(--cyan));color:var(--nuit);font-family:"Righteous";font-size:17px;letter-spacing:1px;overflow:hidden;white-space:nowrap;padding:11px 0}
.mq .t{display:inline-block;animation:defile 40s linear infinite}
.mq .t span{margin:0 26px}
@keyframes defile{to{transform:translateX(-50%)}}
/* formule */
.formule{background:var(--encre);border:1px solid var(--bord);border-radius:22px;padding:34px;display:grid;grid-template-columns:1.1fr .9fr;gap:34px;align-items:center;position:relative;overflow:hidden}
.formule::before{content:"";position:absolute;inset:-2px;background:conic-gradient(from 180deg,var(--rose),var(--violet),var(--cyan),var(--jaune),var(--rose));z-index:-1;filter:blur(26px);opacity:.25}
.formule ul{list-style:none;margin:14px 0 18px}
.formule li{padding:7px 0 7px 32px;position:relative;font-size:16.5px}
.formule li::before{content:"🎤";position:absolute;left:0;top:7px;font-size:15px}
.prix{text-align:center;background:var(--nuit);border-radius:18px;padding:28px 22px;border:1px solid var(--bord)}
.prix .n{font-family:"Righteous";font-size:clamp(54px,8vw,86px);color:var(--jaune);line-height:1;text-shadow:0 0 24px rgba(255,227,71,.45)}
.prix .u{color:var(--gris);font-size:14px;letter-spacing:2px;text-transform:uppercase;margin-top:8px}
.prix p{font-size:14px;color:#dcd9ef;margin-top:12px}
@media(max-width:860px){.formule{grid-template-columns:1fr;padding:24px}}
/* cartes */
.grid{display:grid;gap:20px;grid-template-columns:repeat(auto-fit,minmax(270px,1fr))}
.card{background:var(--carte);border:1px solid var(--bord);border-radius:18px;padding:24px;transition:transform .2s,border-color .2s;position:relative;overflow:hidden}
.card:hover{transform:translateY(-4px);border-color:var(--rose)}
.card .ic{font-size:30px;margin-bottom:10px}
.card p{color:#d6d3ea;font-size:15.5px;margin:0}
.card a.more{display:inline-block;margin-top:12px;font-weight:700;color:var(--jaune)}
.card.pic{padding:0}
.card.pic img{aspect-ratio:3/2;object-fit:cover;width:100%}
.card.pic .tx{padding:20px 22px 24px}
/* étapes */
.etapes{counter-reset:e;display:grid;gap:18px;grid-template-columns:repeat(auto-fit,minmax(230px,1fr))}
.etape{background:var(--encre);border-radius:16px;padding:24px 22px 22px;border:1px solid var(--bord)}
.etape b{display:block;font-family:"Righteous";font-size:44px;color:var(--rose);line-height:1;margin-bottom:10px;text-shadow:0 0 16px rgba(255,46,136,.5)}
.etape h3{font-size:19px}
.etape p{font-size:15px;color:#d6d3ea;margin:0}
/* galerie */
.gal{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(250px,1fr))}
.gal figure{position:relative;border-radius:14px;overflow:hidden;background:var(--carte);cursor:zoom-in}
.gal img{aspect-ratio:4/3;object-fit:cover;width:100%;transition:transform .5s}
.gal figure:hover img{transform:scale(1.05)}
.gal figcaption{position:absolute;left:0;right:0;bottom:0;padding:26px 14px 12px;font-size:13.5px;background:linear-gradient(transparent,rgba(3,5,15,.9));color:#fff}
.gal figure.tall img{aspect-ratio:3/4}
.lb{position:fixed;inset:0;background:rgba(3,5,15,.94);display:none;align-items:center;justify-content:center;z-index:200;padding:20px;flex-direction:column;gap:12px}
.lb.on{display:flex}
.lb img{max-width:min(96vw,1000px);max-height:80vh;border-radius:12px;width:auto}
.lb p{color:#fff;font-size:15px}
.lb button{position:absolute;top:14px;right:16px;background:var(--jaune);border:0;border-radius:40px;padding:8px 16px;font-weight:800;cursor:pointer}
/* clients */
.pu-clients{background:var(--encre);border-top:1px solid var(--bord);border-bottom:1px solid var(--bord);padding:50px 0 34px}
.pu-cl-t{text-align:center;font-family:"Righteous";font-size:30px;margin-bottom:4px}
.pu-cl-st{text-align:center;color:var(--gris);margin-bottom:26px}
.pu-ct{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:16px;max-width:1000px;margin:0 auto 26px;padding:0 22px;text-align:center}
.pu-ct .n{font-family:"Righteous";font-size:44px;color:var(--jaune);line-height:1}
.pu-ct .n .pu-or{color:var(--rose)}
.pu-ct .l{font-size:13.5px;color:var(--gris);margin-top:4px}
.pu-mq{overflow:hidden;white-space:nowrap}
.pu-mq ul{display:inline-block;list-style:none;animation:defile 50s linear infinite}
.pu-mq li{display:inline-block;margin:0 24px;font-weight:700;color:#e4e1f3;font-size:16px}
.pu-cl-p{text-align:center;color:var(--gris);font-size:14px;margin-top:16px}
/* avis */
.avis{display:grid;gap:18px;grid-template-columns:repeat(auto-fit,minmax(290px,1fr))}
.avis figure{background:var(--carte);border:1px solid var(--bord);border-radius:18px;padding:24px;margin:0}
.etoiles{color:var(--jaune);letter-spacing:3px;font-size:17px;margin-bottom:8px}
.avis blockquote p{font-size:16.5px;color:#eceaf8;margin:0 0 12px}
.avis figcaption{font-weight:700}
.avis figcaption span{display:block;font-weight:400;font-size:13px;color:var(--gris)}
/* répertoire */
.repert{display:flex;flex-wrap:wrap;gap:10px}
.repert span{border:1px solid var(--bord);background:var(--encre);padding:9px 16px;border-radius:40px;font-size:15px}
.repert span b{color:var(--jaune)}
/* zones */
.zones{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}
.zone{display:block;background:var(--encre);border:1px solid var(--bord);border-radius:16px;padding:22px;color:inherit}
.zone:hover{border-color:var(--cyan)}
.zone h3{color:var(--cyan)}
.zone p{font-size:14.5px;color:#d6d3ea;margin:0}
/* faq */
.faq details{background:var(--carte);border:1px solid var(--bord);border-radius:14px;padding:0 20px;margin-bottom:10px}
.faq summary{cursor:pointer;font-weight:700;padding:16px 0;font-size:17px;list-style:none;display:flex;justify-content:space-between;gap:12px}
.faq summary::after{content:"+";color:var(--rose);font-family:"Righteous";font-size:24px;line-height:1}
.faq details[open] summary::after{content:"×"}
.faq details p{padding:0 0 16px;color:#dcd9ef;font-size:15.5px}
/* devis */
#devis{background:radial-gradient(circle at 20% 20%,rgba(255,46,136,.18),transparent 45%),radial-gradient(circle at 80% 80%,rgba(31,224,255,.16),transparent 45%),var(--encre)}
.pu-form{max-width:600px;margin:26px auto 0;text-align:left}
.pu-form .duo{display:grid;grid-template-columns:1fr 1fr;gap:0 14px}
@media(max-width:560px){.pu-form .duo{grid-template-columns:1fr}}
.pu-form label{display:block;font-weight:700;font-size:13.5px;margin:12px 0 5px;color:#fff}
.pu-form input,.pu-form select,.pu-form textarea{width:100%;padding:12px 14px;border:2px solid var(--bord);border-radius:10px;background:#fff;color:#111;font-family:"Outfit",sans-serif;font-size:15.5px}
.pu-form input:focus,.pu-form select:focus,.pu-form textarea:focus{outline:none;border-color:var(--jaune)}
.pu-form button.btn{width:100%;margin-top:20px;border:0;cursor:pointer;font-size:16.5px;font-family:"Outfit",sans-serif}
.pu-form button.btn[disabled]{opacity:.6;cursor:default}
.contact-direct{display:flex;gap:14px;flex-wrap:wrap;justify-content:center;margin-top:18px}
/* écosystème */
.eco{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}
.eco a{display:block;background:var(--carte);border:1px solid var(--bord);border-radius:12px;padding:14px 16px;color:#fff;font-weight:600;font-size:15px}
.eco a small{display:block;color:var(--gris);font-weight:400;font-size:13px}
.eco a:hover{border-color:var(--jaune)}
.rs a{display:inline-block;margin:6px 10px 0 0;border:1px solid var(--bord);padding:9px 16px;border-radius:40px;color:#fff;font-weight:600;font-size:14.5px}
/* footer */
footer{background:#03050f;padding:46px 0 90px;border-top:1px solid var(--bord);font-size:14.5px;color:var(--gris)}
footer .fbig{font-family:"Righteous";font-size:30px;color:#fff;margin-bottom:8px}
footer a{color:#e4e1f3}
footer p{margin-bottom:8px}
/* barre d'appel mobile */
.barre-mobile{position:fixed;left:0;right:0;bottom:0;z-index:80;display:none;grid-template-columns:1fr 1fr;gap:8px;padding:10px 12px;background:rgba(3,5,15,.94);border-top:1px solid var(--bord);backdrop-filter:blur(10px)}
.barre-mobile a{text-align:center;padding:12px;border-radius:12px;font-weight:800;font-size:15px}
@media(max-width:760px){.barre-mobile{display:grid}}
/* page intérieure */
.hero-int{position:relative;padding:80px 0 60px;background:var(--encre);overflow:hidden}
.hero-int .bg{position:absolute;inset:0;opacity:.28}
.hero-int .bg img{width:100%;height:100%;object-fit:cover}
.hero-int .in{position:relative;z-index:1}
.hero-int h1{font-size:clamp(34px,6vw,66px);margin:14px 0 12px}
.hero-int h1 span{color:var(--cyan)}
.fil{font-size:13.5px;color:var(--gris);margin-bottom:10px}
.prose{max-width:800px}
.prose h2{font-size:clamp(26px,3.6vw,36px);margin:34px 0 10px}
.prose h3{font-size:21px;margin:22px 0 6px;color:var(--jaune)}
.prose ul,.prose ol{margin:0 0 14px 22px}
.prose li{margin-bottom:6px}
.encart{background:var(--carte);border-left:4px solid var(--rose);border-radius:12px;padding:18px 20px;margin:22px 0}
.cta-fin{background:linear-gradient(135deg,rgba(255,46,136,.22),rgba(31,224,255,.16));border:1px solid var(--bord);border-radius:20px;padding:30px;text-align:center;margin-top:40px}
.cta-fin h2{margin-bottom:8px}
.auteur{display:flex;gap:16px;align-items:center;background:var(--carte);border-radius:14px;padding:18px;margin-top:36px;border:1px solid var(--bord)}
.auteur .av{width:54px;height:54px;border-radius:50%;background:linear-gradient(135deg,var(--rose),var(--violet));display:grid;place-items:center;font-family:"Righteous";font-size:22px;flex:none}
.blog-list{display:grid;gap:18px;grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}
"""

HEAD_FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Righteous&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet" media="print" onload="this.media=\'all\'"><noscript><link href="https://fonts.googleapis.com/css2?family=Righteous&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet"></noscript>'

ORG_JSON = {"@context":"https://schema.org","@type":["Organization","LocalBusiness"],"@id":DOM+"/#organization","name":"Pull Up Événements","legalName":"Pull Up Événements","url":DOM+"/","logo":DOM+"/favicon.svg","image":DOM+"/images/hero-karaoke-neon-reunion-974.jpg","foundingDate":"2017","founder":{"@type":"Person","name":"Romain Capdepont"},"address":{"@type":"PostalAddress","streetAddress":"6 Impasse des Sœurs Brontë","postalCode":"97430","addressLocality":"Le Tampon","addressRegion":"La Réunion","addressCountry":"FR"},"telephone":TELH,"email":MAIL,"areaServed":"La Réunion","priceRange":"€€","openingHours":"Mo-Su 08:30-20:00","aggregateRating":{"@type":"AggregateRating","ratingValue":4.9,"reviewCount":NB,"bestRating":5},"sameAs":["https://pullup.re","https://teambuilding974.re","https://seminaire974.re","https://soiree974.re","https://arbredenoel974.re","https://animationenfant974.re","https://hotesse-reunion.re","https://productionvideo974.re","https://g.page/r/CYZGysYZgL8iEBM","https://www.facebook.com/pullupevenements/","https://www.instagram.com/pull_up_evenements","https://www.tiktok.com/@pull.up.evenements","https://www.youtube.com/@pullupevenements","https://www.linkedin.com/company/pullup-%C3%A9v%C3%A9nements/","https://www.pagesjaunes.fr/pros/63182047","https://fr.mappy.com/poi/668b691bf29adc15d0b11c04","https://www.evenementiel.info/prestataire-11-pull-evenements.html"]}

def trust(pre):
    return f'''<div class="pu-trust"><a href="https://g.page/r/CYZGysYZgL8iEBM" target="_blank" rel="noopener" title="Voir les {NB} avis Google de Pull Up Événements"><span class="pu-opt">Pull Up Événements, agence événementielle à La Réunion · </span><span class="pu-et">★★★★★</span> <b>{NOTE}/5</b> sur Google · <b class="pu-nb-avis">{NB} avis clients</b></a><span class="pu-opt">·</span><a href="tel:{TELH}"><b>📞 {TEL}</b></a></div>'''

def header(pre):
    return f'''<header class="top"><div class="in">
<a class="logo" href="{pre}./" aria-label="Karaoké 974, accueil"><span class="mic">🎤</span><span>Karaoké <span style="color:var(--rose)">974</span><small>by Pull Up Événements</small></span></a>
<nav aria-label="Navigation principale"><a href="{pre}#formule">La formule</a><a href="{pre}#formats">Pour qui</a><a href="{pre}#galerie">Photos</a><a href="{pre}#avis">Avis</a><a href="{pre}#faq">Questions</a><a href="{pre}blog/">Blog</a><a class="dv" href="{pre}#devis">Devis 24 h</a><a class="tel" href="tel:{TELH}">📞 {TEL}</a></nav>
</div></header>'''

ZONES = [
 ('karaoke-nord-saint-denis','Nord','Saint-Denis, Sainte-Marie, Sainte-Suzanne, La Montagne','Le chef-lieu et ses entreprises : sièges, administrations, CSE, bars et restaurants du Barachois au Chaudron.'),
 ('karaoke-sud-saint-pierre','Sud','Saint-Pierre, Le Tampon, Saint-Louis, Saint-Joseph, L\'Étang-Salé, Petite-Île','Notre base : nous sommes installés au Tampon. Terre Sainte, la Ravine Blanche, les Hauts du Tampon, tout est à moins de 30 minutes.'),
 ('karaoke-ouest-saint-paul','Ouest','Saint-Paul, Saint-Gilles, La Saline, Le Port, La Possession, Saint-Leu','Les villas de Saint-Gilles, les salles du Port et les entreprises de la zone de Cambaie : la côte où l\'on fête le plus.'),
 ('karaoke-est-saint-andre','Est','Saint-André, Saint-Benoît, Bras-Panon, Sainte-Rose, Salazie, La Plaine-des-Palmistes','Mariages, fêtes de famille et associations : l\'Est aime chanter, de Cambuston à Sainte-Anne.'),
]
FORMATS = [
 ('karaoke-entreprise-reunion','🏢','Soirée d\'entreprise et CSE','Pot de départ, fête de fin d\'année, afterwork, séminaire : le karaoké casse les étages hiérarchiques en trois chansons. Facture, devis en 24 h et animateur habitué aux publics mixtes.'),
 ('karaoke-anniversaire-reunion','🎂','Anniversaire à domicile','30, 40, 50 ans ou anniversaire surprise : on installe dans votre salon, votre varangue ou votre kiosque. Les invités chantent, l\'animateur gère le reste.'),
 ('karaoke-mariage-reunion','💍','Mariage et fête de famille','Après le repas, avant ou en relais du DJ : une heure de karaoké pour faire monter la famille sur scène, des cousins aux grands-parents.'),
 ('karaoke-association-mairie-reunion','🏘️','Association et mairie','Fête de quartier, loto, kermesse, soirée du club : une formule simple à budgéter, sans acompte pour les collectivités.'),
 ('karaoke-entreprise-reunion','🍹','Bar et restaurant','Une soirée karaoké animée par un pro remplit une salle un jeudi soir. Formule ponctuelle ou rendez-vous mensuel.'),
 ('karaoke-entreprise-reunion','🎄','Arbre de Noël et fête de fin d\'année','Un karaoké spécial familles, avec des titres pour enfants et des classiques de Noël, en complément du Père Noël.'),
]
FAQ = [
 ('Combien coûte une soirée karaoké à La Réunion ?','Notre formule complète est à 470 € HT tout compris, soit 509,95 € TTC : animateur, sonorisation, micros sans fil, catalogue de titres, installation et démontage, pour 3 à 4 heures. Les entreprises reçoivent un devis et une facture. Pour une durée plus longue, un deuxième animateur ou un écran géant, demandez un chiffrage en 24 h.'),
 ('Qui propose des animations karaoké à La Réunion ?','Karaoké 974 est le service karaoké de Pull Up Événements, agence événementielle du Tampon créée en 2017 (société depuis 2022), notée 4,9/5 sur Google. Nous intervenons sur toute l\'île avec un animateur karaoké dédié et notre propre matériel.'),
 ('Le matériel est-il fourni ?','Oui. Sonorisation adaptée à la taille de la salle, micros sans fil, pupitre de l\'animateur, affichage des paroles sur écran ou vidéoprojecteur selon le lieu, jeux de lumière d\'ambiance. Vous n\'avez rien à louer ni à brancher.'),
 ('Combien de temps dure la prestation ?','La formule standard couvre 3 à 4 heures d\'animation, hors installation. C\'est la bonne durée pour une soirée : tout le monde a le temps de passer, personne ne se lasse. Au-delà, nous ajustons le devis.'),
 ('Quelles chansons sont disponibles ?','Le catalogue réunit des milliers de titres : variété française, tubes internationaux, années 80 et 90, séga et maloya, zouk, dancehall, titres pour enfants et grands classiques à reprendre en chœur. Vous pouvez nous transmettre une liste de souhaits avant la soirée.'),
 ('Intervenez-vous partout sur l\'île ?','Oui, du Nord au Sud et de l\'Est à l\'Ouest. Nous sommes basés au Tampon et nous nous déplaçons à Saint-Denis, Saint-Paul, Saint-Pierre, Saint-André et dans les Hauts. Le déplacement est précisé sur le devis.'),
 ('Peut-on organiser un karaoké en entreprise ?','C\'est même notre spécialité : pot de départ, séminaire, fête de fin d\'année, afterwork, arbre de Noël. L\'animateur sait gérer un public mixte, faire chanter les volontaires et ménager les timides. Devis, facture et interlocuteur unique côté Pull Up.'),
 ('Faut-il une grande salle ?','Non. Un salon, une varangue, un kiosque, une salle de réunion ou une salle polyvalente conviennent. Il faut une prise électrique et un mur ou un espace pour l\'écran. En extérieur, prévoyez un abri en cas de pluie.'),
 ('L\'animateur fait-il aussi DJ ?','Entre deux chansons, l\'animateur enchaîne les titres et garde le rythme de la soirée. Pour une vraie partie dancefloor après le karaoké, nous proposons un DJ de l\'équipe Pull Up en complément : parlez-en au devis.'),
 ('Comment réserver une date ?','Appelez le 06 93 49 19 02 ou remplissez le formulaire : vous recevez un devis sous 24 h. La date est bloquée à la signature. Les collectivités règlent après la prestation, sans acompte.'),
 ('Le karaoké convient-il aux enfants ?','Oui. Pour un anniversaire d\'enfant ou un arbre de Noël, nous sélectionnons des titres adaptés (dessins animés, comédies musicales, tubes du moment) et l\'animateur adapte son rythme. Pour une animation enfants complète, voyez aussi animationenfant974.re.'),
 ('Pourquoi passer par Pull Up Événements plutôt qu\'un animateur seul ?','Vous avez un interlocuteur agence, un devis clair, une facture, une solution de remplacement si l\'animateur est indisponible, et la possibilité d\'ajouter d\'autres prestations : DJ, hôtesses, photobooth, traiteur, décoration. Plus de 500 événements réalisés et 4,9/5 sur Google.'),
]

AVIS = [
 ('angelique socolingom',5,'Super et beaucoup patience vue qu\'on etait 1 peu dissiper "lol ". Franchement super et merci pour votre collaboration'),
 ('Teddy CLAIN',5,'Très belle journée ce samedi 4 avril 2026 qui s\'est déroulée dans l\'amour, la paix et la joie. Des animateurs au top qui ont bien mené les activités tout au long de cette journée. Merci à eux pour ce moment mémorable 👏'),
]

def clients_block():
    li = ''.join(f'<li>{c}</li>' for c in ['Crédit Agricole','Crédit Moderne','INSEE','SAPMER','CILAM','Mercialys','Sudeco','Ravate Pro','Croix-Rouge française','Fondation Père Favron','Groupe Caillé','Testoni','IAE Réunion'])
    return f'''<section class="pu-clients" aria-label="Ils nous font confiance"><p class="pu-cl-t">Ils font confiance à Pull Up</p><p class="pu-cl-st">Entreprises, institutions et CSE de toute La Réunion.</p>
<div class="pu-ct"><div><div class="n"><em data-pu-n="500">500</em><span class="pu-or">+</span></div><div class="l">événements réalisés</div></div><div><div class="n">2017</div><div class="l">naissance de la marque · société depuis 2022</div></div><div><div class="n">{NOTE}<span class="pu-or">/5</span></div><div class="l">note moyenne Google</div></div><div><div class="n">{NB}</div><div class="l">avis clients</div></div></div>
<div class="pu-mq" role="presentation"><ul>{li}</ul><ul aria-hidden="true">{li}</ul></div>
<p class="pu-cl-p">…et des dizaines de comités d'entreprise et d'associations. <a href="https://pullup.re/ils-nous-font-confiance/">Voir nos références →</a></p></section>'''

def avis_block(pre):
    figs = ''.join(f'<figure><div class="etoiles" aria-label="{s} sur 5">{"★"*s}{"☆"*(5-s)}</div><blockquote><p>{escape(t)}</p></blockquote><figcaption>{escape(n)}<span>Avis Google · {s}/5</span></figcaption></figure>' for n,s,t in AVIS)
    return f'''<section id="avis"><div class="wrap"><span class="sur">Avis Google</span><h2>Ce que disent les clients de Pull Up</h2><p class="lead">Deux avis publics parmi les {NB} laissés sur notre fiche Google, repris mot pour mot.</p>
<div class="avis reveal">{figs}</div>
<p style="text-align:center;margin-top:22px"><a class="btn jaune" href="https://g.page/r/CYZGysYZgL8iEBM" target="_blank" rel="noopener">Lire les {NB} avis Google</a></p></div></section>'''

def devis_block(pre, type_default='Soirée d\'entreprise'):
    opts = ''.join(f'<option{" selected" if o==type_default else ""}>{o}</option>' for o in ['Soirée d\'entreprise','Anniversaire','Mariage','Association / mairie','Bar / restaurant','Arbre de Noël','Autre'])
    return f'''<section id="devis"><div class="wrap" style="text-align:center"><span class="sur">Devis gratuit</span><h2>Réservez votre soirée karaoké</h2><p class="lead" style="margin:0 auto">Ketsia vous répond sous 24 h, souvent dans l'heure. Dites-nous la date, le lieu et le nombre d'invités : on s'occupe du reste.</p>
<div class="contact-direct"><a class="btn jaune" href="tel:{TELH}">📞 {TEL}</a><a class="btn ghost" href="mailto:{MAIL}?subject=Devis%20karaok%C3%A9%20%C3%A0%20La%20R%C3%A9union&body=Bonjour%2C%0A%0AJe%20souhaite%20un%20devis%20pour%20une%20soir%C3%A9e%20karaok%C3%A9.%0ADate%20%3A%20%0ALieu%20%3A%20%0ANombre%20d'invit%C3%A9s%20%3A%20%0AType%20(entreprise%2C%20anniversaire%2C%20mariage...)%20%3A%20%0A%0AMerci%20!">✉️ {MAIL}</a></div>
<form class="pu-form" id="form-devis">
<input type="checkbox" name="botcheck" tabindex="-1" autocomplete="off" style="display:none" aria-hidden="true"><input type="hidden" name="source_page" value=""><input type="hidden" name="site" value="karaoke974.re">
<label for="nom">Votre nom / société</label><input id="nom" name="nom" required>
<div class="duo"><div><label for="tel">Téléphone</label><input id="tel" name="telephone" type="tel" required></div><div><label for="email">E-mail</label><input id="email" name="email" type="email" autocomplete="email" required placeholder="Pour recevoir le devis"></div></div>
<div class="duo"><div><label for="invites">Nombre d'invités</label><input id="invites" name="invites" type="number" min="1" inputmode="numeric" placeholder="Ex : 40"></div><div><label for="date">Date de l'événement</label><input id="date" name="date" placeholder="Ex : 12/12/2026"></div></div>
<div class="duo"><div><label for="lieu">Lieu ou commune</label><input id="lieu" name="lieu" placeholder="Ex : Saint-Pierre, salle à définir…"></div><div><label for="type">Type d'événement</label><select id="type" name="type">{opts}</select></div></div>
<label for="msg">Votre projet en quelques mots</label><textarea id="msg" name="message" rows="3" placeholder="Horaires, salle, intérieur ou extérieur, chansons incontournables…"></textarea>
<label for="connu-par">Comment nous avez-vous connus ?</label><select id="connu-par" name="Comment nous avez-vous connus" required><option value="">Choisir dans la liste</option><option>Google</option><option>IA (ChatGPT, Perplexity, autre assistant)</option><option>Facebook / Instagram</option><option>LinkedIn</option><option>Bouche-à-oreille</option><option>Déjà client</option><option>Annuaire</option><option>Autre</option></select>
<button class="btn rose" type="submit" id="btn-devis">Demander mon devis karaoké</button>
<label for="pu-consent" style="display:flex;gap:9px;align-items:flex-start;margin:16px 0 0;font-weight:400;font-size:13.5px;line-height:1.45;cursor:pointer"><input type="checkbox" id="pu-consent" name="consentement" value="oui" required style="width:auto;flex:none;margin:3px 0 0"><span>J'accepte que mes informations soient utilisées pour traiter ma demande.</span></label>
<p style="font-size:12.5px;line-height:1.5;margin:8px 0 0;color:var(--gris)">Vos coordonnées servent uniquement à vous répondre et à établir votre devis. Conservées 3 ans au plus. Détails dans la <a href="{pre}confidentialite/">politique de confidentialité</a>.</p>
<p id="devis-etat" style="margin-top:12px;font-weight:600" aria-live="polite"></p>
</form></div></section>'''

def eco_block(pre):
    sites = [('https://pullup.re/','Pull Up Événements','l\'agence : toutes nos prestations'),('https://soiree974.re/','Soirée 974','soirées d\'entreprise et galas'),('https://teambuilding974.re/','Team Building 974','journées de cohésion'),('https://arbredenoel974.re/','Arbre de Noël 974','Père Noël et fêtes de fin d\'année'),('https://animationenfant974.re/','Animation Enfant 974','anniversaires et kids club'),('https://seminaire974.re/','Séminaire 974','séminaires résidentiels et incentive'),('https://hotesse-reunion.re/','Hôtesse Réunion','hôtesses d\'accueil'),('https://productionvideo974.re/','Production Vidéo 974','aftermovies et captations'),('https://g.page/r/CYZGysYZgL8iEBM','Notre fiche Google','4,9/5 sur 144 avis')]
    a = ''.join(f'<a href="{u}">{n}<small>{d}</small></a>' for u,n,d in sites)
    return f'''<section id="ecosysteme"><div class="wrap"><span class="sur">Une agence, huit sites</span><h2>Le karaoké se marie avec tout le reste</h2><p class="lead">Karaoké 974 est l'un des services de Pull Up Événements. Besoin d'un DJ après le karaoké, d'hôtesses à l'accueil, d'un Père Noël ou d'une vidéo souvenir ? Un seul interlocuteur, un seul devis.</p>
<div class="eco reveal">{a}</div>
<div class="rs" style="margin-top:26px"><span class="sur" style="display:block">Suivez Pull Up</span><a href="https://www.facebook.com/pullupevenements/" rel="noopener" target="_blank">Facebook</a><a href="https://www.instagram.com/pull_up_evenements" rel="noopener" target="_blank">Instagram</a><a href="https://www.tiktok.com/@pull.up.evenements" rel="noopener" target="_blank">TikTok</a><a href="https://www.youtube.com/@pullupevenements" rel="noopener" target="_blank">YouTube</a><a href="https://www.linkedin.com/company/pullup-%C3%A9v%C3%A9nements/" rel="noopener" target="_blank">LinkedIn</a></div></div></section>'''

def footer(pre):
    zones = ' · '.join(f'<a href="{pre}{z}/">Karaoké {n}</a>' for z,n,_,_ in ZONES)
    formats = ' · '.join(f'<a href="{pre}{s}/">{t}</a>' for s,_,t,_ in FORMATS[:4])
    return f'''<footer><div class="wrap"><p class="fbig">Karaoké 974</p>
<p>Le service karaoké de <a href="https://pullup.re/">Pull Up Événements, la grande agence événementielle de La Réunion</a>. Marque créée en 2017, société depuis 2022 · {NOTE}/5 sur Google · {TEL}.</p>
<p>{formats}</p><p>{zones}</p>
<p><a href="{pre}blog/">Le blog du karaoké péi</a> · <a href="https://g.page/r/CYZGysYZgL8iEBM">⭐ {NOTE}/5 sur Google</a> · 6 Impasse des Sœurs Brontë, 97430 Le Tampon · <a href="mailto:{MAIL}">{MAIL}</a></p>
<p style="font-size:13px"><a href="{pre}mentions-legales/" style="text-decoration:underline">Mentions légales</a> · <a href="{pre}confidentialite/" style="text-decoration:underline">Politique de confidentialité</a> · Photos d'illustration : Unsplash (licence libre), en attendant les photos de nos soirées.</p>
<p id="pu-maj" style="font-size:13px;opacity:.8;margin-top:10px">Dernière mise à jour : <time datetime="{TODAY.isoformat()}">{TODAY_FR}</time>.</p></div></footer>
<div class="barre-mobile"><a class="btn jaune" href="tel:{TELH}">📞 Appeler</a><a class="btn rose" href="{pre}#devis">Devis 24 h</a></div>'''

JS = r"""
<script>
(function(){
  var calme = matchMedia('(prefers-reduced-motion: reduce)').matches;
  /* apparition au défilement */
  var io = new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('on');io.unobserve(e.target);}})},{threshold:.12});
  document.querySelectorAll('.reveal').forEach(function(el){io.observe(el)});
  /* barre paroles : les mots s'allument comme au karaoké */
  var ly=document.querySelector('.lyrics .txt');
  if(ly && !calme){var mots=ly.textContent.trim().split(/\s+/);ly.innerHTML=mots.map(function(m){return '<span class="w">'+m+'</span>'}).join(' ');var ws=ly.querySelectorAll('.w'),i=0;setInterval(function(){ws.forEach(function(w,k){w.classList.toggle('on',k<=i)});i=(i+1)%(ws.length+6);},420);}
  /* visionneuse */
  var lb=document.querySelector('.lb'); if(lb){var im=lb.querySelector('img'),cap=lb.querySelector('p');
    document.querySelectorAll('.gal figure').forEach(function(f){f.addEventListener('click',function(){var g=f.querySelector('img');im.src=g.src;im.alt=g.alt;cap.textContent=(f.querySelector('figcaption')||{}).textContent||'';lb.classList.add('on');})});
    lb.addEventListener('click',function(e){if(e.target!==im)lb.classList.remove('on')}); document.addEventListener('keydown',function(e){if(e.key==='Escape')lb.classList.remove('on')});}
  /* compteur */
  document.querySelectorAll('[data-pu-n]').forEach(function(el){var fin=parseFloat(el.getAttribute('data-pu-n')),t0=null;var o=new IntersectionObserver(function(es){if(!es[0].isIntersecting)return;o.disconnect();if(calme)return;function f(ts){if(!t0)t0=ts;var p=Math.min(1,(ts-t0)/1400);el.textContent=Math.round(fin*p);if(p<1)requestAnimationFrame(f);else el.textContent=fin;}requestAnimationFrame(f);});o.observe(el);});
})();
/* ── formulaire : relais pullup.re, secours Web3Forms, puis messagerie ── */
var CLE_WEB3FORMS = "b3c46110-bfbb-43f9-82b0-d856c919590d"; var SITE = "karaoke974.re";
function pisterEvenement(nom, params){ if (typeof gtag !== 'function') return; gtag('event', nom, params || {}); }
document.querySelectorAll('a[href^="tel:"]').forEach(function(a){ a.addEventListener('click', function(){ pisterEvenement('appel_clic', { site: SITE, page: location.pathname }); }); });
(function(){ var f=document.getElementById('form-devis'), btn=document.getElementById('btn-devis'), etat=document.getElementById('devis-etat'); if(!f) return;
  try{ if(f.source_page) f.source_page.value=location.pathname; }catch(e){}
  function champs(){ return {"Nom / société":f.nom.value,"Téléphone":f.telephone.value,"E-mail":f.email.value,"Nombre d'invités":f.invites.value||"non précisé","Date envisagée":f.date.value||"non précisée","Lieu ou commune":f.lieu.value||"non précisé","Type d'événement":f.type.value,"Le projet":f.message.value||"—","Comment nous avez-vous connus":f["Comment nous avez-vous connus"].value||"non précisé"}; }
  function secours(){ var d=champs(), corps="Bonjour,\r\n\r\nJe souhaite réserver une soirée karaoké à La Réunion.\r\n\r\n"; for(var k in d) corps+=k+" : "+d[k]+"\r\n"; corps+="\r\n(Demande envoyée depuis "+SITE+")"; location.href="mailto:contact@pullup.re?subject="+encodeURIComponent("Devis karaoké — "+f.nom.value)+"&body="+encodeURIComponent(corps); }
  f.addEventListener('submit', function(e){ e.preventDefault(); if(f.botcheck&&f.botcheck.checked){f.reset();return;} btn.disabled=true; var lib=btn.textContent; btn.textContent="Envoi en cours…"; etat.textContent="";
    var d=champs(); d._subject="Devis karaoké — "+f.nom.value; d["Reçu depuis"]=SITE; d.source_page=(f.source_page&&f.source_page.value)||location.pathname; d.site=SITE; d.botcheck=false; d["Consentement RGPD"]=(f.consentement&&f.consentement.checked)?"oui":"non";
    function web3(){ var c={access_key:CLE_WEB3FORMS,subject:d._subject,from_name:'Karaoké 974'}; for(var k in d) if(k.charAt(0)!=='_') c[k]=d[k]; return fetch('https://api.web3forms.com/submit',{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(c)}).then(function(r){return r.json()}).then(function(rep){ if(rep&&rep.success) return rep; throw new Error('refus'); }); }
    function relais(){ return fetch('https://pullup.re/relais-formulaires.php',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)}).then(function(r){return r.json()}).then(function(rep){ if(rep&&rep.success) return rep; throw new Error('refus'); }); }
    relais().catch(web3).then(function(){ f.reset(); btn.textContent="Demande envoyée ✓"; etat.style.color="#fff"; etat.textContent="Merci ! Votre demande est bien arrivée. Nous revenons vers vous sous 24 h. Pour aller plus vite, appelez le 06 93 49 19 02."; pisterEvenement('devis_envoye',{site:SITE,prestation:f.type?f.type.value:'',source_page:location.pathname}); })
    .catch(function(){ btn.disabled=false; btn.textContent=lib; etat.style.color="#ffe347"; etat.textContent="L'envoi automatique n'a pas fonctionné : nous ouvrons votre messagerie avec la demande pré-remplie. Ou appelez le 06 93 49 19 02."; secours(); });
  });
})();
</script>"""

def page(path, title, desc, body, pre, og_img='hero-karaoke-neon-reunion-974.jpg', jsonld=(), preload=None, noindex=False):
    url = DOM + '/' + (path + '/' if path else '')
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(j,ensure_ascii=False)}</script>' for j in jsonld)
    html = f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{url}">
{'<meta name="robots" content="noindex">' if noindex else ''}
<meta name="theme-color" content="#070b1c">
<meta property="og:type" content="website"><meta property="og:locale" content="fr_FR"><meta property="og:site_name" content="Karaoké 974 by Pull Up Événements">
<meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(desc)}"><meta property="og:image" content="{DOM}/images/{og_img}"><meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{pre}favicon.svg" type="image/svg+xml">
{HEAD_FONTS}
{f'<link rel="preload" as="image" href="{pre}images/{preload}" fetchpriority="high">' if preload else ''}
<style>{CSS}</style>
<script src="{pre}suivi.js" defer></script>
</head>
<body>
{trust(pre)}
{header(pre)}
<main>
{body}
</main>
{footer(pre)}
<div class="lb" role="dialog" aria-label="Photo agrandie"><button type="button">Fermer ✕</button><img src="" alt=""><p></p></div>
{JS}
{ld}
</body>
</html>'''
    d = os.path.join(OUT, path) if path else OUT
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d,'index.html'),'w',encoding='utf-8') as f: f.write(html)
    return url

# ───────────────────────── ACCUEIL ─────────────────────────
def accueil():
    pre=''
    formats = ''.join(f'<article class="card reveal"><div class="ic">{ic}</div><h3>{t}</h3><p>{d}</p><a class="more" href="{pre}{s}/">En savoir plus →</a></article>' for s,ic,t,d in FORMATS)
    gal_items = [
     ('enseigne-karaoke-neon-soiree-reunion-974.jpg','Le signal est donné : la soirée karaoké peut commencer',''),
     ('salle-karaoke-ecrans-ambiance-rose-974.jpg','Paroles sur écran, lumières d\'ambiance : la scène est prête',''),
     ('micro-sans-fil-soiree-entreprise-karaoke-974.jpg','Micros sans fil : on chante depuis la table, pas besoin de monter sur scène',''),
     ('public-mains-levees-soiree-karaoke-entreprise-974.jpg','Le refrain repris en chœur par toute la salle',''),
     ('micro-vintage-lumieres-soiree-karaoke-reunion.jpg','Micro vintage et guirlandes : l\'ambiance cabaret pour un anniversaire',''),
     ('dancefloor-lumieres-bleues-soiree-karaoke-974.jpg','Quand le karaoké se transforme en dancefloor','tall'),
     ('micro-retro-ambiance-doree-karaoke-974.jpg','Lumière dorée pour un mariage : le micro attend les témoins','tall'),
     ('bar-neon-karaoke-prive-ambiance-974.jpg','Soirée karaoké dans un bar : un jeudi soir qui fait le plein',''),
     ('micro-sur-pied-projecteur-animation-karaoke.jpg','Le projecteur sur le micro : à qui le tour ?','tall'),
     ('jeux-de-lumiere-sono-karaoke-reunion.jpg','Jeux de lumière fournis avec la sonorisation',''),
     ('micro-scene-bleue-karaoke-anniversaire-974.jpg','Ambiance bleue pour une soirée d\'entreprise',''),
     ('invites-devant-la-scene-karaoke-reunion.jpg','Les invités devant la scène, prêts à encourager',''),
    ]
    gal = ''.join(f'<figure class="reveal {cls}">{IMG(n,a,pre)}<figcaption>{escape(a)}</figcaption></figure>' for n,a,cls in gal_items)
    faq = ''.join(f'<details{" open" if i==0 else ""}><summary>{escape(q)}</summary><p>{escape(a)}</p></details>' for i,(q,a) in enumerate(FAQ))
    zones = ''.join(f'<a class="zone reveal" href="{pre}{z}/"><h3>Karaoké {n}</h3><p><b>{c}.</b> {d}</p></a>' for z,n,c,d in ZONES)
    repert = ''.join(f'<span>{r}</span>' for r in ['<b>Séga</b> et maloya','<b>Variété</b> française','<b>Tubes</b> internationaux','Années <b>80 et 90</b>','<b>Zouk</b> et dancehall','<b>Disney</b> et dessins animés','<b>Duos</b> et chansons à reprendre en chœur','Classiques de <b>Noël</b>','Rock et <b>pop</b>','R&amp;B et <b>hip-hop</b>'])
    body = f'''
<section class="hero" aria-label="Karaoké à La Réunion">
<div class="bg">{IMG('hero-karaoke-neon-reunion-974.jpg','Enseigne karaoké au néon : soirée karaoké à La Réunion avec Pull Up Événements',pre,lazy=False)}</div>
<div class="glow a"></div><div class="glow b"></div>
<div class="in">
<a class="badge" href="https://g.page/r/CYZGysYZgL8iEBM" target="_blank" rel="noopener">★★★★★ {NOTE}/5 sur Google · {NB} avis · un service de Pull Up Événements</a>
<h1><span class="neon">Karaoké</span> à La Réunion<span class="l2">animateur + sono, clé en main</span></h1>
<p class="lead">Un animateur karaoké professionnel, la sonorisation, les micros sans fil et des milliers de titres livrés chez vous, dans votre entreprise ou votre salle. 3 à 4 heures de show, partout sur l'île, pour <b style="color:var(--jaune)">470 € HT tout compris</b>.</p>
<div class="cta"><a class="btn rose" href="#devis">Réserver ma date</a><a class="btn ghost" href="tel:{TELH}">📞 {TEL}</a><span class="note">Devis en 24 h <span class="eq" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></span></span></div>
<div class="lyrics" aria-hidden="true"><span class="tag">♪ En cours</span><span class="txt">Ce soir on chante tous ensemble, du séga à la variété, et personne ne reste assis</span></div>
</div></section>

<div class="mq" aria-hidden="true"><div class="t"><span>Soirée d'entreprise</span>★<span>Anniversaire</span>★<span>Mariage</span>★<span>Association et mairie</span>★<span>Bar et restaurant</span>★<span>Arbre de Noël</span>★<span>Partout à La Réunion</span>★<span>Soirée d'entreprise</span>★<span>Anniversaire</span>★<span>Mariage</span>★<span>Association et mairie</span>★<span>Bar et restaurant</span>★<span>Arbre de Noël</span>★<span>Partout à La Réunion</span>★</div></div>

<section id="formule"><div class="wrap">
<span class="sur">La formule</span><h2>Une soirée karaoké complète, un seul prix</h2>
<p class="lead">Pas de location de matériel d'un côté et d'animateur de l'autre : Karaoké 974 livre une prestation complète, montée et démontée par nos soins. Vous invitez, nous faisons chanter.</p>
<div class="formule reveal"><div>
<h3>Ce qui est compris</h3>
<ul><li><b>Un animateur karaoké</b> qui lance les titres, présente les chanteurs, gère les enchaînements et relance la salle quand elle hésite.</li><li><b>La sonorisation</b> dimensionnée pour votre salle, de 20 à 150 personnes.</li><li><b>Les micros sans fil</b> pour chanter en solo, en duo ou à toute la table.</li><li><b>Le catalogue de titres</b> : variété française, séga et maloya, tubes internationaux, années 80, Disney, zouk.</li><li><b>L'affichage des paroles</b> sur écran ou vidéoprojecteur selon le lieu.</li><li><b>Les jeux de lumière</b> d'ambiance, l'installation avant les invités et le démontage après.</li></ul>
<p style="color:var(--gris);font-size:15px">Options sur devis : deuxième animateur, écran géant, DJ pour la suite de la soirée, photobooth, hôtesses d'accueil, prolongation.</p>
</div>
<div class="prix"><div class="n">470 €<small style="font-size:.38em;color:var(--gris)"> HT</small></div><div class="u">tout compris · 3 à 4 heures</div><p><b>Soit 509,95 € TTC</b> (TVA 8,5 %). Animateur, sono, micros, titres, installation. Entreprises et collectivités : devis et facture, règlement après prestation pour les mairies.</p><a class="btn rose" href="#devis" style="margin-top:14px">Demander mon devis</a></div></div>
</div></section>

<section id="formats" style="background:var(--encre)"><div class="wrap">
<span class="sur">Pour qui</span><h2>Six occasions de sortir les micros</h2>
<p class="lead">Le karaoké est l'animation qui met tout le monde au même niveau : le directeur et le stagiaire, la grand-mère et le petit-fils, le timide et la star du bureau. Voici les six formats que nous organisons le plus souvent à La Réunion.</p>
<div class="grid">{formats}</div>
</div></section>

<section id="deroule"><div class="wrap">
<span class="sur">Comment ça se passe</span><h2>De votre appel à la dernière chanson</h2>
<div class="etapes">
<div class="etape reveal"><b>1</b><h3>Vous nous appelez</h3><p>Date, lieu, nombre d'invités, type de public. Nous vérifions la disponibilité et vous envoyons le devis sous 24 h.</p></div>
<div class="etape reveal"><b>2</b><h3>On prépare la playlist</h3><p>Vous nous donnez vos incontournables et les chansons à éviter. Nous préparons le catalogue, les transitions et la surprise éventuelle (chanson pour le héros de la soirée).</p></div>
<div class="etape reveal"><b>3</b><h3>On installe avant les invités</h3><p>L'animateur arrive en avance, monte la sono, règle les micros et l'écran, teste le son dans la salle. Vous n'avez rien à brancher.</p></div>
<div class="etape reveal"><b>4</b><h3>Tout le monde chante</h3><p>3 à 4 heures d'animation : échauffement en groupe, solos, duos, battles de tables, final en chœur. Puis démontage et salle rendue propre.</p></div>
</div></div></section>

<section id="galerie" style="background:var(--encre)"><div class="wrap">
<span class="sur">En images</span><h2>L'ambiance d'une soirée karaoké</h2>
<p class="lead">Micros, écrans, lumières et public : ce que vous retrouverez chez vous. Les photos de nos propres soirées réunionnaises arrivent au fil des prestations.</p>
<div class="gal">{gal}</div>
</div></section>

{clients_block()}

<section id="repertoire"><div class="wrap">
<span class="sur">Le répertoire</span><h2>Des milliers de titres, du séga à la pop</h2>
<p class="lead">À La Réunion, un karaoké sans séga ni maloya n'est pas un karaoké. Notre catalogue mélange les classiques péi, la variété française que tout le monde connaît par cœur et les tubes internationaux qui font lever les tables.</p>
<div class="repert reveal">{repert}</div>
<p style="margin-top:18px;color:var(--gris)">Une chanson précise vous tient à cœur ? Dites-le au devis : nous vérifions qu'elle figure au catalogue avant la soirée.</p>
</div></section>

{avis_block(pre)}

<section id="zones" style="background:var(--encre)"><div class="wrap">
<span class="sur">Partout sur l'île</span><h2>Karaoké à domicile ou en salle, du Nord au Sud</h2>
<p class="lead">Nous sommes basés au Tampon et nous nous déplaçons dans toutes les communes de La Réunion. Chaque page détaille les lieux habituels du secteur et les contraintes locales (bruit, voisinage, accès).</p>
<div class="zones">{zones}</div>
</div></section>

<section id="pourquoi"><div class="wrap prose">
<span class="sur">Pourquoi ça marche</span><h2>Le karaoké, l'animation la plus rentable d'une soirée</h2>
<p>Un spectacle se regarde. Un DJ se danse. Un karaoké se vit : chaque invité devient acteur de la soirée, et c'est pour cela que les souvenirs durent. En entreprise, c'est l'animation qui fait parler les collègues le lundi matin. En famille, c'est celle qui fait monter sur scène la tante qui « ne chante jamais ». Dans un bar, c'est celle qui remplit la salle un soir de semaine.</p>
<p>La différence entre un karaoké qui prend et un karaoké qui s'éteint au bout de vingt minutes tient à une personne : l'animateur. Il connaît la salle, repère les volontaires, trouve le duo qui va lancer la soirée, ménage les timides et sait quand enchaîner un titre que tout le monde connaît pour relancer l'énergie. C'est le cœur de notre formule, avant même le matériel.</p>
<p>Avec Pull Up Événements, vous ajoutez à cela ce qu'une agence apporte : un devis clair, une facture, une solution de remplacement en cas d'imprévu, et la possibilité de compléter la soirée avec un DJ, des hôtesses, un photobooth ou un traiteur. Plus de 500 événements réalisés sur l'île depuis 2017, et une note de {NOTE}/5 sur Google.</p>
<div class="encart"><b>Bon à savoir.</b> La formule à 470 € couvre la grande majorité des soirées privées et des événements d'entreprise jusqu'à 150 personnes. Au-delà, ou pour une scène avec écran géant, nous chiffrons une configuration renforcée.</div>
</div></section>

<section id="faq" style="background:var(--encre)"><div class="wrap">
<span class="sur">Questions fréquentes</span><h2>Tout ce qu'on nous demande avant de réserver</h2>
<div class="faq" style="max-width:860px">{faq}</div>
</div></section>

{devis_block(pre)}
{eco_block(pre)}
'''
    ld_service = {"@context":"https://schema.org","@type":"Service","name":"Animation karaoké à La Réunion","serviceType":"Soirée karaoké clé en main : animateur, sonorisation, micros, catalogue de titres","provider":{"@id":DOM+"/#organization"},"areaServed":{"@type":"Place","name":"La Réunion (974)"},"url":DOM+"/","image":DOM+"/images/hero-karaoke-neon-reunion-974.jpg","aggregateRating":{"@type":"AggregateRating","ratingValue":"4.9","reviewCount":NB},"offers":{"@type":"Offer","name":"Formule karaoké complète 3 à 4 heures","price":"470","priceCurrency":"EUR","priceSpecification":{"@type":"UnitPriceSpecification","price":"470","priceCurrency":"EUR","valueAddedTaxIncluded":False},"availability":"https://schema.org/InStock","url":DOM+"/#formule"},"hasOfferCatalog":{"@type":"OfferCatalog","name":"Formats de soirée karaoké","itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","name":t,"url":DOM+"/"+s+"/"}} for s,_,t,_ in FORMATS]}}
    ld_faq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]}
    ld_howto = {"@context":"https://schema.org","@type":"HowTo","name":"Comment organiser une soirée karaoké à La Réunion","totalTime":"PT4H","step":[{"@type":"HowToStep","name":"Demander un devis","text":"Appelez le 06 93 49 19 02 ou remplissez le formulaire : date, lieu, nombre d'invités. Devis sous 24 h."},{"@type":"HowToStep","name":"Préparer la playlist","text":"Transmettez vos chansons incontournables et celles à éviter ; l'animateur prépare le catalogue et les transitions."},{"@type":"HowToStep","name":"Installation","text":"L'animateur arrive avant les invités, installe la sonorisation, les micros et l'écran, et teste le son."},{"@type":"HowToStep","name":"La soirée","text":"3 à 4 heures d'animation karaoké, puis démontage du matériel."}]}
    page('', 'Karaoké à La Réunion (974) : animateur + sono, 470 € HT tout compris | Pull Up', 'Soirée karaoké clé en main à La Réunion : animateur professionnel, sono, micros sans fil, milliers de titres. 3 à 4 h pour 470 € HT tout compris. Entreprise, anniversaire, mariage. 4,9/5 sur Google.', body, pre, jsonld=[ORG_JSON, ld_service, ld_faq, ld_howto], preload='hero-karaoke-neon-reunion-974.jpg')

# ───────────────────────── PAGES INTÉRIEURES ─────────────────────────
def interieure(slug, h1, titre, desc, intro, sections, img, type_default='Soirée d\'entreprise', fil='Formats', extra_ld=None):
    pre='../'
    secs = ''.join(f'<h2>{h}</h2>{c}' for h,c in sections)
    body = f'''
<section class="hero-int"><div class="bg">{IMG(img,h1,pre,lazy=False)}</div><div class="wrap in"><p class="fil"><a href="{pre}./">Karaoké 974</a> › {fil}</p><span class="badge">★ {NOTE}/5 sur Google · {NB} avis</span><h1>{h1}</h1><p class="lead">{intro}</p><div class="cta" style="display:flex;gap:12px;flex-wrap:wrap;margin-top:18px"><a class="btn rose" href="#devis">Devis en 24 h</a><a class="btn ghost" href="tel:{TELH}">📞 {TEL}</a></div></div></section>
<section><div class="wrap prose">{secs}
<div class="cta-fin"><h2>470 € HT tout compris, 3 à 4 heures</h2><p>Soit 509,95 € TTC. Animateur, sono, micros, titres, installation et démontage. Partout à La Réunion.</p><a class="btn jaune" href="#devis">Réserver ma date</a></div>
</div></section>
{avis_block(pre)}
{devis_block(pre, type_default)}
{eco_block(pre)}'''
    ld = [ {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Karaoké 974","item":DOM+"/"},{"@type":"ListItem","position":2,"name":h1,"item":DOM+"/"+slug+"/"}]},
           {"@context":"https://schema.org","@type":"Service","name":h1,"provider":{"@id":DOM+"/#organization"},"areaServed":"La Réunion","url":DOM+"/"+slug+"/","offers":{"@type":"Offer","price":"470","priceCurrency":"EUR"}} ]
    if extra_ld: ld.append(extra_ld)
    page(slug, titre, desc, body, pre, og_img=img, jsonld=ld, preload=img)

def P(*ps): return ''.join(f'<p>{p}</p>' for p in ps)
def UL(*ls): return '<ul>'+''.join(f'<li>{l}</li>' for l in ls)+'</ul>'

def pages_formats():
    interieure('karaoke-entreprise-reunion','Karaoké d\'entreprise à La Réunion','Karaoké d\'entreprise à La Réunion : pot de départ, fin d\'année, séminaire | Karaoké 974','Soirée karaoké pour entreprise et CSE à La Réunion : animateur pro, sono, micros, 3 à 4 h pour 470 € HT tout compris. Devis et facture en 24 h. Pull Up Événements, 4,9/5.',
      'Pot de départ, fête de fin d\'année, afterwork, soirée de séminaire ou arbre de Noël : le karaoké est l\'animation d\'entreprise qui fait tomber les étiquettes en trois chansons. Formule complète, devis et facture, interlocuteur unique.',
      [('Pourquoi le karaoké fonctionne si bien en entreprise',P('Dans une soirée d\'entreprise, le piège classique est la salle coupée en deux : la direction d\'un côté, les équipes de l\'autre, et un DJ qui joue devant une piste vide jusqu\'à 23 h. Le karaoké règle le problème parce qu\'il ne demande aucune compétence : on ne chante pas bien, on chante ensemble. Le premier duo improbable (le responsable comptable et l\'alternante sur un tube des années 80) déclenche le reste de la soirée.','C\'est aussi une animation qui se maîtrise dans le temps : 3 à 4 heures, un début et une fin, ce qui convient aux soirées en semaine où tout le monde travaille le lendemain. Et elle s\'adapte à tous les lieux : salle de réunion transformée pour l\'occasion, restaurant privatisé, domaine, ou vos propres locaux.')),
       ('Les occasions que nous animons le plus',UL('<b>Fête de fin d\'année et soirée du personnel</b> : le karaoké en plat principal ou en première partie du DJ.','<b>Pot de départ et départ à la retraite</b> : une chanson surprise préparée par les collègues pour le partant, nous la mettons en scène.','<b>Soirée de séminaire</b> : après une journée de travail, une animation qui défoule sans discours.','<b>Afterwork et anniversaire d\'entreprise</b> : format court, deux heures, dans vos locaux ou un bar partenaire.','<b>Arbre de Noël</b> : karaoké familial avec titres pour enfants, en complément du Père Noël et des animations de <a href="https://arbredenoel974.re/">Arbre de Noël 974</a>.','<b>Team building</b> : battle de karaoké par équipes, avec jury et trophée, en clôture d\'une journée de cohésion <a href="https://teambuilding974.re/">Team Building 974</a>.')),
       ('Ce que comprend la formule entreprise',P('La formule à 470 € HT tout compris couvre l\'animateur, la sonorisation, les micros sans fil, le catalogue de titres, l\'affichage des paroles et les jeux de lumière, pour 3 à 4 heures d\'animation. Vous recevez un devis sous 24 h et une facture après la prestation. Pour les événements de plus de 150 personnes, une scène ou un écran géant, nous chiffrons une configuration renforcée.','Les options les plus demandées : un DJ pour prolonger la soirée en dancefloor, des hôtesses à l\'accueil (<a href="https://hotesse-reunion.re/">Hôtesse Réunion</a>), un photobooth, une captation vidéo pour vos réseaux internes (<a href="https://productionvideo974.re/">Production Vidéo 974</a>).')),
       ('Comment se déroule une soirée karaoké d\'entreprise',P('L\'animateur arrive une heure avant pour installer et tester le son. La soirée s\'ouvre par un échauffement collectif sur un titre que tout le monde connaît, puis alterne solos volontaires, duos tirés au sort, battles de services et chansons dédiées. Le final réunit toute la salle sur un hymne. Nous adaptons le niveau sonore aux lieux et aux horaires, et nous gérons les enchaînements pour que personne n\'attende trop longtemps son tour.'),),
       ('Idées de formats pour aller plus loin',UL('<b>La battle des services</b> : chaque équipe prépare un titre, un jury de direction note la prestation, la mise en scène et l\'ambiance.','<b>Le blind test karaoké</b> : on devine la chanson, on la chante ensuite. Lisez aussi notre comparatif <a href="https://soiree974.re/blog/karaoke-blind-test-soiree-entreprise-reunion/">karaoké ou blind test pour une soirée d\'entreprise</a>.','<b>Le karaoké des managers</b> : la direction ouvre la soirée, et tout le monde suit.')),
      ],'micro-sans-fil-soiree-entreprise-karaoke-974.jpg','Soirée d\'entreprise')
    interieure('karaoke-anniversaire-reunion','Karaoké d\'anniversaire à domicile à La Réunion','Karaoké anniversaire à domicile à La Réunion : animateur + sono 470 € | Karaoké 974','Animez un anniversaire à La Réunion avec un karaoké à domicile : animateur, sono, micros sans fil et milliers de titres pour 470 € HT tout compris. 30, 40, 50 ans, surprise. Devis en 24 h.',
      '30, 40, 50 ans, anniversaire surprise ou anniversaire d\'enfant : nous installons le karaoké dans votre salon, votre varangue, votre kiosque ou la salle que vous avez louée. L\'animateur s\'occupe de tout, vous profitez de vos invités.',
      [('Un anniversaire dont on parle encore l\'année suivante',P('Un repas d\'anniversaire se ressemble souvent d\'une année à l\'autre. Un karaoké à domicile le transforme : les cousins font un duo, les parents ressortent un tube de leur jeunesse, les enfants chantent un dessin animé, et la personne fêtée reçoit « sa » chanson préparée en secret par ses proches. C\'est l\'animation qui mélange les générations sans que personne ne se sente mis en scène.','À La Réunion, la varangue ou le kiosque sont des scènes parfaites : nous installons la sonorisation et l\'écran à l\'abri, et les invités chantent depuis la table grâce aux micros sans fil.')),
       ('Ce qui est compris pour un anniversaire',UL('Un animateur karaoké qui anime, présente et fait monter les volontaires.','La sonorisation adaptée à une maison ou une petite salle, réglée pour respecter le voisinage.','Deux micros sans fil au minimum, pour les duos.','Un catalogue de milliers de titres : séga, variété française, années 80 et 90, Disney, tubes du moment.','L\'affichage des paroles sur écran ou vidéoprojecteur, les lumières d\'ambiance.','Installation avant l\'arrivée des invités et démontage en fin de soirée.')),
       ('Les formats d\'anniversaire que nous animons',UL('<b>Anniversaire surprise</b> : l\'animateur arrive après l\'arrivée de la personne fêtée, le matériel est prêt, la première chanson lui est dédiée.','<b>Anniversaire des 40 ou 50 ans</b> : playlist calée sur les années de jeunesse du héros de la soirée.','<b>Anniversaire d\'enfant ou d\'ado</b> : titres adaptés, animateur habitué aux jeunes publics. Pour une fête complète avec jeux et ateliers, voyez <a href="https://animationenfant974.re/">Animation Enfant 974</a>.','<b>Anniversaire en salle louée</b> : nous nous adaptons à la salle polyvalente, au restaurant ou au gîte.')),
       ('Conseils pratiques',P('Prévoyez une prise électrique à proximité et un mur ou un espace libre pour l\'écran. Prévenez les voisins pour une soirée en extérieur, nous réglons le volume en conséquence. Transmettez-nous trois ou quatre chansons incontournables pour la personne fêtée : nous les gardons pour les moments forts. La formule standard dure 3 à 4 heures : commencez le karaoké après le plat principal, pas après le dessert, pour laisser le temps à tout le monde de passer.'),),
      ],'micro-vintage-lumieres-soiree-karaoke-reunion.jpg','Anniversaire')
    interieure('karaoke-mariage-reunion','Karaoké de mariage à La Réunion','Karaoké mariage à La Réunion : animation familiale avec animateur et sono | Karaoké 974','Animation karaoké pour mariage à La Réunion : animateur, sono, micros sans fil, séga et variété. En relais du DJ ou pour le lendemain de mariage. 470 € HT tout compris, devis en 24 h.',
      'Le soir du mariage en relais du DJ, ou le lendemain pour le brunch des familles : une heure ou une soirée de karaoké réunit les deux familles autour du micro, des témoins aux grands-parents.',
      [('Le karaoké, l\'animation qui réunit les deux familles',P('Un mariage, c\'est deux familles qui se découvrent. Les discours les présentent, le repas les assoit côte à côte, le karaoké les fait chanter ensemble. Le duo des deux pères sur un séga, les témoins qui reprennent la chanson des mariés, les cousines sur un tube des années 2000 : ce sont les séquences que l\'on retrouve dans toutes les vidéos de mariage réussies.','À La Réunion, le karaoké trouve naturellement sa place le soir après le gâteau, en alternance avec le DJ, ou le lendemain midi au repas de famille, quand l\'ambiance est détendue et que l\'on a le temps.')),
       ('Trois façons d\'intégrer le karaoké à votre mariage',UL('<b>En ouverture de soirée</b> : une heure de karaoké après le repas pour lancer la piste, puis le DJ prend le relais.','<b>En soirée complète</b> : 3 à 4 heures de karaoké animé, l\'animateur enchaîne les titres dansants entre les passages pour garder la piste vivante.','<b>Le lendemain</b> : brunch ou déjeuner des familles, format décontracté, titres péi et classiques que tout le monde connaît.')),
       ('Ce que nous apportons',P('L\'animateur, la sonorisation, les micros sans fil, le catalogue, l\'affichage des paroles et les lumières d\'ambiance, pour 470 € HT tout compris sur la formule standard. Nous coordonnons avec votre DJ, votre traiteur et votre lieu pour les horaires et l\'installation. Pour un mariage avec hôtesses d\'accueil, photobooth ou captation vidéo, Pull Up Événements réunit tout sur un seul devis.'),),
       ('Les titres qui marchent à tous les coups',P('La chanson des mariés en duo (ou en solo surprise de l\'un des deux), un séga que toute la salle connaît, un tube français des années 80 pour les parents, un titre de dessin animé pour faire monter les enfants, et un hymne de fin de soirée repris par tout le monde. Transmettez-nous votre liste : nous préparons les enchaînements et nous gardons les surprises secrètes.'),),
      ],'micro-retro-ambiance-doree-karaoke-974.jpg','Mariage')
    interieure('karaoke-association-mairie-reunion','Karaoké pour associations et mairies à La Réunion','Karaoké pour association, mairie et CCAS à La Réunion : animateur + sono | Karaoké 974','Soirée karaoké pour associations, mairies, CCAS et comités des fêtes à La Réunion : animateur, sono, micros, 470 € HT tout compris, sans acompte pour les collectivités. Devis en 24 h.',
      'Fête de quartier, loto, kermesse, soirée du club, semaine bleue, fête de fin de saison : une formule simple à budgéter, un devis en 24 h, et pour les collectivités une facture après la prestation, sans acompte.',
      [('Une animation accessible à tous les publics',P('Le karaoké est l\'animation idéale pour une collectivité ou une association parce qu\'il s\'adresse à tout le monde sans distinction d\'âge ni de moyens : les gramounes chantent les ségas d\'autrefois, les parents la variété, les enfants les dessins animés. Il ne demande pas de piste de danse ni de scène, il fonctionne en salle polyvalente, sous un chapiteau ou dans un kiosque.','Notre animateur a l\'habitude des publics intergénérationnels : il adapte le rythme, propose des chansons que la salle connaît et ménage les volontaires les plus timides.')),
       ('Les événements que nous animons',UL('<b>Fêtes de quartier et fêtes communales</b> : karaoké en soirée après le repas partagé.','<b>Soirées d\'associations</b> : club sportif, association de parents d\'élèves, comité des fêtes, fin de saison.','<b>Semaine bleue, repas des aînés, CCAS</b> : répertoire ciblé, volume adapté, animateur attentif.','<b>Kermesses et lotos</b> : karaoké en animation d\'attente ou en clôture.','<b>Centres de loisirs et maisons de quartier</b> : karaoké pour enfants et ados en journée.')),
       ('Budget et modalités pour les collectivités',P('La formule complète est à 470 € HT tout compris pour 3 à 4 heures : animateur, sonorisation, micros, catalogue, écran, installation et démontage. Les mairies, CCAS et établissements publics ne versent pas d\'acompte : la facture est émise après la prestation, payable à 30 jours. Les associations reçoivent un devis détaillé utilisable pour une demande de subvention. Nous pouvons fournir une attestation d\'assurance et les documents administratifs habituels.'),),
       ('Pull Up Événements et les collectivités',P('Pull Up Événements travaille régulièrement avec des mairies, des CCAS, des CIAS et des institutions de l\'île pour des journées de cohésion, des arbres de Noël et des animations publiques. Le karaoké vient compléter cette offre avec une formule légère, facile à installer dans les salles communales et à insérer dans un programme de fête.'),),
      ],'public-mains-levees-soiree-karaoke-entreprise-974.jpg','Association / mairie')

def pages_zones():
    details = {
     'Nord':[('Où chante-t-on dans le Nord ?',P('Saint-Denis concentre les sièges d\'entreprise, les administrations et les bars qui programment des soirées karaoké : le Barachois, le centre-ville, le Chaudron, Sainte-Clotilde et la zone de la Technopole côté entreprises. À Sainte-Marie, la zone de Duparc et les salles polyvalentes accueillent fêtes de famille et soirées d\'entreprise. Sainte-Suzanne et La Montagne complètent le secteur avec des gîtes et des salles de réception.','Nous intervenons dans les locaux d\'entreprise, les salles louées, les restaurants privatisés et à domicile. Les immeubles du centre-ville imposent de surveiller le volume et l\'heure de fin : la sonorisation est réglée en conséquence.')),
             ('Idées pour le Nord',UL('Afterwork karaoké dans vos locaux de Sainte-Clotilde ou de la Technopole, format deux heures.','Soirée karaoké mensuelle dans un bar du Barachois ou de la rue Pasteur.','Anniversaire en villa à La Montagne ou au Brûlé, varangue et vue sur la ville.','Fête de fin d\'année d\'un CSE de Saint-Denis dans une salle de Sainte-Marie, avec DJ en relais.'))],
     'Sud':[('Notre terrain de jeu',P('Pull Up Événements est installé au Tampon : le Sud est notre base. Saint-Pierre (Terre Sainte, la Ravine Blanche, le centre-ville et ses bars), Le Tampon et ses Hauts, Saint-Louis, Saint-Joseph, L\'Étang-Salé et Petite-Île sont à moins de 30 minutes de notre dépôt, ce qui simplifie l\'installation et les horaires.','Le Sud compte déjà des lieux de karaoké en salles privées à Saint-Pierre. Notre offre est différente : nous venons chez vous, dans votre entreprise, votre salle ou votre jardin, avec un animateur et le matériel, pour votre groupe uniquement.')),
            ('Idées pour le Sud',UL('Soirée d\'entreprise dans un domaine de Saint-Pierre ou de L\'Étang-Salé avec karaoké puis DJ.','Anniversaire sous le kiosque, à la Plaine des Cafres ou dans les Hauts du Tampon.','Fête de quartier ou soirée d\'association à Saint-Louis, Saint-Joseph ou Petite-Île.','Karaoké pour un restaurant de Terre Sainte un jeudi soir, formule ponctuelle ou mensuelle.'))],
     'Ouest':[('La côte où l\'on fête le plus',P('Saint-Gilles et La Saline concentrent les villas de location et les lieux de réception ; Saint-Paul et Le Port accueillent les entreprises de Cambaie et de la zone portuaire ; La Possession et Saint-Leu complètent le secteur avec des salles communales et des gîtes dans les Hauts. L\'Ouest est le secteur où nous animons le plus de soirées privées.','En villa, nous installons sous la varangue ou au bord de la piscine, à l\'abri. En entreprise, dans une salle de réunion ou un entrepôt aménagé. Dans les bars de Saint-Gilles, en soirée à thème.')),
              ('Idées pour l\'Ouest',UL('Week-end d\'entreprise en villa à Saint-Gilles avec soirée karaoké le samedi.','Mariage à Saint-Leu ou à La Saline : une heure de karaoké après le gâteau, puis le DJ.','Soirée du personnel d\'une entreprise du Port ou de Cambaie dans une salle de Saint-Paul.','Anniversaire à La Possession ou dans les Hauts de Saint-Paul.'))],
     'Est':[('L\'Est aime chanter',P('Saint-André et Saint-Benoît sont les deux pôles de l\'Est : salles polyvalentes, associations actives, fêtes de famille nombreuses. Bras-Panon, Sainte-Rose, Salazie et La Plaine-des-Palmistes ajoutent des gîtes et des salles communales où les mariages et les fêtes de quartier se tiennent toute l\'année.','Le répertoire péi prend ici toute sa place : séga, maloya, variété créole, et les grands classiques français que trois générations reprennent ensemble. L\'animateur adapte la playlist au public de l\'Est.')),
            ('Idées pour l\'Est',UL('Mariage à Saint-André ou Bras-Panon : karaoké familial le lendemain au repas des familles.','Soirée d\'association ou de club à Saint-Benoît.','Séminaire au vert à Salazie ou à La Plaine-des-Palmistes avec karaoké en soirée.','Fête communale ou kermesse à Sainte-Rose ou Sainte-Anne.'))],
    }
    imgs={'Nord':'bar-neon-karaoke-prive-ambiance-974.jpg','Sud':'enseigne-karaoke-neon-soiree-reunion-974.jpg','Ouest':'dancefloor-lumieres-bleues-soiree-karaoke-974.jpg','Est':'micro-karaoke-salle-de-fete-reunion.jpg'}
    for slug,n,communes,d in ZONES:
        ville = communes.split(',')[0]
        secs = details[n] + [('La formule, identique partout sur l\'île',P(f'Animateur karaoké, sonorisation, micros sans fil, catalogue de milliers de titres, affichage des paroles et lumières d\'ambiance : 470 € HT tout compris pour 3 à 4 heures, installation et démontage inclus. Le déplacement dans le secteur {n} est précisé sur le devis. Les entreprises reçoivent une facture, les collectivités règlent après la prestation.'))]
        interieure(slug, f'Karaoké {n} de La Réunion : {ville} et alentours', f'Karaoké à {ville} et dans le {n} de La Réunion : animateur + sono | Karaoké 974', f'Soirée karaoké à domicile ou en salle à {ville} et dans tout le {n} de La Réunion ({communes}) : animateur, sono, micros, 470 € HT tout compris. Devis en 24 h.', f'{communes}. {d}', secs, imgs[n], fil='Secteurs')

# ───────────────────────── BLOG ─────────────────────────
ARTICLES = [
 ('combien-coute-soiree-karaoke-reunion','Combien coûte une soirée karaoké à La Réunion ?','Prix d\'un karaoké à La Réunion en 2026 : location seule, animateur, formule complète. Ce qui est compris, ce qui ne l\'est pas, et comment comparer les devis.',
  [('Trois façons de faire un karaoké, trois budgets',P('La question « combien coûte un karaoké » n\'a pas une réponse mais trois, parce qu\'il existe trois façons de l\'organiser à La Réunion.','<b>La location de matériel seule.</b> Une enceinte, un micro ou deux, parfois un vidéoprojecteur et un ordinateur avec un logiciel de karaoké. On trouve des kits entre 30 et 100 € la journée. C\'est la solution la moins chère, mais c\'est vous qui installez, qui réglez le son, qui gérez la file des chanteurs et qui rangez à deux heures du matin. Dans les faits, l\'organisateur passe sa soirée derrière l\'ordinateur.','<b>L\'animateur indépendant.</b> Il vient avec son matériel et anime. À La Réunion, les prestations annoncées démarrent autour de 300 € et montent jusqu\'à 700 € selon la durée, le matériel et la notoriété. La qualité varie beaucoup d\'une personne à l\'autre, les prix ne sont presque jamais affichés, et en cas d\'empêchement il n\'y a pas de remplaçant.','<b>La formule agence.</b> C\'est notre offre : un animateur dédié, la sonorisation, les micros, le catalogue, l\'écran, l\'installation et le démontage, pour 470 € HT tout compris sur 3 à 4 heures, avec devis, facture et solution de remplacement. Entre les deux premières options et la troisième, la différence de prix paie la tranquillité et la régularité.')),
   ('Ce qui fait varier le prix',UL('<b>La durée</b> : au-delà de 4 heures, comptez un supplément horaire.','<b>La taille de la salle</b> : au-delà de 150 personnes, il faut une sonorisation renforcée et souvent un écran géant.','<b>Le lieu</b> : un domaine à l\'autre bout de l\'île ou un accès difficile peut ajouter un déplacement.','<b>Les options</b> : deuxième animateur, DJ pour la suite, photobooth, hôtesses, captation vidéo.','<b>Le jour</b> : un samedi de décembre se réserve des semaines à l\'avance, pas un mardi de mars.')),
   ('Comment comparer deux devis',P('Vérifiez que l\'animateur est bien compris (et pas seulement « mise à disposition du matériel »), que la durée est précisée, que l\'installation et le démontage sont inclus, que l\'affichage des paroles est prévu, et que vous recevrez une facture. Demandez ce qui se passe si l\'animateur est malade le jour J. Enfin, regardez les avis : une agence qui affiche 144 avis publics à 4,9/5 prend un risque sur chaque prestation, c\'est votre meilleure garantie.'),),
   ('Notre réponse en une ligne',P('À La Réunion, une soirée karaoké complète et animée par un professionnel, avec tout le matériel, coûte 470 € HT tout compris chez Karaoké 974 pour 3 à 4 heures. <a href="../../#devis">Demandez votre devis</a>, vous l\'aurez sous 24 h.'),)],
  'micro-chrome-fond-bleu-karaoke-mariage-reunion.jpg'),
 ('karaoke-ou-dj-soiree-entreprise','Karaoké ou DJ pour une soirée d\'entreprise à La Réunion ?','Karaoké ou DJ : lequel choisir pour une soirée d\'entreprise ? Les points forts de chacun, les publics, les horaires, et la formule qui combine les deux.',
  [('Deux animations, deux façons de vivre la soirée',P('Le DJ fait danser ; le karaoké fait participer. Le DJ est à son meilleur quand la salle est déjà chaude, tard dans la soirée, avec un public qui aime danser. Le karaoké prend dès le début, même avec un public mélangé qui ne se connaît pas, même dans une salle de réunion sans piste de danse, même un mardi soir.','En entreprise, la vraie question est souvent : qui va se lever en premier ? Devant un DJ, personne n\'ose ouvrir la piste. Devant un karaoké, l\'animateur trouve toujours deux volontaires, et les autres suivent.')),
   ('Choisir selon votre soirée',UL('<b>Soirée en semaine, fin à 22 h 30</b> : karaoké. Il démarre vite et a une fin naturelle.','<b>Gala ou grande fête de fin d\'année</b> : DJ, avec une heure de karaoké en ouverture pour lancer la piste.','<b>Petite équipe (moins de 40 personnes)</b> : karaoké. Un DJ devant 30 personnes qui ne dansent pas, c\'est long.','<b>Public très mélangé en âge</b> : karaoké, grâce au répertoire qui traverse les générations.','<b>Soirée dans vos locaux</b> : karaoké, sans besoin de piste ni de grosse installation.')),
   ('La formule qui combine les deux',P('La combinaison la plus efficace : une heure trente de karaoké après le repas, puis le DJ prend le relais quand la salle est lancée. L\'animateur karaoké a fait tomber les barrières, le DJ récupère un public debout. Pull Up Événements propose les deux sur un seul devis : le karaoké à 470 € HT tout compris, le DJ en option. Pour le volet soirée complète, voyez <a href="https://soiree974.re/">Soirée 974</a>.'),),
   ('Et le blind test ?',P('Le blind test est le cousin du karaoké : on devine au lieu de chanter. Il convient aux publics plus réservés et se joue assis, par équipes. Nous le proposons aussi, et la meilleure version enchaîne les deux : on devine la chanson, puis on la chante.'),),
   ('Le budget, concrètement',P('Un karaoké complet avec animateur et matériel coûte 470 € HT tout compris pour 3 à 4 heures. Un DJ professionnel à La Réunion se situe généralement dans une fourchette comparable ou supérieure selon la durée et l\'installation lumière. La formule combinée (karaoké puis DJ) revient donc à peu près au double, pour une soirée qui tient de 20 h à 2 h du matin sans temps mort. Pour une petite équipe, le karaoké seul suffit largement et laisse du budget pour le traiteur.'),),
   ('Notre conseil',P('Si vous hésitez, posez-vous une seule question : est-ce que vos collègues dansent spontanément ? Si la réponse est « pas vraiment », prenez le karaoké. Si la réponse est « oui, dès la deuxième chanson », prenez le DJ et ajoutez une heure de karaoké en ouverture pour ceux qui ne dansent pas. Dans les deux cas, <a href="../../#devis">demandez un devis</a> : nous vous conseillons le format selon votre public et votre salle.'),)],
  'jeux-de-lumiere-sono-karaoke-reunion.jpg'),
 ('chansons-karaoke-pei-incontournables','Les chansons péi qui marchent à tous les coups en karaoké','Séga, maloya, variété créole : les titres réunionnais qui font lever une salle en karaoké, et comment construire une playlist qui parle à toutes les générations.',
  [('Pourquoi commencer par le répertoire péi',P('À La Réunion, un karaoké qui n\'ouvre pas sur un séga perd une partie de la salle dès les premières minutes. Le répertoire péi a une qualité rare : trois générations le connaissent par cœur. Les gramounes chantent les ségas des années 70, les parents ceux des années 90, les jeunes les titres dancehall et séga moderne, et tout le monde reprend les refrains des autres.','Notre animateur construit la soirée en alternant le péi et le reste : un séga, un tube français, un titre international, un duo, un dessin animé pour les enfants, et retour au séga quand l\'énergie baisse.')),
   ('Construire une playlist qui parle à tout le monde',UL('<b>Ouverture</b> : un séga que toute la salle connaît, chanté en groupe, micro tendu vers le public.','<b>Montée</b> : variété française des années 80 et 90, les refrains que personne n\'a oubliés.','<b>Cœur de soirée</b> : solos volontaires, duos tirés au sort, chansons dédiées.','<b>Relance</b> : un maloya ou un séga dansant quand la salle s\'assoit.','<b>Final</b> : un hymne repris debout par tout le monde, puis le DJ ou la fin de soirée.')),
   ('Les erreurs à éviter',P('Laisser le même groupe monopoliser le micro : l\'animateur tourne les volontaires. Enchaîner trois ballades : la salle s\'endort. Oublier les enfants : un titre de dessin animé toutes les heures les garde dans la fête. Mettre le volume trop fort dans une maison : les voisins appellent. Et surtout, choisir les chansons à la place des invités : la bonne playlist est celle que l\'on construit avec vous avant la soirée, puis que l\'animateur ajuste en direct.'),),
   ('Adapter la playlist au public',P('Une soirée d\'entreprise de 35 ans de moyenne d\'âge n\'a pas la même playlist qu\'un repas des aînés ou qu\'un anniversaire de 18 ans. Pour un public d\'entreprise, nous misons sur les refrains fédérateurs des années 80 à 2000 et deux ou trois ségas que tout le monde connaît. Pour une fête de famille, nous élargissons vers le répertoire créole d\'hier et les titres pour enfants. Pour un public jeune, le séga moderne, le dancehall et les tubes du moment prennent le dessus, avec quelques classiques pour les parents présents.','Dans tous les cas, l\'animateur garde une règle simple : jamais plus de deux titres d\'affilée dans le même registre, et toujours un titre connu de toute la salle quand l\'énergie retombe.')),
   ('Dites-nous vos incontournables',P('Avant chaque soirée, nous vous demandons vos cinq chansons indispensables et celles à éviter. Nous vérifions qu\'elles sont au catalogue, nous gardons les surprises secrètes, et nous laissons le reste à l\'ambiance de la salle. <a href="../../#devis">Demandez votre devis</a> et racontez-nous votre soirée.'),)],
  'silhouette-danse-lumieres-karaoke-soiree.jpg'),
]

def blog():
    pre='../../'
    for slug,t,d,secs,img in ARTICLES:
        body_secs=''.join(f'<h2>{h}</h2>{c}' for h,c in secs)
        words=len(re.sub(r'<[^>]+>',' ',body_secs).split())
        body=f'''<section class="hero-int"><div class="bg">{IMG(img,t,pre,lazy=False)}</div><div class="wrap in"><p class="fil"><a href="{pre}./">Karaoké 974</a> › <a href="{pre}blog/">Blog</a></p><h1>{t}</h1><p class="lead">{d}</p><p class="fil">Publié le {TODAY_FR} · {max(2,words//220)} min de lecture</p></div></section>
<article><section><div class="wrap prose">{body_secs}
<div class="auteur"><div class="av">PU</div><div><b>À propos de l'auteur</b><br>Article rédigé par l'équipe de <a href="https://pullup.re/">Pull Up Événements, la grande agence événementielle de La Réunion</a> : plus de 500 événements depuis 2017, {NOTE}/5 sur Google. Karaoké 974 est son service karaoké.</div></div>
<div class="cta-fin"><h2>Une soirée karaoké à organiser ?</h2><p>470 € HT tout compris, animateur et matériel, partout à La Réunion. Devis en 24 h.</p><a class="btn jaune" href="#devis">Demander un devis</a></div></div></section></article>
{devis_block(pre)}{eco_block(pre)}'''
        ld={"@context":"https://schema.org","@type":"BlogPosting","headline":t,"description":d,"image":DOM+"/images/"+img,"datePublished":TODAY.isoformat(),"dateModified":TODAY.isoformat(),"author":{"@type":"Organization","name":"Pull Up Événements","url":"https://pullup.re/"},"publisher":{"@id":DOM+"/#organization"},"mainEntityOfPage":DOM+"/blog/"+slug+"/","wordCount":words}
        page('blog/'+slug, t+' | Karaoké 974', d, body, pre, og_img=img, jsonld=[ld], preload=img)
        print('article',slug,words,'mots')
    # index blog
    pre='../'
    cards=''.join(f'<article class="card pic reveal">{IMG(img,t,pre)}<div class="tx"><h3><a href="{pre}blog/{slug}/" style="color:#fff">{t}</a></h3><p>{d}</p><a class="more" href="{pre}blog/{slug}/">Lire →</a></div></article>' for slug,t,d,_,img in ARTICLES)
    body=f'''<section class="hero-int"><div class="wrap in"><p class="fil"><a href="{pre}./">Karaoké 974</a> › Blog</p><h1>Le blog du <span>karaoké péi</span></h1><p class="lead">Prix, playlists, choix entre karaoké et DJ : nos conseils pour réussir une soirée karaoké à La Réunion.</p></div></section>
<section><div class="wrap"><div class="blog-list">{cards}</div></div></section>{devis_block(pre)}{eco_block(pre)}'''
    page('blog','Blog karaoké La Réunion : conseils, prix, playlists | Karaoké 974','Conseils pour organiser une soirée karaoké à La Réunion : budget, karaoké ou DJ, chansons péi incontournables. Par Pull Up Événements.',body,pre)

# ───────────────────────── LÉGAL, 404, FICHIERS ─────────────────────────
def legal():
    pre='../'
    ml=f'''<section class="hero-int"><div class="wrap in"><p class="fil"><a href="{pre}./">← Retour à Karaoké 974</a></p><h1>Mentions légales</h1></div></section><section><div class="wrap prose">
<p>Le site karaoke974.re est un site de la marque Karaoké 974, éditée par Pull Up Événements.</p>
<h2>Éditeur du site</h2><p>Pull Up Événements<br>SIRET : 918 044 611 00054, immatriculée au RCS de Saint-Pierre (La Réunion)<br>Siège : 6 Impasse des Sœurs Brontë, 97430 Le Tampon, La Réunion<br>Téléphone : <a href="tel:{TELH}">{TEL}</a> · E-mail : <a href="mailto:{MAIL}">{MAIL}</a></p>
<h2>Directeur de la publication</h2><p>Romain Capdepont, fondateur de Pull Up Événements.</p>
<h2>Hébergement</h2><p>Le site est hébergé par GitHub Pages, un service de GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis (pages.github.com).</p>
<h2>Crédits</h2><p>Textes : © Pull Up Événements. Photos d'illustration : Unsplash, sous licence Unsplash (utilisation libre), dans l'attente des photos de nos propres soirées. Toute reproduction des textes sans autorisation écrite est interdite.</p>
<h2>Données personnelles</h2><p>Le détail de la collecte et de vos droits figure dans notre <a href="{pre}confidentialite/">politique de confidentialité</a>.</p></div></section>'''
    page('mentions-legales','Mentions légales | Karaoké 974','Mentions légales du site karaoke974.re, édité par Pull Up Événements.',ml,pre,noindex=True)
    cf=f'''<section class="hero-int"><div class="wrap in"><p class="fil"><a href="{pre}./">← Retour à Karaoké 974</a></p><h1>Politique de confidentialité</h1></div></section><section><div class="wrap prose">
<p>Cette page explique simplement ce que deviennent les informations que vous nous confiez sur karaoke974.re.</p>
<h2>Quelles données collectons-nous ?</h2><p>Uniquement ce que vous saisissez dans le formulaire de demande de devis : votre identité et vos coordonnées (nom ou société, téléphone, e-mail) et les précisions que vous donnez sur votre projet (date, lieu, nombre d'invités, message).</p>
<h2>Pour quoi faire ?</h2><p>Pour une seule chose : vous répondre et établir votre devis. L'envoi du formulaire nécessite votre accord explicite (case à cocher).</p>
<h2>Combien de temps ?</h2><p>3 ans maximum après notre dernier échange, puis vos données sont supprimées.</p>
<h2>Qui y a accès ?</h2><p>Pull Up Événements uniquement. Vos données ne sont jamais vendues ni transmises à des tiers à des fins commerciales.</p>
<h2>Nos sous-traitants techniques</h2><ul><li><b>Acheminement du formulaire</b> : votre demande nous parvient par notre relais installé sur pullup.re et, en secours, par le service Web3Forms, qui transmet le message à notre boîte contact@pullup.re.</li><li><b>Mesure d'audience</b> : Google Analytics, uniquement si vous cliquez sur « Accepter » dans le bandeau cookies. Sinon, aucun cookie de mesure n'est posé. Votre choix est retenu 6 mois.</li><li><b>Hébergement</b> : GitHub Pages (GitHub, Inc., États-Unis).</li></ul>
<h2>Vos droits</h2><p>Vous pouvez à tout moment demander l'accès, la rectification ou la suppression de vos données : écrivez à <a href="mailto:{MAIL}">{MAIL}</a> ou appelez le <a href="tel:{TELH}">{TEL}</a>. Nous répondons sous 30 jours. Vous pouvez aussi déposer une réclamation auprès de la CNIL (www.cnil.fr).</p>
<h2>Responsable du traitement</h2><p>Pull Up Événements, 6 Impasse des Sœurs Brontë, 97430 Le Tampon, La Réunion (SIRET 918 044 611 00054, RCS Saint-Pierre). Voir aussi les <a href="{pre}mentions-legales/">mentions légales</a>.</p></div></section>'''
    page('confidentialite','Politique de confidentialité | Karaoké 974','Politique de confidentialité du site karaoke974.re (Pull Up Événements).',cf,pre,noindex=True)

def fichiers(urls):
    # 404
    open(os.path.join(OUT,'404.html'),'w',encoding='utf-8').write(f'''<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Page introuvable : Karaoké 974</title><meta name="robots" content="noindex">{HEAD_FONTS}<style>body{{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;text-align:center;background:#070b1c;color:#f7f5ff;font-family:"Outfit",sans-serif;padding:24px}}h1{{font-family:"Righteous",cursive;font-size:clamp(70px,18vw,160px);color:#ff2e88;margin:0;text-shadow:0 0 30px rgba(255,46,136,.6)}}p{{color:#aab1d2;max-width:420px;margin:10px auto 26px}}a{{display:inline-block;background:#ffe347;color:#070b1c;font-weight:800;padding:14px 28px;border-radius:40px;text-decoration:none}}</style></head><body><div><h1>404</h1><p>Cette page a raté son entrée. Le micro, lui, vous attend sur la page d'accueil.</p><a href="/">Retour à Karaoké 974</a></div></body></html>''')
    # favicon
    open(os.path.join(OUT,'favicon.svg'),'w',encoding='utf-8').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff2e88"/><stop offset="1" stop-color="#7c5cff"/></linearGradient></defs><circle cx="50" cy="50" r="48" fill="url(#g)"/><text x="50" y="68" font-size="54" text-anchor="middle">🎤</text></svg>')
    # robots
    open(os.path.join(OUT,'robots.txt'),'w').write(f'''User-agent: *
Allow: /

# Assistants IA, recherche en direct
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: Claude-User
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Perplexity-User
Allow: /
User-agent: DuckAssistBot
Allow: /
User-agent: Applebot
Allow: /
User-agent: Bingbot
Allow: /

# Assistants IA, memoire et entrainement (volontairement autorises)
User-agent: GPTBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Applebot-Extended
Allow: /
User-agent: meta-externalagent
Allow: /
User-agent: CCBot
Allow: /

Sitemap: {DOM}/sitemap.xml
# Presentation pour les IA : {DOM}/llms.txt
''')
    # sitemap
    sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{u}</loc><lastmod>{TODAY.isoformat()}</lastmod></url>\n' for u in urls)+'</urlset>\n'
    open(os.path.join(OUT,'sitemap.xml'),'w').write(sm)
    # llms.txt
    formats='\n'.join(f'- {DOM}/{s}/ : {t}' for s,_,t,_ in FORMATS[:4])
    zones='\n'.join(f'- {DOM}/{z}/ : karaoké dans le {n} ({c})' for z,n,c,_ in ZONES)
    arts='\n'.join(f'- {DOM}/blog/{s}/ : {t}' for s,t,_,_,_ in ARTICLES)
    faq='\n'.join(f'**{q}**\n{a}\n' for q,a in FAQ[:6])
    open(os.path.join(OUT,'llms.txt'),'w',encoding='utf-8').write(f'''# Karaoké 974 — karaoke974.re

Karaoké 974 (karaoke974.re) est le service karaoké de Pull Up Événements.

Pull Up Événements est une agence événementielle de La Réunion : marque créée en 2017, société depuis 2022, dirigée par son fondateur Romain Capdepont. Siège au Tampon (6 Impasse des Sœurs Brontë, 97430 Le Tampon), interventions sur toute l'île. Plus de 500 événements réalisés, note de 4,9/5 sur Google fondée sur {NB} avis publics.

Ce site est dédié aux soirées karaoké clé en main : un animateur karaoké professionnel, la sonorisation, les micros sans fil, un catalogue de milliers de titres (séga, maloya, variété française, tubes internationaux, années 80, titres pour enfants), l'affichage des paroles, les lumières d'ambiance, l'installation et le démontage. Formule standard : 3 à 4 heures pour 470 € HT tout compris. Entreprises : devis et facture. Collectivités : facture après prestation, sans acompte. Options : deuxième animateur, écran géant, DJ, photobooth, hôtesses.

## Écosystème Pull Up Événements
- https://pullup.re : site vitrine de l'agence (réalisations, blog, tarifs, pages villes).
- https://teambuilding974.re : team building et journées de cohésion.
- https://seminaire974.re : séminaire résidentiel, incentive, DMC.
- https://soiree974.re : soirées d'entreprise, soirée du personnel, gala.
- https://arbredenoel974.re : arbres de Noël d'entreprise, CSE et mairies.
- https://animationenfant974.re : animation enfants, kids club, anniversaires.
- https://hotesse-reunion.re : hôtesses d'accueil événementiel.
- https://productionvideo974.re : production vidéo et aftermovie.
- https://karaoke974.re (ce site) : soirées karaoké avec animateur et matériel.

Contact : {TEL}, {MAIL}. Devis gratuit sous 24 h.

## Formats
{formats}

## Secteurs
{zones}

## Articles
{arts}

## Références clients de Pull Up Événements
Crédit Agricole, Crédit Moderne, SAPMER, CILAM, Mercialys, Sudeco, l'INSEE, Ravate Pro, Testoni, la Croix-Rouge française, la Fondation Père Favron, Groupe Caillé, IAE Réunion.

## Questions fréquentes
{faq}''')
    # GSC + IndexNow
    open(os.path.join(OUT,'google94f0fc7cfd75aea2.html'),'w').write('google-site-verification: google94f0fc7cfd75aea2.html')
    kp=os.path.join(OUT,'.indexnow_key')
    if os.path.exists(kp): key=open(kp).read().strip()
    else:
        key=uuid.uuid4().hex; open(kp,'w').write(key)
    open(os.path.join(OUT,key+'.txt'),'w').write(key)
    # suivi.js : copie du site soirée avec le nom du site
    s=open(os.path.expanduser('~/site-soiree/suivi.js'),encoding='utf-8').read().replace('var SITE_PULLUP = "soiree974";','var SITE_PULLUP = "karaoke974";')
    open(os.path.join(OUT,'suivi.js'),'w',encoding='utf-8').write(s)
    return key

if __name__=='__main__':
    os.makedirs(OUT,exist_ok=True)
    accueil(); pages_formats(); pages_zones(); blog(); legal()
    # NB : après ce script, lancer outils/publier-article.py --regenerer pour inclure les articles Markdown (blog, sitemap, llms.txt)
    urls=[DOM+'/']+[f'{DOM}/{s}/' for s,_,_,_ in FORMATS[:4]]+[f'{DOM}/{z}/' for z,_,_,_ in ZONES]+[DOM+'/blog/']+[f'{DOM}/blog/{s}/' for s,_,_,_,_ in ARTICLES]
    key=fichiers(urls)
    h=open(os.path.join(OUT,'index.html'),encoding='utf-8').read()
    vis=re.sub(r'<[^>]+>',' ',re.sub(r'<(script|style)[^>]*>.*?</\1>','',h,flags=re.S))
    print('accueil : ~%d mots visibles'%len(vis.split()), '| clé IndexNow', key)
