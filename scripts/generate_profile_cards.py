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
    .bg {{ fill: #fcfff9; stroke: #d8efcf; }}
    .title {{ fill: #25613a; font: 700 18px Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif; }}
    .label {{ fill: #5d7b62; font: 500 12px Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif; }}
    .value {{ fill: #2F6F3E; font: 700 22px Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif; }}
    .small {{ fill: #4f7056; font: 500 11px Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif; }}
    .track {{ fill: #eaf7e3; }}
    @media (prefers-color-scheme: dark) {{
      .bg {{ fill: #102419; stroke: #356447; }}
      .title, .value {{ fill: #e8f8df; }}
      .label, .small {{ fill: #bfe0c3; }}
      .track {{ fill: #254832; }}
    }}
  </style>
  <rect class="bg" x="1" y="1" width="{width-2}" height="{height-2}" rx="14"/>
  {body}
</svg>
'''


def render_stats(user: dict, repos: list[dict], contributions: int) -> str:
    owned = [r for r in repos if not r.get("fork")]
    stars = sum(int(r.get("stargazers_count", 0)) for r in owned)
    forks = sum(int(r.get("forks_count", 0)) for r in owned)
    values = [
        ("Public repos", len(owned)),
        ("Stars", stars),
        ("Followers", int(user.get("followers", 0))),
        ("Contributions", contributions),
        ("Forks", forks),
    ]
    xs = [42, 162, 282, 402, 522]
    chunks = ['<text x="28" y="34" class="title">GitHub snapshot</text>']
    for x, (label, value) in zip(xs, values):
        chunks.append(f'<text x="{x}" y="75" class="value">{value}</text>')
        chunks.append(f'<text x="{x}" y="96" class="label">{html.escape(label)}</text>')
    return svg_shell(640, 120, "GitHub snapshot", "\n  ".join(chunks))


def render_languages(totals: Counter[str]) -> str:
    palette = ["#2F6F3E", "#3F8F4E", "#5FBF5F", "#7BCF68", "#98DC7F", "#B9E9A5"]
    total = sum(totals.values()) or 1
    top = totals.most_common(6)
    chunks = ['<text x="28" y="34" class="title">Top languages</text>']
    y = 62
    for idx, (lang, count) in enumerate(top):
        pct = count / total
        width = int(330 * pct)
        chunks.append(f'<text x="28" y="{y+10}" class="small">{html.escape(lang)}</text>')
        chunks.append(f'<rect x="142" y="{y}" width="330" height="11" rx="5.5" class="track"/>')
        chunks.append(f'<rect x="142" y="{y}" width="{max(width, 3)}" height="11" rx="5.5" fill="{palette[idx % len(palette)]}"/>')
        chunks.append(f'<text x="492" y="{y+10}" class="small">{pct*100:.1f}%</text>')
        y += 25
    if not top:
        chunks.append('<text x="28" y="78" class="label">Language data will appear after the first refresh.</text>')
    return svg_shell(560, 220, "Top languages", "\n  ".join(chunks))


def contribution_color(count: int) -> str:
    if count <= 0:
        return "#eaf7e3"
    if count == 1:
        return "#cceec1"
    if count <= 3:
        return "#98DC7F"
    if count <= 6:
        return "#5FBF5F"
    return "#2F6F3E"


def render_activity(calendar: dict) -> str:
    weeks = calendar.get("weeks", [])[-53:]
    cell = 10
    gap = 3
    left = 54
    top = 52
    chunks = [
        '<text x="24" y="30" class="title">Contribution activity</text>',
        f'<text x="790" y="30" text-anchor="end" class="label">{int(calendar.get("totalContributions", 0))} contributions in the last year</text>',
    ]
    for wi, week in enumerate(weeks):
        for day in week.get("contributionDays", []):
            weekday = int(day.get("weekday", 0))
            count = int(day.get("contributionCount", 0))
            x = left + wi * (cell + gap)
            y = top + weekday * (cell + gap)
            color = contribution_color(count)
            date = html.escape(str(day.get("date", "")))
            chunks.append(
                f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{color}"><title>{date}: {count}</title></rect>'
            )
    chunks.extend([
        '<text x="24" y="64" class="small">Mon</text>',
        '<text x="24" y="90" class="small">Wed</text>',
        '<text x="24" y="116" class="small">Fri</text>',
        '<text x="24" y="152" class="small">Less</text>',
        '<rect x="58" y="143" width="10" height="10" rx="2" fill="#eaf7e3"/>',
        '<rect x="74" y="143" width="10" height="10" rx="2" fill="#cceec1"/>',
        '<rect x="90" y="143" width="10" height="10" rx="2" fill="#98DC7F"/>',
        '<rect x="106" y="143" width="10" height="10" rx="2" fill="#5FBF5F"/>',
        '<rect x="122" y="143" width="10" height="10" rx="2" fill="#2F6F3E"/>',
        '<text x="140" y="152" class="small">More</text>',
    ])
    return svg_shell(820, 174, "Contribution activity", "\n  ".join(chunks))


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
