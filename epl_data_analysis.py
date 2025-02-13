import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Load the dataset
df = pd.read_csv('C:\\Users\\Asus\\Downloads\\pl-tables-1993-2024.csv')

# Ensure required columns exist
required_columns = ['season_end_year', 'team', 'position']
if not all(col in df.columns for col in required_columns):
    raise ValueError(f"The dataset must contain the following columns: {required_columns}")

# Convert Season to integer if necessary
df['season_end_year'] = df['season_end_year'].astype(int)

# Filter data for seasons 1993 to 2022
df = df[(df['season_end_year'] >= 1993) & (df['season_end_year'] <= 2022)]

# Get a full list of seasons and teams to ensure all data points are plotted
all_seasons = np.arange(1993, 2023, 1)
all_teams = df['team'].unique()

# Create a complete DataFrame ensuring all teams have a position for each season
full_data = []
for team in all_teams:
    team_data = df[df['team'] == team].set_index('season_end_year')['position'].reindex(all_seasons)
    full_data.append(pd.DataFrame({'Season': all_seasons, 'Team': team, 'Position': team_data}))

df = pd.concat(full_data).reset_index(drop=True)

# Pivot the DataFrame to have seasons as columns and teams as rows
pivot_df = df.pivot(index='Team', columns='Season', values='Position')

# Initialize the plot
fig, ax = plt.subplots(figsize=(12, 8))
ax.invert_yaxis()  # Invert y-axis to have 1 at the top
ax.set_xlabel('Season')
ax.set_ylabel('Position')
ax.set_yticks(np.arange(1, 23, 1))  # Set y-axis intervals from 1 to 22
ax.set_title('Premier League Team Positions Over the Years')

# Define the animation function
lines = {}

def animate(season):
    ax.clear()
    ax.invert_yaxis()
    ax.set_xlabel('Season')
    ax.set_ylabel('Position')
    ax.set_yticks(np.arange(1, 23, 1))
    ax.set_title(f'Premier League Team Positions - {season}')

    for team in pivot_df.index:
        positions = pivot_df.loc[team].dropna()
        seasons = positions.index
        if season in seasons:
            line, = ax.plot(seasons[seasons <= season], positions[seasons <= season], marker='o', linestyle='-', label=team, alpha=0.8, picker=True)
            lines[team] = line  # Store reference for interactivity

    ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize='small', ncol=2)  # Adjust legend position

# List of seasons to animate
seasons = sorted(pivot_df.columns.dropna())

# Create the animation
ani = FuncAnimation(fig, animate, frames=seasons, repeat=False)

# Function to highlight a selected team when clicked
def on_pick(event):
    picked_line = event.artist
    for team, line in lines.items():
        if line == picked_line:
            line.set_linewidth(3)  # Bold the selected team's line
            line.set_alpha(1)  # Make it fully visible
        else:
            line.set_linewidth(1)  # Reduce other lines
            line.set_alpha(0.2)  # Fade out other lines
    fig.canvas.draw()

# Connect the event handler
fig.canvas.mpl_connect('pick_event', on_pick)

# Save the animation
ani.save('C:\\Users\\Asus\\Downloads\\positions.gif', writer='imagemagick', fps=1)
# ani.save('premier_league_positions.mp4', writer='ffmpeg', fps=1)  # For MP4 output

plt.show()
