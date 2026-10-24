"""Fetch official NBA regular-season team game logs and calculate scoring/defense."""
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from nba_api.stats.endpoints import leaguegamelog

output = {'updated_at': datetime.now(timezone.utc).isoformat(), 'seasons': {}}
for season in ('2025-26', '2026-27'):
    response = leaguegamelog.LeagueGameLog(season=season, season_type_all_star='Regular Season', player_or_team_abbreviation='T', timeout=60)
    rows = response.get_normalized_dict()['LeagueGameLog']
    games = defaultdict(list)
    for row in rows:
        if row.get('GAME_ID') and row.get('TEAM_ID'):
            games[str(row['GAME_ID'])].append(row)
    totals = defaultdict(lambda: {'team': '', 'gp': 0, 'pts': 0, 'allowed': 0})
    completed = 0
    for sides in games.values():
        if len(sides) != 2 or sides[0]['TEAM_ID'] == sides[1]['TEAM_ID'] or any(s.get('PTS') is None for s in sides):
            continue
        completed += 1
        a, b = sides
        for team, opponent in ((a, b), (b, a)):
            t = totals[str(team['TEAM_ID'])]
            t['team'] = team['TEAM_ABBREVIATION']
            t['gp'] += 1
            t['pts'] += int(team['PTS'])
            t['allowed'] += int(opponent['PTS'])
    teams = []
    for t in totals.values():
        if t['gp']:
            teams.append({'team': t['team'], 'gp': t['gp'], 'ppg': round(t['pts']/t['gp'],2), 'opp_ppg': round(t['allowed']/t['gp'],2), 'quality': 'Derived from NBA official game logs'})
    for rank_field, metric, reverse in (('scoring_rank','ppg',True),('defense_rank','opp_ppg',False)):
        ordered = sorted(teams, key=lambda t: (-t[metric] if reverse else t[metric], t['team']))
        for rank, t in enumerate(ordered,1):
            t[rank_field] = rank
    output['seasons'][season] = {'games': completed, 'teams': sorted(teams,key=lambda t:t['team'])}
path = Path('data/summary.json')
path.parent.mkdir(exist_ok=True)
path.write_text(json.dumps(output,indent=2)+'\n')
print('Wrote',path)
