# Interview Kit: How to Explain the Prototype

## 30-second version
I started building a workflow automation prototype for flagged-case triage. The prototype takes synthetic risk signals like VPN detection, location mismatch, device mismatch, spoofing flags, and suspicious session history, then produces an explainable risk score, recommended next action, and analyst-ready summary. I focused on reducing repetitive analyst work rather than trying to rebuild a fraud engine.

## 60-second version
What interested me about GeoComply is that the company sits at the intersection of geolocation compliance, fraud prevention, and device intelligence. I wanted to explore where business automation could create value around those signals. So I built a small prototype that simulates first-pass investigation support for flagged cases. It aggregates mock signals, applies transparent scoring rules, then drafts a consistent case summary and recommended action. My thinking was that if a team already has strong signal intelligence, one high-impact automation opportunity is reducing manual triage effort, speeding up escalations, and improving consistency across investigations.

## Architecture
Flagged case -> signal aggregation -> rule-based scoring -> summary generation -> analyst queue/dashboard

## Key talking points
- I intentionally used synthetic data because I do not have access to real internal data.
- I chose explainable rules first because trust and auditability matter in compliance workflows.
- This is a workflow-automation prototype, not a claim that I rebuilt GeoComply's core detection stack.
- The next iteration would be integration into Jira/Slack/case management tools.

## If they ask "Why not ML first?"
Because in a high-risk operational workflow, I wanted a first version that is transparent, easy to validate, and simple for stakeholders to challenge. Once the workflow is stable, a team can evaluate whether machine learning improves prioritization.

## If they ask "What metric would you track?"
- analyst time per case
- percent of cases auto-summarized
- escalation turnaround time
- summary consistency / analyst edits required
- false positive review effort

## If they ask "What would you do next?"
1. Add workflow routing for high-risk cases.
2. Add analyst feedback capture.
3. Track overrides to improve rules.
4. Connect to an ops dashboard measuring time saved.
