# EFETACK Social-Media-Pipeline

Dieses Repo ist **öffentlich** und dient nur als Bild-Hosting für Metricool. Nichts Privates committen.

## Regeln
- Keine neuen Ordner außerhalb dieses Repos anlegen. Alles hier organisiert einsortieren.
- Sprache: Deutsch, Du-Form. Zielgruppe: lokale KMU. Themen: Webdesign.

## Struktur
- `tools/render.py` – Render-Skript (HTML → Playwright/Chromium → JPG)
- `tools/fonts/` – Schriften (Archivo Variable Font + OFL-Lizenz)
- `posts/YYYY-MM-DD-thema/` – `slides.json` (Inhalt) + `slide-01.jpg` … (1080x1350)

## Slides rendern
```bash
python3 tools/render.py posts/<ordner>
```
Voraussetzung (einmalig): `pip3 install --user playwright && python3 -m playwright install chromium`

`slides.json`: Liste von Slides. Cover: `type: "cover"`, `bubble` [Meta, Nachricht], `headline_html`
(`<em>` = gelb), `sub`, `footer`. Inhalt: `type: "content"`, `headline`, `text`, `fix`, optional `footer`.

## Design
- Schrift Archivo (Google Fonts), Datei unter `tools/fonts`, per base64 ins HTML eingebettet
- Headlines: Gewicht 800, `font-stretch: 75%`
- Farben: Hintergrund `#EEF1F5`, Text `#14213D`, Akzent `#FFC93C`, Grau `#5B6B86`
- Cover dunkel (`#14213D`) mit gelber Benachrichtigungs-Bubble
- Inhaltsslides hell: große Headline, Erklärtext, gelber Block „So behebst du es“ unten
- Zähler `x/N` oben rechts, `@efetack` unten links

## Workflow
1. Slides erstellen (`slides.json` + rendern), Vorschau zeigen und auf OK warten
2. `git add` / `commit` / `push` auf `main`
3. Bild-URLs: `https://raw.githubusercontent.com/EFETACK/social-assets/main/posts/<ordner>/<datei>`
4. Per Metricool-MCP einplanen:
   - **Immer `draft: true`. Nie ohne.**
   - Marke EFETACK, blogId `4620129`, Zeitzone `Europe/Berlin`
   - Netzwerke `instagram` + `facebook`, `instagramData.type: "POST"`, `facebookData.type: "POST"`
   - Slides in Reihenfolge als `media`
5. `plannerUrl` an den User zurückgeben

## Standardzeiten
Di/Do 15:00, Sa 13:00 (Europe/Berlin)
