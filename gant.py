import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta


tasks = [
    # Sandy Wang
    {"id": "609", "summary": "fix test dashboard CORS issue",
     "start": "2025-11-21", "end": "2025-11-26",
     "assignee": "Sandy Wang", "status": "DONE", "color": "green"},

    {"id": "608", "summary": "https: add cert to test dashboard",
     "start": "2025-11-21", "end": "2025-11-26",
     "assignee": "Sandy Wang", "status": "DONE", "color": "green"},

    {"id": "607", "summary": "Add resource (RAM, ROM) for test dashboard",
     "start": "2025-11-21", "end": "2025-11-26",
     "assignee": "Sandy Wang", "status": "IN_PROGRESS", "color": "blue"},

    # Max Wen
    {"id": "602", "summary": "Integrate Test report to DB",
     "start": "2025-11-20", "end": "2025-11-26",
     "assignee": "Max Wen", "status": "IN_PROGRESS", "color": "blue"},

    # Gary Lee
    {"id": "599", "summary": "Enumerate each project ID's performance metric",
     "start": "2025-11-19", "end": "2025-11-26",
     "assignee": "Gary Lee", "status": "DONE", "color": "green"},

    {"id": "597", "summary": "ETL, extract coverage report data and feed into DB",
     "start": "2025-11-19", "end": "2025-11-26",
     "assignee": "Gary Lee", "status": "IN_PROGRESS", "color": "blue"},

    {"id": "595", "summary": "Show MCU performance metric in firmware report page",
     "start": "2025-11-18", "end": "2025-11-26",
     "assignee": "Gary Lee", "status": "DONE", "color": "green"},

    # Gary Lin
    {"id": "588", "summary": "[Tool dashboard] Fix the page cannot refresh/navigate issue",
     "start": "2025-11-17", "end": "2025-11-26",
     "assignee": "Gary Lin", "status": "IN_PROGRESS", "color": "blue"},

    {"id": "583", "summary": "[Tool] Add pldm pack utility",
     "start": "2025-11-14", "end": "2025-11-26",
     "assignee": "Gary Lin", "status": "IN_PROGRESS", "color": "blue"},

    {"id": "582", "summary": "[Tool] Add pldm unpack utility",
     "start": "2025-11-14", "end": "2025-11-26",
     "assignee": "Gary Lin", "status": "IN_PROGRESS", "color": "blue"},

    {"id": "581", "summary": "[opengrok] Add mcuapp source code",
     "start": "2025-11-14", "end": "2025-11-26",
     "assignee": "Gary Lin", "status": "IN_PROGRESS", "color": "blue"},

    {"id": "573", "summary": "[Tool] Add fw parser",
     "start": "2025-11-11", "end": "2025-11-26",
     "assignee": "Gary Lin", "status": "IN_PROGRESS", "color": "blue"},
]



# Sort by Assignee then by Start Date
tasks.sort(key=lambda x: (x['assignee'], x['start']))

# Timeline bounds: earliest issue creation date to ETA 11/26
earliest_start_date = min(datetime.strptime(task['start'], "%Y-%m-%d") for task in tasks)
chart_end_eta = datetime.strptime("2025-11-26", "%Y-%m-%d")

# Colors
colors = {
    "DONE": "#90EE90",       # Light Green
    "TODO": "#FFFACD",       # Lemon Chiffon (Yellowish)
    "IN_PROGRESS": "#ADD8E6" # Light Blue
}

# Plot Setup
fig, ax = plt.subplots(figsize=(14, 10))

y_labels = []
y_ticks = []

# Plotting
for i, task in enumerate(tasks):
    start_date = datetime.strptime(task['start'], "%Y-%m-%d")
    end_date = datetime.strptime(task['end'], "%Y-%m-%d")
    duration = (end_date - start_date).days
    if duration == 0: duration = 1 # Ensure single day tasks are visible

    color = colors.get(task['status'], "gray")

    ax.barh(i, duration, left=start_date, height=0.6, color=color, edgecolor='black', alpha=0.9)

    # Label format: [ID] Summary
    label = f"[{task['id']}] {task['summary']}"
    y_labels.append(label)
    y_ticks.append(i)

    # Status label above the bar for quick at-a-glance state
    status_label = None
    text_color = "black"
    if task['status'] == "DONE":
        status_label = "Done"
        text_color = "green"
    elif task['status'] == "IN_PROGRESS":
        status_label = "In Progress"
        text_color = "blue"

    if status_label:
        label_x = start_date + timedelta(days=duration / 2)
        ax.text(label_x, i, status_label,
                ha='center', va='center', fontsize=9, fontweight='bold', color=text_color)

# Formatting
ax.set_yticks(y_ticks)
ax.set_yticklabels(y_labels)
ax.set_xlabel("Date")
ax.set_title("Project Timeline by Assignee (Issue creation start → ETA 26-Nov)")
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
ax.grid(axis='x', linestyle='--', alpha=0.7)

# Add Assignee Grouping Text (Manual for simplicity in matplotlib)
# Group indices
groups = {}
group_label_x = chart_end_eta + timedelta(days=1)
for i, task in enumerate(tasks):
    assignee = task['assignee']
    if assignee not in groups:
        groups[assignee] = []
    groups[assignee].append(i)

# Draw lines between groups
for assignee, indices in groups.items():
    # Draw a line slightly above the last item of the group
    ax.axhline(y=indices[-1] + 0.5, color='grey', linewidth=0.8, linestyle='-')
    # Add text label for group
    mid_point = sum(indices) / len(indices)
    ax.text(group_label_x, mid_point, assignee,
            fontsize=12, fontweight='bold', color='green', rotation=0, va='center', ha='left')

ax.set_xlim(left=earliest_start_date - timedelta(days=0.5),
            right=group_label_x + timedelta(days=1))

plt.tight_layout()
plt.show()
