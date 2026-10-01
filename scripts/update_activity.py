"""Refresh the profile graphic with GitHub data; requires only Python's standard library."""
import json
import os
from pathlib import Path
from html import escape
from datetime import datetime, timezone
from urllib.request import Request, urlopen

OUTPUT = Path(__file__).resolve().parents[1] / 'assets' / 'activity.svg'
QUERY = '''query($login:String!) { user(login:$login) {
  repositories(privacy:PUBLIC,ownerAffiliations:OWNER) { totalCount }
  followers { totalCount }
  contributionsCollection { contributionCalendar {
    totalContributions weeks { contributionDays { date weekday contributionCount } }
  } }
} }'''

def render(user):
    calendar = user['contributionsCollection']['contributionCalendar']
    weeks = calendar['weeks']
    if not weeks or len(weeks) > 54:
        raise ValueError('Missing or unexpected contribution calendar')
    def text(x, y, value, size=15, color='#939daa'):
        return f'<text x="{x}" y="{y}" fill="{color}" font-family="monospace" font-size="{size}">{escape(str(value))}</text>'
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="298" viewBox="0 0 1000 298">',
             '<rect x="1" y="1" width="998" height="296" rx="10" fill="#090b0f" stroke="#292e38"/>',
             '<title>GitHub contribution activity for SinthujanCoder</title>']
    values = [(calendar['totalContributions'], 'CONTRIBUTIONS / PAST YEAR'),
              (user['repositories']['totalCount'], 'PUBLIC REPOSITORIES'),
              (user['followers']['totalCount'], 'FOLLOWERS')]
    for i, (value, label) in enumerate(values):
        x = 30 + i * 330
        parts += [text(x, 51, value, 31, '#e6edf3'), text(x, 78, label, 11, '#f03247')]
    step = min(17, 912 / len(weeks))
    colors = ['#1c222c', '#3b1720', '#742331', '#b42b40', '#f03247']
    for col, week in enumerate(weeks):
        for day in week['contributionDays']:
            count = max(0, int(day['contributionCount']))
            level = 0 if count == 0 else 1 if count < 3 else 2 if count < 6 else 3 if count < 10 else 4
            weekday = int(day['weekday'])
            if weekday not in range(7):
                raise ValueError('Invalid weekday')
            x, y = 50 + col * step, 116 + weekday * 17
            title = escape(f"{day['date']}: {count} contributions")
            parts.append(f'<rect x="{x:.1f}" y="{y}" width="13" height="13" rx="3" fill="{colors[level]}"><title>{title}</title></rect>')
    parts += [text(30, 260, 'LESS', 10)]
    for i, color in enumerate(colors):
        parts.append(f'<rect x="{70+i*18}" y="248" width="13" height="13" rx="3" fill="{color}"/>')
    stamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    parts += [text(168, 260, 'MORE', 10), text(625, 260, f'REFRESHED {stamp}', 11), '</svg>']
    return ''.join(parts)

def main():
    token = os.environ['GH_TOKEN']
    login = os.environ.get('PROFILE_USER', 'SinthujanCoder')
    req = Request('https://api.github.com/graphql', data=json.dumps({'query': QUERY, 'variables': {'login': login}}).encode(),
                  headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json', 'User-Agent': 'profile-activity'})
    with urlopen(req, timeout=30) as response:
        payload = json.load(response)
    if payload.get('errors'):
        raise RuntimeError('GitHub GraphQL returned an error; previous activity graphic retained')
    user = payload.get('data', {}).get('user')
    if not user:
        raise RuntimeError('No GitHub user data; previous activity graphic retained')
    result = render(user)
    temp = OUTPUT.with_suffix('.tmp')
    temp.write_text(result, encoding='utf-8')
    temp.replace(OUTPUT)

if __name__ == '__main__':
    main()
