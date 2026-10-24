#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
publier-article.py : publie un article du blog Karaoké 974 (karaoke974.re) à partir d'un fichier Markdown,
puis régénère la liste du blog, le sitemap et la section « Articles » de llms.txt.

Usage (depuis la racine du dépôt ~/site-karaoke) :
  python3 outils/publier-article.py outils/articles/mon-article.md            # génère seulement
  python3 outils/publier-article.py outils/articles/mon-article.md --publier  # + git push + vérification HTTP 200
  python3 outils/publier-article.py --regenerer [--publier]                   # régénère tout depuis outils/articles.json

Format du .md (en-tête puis corps) :
---
titre: Organiser un karaoké à La Réunion : le guide complet
description: meta description, 158 caractères maximum
slug: organiser-karaoke-reunion-guide
date: 2026-10-24
image: micro-sans-fil-soiree-entreprise-karaoke-974.jpg   (fichier existant dans /images/)
alt: Micro sans fil lors d'une soirée karaoké d'entreprise
---
Corps en Markdown simple : ## titres, ### sous-titres, paragraphes, listes « - », **gras**, [liens](url).
Le premier paragraphe commence par « **En bref.** » : il devient l'encadré repris par Google et les IA.
Une section « ## Questions fréquentes » avec des paragraphes « **Question ?** Réponse. » produit un schéma FAQPage.

Règles vérifiées avant écriture : pas de tiret cadratin ni demi-cadratin, meta <= 158, titre <= 70, slug unique,
image existante, « En bref. » en tête, aucun montant en euros autre que 470 € HT / 509,95 € TTC.
"""
import json, re, sys, subprocess, datetime, os, time, urllib.request
from html import escape

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import gen_karaoke as G

RACINE = G.OUT
REG = os.path.join(ICI, 'articles.json')
MOIS = ['janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre']

def date_fr(iso):
    d = datetime.date.fromisoformat(iso); return f"{d.day} {MOIS[d.month-1]} {d.year}"

def lire_registre():
    return json.load(open(REG, encoding='utf-8')) if os.path.exists(REG) else []

def ecrire_registre(r):
    json.dump(r, open(REG, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)

# ───────── Markdown minimal ─────────
def inline(t):
    t = escape(t, quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', t)
    return t

def md_vers_html(corps):
    lignes = corps.strip().split('\n'); html = []; faq = []; en_bref = None; i = 0; dans_faq = False; liste = []
    def flush_liste():
        nonlocal liste
        if liste: html.append('<ul>' + ''.join(f'<li>{inline(l)}</li>' for l in liste) + '</ul>'); liste = []
    paras = []
    # regrouper en blocs
    bloc = []
    for l in lignes + ['']:
        if l.strip() == '':
            if bloc: paras.append('\n'.join(bloc)); bloc = []
        else: bloc.append(l)
    for p in paras:
        if p.startswith('## '):
            flush_liste(); titre = p[3:].strip(); dans_faq = titre.lower().startswith('questions fréquentes')
            html.append(f'<h2>{inline(titre)}</h2>'); continue
        if p.startswith('### '):
            flush_liste(); html.append(f'<h3>{inline(p[4:].strip())}</h3>'); continue
        if all(l.lstrip().startswith('- ') for l in p.split('\n')):
            liste = [l.lstrip()[2:] for l in p.split('\n')]; flush_liste(); continue
        flush_liste()
        texte = ' '.join(l.strip() for l in p.split('\n'))
        if en_bref is None and texte.startswith('**En bref.**'):
            en_bref = texte; html.append(f'<div class="encart">{inline(texte)}</div>'); continue
        if dans_faq:
            m = re.match(r'\*\*(.+?\?)\*\*\s*(.+)', texte)
            if m:
                faq.append((m.group(1).strip(), m.group(2).strip()))
                html.append(f'<p><b>{inline(m.group(1))}</b> {inline(m.group(2))}</p>'); continue
        html.append(f'<p>{inline(texte)}</p>')
    return ''.join(html), faq, en_bref

def lire_md(chemin):
    t = open(chemin, encoding='utf-8').read()
    m = re.match(r'---\n(.*?)\n---\n(.*)', t, re.S)
    if not m: sys.exit('En-tête --- manquant : ' + chemin)
    meta = {}
    for l in m.group(1).split('\n'):
        if ':' in l:
            k, v = l.split(':', 1); meta[k.strip()] = v.strip()
    return meta, m.group(2)

def verifier(meta, corps, registre, slug_existant_ok=False):
    erreurs = []
    tout = meta.get('titre','') + meta.get('description','') + corps
    if '—' in tout or '–' in tout: erreurs.append('tiret cadratin ou demi-cadratin présent')
    if len(meta.get('titre','')) > 70: erreurs.append('titre > 70 caractères (%d)' % len(meta['titre']))
    if len(meta.get('description','')) > 158: erreurs.append('description > 158 caractères (%d)' % len(meta['description']))
    for k in ('titre','description','slug','date','image','alt'):
        if not meta.get(k): erreurs.append('champ manquant : ' + k)
    if meta.get('slug') and not re.fullmatch(r'[a-z0-9-]+', meta['slug']): erreurs.append('slug invalide')
    if not slug_existant_ok and any(a['slug'] == meta.get('slug') for a in registre): erreurs.append('slug déjà publié')
    if meta.get('slug') in [s for s,_,_,_,_ in G.ARTICLES]: erreurs.append('slug déjà utilisé par un article fixe')
    if meta.get('image') and not os.path.exists(os.path.join(RACINE, 'images', meta['image'])): erreurs.append('image introuvable dans images/ : ' + meta['image'])
    if not corps.strip().startswith('**En bref.**'): erreurs.append('le corps doit commencer par « **En bref.** »')
    for m in re.finditer(r'(\d[\d\s]*(?:,\d+)?)\s?€', corps):
        montant = m.group(1).replace(' ', '')
        if montant not in ('470', '509,95'): erreurs.append('montant en euros non autorisé : ' + m.group(0))
    mots = len(re.sub(r'[#*\[\]()]', ' ', corps).split())
    if mots < 550: erreurs.append('article trop court : %d mots (minimum 550)' % mots)
    if erreurs: sys.exit('REFUSÉ : ' + ' ; '.join(erreurs))
    return mots

def generer_article(meta, corps):
    pre = '../../'
    html_corps, faq, en_bref = md_vers_html(corps)
    mots = len(re.sub(r'<[^>]+>', ' ', html_corps).split())
    t, d, slug, img = meta['titre'], meta['description'], meta['slug'], meta['image']
    body = f'''<section class="hero-int"><div class="bg">{G.IMG(img, meta['alt'], pre, lazy=False)}</div><div class="wrap in"><p class="fil"><a href="{pre}./">Karaoké 974</a> › <a href="{pre}blog/">Blog</a></p><h1>{escape(t)}</h1><p class="lead">{escape(d)}</p><p class="fil">Publié le {date_fr(meta['date'])} · {max(2, mots // 220)} min de lecture</p></div></section>
<article><section><div class="wrap prose">{html_corps}
<div class="auteur"><div class="av">PU</div><div><b>À propos de l'auteur</b><br>Article rédigé par l'équipe de <a href="https://pullup.re/">Pull Up Événements, la grande agence événementielle de La Réunion</a> : plus de 500 événements depuis 2017, {G.NOTE}/5 sur Google ({G.NB} avis). Karaoké 974 est son service karaoké, géré par Ketsia.</div></div>
<div class="cta-fin"><h2>Une soirée karaoké à organiser ?</h2><p>470 € HT tout compris (509,95 € TTC), animateur et matériel, partout à La Réunion. Ketsia vous répond sous 24 h au {G.TEL}.</p><a class="btn jaune" href="#devis">Demander un devis</a></div></div></section></article>
{G.devis_block(pre)}{G.eco_block(pre)}'''
    ld = [{"@context":"https://schema.org","@type":"BlogPosting","headline":t,"description":d,"image":G.DOM+"/images/"+img,"datePublished":meta['date'],"dateModified":meta['date'],"author":{"@type":"Organization","name":"Pull Up Événements","url":"https://pullup.re/"},"publisher":{"@id":G.DOM+"/#organization"},"mainEntityOfPage":G.DOM+"/blog/"+slug+"/","wordCount":mots,"inLanguage":"fr"},
          {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Karaoké 974","item":G.DOM+"/"},{"@type":"ListItem","position":2,"name":"Blog","item":G.DOM+"/blog/"},{"@type":"ListItem","position":3,"name":t,"item":G.DOM+"/blog/"+slug+"/"}]}]
    if faq:
        ld.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]})
    G.page('blog/' + slug, t + ' | Karaoké 974', d, body, pre, og_img=img, jsonld=ld, preload=img)
    return mots

def tous_articles(registre):
    """Articles fixes du générateur + articles Markdown, du plus récent au plus ancien."""
    fixes = [{'slug': s, 'titre': t, 'description': d, 'image': img, 'date': G.TODAY.isoformat() if False else '2026-10-23'} for s,t,d,_,img in G.ARTICLES]
    md = [{'slug': a['slug'], 'titre': a['titre'], 'description': a['description'], 'image': a['image'], 'date': a['date']} for a in registre]
    return sorted(md + fixes, key=lambda a: a['date'], reverse=True)

def regenerer_blog_index(registre):
    pre = '../'
    arts = tous_articles(registre)
    cards = ''.join(f'<article class="card pic reveal">{G.IMG(a["image"], a["titre"], pre)}<div class="tx"><p class="fil">{date_fr(a["date"])}</p><h3><a href="{pre}blog/{a["slug"]}/" style="color:#fff">{escape(a["titre"])}</a></h3><p>{escape(a["description"])}</p><a class="more" href="{pre}blog/{a["slug"]}/">Lire →</a></div></article>' for a in arts)
    body = f'''<section class="hero-int"><div class="wrap in"><p class="fil"><a href="{pre}./">Karaoké 974</a> › Blog</p><h1>Le blog du <span>karaoké péi</span></h1><p class="lead">Organiser un karaoké à La Réunion, à domicile ou en entreprise : prix, playlists, animateur, matériel. Les conseils de Pull Up Événements, {len(arts)} articles.</p></div></section>
<section><div class="wrap"><div class="blog-list">{cards}</div></div></section>{G.devis_block(pre)}{G.eco_block(pre)}'''
    G.page('blog', 'Blog karaoké La Réunion : conseils, prix, playlists | Karaoké 974', 'Conseils pour organiser une soirée karaoké à La Réunion : budget, karaoké à domicile, animateur, karaoké ou DJ, chansons péi. Par Pull Up Événements.', body, pre)

def regenerer_sitemap_llms(registre):
    arts = tous_articles(registre)
    urls = [G.DOM+'/'] + [f'{G.DOM}/{s}/' for s,_,_,_ in G.FORMATS[:4]] + [f'{G.DOM}/{z}/' for z,_,_,_ in G.ZONES] + [G.DOM+'/blog/']
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls: sm += f'  <url><loc>{u}</loc><lastmod>{G.TODAY.isoformat()}</lastmod></url>\n'
    for a in arts: sm += f'  <url><loc>{G.DOM}/blog/{a["slug"]}/</loc><lastmod>{a["date"]}</lastmod></url>\n'
    sm += '</urlset>\n'
    open(os.path.join(RACINE, 'sitemap.xml'), 'w').write(sm)
    lp = os.path.join(RACINE, 'llms.txt'); t = open(lp, encoding='utf-8').read()
    bloc = '## Articles\n' + '\n'.join(f'- {G.DOM}/blog/{a["slug"]}/ : {a["titre"]}' for a in arts) + '\n'
    t2 = re.sub(r'## Articles\n(?:- .*\n?)+', bloc, t)
    if t2 == t: t2 = t.rstrip('\n') + '\n\n' + bloc
    open(lp, 'w', encoding='utf-8').write(t2)
    return [f'{G.DOM}/blog/{a["slug"]}/' for a in arts]

def publier(urls_a_verifier, message):
    r = subprocess.run(['git', '-C', RACINE, 'status', '--porcelain'], capture_output=True, text=True).stdout.strip()
    if r:
        subprocess.run(['git', '-C', RACINE, 'add', '-A'], check=True)
        subprocess.run(['git', '-C', RACINE, '-c', 'user.name=Romain Capdepont', '-c', 'user.email=capdepontromain@gmail.com', 'commit', '-q', '-m', message + '\n\nCo-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>'], check=True)
        subprocess.run(['git', '-C', RACINE, 'pull', '-q', '--rebase', 'origin', 'main'])
        p = subprocess.run(['git', '-C', RACINE, 'push', '-q', 'origin', 'main'], capture_output=True, text=True)
        print('push :', 'ok' if p.returncode == 0 else 'ÉCHEC ' + p.stderr[-300:])
    else:
        print('rien à commiter')
    print('vérification en ligne (GitHub Pages peut mettre 1 à 3 minutes)…')
    for u in urls_a_verifier:
        code = '000'
        for essai in range(12):
            try:
                req = urllib.request.Request(u + '?nc=%d' % int(time.time()), headers={'User-Agent': 'Mozilla/5.0'})
                code = str(urllib.request.urlopen(req, timeout=30).getcode())
            except urllib.error.HTTPError as e: code = str(e.code)
            except Exception: code = '000'
            if code == '200': break
            time.sleep(15)
        print(f'  {code} {u}')

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    PUB = '--publier' in sys.argv
    registre = lire_registre()
    a_verifier = []
    if '--regenerer' in sys.argv:
        for a in registre:
            meta, corps = lire_md(os.path.join(ICI, 'articles', a['slug'] + '.md'))
            generer_article(meta, corps); a_verifier.append(f'{G.DOM}/blog/{a["slug"]}/')
        print('%d article(s) Markdown régénéré(s)' % len(registre))
    elif args:
        chemin = args[0]
        meta, corps = lire_md(chemin)
        mots = verifier(meta, corps, registre)
        generer_article(meta, corps)
        registre.append({'slug': meta['slug'], 'titre': meta['titre'], 'description': meta['description'], 'image': meta['image'], 'date': meta['date'], 'mots': mots})
        ecrire_registre(registre)
        a_verifier.append(f'{G.DOM}/blog/{meta["slug"]}/')
        print(f'article généré : {meta["slug"]} ({mots} mots)')
        # garde une copie du .md à côté du registre si elle n'y est pas déjà
        dest = os.path.join(ICI, 'articles', meta['slug'] + '.md')
        if os.path.abspath(chemin) != os.path.abspath(dest):
            open(dest, 'w', encoding='utf-8').write(open(chemin, encoding='utf-8').read())
    else:
        sys.exit(__doc__)
    regenerer_blog_index(registre)
    regenerer_sitemap_llms(registre)
    a_verifier.append(G.DOM + '/blog/')
    print('blog/index.html, sitemap.xml et llms.txt régénérés')
    if PUB:
        publier(a_verifier, 'Blog : ' + (args[0].split('/')[-1].replace('.md','') if args else 'régénération'))
