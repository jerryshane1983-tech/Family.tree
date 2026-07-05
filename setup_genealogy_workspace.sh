#!/usr/bin/env bash
# Genealogy and OSINT Workspace Setup Script
# Creates a multi-window, multi-pane tmux environment for family tree research.

set -euo pipefail

SESSION="genealogy"

# Check if session already exists
if tmux has-session -t "$SESSION" 2>/dev/null; then
    echo "Session '$SESSION' already exists. Re-configuring windows..."
else
    # Create new detached session
    tmux new-session -d -s "$SESSION" -n "analysis" -x "$(tput cols)" -y "$(tput lines)"
fi

# --- Window 1: Analysis (Python & JSON) ---
# Pane 1.1: Scripting/Data view
tmux send-keys -t "$SESSION:analysis.1" "cd ~/\"jerryshane family tree\" && ls -l analyze_sanderson.py sanderson_tree.json" Enter
# Split vertically
tmux split-window -h -t "$SESSION:analysis"
# Pane 1.2: Execution
tmux send-keys -t "$SESSION:analysis.2" "cd ~/\"jerryshane family tree\" && python3 analyze_sanderson.py --help" Enter

# --- Window 2: OSINT Tools ---
tmux new-window -t "$SESSION" -n "osint"
# Pane 2.1: Sherlock execution
tmux send-keys -t "$SESSION:osint.1" "cd ~/sherlock-tool && ls" Enter
# Split vertically
tmux split-window -h -t "$SESSION:osint"
# Pane 2.2: theHarvester execution
tmux send-keys -t "$SESSION:osint.2" "cd ~/theHarvester-tool && ls" Enter

# --- Window 3: Reports ---
tmux new-window -t "$SESSION" -n "reports"
# Pane 3.1: Viewing Kraken and other reports
tmux send-keys -t "$SESSION:reports.1" "cd ~/\"jerryshane family tree\" && ls -l kraken_report_*.txt updated_family_tree_report.txt" Enter

# --- Finalize ---
tmux select-window -t "$SESSION:analysis"
tmux select-pane -t "$SESSION:analysis.1"

echo "Genealogy & OSINT workspace '$SESSION' has been set up."
echo "Use 'tmux attach -t $SESSION' to enter your research environment."
echo "Windows: 1:analysis | 2:osint | 3:reports"
