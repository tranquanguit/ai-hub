---
type: skill-delta
key: skill.task-close.draft-stats
claim: task-close should record stats for draft skills used in real tasks and avoid
  the positional-count re.sub DeprecationWarning
value: null
source: tasks/2026-11-10-ops-review-w45/LEDGER.md
confidence: medium
tags:
- task-close
- task-start
task: 2026-11-10-ops-review-w45
verification:
  kind: tool
  evidence: tasks/2026-11-10-ops-review-w45/LEDGER.md
created: '2026-11-10'
---
close_task.py printed 'skills=ops-review' but ops-review/stats.json was not updated (only .claude/skills/ is checked). Python 3.13 DeprecationWarning at close_task.py:108 and start_task.py:111.
