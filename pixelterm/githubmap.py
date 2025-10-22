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
    #Get GitHub token from GitHub CLI.
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
    # Convert hex color to RGB tuple.
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def _generate_calendar_grid():
    # Generate 53-week calendar grid with complete first week.
    today = datetime.date.today()
    start = today - datetime.timedelta(weeks=52)
    # Align to Sunday of that week
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
    # Fetch contribution data from GitHub API.
    url = "https://api.github.com/graphql"
    headers = {"Authorization": f"bearer {token}"}
    
    query = """
    query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                date
                contributionCount
              }
            }
          }
        }
      }
    }
    """

    from_date = start_date.isoformat() + "T00:00:00Z"
    to_date = end_date.isoformat() + "T23:59:59Z"
    
    response = requests.post(
        url, 
        json={
            "query": query, 
            "variables": {
                "login": username,
                "from": from_date,
                "to": to_date
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
    # Get color scheme for theme (dark/light).
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


def _map_count_to_color(count, theme_colors):
    # Map contribution count to color level.
    if count == 0:
        return theme_colors[0]
    elif count <= 3:
        return theme_colors[1]
    elif count <= 6:
        return theme_colors[2]
    elif count <= 9:
        return theme_colors[3]
    else:
        return theme_colors[4]


def show_github_heatmap(username, dark=True):
    """
    Display GitHub contribution heatmap in terminal.
    
    Args:
        username (str): GitHub username
        dark (bool): Use dark theme (default: True)
    """
    token = get_github_token()
    if not token:
        print("Could not get GitHub token. Try running `gh auth login` first.")
        return

    try:
        print(f"Fetching GitHub contributions for @{username}...")
        
        # Get date range
        calendar_grid = _generate_calendar_grid()
        start_date = calendar_grid[0][0]
        end_date = calendar_grid[-1][-1]
        
        # Fetch data
        calendar_data = _fetch_contribution_data(username, token, start_date, end_date)
        
        # Show info before rendering
        total_contributions = calendar_data['totalContributions']
        theme_name = 'Dark' if dark else 'Light'
        print(f"@{username} - {total_contributions} contributions ({theme_name} theme)")
        
        # Process contributions
        theme_colors = _get_theme_colors(dark)
        contrib_map = {}
        
        for week in calendar_data["weeks"]:
            for day in week["contributionDays"]:
                count = day["contributionCount"]
                color = _map_count_to_color(count, theme_colors)
                contrib_map[day["date"]] = {
                    'count': count,
                    'color': color
                }
        
        # Render heatmap
        today = datetime.date.today()
        r = PixelRenderer(width=53, height=7, cell="██", use_alt_screen=True)
        
        try:
            for week_idx, week in enumerate(calendar_grid):
                if week_idx >= r.width:
                    break
                    
                for day_idx, date in enumerate(week):
                    if day_idx >= r.height:
                        break
                    
                    if date <= today:
                        date_str = date.strftime("%Y-%m-%d")
                        day_data = contrib_map.get(date_str)
                        
                        if day_data:
                            rgb_color = hex_to_rgb(day_data['color'])
                            r.set_pixel(week_idx, day_idx, rgb_color)
            
            r.render()
            
        finally:
            r.cleanup(preserve_final_frame=True)
            
    except Exception as e:
        print(f"Error: {e}")
