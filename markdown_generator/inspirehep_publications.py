#!/usr/bin/env python3
"""
INSPIRE-HEP publications markdown generator for AcademicPages.

Fetches the publication list for an INSPIRE-HEP author and writes one
markdown file per record into _publications/, formatted for the
academicpages `publications` collection (same frontmatter shape as
publications.py, but sourced live from the INSPIRE-HEP API instead of
a manually maintained CSV/TSV).

The author is identified by their INSPIRE-HEP numeric id (the number in
https://inspirehep.net/authors/<ID>). If --author-id is not given, it is
read from the `author.inspire-hep` field in _config.yml.

Usage:
    python3 inspirehep_publications.py [--author-id ID] [--out-dir DIR] [--max N] [--dry-run]
"""
import argparse
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request

API_BASE = "https://inspirehep.net/api"
USER_AGENT = "toicca.github.io-publication-generator/1.0"

CATEGORY_BY_DOC_TYPE = {
    "article": "inspire-manuscripts",
    "conference paper": "inspire-conferences",
    "proceedings": "inspire-conferences",
    "book": "inspire-books",
    "book chapter": "inspire-books",
    "thesis": "inspire-manuscripts",
    "report": "inspire-manuscripts",
}

RECORD_FIELDS = (
    "control_number,titles,collaborations,publication_info,"
    "dois,arxiv_eprints,earliest_date,document_type"
)

HTML_ESCAPE_TABLE = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
}


def html_escape(text):
    for a, b in HTML_ESCAPE_TABLE.items():
        text = text.replace(a, b)
    return text


def fetch_json(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def get_author(author_id):
    data = fetch_json(f"{API_BASE}/authors/{author_id}")
    md = data["metadata"]
    bai = next((i["value"] for i in md.get("ids", []) if i.get("schema") == "INSPIRE BAI"), None)
    if not bai:
        raise RuntimeError(f"No INSPIRE BAI found for author id {author_id}")
    preferred_name = md.get("name", {}).get("preferred_name", "")
    return bai, preferred_name


def fetch_records(bai, max_records=None):
    records = []
    page = 1
    size = 100
    while True:
        q = urllib.parse.quote(f"a {bai}")
        url = (
            f"{API_BASE}/literature?q={q}&sort=mostrecent"
            f"&size={size}&page={page}&fields={RECORD_FIELDS}"
        )
        data = fetch_json(url)
        hits = data["hits"]["hits"]
        if not hits:
            break
        records.extend(hits)
        if max_records and len(records) >= max_records:
            return records[:max_records]
        if len(hits) < size:
            break
        page += 1
        time.sleep(0.3)
    return records


def find_author_id_from_config(config_path):
    with open(config_path) as f:
        content = f.read()
    m = re.search(r'inspire-hep\s*:\s*"?https?://inspirehep\.net/authors/(\d+)', content)
    if not m:
        raise RuntimeError("Could not find author.inspire-hep in _config.yml")
    return m.group(1)


def best_doi(dois):
    if not dois:
        return None
    for d in dois:
        if d.get("material") == "publication":
            return d["value"]
    return dois[0]["value"]


def pick_title(titles):
    # Prefer arXiv-sourced titles: they use LaTeX (rendered by MathJax on
    # the site), while APS/journal-sourced titles embed raw MathML markup
    # that shows up as literal tags on the page.
    if not titles:
        return "Untitled"
    for t in titles:
        if t.get("source") == "arXiv":
            return t["title"]
    return titles[0]["title"]


def venue_for(pub_info, arxiv):
    if pub_info:
        info = pub_info[0]
        journal = info.get("journal_title", "")
        vol = info.get("journal_volume", "")
        page = info.get("artid") or info.get("page_start", "")
        year = info.get("year", "")
        venue = " ".join(p for p in [journal, vol] if p)
        if page:
            venue += f", {page}"
        if year:
            venue += f" ({year})"
        return venue.strip()
    if arxiv:
        return f"arXiv:{arxiv[0]['value']}"
    return "Preprint"


def record_to_markdown(record, author_name):
    md = record["metadata"]
    control_number = md["control_number"]
    title = pick_title(md.get("titles") or [])
    collabs = [c["value"] for c in (md.get("collaborations") or []) if c.get("value")]
    doc_types = md.get("document_type") or ["article"]
    category = CATEGORY_BY_DOC_TYPE.get(doc_types[0], "inspire-manuscripts")
    date = md.get("earliest_date", "")
    year = date[:4] if date else ""
    pub_info = md.get("publication_info")
    arxiv = md.get("arxiv_eprints")
    venue = venue_for(pub_info, arxiv)
    doi = best_doi(md.get("dois"))

    author_display = f"{', '.join(collabs)} Collaboration" if collabs else f"{author_name} et al."
    citation = f"{author_display}"
    if year:
        citation += f" ({year})"
    citation += f'. &quot;{html_escape(title)}.&quot; <i>{html_escape(venue)}</i>.'

    paperurl = f"https://doi.org/{doi}" if doi else f"https://inspirehep.net/literature/{control_number}"

    lines = [
        "---",
        # single-quoted: titles often contain LaTeX backslashes (\to, \sqrt, ...)
        # which are invalid escape sequences inside a double-quoted YAML scalar
        f"title: '{html_escape(title)}'",
        "collection: publications",
        f"category: {category}",
        f"permalink: /publication/inspire-{control_number}",
    ]
    if collabs:
        lines.append(f"excerpt: '{html_escape(collabs[0])} Collaboration paper.'")
    if date:
        lines.append(f"date: {date}")
    lines.append(f"venue: '{html_escape(venue)}'")
    lines.append(f"paperurl: '{paperurl}'")
    if arxiv:
        lines.append(f"arxiv: 'https://arxiv.org/abs/{arxiv[0]['value']}'")
    lines.append(f"citation: '{citation}'")
    lines.append("---")
    return f"inspire-{control_number}.md", "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--author-id", help="INSPIRE-HEP numeric author id (default: from _config.yml)")
    parser.add_argument("--out-dir", default=None, help="Output directory (default: ../_publications)")
    parser.add_argument("--max", type=int, default=None, help="Max number of records to fetch")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be written, don't write files")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    config_path = os.path.join(repo_root, "_config.yml")
    out_dir = args.out_dir or os.path.join(repo_root, "_publications")

    author_id = args.author_id or find_author_id_from_config(config_path)
    print(f"Looking up INSPIRE author id {author_id}...")
    bai, author_name = get_author(author_id)
    print(f"Author BAI: {bai} ({author_name})")

    records = fetch_records(bai, args.max)
    print(f"Fetched {len(records)} record(s).")

    written = 0
    if not args.dry_run:
        os.makedirs(out_dir, exist_ok=True)
    for record in records:
        filename, content = record_to_markdown(record, author_name)
        path = os.path.join(out_dir, filename)
        if args.dry_run:
            print(f"--- Would write {path} ---")
            print(content)
            continue
        with open(path, "w") as f:
            f.write(content)
        os.chmod(path, 0o644)  # host umask may default to 600, unreadable by the Docker container's uid
        written += 1

    if not args.dry_run:
        print(f"Wrote {written} publication file(s) to {out_dir}")


if __name__ == "__main__":
    main()
