NBA DEFENSIVE DASHBOARD — STARTER

1. Extract this ZIP to your computer.
2. Open https://github.com/eec757/nba-defensive-dashboard
3. Choose Add file > Upload files. Drag in the extracted contents, preserving the scripts/, data/, and .github/workflows/ directories. GitHub's web upload may not preserve hidden folders from all browsers; if .github/workflows/daily.yml is missing, create it with Add file > Create new file and type that exact path.
4. Commit changes.
5. Open Actions > Daily NBA Update > Run workflow to test collection.
6. Open Settings > Pages > Deploy from a branch > main > /(root) > Save.

This is a starter, not the full requested analytics platform. Team PPG and points allowed are computed from NBA official team game logs. Position, 3PT, paint and rim splits are not yet implemented. The workflow runs at 14:00 UTC (8 AM Central Standard / 9 AM Central Daylight), not a DST-adjusted 8 AM year-round. NBA endpoints can block GitHub-hosted requests. Failed collections will not replace existing data.
