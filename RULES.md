
## STATUS 2026-09-23 — approved direction
Jordan approved the "modernized a bit" Services page ("modern is good"). All six pages are
generated from one shell by `restore/gen.py` into `restore/site/` (index, services, about,
about_mold, partner, contact + site.css + img/). Edit gen.py, re-run, never hand-edit site/*.html.
Reference builds kept beside it: restore/services.html (pure restoration), services-modern.html.
Open loops before deploy: form has no backend (mailto only); "Click here / Tell You More"
links still point at dead Stupeflix; old .html URLs already match (same slugs); needs HTTPS host.
