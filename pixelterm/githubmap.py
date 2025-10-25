"""
pixelterm.githubmap
--------------------
Render your GitHub contribution heatmap in the terminal using pixelterm.
Automatically authenticates using `gh auth login` if available.
"""

import datetime
import subprocess
import requests
from .renderer import PixelRenderer


def get_github_token():
    """Get GitHub token from GitHub CLI."""
    try:
        result = subprocess.run(
            ["gh", "auth", "token"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception:
        return None


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def _generate_calendar_grid():
    """Generate 53-week calendar grid starting from Sunday."""
    today = datetime.date.today()
    start = today - datetime.timedelta(weeks=52)
    days_since_sunday = (start.weekday() + 1) % 7
    start = start - datetime.timedelta(days=days_since_sunday)

    grid = []
    current = start
    for _ in range(53):
        week = [current + datetime.timedelta(days=i) for i in range(7)]
        grid.append(week)
        current += datetime.timedelta(days=7)
    return grid


def _fetch_contribution_data(username, token, start_date, end_date):
    """Fetch contribution data from GitHub GraphQL API."""
    url = "https://api.github.com/graphql"
    headers = {"Authorization": f"bearer {token}"}
    
    query = """
    query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar {
            totalContributions
            colors
            weeks {
              contributionDays {
                date
                contributionCount
                color
              }
            }
          }
        }
      }
    }
    """

    response = requests.post(
        url, 
        json={
            "query": query, 
            "variables": {
                "login": username,
                "from": start_date.isoformat() + "T00:00:00Z",
                "to": end_date.isoformat() + "T23:59:59Z"
            }
        }, 
        headers=headers
    )
    
    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code}\n{response.text}")
        
    data = response.json()
    if "errors" in data:
        raise Exception(f"GraphQL Errors: {data['errors']}")

    return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def _get_theme_colors(dark_mode):
    """Get color scheme for the specified theme."""
    if dark_mode:
        return [
            "#161b22",  # No contributions
            "#0e4429",  # Level 1
            "#006d32",  # Level 2
            "#26a641",  # Level 3
            "#39d353"   # Level 4
        ]
    else:
        return [
            "#ebedf0",  # No contributions
            "#9be9a8",  # Level 1
            "#40c463",  # Level 2
            "#30a14e",  # Level 3
            "#216e39"   # Level 4
        ]


def _map_github_color_to_theme_index(github_color, github_colors, theme_colors):
    """Map GitHub's actual color to the corresponding theme color."""
    no_contrib_colors = ["#ebedf0", "#161b22"]
    if github_color in no_contrib_colors:
        return theme_colors[0]
    
    try:
        github_index = github_colors.index(github_color)
        theme_index = github_index + 1
        return theme_colors[min(theme_index, len(theme_colors) - 1)]
    except ValueError:
        return theme_colors[0]


def show_github_heatmap(username, dark=True):
    """Display GitHub contribution heatmap in terminal."""
    
    # Validate username
    if not username or not isinstance(username, str):
        print("Error: Invalid username")
        return
    
    # Basic username validation (GitHub allows alphanumeric, hyphens)
    import re
    if not re.match(r'^[a-zA-Z0-9\-]+$', username):
        print("Error: Invalid GitHub username format")
        return
    
    if len(username) > 39:  # GitHub's max username length
        print("Error: Username too long")
        return
    
    token = get_github_token()
    if not token:
        print("Could not get GitHub token. Try running `gh auth login` first.")
        return

    try:
        print(f"Fetching GitHub contributions for @{username}...")
        
        calendar_grid = _generate_calendar_grid()
        calendar_data = _fetch_contribution_data(
            username, token, calendar_grid[0][0], calendar_grid[-1][-1]
        )
        
        total_contributions = calendar_data['totalContributions']
        theme_name = 'Dark' if dark else 'Light'
        print(f"@{username} - {total_contributions} contributions ({theme_name} theme)")
        
        github_colors = calendar_data['colors']
        theme_colors = _get_theme_colors(dark)
        today = datetime.date.today()
        
        contrib_map = {}
        for week in calendar_data["weeks"]:
            for day in week["contributionDays"]:
                day_date = datetime.datetime.strptime(day["date"], "%Y-%m-%d").date()
                if day_date <= today:
                    github_color = day["color"]
                    theme_color = _map_github_color_to_theme_index(
                        github_color, github_colors, theme_colors
                    )
                    contrib_map[day["date"]] = theme_color
        
        r = PixelRenderer(width=53, height=7, cell="██")
        
        for week_idx, week in enumerate(calendar_grid):
            if week_idx >= r.width:
                break
                
            for day_idx, date in enumerate(week):
                if day_idx >= r.height or date > today:
                    continue
                
                date_str = date.strftime("%Y-%m-%d")
                if date_str in contrib_map:
                    rgb_color = hex_to_rgb(contrib_map[date_str])
                    r.set_pixel(week_idx, day_idx, rgb_color)
        
        r.render()
        r.cleanup()
            
    except Exception as e:
        print(f"Error: {e}")


def main():
    """CLI entry point for pixelterm-github command."""
    import sys
    if len(sys.argv) != 2:
        print("Usage: pixelterm-github <username>")
        sys.exit(1)
    
    username = sys.argv[1]
    show_github_heatmap(username)


if __name__ == "__main__":
    main()
