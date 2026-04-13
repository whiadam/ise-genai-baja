# Usability Test — Event Creation Assistant

## Intro

My name is Jeffrey and I'm working on the Event Creation Assistant, an app that uses an AI agent to help students get campus events added to the calendar. Students can chat with the agent, take photos of flyers, or upload flyer images, and the agent handles extracting event details and submitting them. I asked two participants to test the paper prototype. I told them to imagine they were using a real app and to think out loud while completing the tasks.

Participant 1: A college student who goes to campus events regularly and is comfortable using apps.
Participant 2: A college student who doesn't really follow campus events and mostly uses their phone for texting and social media.

## Tasks

### Task 1
You know about a study group happening in the library this Thursday at 5 PM but there's no flyer for it. You want to get it listed on the campus calendar using this app.

### Task 2
You took a photo of a flyer on the bulletin board and the app pulled out some event details, but the time it found is wrong. You need to fix it before the event gets submitted.

## Notes

### Participant 1
- For Task 1, looked at all three tabs and picked Chat right away
- Typed into the text box but paused before sending — said "do I just tell it the details?"
- Wasn't sure how specific to be or what format the agent expected
- Said "I guess I'd just say 'there's a study group Thursday at 5 in the library' and see what happens"
- For Task 2, started in Chat and said "I'd just tell it the time is wrong"
- Paused and asked "wait, does it show me what it found first so I can check it?"
- Wasn't sure where the extracted details would appear or how to review them before submitting

### Participant 2
- For Task 1, looked at Chat but hesitated — said "what do I even say to this?"
- Didn't realize they could just describe the event in plain language
- Tried tapping on the existing messages in the chat history thinking they might be templates or suggestions
- Eventually typed something but said "I hope this is right, I don't know what it wants"
- For Task 2, wasn't sure how to correct the agent — said "do I just say 'that's wrong'?"
- Looked for an edit button or a way to tap on the extracted info directly
- Said "I'd rather just fix the field myself than explain it to a chatbot"

## Feedback

### Participant 1
- Said chatting with the agent felt natural once they got going but the first message was intimidating
- "I didn't know what to say at first. Some kind of example or hint would help."
- Thought reviewing and correcting extracted info should be more visual, not just back-and-forth in chat
- Rated Task 1 about a 4/5, Task 2 about a 3/5

### Participant 2
- Said the blank chat screen didn't give enough guidance on what the agent can do
- "I've never used a chatbot like this. I didn't know I could just talk to it normally."
- Wanted to be able to directly edit fields instead of explaining corrections through chat
- Rated Task 1 about a 2/5, Task 2 about a 2/5

## Results

### Issue 1: No guidance on what to say to the agent
Both participants hesitated before their first message because the chat screen didn't indicate what the agent expects or what it can do. The blank input and existing messages didn't help new users get started.
Remedy: Add a welcome message or starter prompts like "Tell me about an event" or "I found a flyer" so users know how to begin.

### Issue 2: Users weren't sure how to review extracted event details
When the agent pulls info from a flyer, users expected to see the details laid out in editable fields, not buried in chat messages. Reviewing accuracy through conversation felt slow and unclear.
Remedy: Show a summary card with the extracted event details (title, date, time, location) that users can review and edit directly before confirming submission.

### Issue 3: Correcting the agent through chat felt unnatural
Both participants wanted to tap on a wrong field and fix it rather than type out a correction in the chat. Participant 2 in particular said they'd rather edit a form than argue with a chatbot.
Remedy: When the agent extracts event info, present it in an editable form view so users can make corrections directly instead of going back and forth in chat.

### Issue 4: Less tech-savvy users didn't realize they could use natural language
Participant 2 didn't understand that they could just describe an event in plain English. They expected more structure or prompts from the app.
Remedy: Include example prompts or a short onboarding message explaining that users can describe events however they want and the agent will figure out the details.
