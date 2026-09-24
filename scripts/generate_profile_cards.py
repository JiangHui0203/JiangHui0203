#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import os
import pathlib
import urllib.request
from collections import Counter

API = "https://api.github.com"
GRAPHQL = "https://api.github.com/graphql"


def request_json(url: str, token: str | None = None, data: dict | None = None):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "profile-card-generator",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    body = None
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if data is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, headers=headers, data=body)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def fetch_all_repos(username: str, token: str):
    repos = []
    page = 1
    while True:
        url = f"{API}/users/{username}/repos?per_page=100&page={page}&type=owner&sort=updated"
        batch = request_json(url, token)
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return repos


def fetch_contributions(username: str, token: str):
    query = '''
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                date
                contributionCount
                weekday
              }
            }
          }
        }
      }
    }
    '''
    data = request_json(
        GRAPHQL,
        token,
        {"query": query, "variables": {"login": username}},
    )
    if "errors" in data:
        raise RuntimeError(data["errors"])
    return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def fetch_language_bytes(repos: list[dict], token: str):
    totals: Counter[str] = Counter()
    for repo in repos:
        if repo.get("fork") or repo.get("archived"):
            continue
        languages_url = repo.get("languages_url")
        if not languages_url:
            continue
        try:
            payload = request_json(languages_url, token)
        except Exception:
            continue
        for lang, count in payload.items():
            totals[lang] += int(count)
    return totals


def svg_shell(width: int, height: int, title: str, body: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(title)}">
  <style>
    .bg {{ fill: #fbfdfc; stroke: #d3e4da; stroke-width: 1px; }}
    .title {{ fill: #113f28; font: 700 16px Inter, ui-sans-serif, system-ui, -apple-system, sans-serif; letter-spacing: -0.2px; }}
    .subtitle {{ fill: #527562; font: 500 11px Inter, ui-sans-serif, system-ui, -apple-system, sans-serif; }}
    .label {{ fill: #527562; font: 500 11px Inter, ui-sans-serif, system-ui, -apple-system, sans-serif; }}
    .value {{ fill: #0f7647; font: 700 20px Inter, ui-sans-serif, system-ui, -apple-system, sans-serif; }}
    .small {{ fill: #355342; font: 500 11px Inter, ui-sans-serif, system-ui, -apple-system, sans-serif; }}
    .tile {{ fill: #f2f8f4; stroke: #e1efe7; stroke-width: 1px; rx: 8px; }}
    .track {{ fill: #e8f4ed; }}
    .c0 {{ fill: #e8f4ed; }}
    .c1 {{ fill: #a7f3d0; }}
    .c2 {{ fill: #4ade80; }}
    .c3 {{ fill: #16a34a; }}
    .c4 {{ fill: #0f7647; }}
    @media (prefers-color-scheme: dark) {{
      .bg {{ fill: #0e1713; stroke: #1e3a2b; }}
      .title {{ fill: #eaf7f0; }}
      .subtitle {{ fill: #7f9f8c; }}
      .label {{ fill: #8ea99a; }}
      .value {{ fill: #34d399; }}
      .small {{ fill: #b8d4c5; }}
      .tile {{ fill: #13221b; stroke: #203c2d; }}
      .track {{ fill: #193124; }}
      .c0 {{ fill: #16271e; }}
      .c1 {{ fill: #1d4d35; }}
      .c2 {{ fill: #1d7b4e; }}
      .c3 {{ fill: #10b981; }}
      .c4 {{ fill: #34d399; }}
    }}
  </style>
  <rect class="bg" x="1" y="1" width="{width-2}" height="{height-2}" rx="12"/>
  {body}
</svg>
'''


def render_stats(user: dict, repos: list[dict], contributions: int) -> str:
    owned = [r for r in repos if not r.get("fork")]
    stars = sum(int(r.get("stargazers_count", 0)) for r in owned)
    forks = sum(int(r.get("forks_count", 0)) for r in owned)

    chunks = [
        '<text x="24" y="32" class="title">GitHub snapshot</text>',
        '<circle cx="340" cy="28" r="3.5" fill="#10b981"/>',
        '<text x="350" y="32" class="subtitle">Overview</text>',
    ]

    # Row 1 (3 tiles: Repos, Stars, Followers)
    r1_items = [
        (24, 114, owned and len(owned) or 0, "Repositories"),
        (148, 114, stars, "Stars earned"),
        (272, 114, int(user.get("followers", 0)), "Followers"),
    ]
    for x, w, val, lbl in r1_items:
        chunks.append(f'<rect class="tile" x="{x}" y="48" width="{w}" height="64" rx="8"/>')
        chunks.append(f'<text x="{x+14}" y="78" class="value">{val}</text>')
        chunks.append(f'<text x="{x+14}" y="98" class="label">{html.escape(lbl)}</text>')

    # Row 2 (2 tiles: Total contributions, Forks)
    r2_items = [
        (24, 176, contributions, "Contributions (1 yr)"),
        (210, 176, forks, "Total forks"),
    ]
    for x, w, val, lbl in r2_items:
        chunks.append(f'<rect class="tile" x="{x}" y="122" width="{w}" height="64" rx="8"/>')
        chunks.append(f'<text x="{x+16}" y="152" class="value">{val}</text>')
        chunks.append(f'<text x="{x+16}" y="172" class="label">{html.escape(lbl)}</text>')

    return svg_shell(410, 206, "GitHub snapshot", "\n  ".join(chunks))


def render_languages(totals: Counter[str]) -> str:
    palette = ["#0f7647", "#10b981", "#34d399", "#5eead4", "#86efac", "#a7f3d0"]
    total = sum(totals.values()) or 1
    top = totals.most_common(5)

    chunks = [
        '<text x="24" y="32" class="title">Top languages</text>',
        '<text x="386" y="32" text-anchor="end" class="subtitle">By code volume</text>',
    ]

    y = 54
    for idx, (lang, count) in enumerate(top):
        pct = count / total
        bar_w = int(200 * pct)
        color = palette[idx % len(palette)]
        chunks.append(f'<text x="24" y="{y+11}" class="small">{html.escape(lang)}</text>')
        chunks.append(f'<rect x="122" y="{y+2}" width="200" height="8" rx="4" class="track"/>')
        chunks.append(f'<rect x="122" y="{y+2}" width="{max(bar_w, 3)}" height="8" rx="4" fill="{color}"/>')
        chunks.append(f'<text x="334" y="{y+11}" class="small">{pct*100:.1f}%</text>')
        y += 28

    if not top:
        chunks.append('<text x="24" y="90" class="label">Language data will appear after the first refresh.</text>')

    return svg_shell(410, 206, "Top languages", "\n  ".join(chunks))


def get_contribution_level(count: int) -> str:
    if count <= 0:
        return "c0"
    if count == 1:
        return "c1"
    if count <= 3:
        return "c2"
    if count <= 6:
        return "c3"
    return "c4"


def render_activity(calendar: dict) -> str:
    weeks = calendar.get("weeks", [])[-53:]
    cell = 11
    gap = 3.6
    left = 52
    top = 52
    chunks = [
        '<text x="24" y="32" class="title">Contribution activity</text>',
        f'<text x="836" y="32" text-anchor="end" class="subtitle">{int(calendar.get("totalContributions", 0))} contributions in the last year</text>',
    ]
    for wi, week in enumerate(weeks):
        for day in week.get("contributionDays", []):
            weekday = int(day.get("weekday", 0))
            count = int(day.get("contributionCount", 0))
            x = round(left + wi * (cell + gap), 1)
            y = round(top + weekday * (cell + gap), 1)
            level = get_contribution_level(count)
            date = html.escape(str(day.get("date", "")))
            chunks.append(
                f'<rect class="{level}" x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2.5"><title>{date}: {count}</title></rect>'
            )
    chunks.extend([
        '<text x="24" y="65" class="small">Mon</text>',
        '<text x="24" y="94" class="small">Wed</text>',
        '<text x="24" y="123" class="small">Fri</text>',
        '<text x="24" y="156" class="small">Less</text>',
        '<rect class="c0" x="58" y="146" width="11" height="11" rx="2.5"/>',
        '<rect class="c1" x="75" y="146" width="11" height="11" rx="2.5"/>',
        '<rect class="c2" x="92" y="146" width="11" height="11" rx="2.5"/>',
        '<rect class="c3" x="109" y="146" width="11" height="11" rx="2.5"/>',
        '<rect class="c4" x="126" y="146" width="11" height="11" rx="2.5"/>',
        '<text x="146" y="156" class="small">More</text>',
    ])
    return svg_shell(860, 176, "Contribution activity", "\n  ".join(chunks))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        raise SystemExit("GITHUB_TOKEN is required")

    out = pathlib.Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    user = request_json(f"{API}/users/{args.username}", token)
    repos = fetch_all_repos(args.username, token)
    calendar = fetch_contributions(args.username, token)
    languages = fetch_language_bytes(repos, token)

    (out / "stats.svg").write_text(
        render_stats(user, repos, int(calendar.get("totalContributions", 0))),
        encoding="utf-8",
    )
    (out / "top-langs.svg").write_text(render_languages(languages), encoding="utf-8")
    (out / "activity.svg").write_text(render_activity(calendar), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
