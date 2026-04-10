# Usability Test

## Intro
We are students developing a Campus Info App with an Alerts page. In this usability test, participants will interact with paper prototypes for two new features: an Active Alert Carousel and a GenAI Smart Alert Summary. The participant should imagine they are a student trying to manage campus reminders efficiently. They were asked to speak aloud while using the prototype and explain what they expected to happen before each action.

## Tasks

### Feature 1: Active Alert Carousel
Task:
You are checking your campus alerts and want to quickly browse through your current active reminders without scrolling through a long page. Show how you would move through your alerts and find one that seems important.

### Feature 2: GenAI Smart Alert Summary
Task:
You open the Alerts page and want to quickly understand what reminders matter most today. Show how you would use the page to understand your schedule and find the most urgent alert.

## Notes

### Participant 1
- Understood that the alert card was the current active alert
- Initially did not notice the right arrow
- Expected a visual indicator to show how many alerts existed
- Thought the summary was useful but wanted it higher on the page
- Hesitated before pressing “Refresh Summary” because they were unsure what would change

### Participant 2
- Quickly understood the carousel interaction
- Expected swipe gestures because the design looked mobile-like
- Said the summary was helpful but wanted clearer labels like “Urgent” or “Recurring”
- Looked for the summary near the top of the alert section
- Wanted a shorter version of the summary first, with an option to expand

## Feedback

### Participant 1
- The carousel felt easier than scrolling through many alerts
- The arrows were too easy to miss
- The summary was useful for getting a quick overview
- Suggested stronger emphasis on the most urgent alert

Quote:
“I like the idea, but I didn’t notice the next button right away.”

### Participant 2
- The card view felt cleaner and more organized
- Wanted to know whether there were more alerts without guessing
- Preferred a short summary first and details second

Quote:
“This makes more sense than reading all those alert cards one by one.”

## Results

### Issue 1: Carousel navigation was not immediately visible
Hypothesis:
The arrows were too small and did not stand out enough from the card layout.
Remedy:
Increase arrow size, add stronger contrast, and include position indicators such as dots and “2 of 8”.

### Issue 2: Users wanted stronger awareness of alert count
Hypothesis:
Showing only one card at a time made it unclear how many alerts remained.
Remedy:
Add a progress label and dot indicators below the active alert card.

### Issue 3: Summary placement was not prominent enough
Hypothesis:
Users naturally scan near the top of the page for overview information.
Remedy:
Move the Smart Summary box higher on the page, above or beside the active alert area.

### Issue 4: Users wanted the summary to identify urgency more clearly
Hypothesis:
The summary text alone was not enough to guide quick action.
Remedy:
Highlight the most urgent alert in a separate badge or callout box and label key items such as “Urgent” or “Recurring”.
