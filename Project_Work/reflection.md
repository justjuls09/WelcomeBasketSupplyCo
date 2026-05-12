# Sprint 7 Reflection — Welcome Basket Supply Co.

## What went well?
I successfully installed Streamlit and verified it worked by launching the demo app in the browser. I learned the difference between running commands in the terminal versus the Python interpreter, and I resolved a real syntax error by reading the Streamlit traceback and removing stray backticks. After that, I built a working Streamlit UI with kit type selection and quantity input, which confirmed my app reruns correctly and responds to user interaction.

## What could you have done better?
I could have avoided the syntax error by using a code editor with linting and line numbers earlier instead of relying on Notepad. I also could have tested smaller code edits more frequently to isolate problems faster.

## What could I have done better?
I could have captured and shared the full error message earlier to speed up debugging. I also could have planned the session-state design first so the Grand Total feature fit naturally into the initial structure rather than being added after the UI was working.

## What have we learned?
Streamlit reruns the script from top to bottom during interaction, so state must be managed intentionally using st.session_state. Debugging is faster when I trust the traceback line number and fix the specific problem instead of guessing. Finally, keeping business logic in the WelcomeKitOrder class and using Streamlit only for UI produces cleaner, more maintainable code and a more professional final product.