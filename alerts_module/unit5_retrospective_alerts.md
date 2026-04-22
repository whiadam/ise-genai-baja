# Alerts Module Feature Retrospectives

## Feature Retrospective 1: Active Alerts Carousel

### What went well
The Active Alerts Carousel significantly improved the usability of the alerts page. Instead of displaying all alerts in a long vertical list, the carousel allowed users to focus on one alert at a time while still being able to navigate easily using arrow buttons. The addition of navigation controls and the "Jump to Urgent" feature made it intuitive and efficient. The UI looks more polished and aligns better with modern app design.

### What went poorly
One challenge was restructuring the existing alert display logic into a carousel without breaking existing functionality. There were also issues ensuring that session state updates (like the current index) worked correctly across reruns. Additionally, maintaining compatibility with existing unit tests required careful handling so that UI changes did not break test expectations.

### What we will do differently next time
In the future, we will design UI components like this in a more modular way from the beginning, instead of refactoring a large existing section. We will also plan state management (such as indexes and navigation) earlier to avoid rework. Breaking UI logic into helper functions earlier would make changes like this easier to implement and debug.

---
## Feature Retrospective 2: GenAI Smart Alert Summary

### What went well
The GenAI Smart Alert Summary successfully adds an advanced and unique feature to the app by summarizing alerts into a concise, user-friendly format. It integrates well with the BigQuery data and enhances the overall usefulness of the alerts page. The refresh button and loading spinner improve the user experience by making the feature interactive and responsive. This feature helps differentiate the app from others by incorporating AI in a meaningful way.

### What went poorly
Integrating GenAI introduced some challenges, including handling API setup, managing errors, and ensuring the feature did not interfere with testing. There were also issues with data formatting, such as missing fields (like preference) and ensuring the input to the model was consistent. Additionally, we had to be careful not to automatically call the model during tests to avoid failures or unnecessary API usage.

### What we will do differently next time
Next time, we will isolate AI-related functionality more clearly from the main application logic to simplify testing and debugging. We will also validate and standardize data earlier before passing it into AI models. Additionally, we will design fallback behaviors and error handling earlier in development to make the feature more robust.
