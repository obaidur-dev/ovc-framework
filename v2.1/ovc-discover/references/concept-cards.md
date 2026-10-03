# Concept cards (for beginners; load on demand)

Use these when a beginner meets a term they do not know, during the stack
choice or the interview. Give **one card at a time**, in your own words, then
continue. Define a term the first time it appears and do not repeat the card
unless asked. Intermediate and expert levels: skip unless asked.

Each card: what it is, an everyday picture, and why it matters for a decision.

| Term | What it is | Everyday picture | Why it matters here |
|---|---|---|---|
| Frontend | The part users see and click: pages, buttons, forms. | The shop window and counter. | Decides how it looks and feels, and how fast it appears. |
| Backend | The part users do not see: it stores data, applies rules, talks to other services. | The kitchen and stockroom. | Where logins, data, and secrets live, so most security work is here. |
| Database | Organized storage that survives restarts. | A filing cabinet with an index. | Slow questions to the database are the usual cause of a slow app. |
| API | A defined way for one program to ask another for something. | A restaurant menu: you order from a list, you don't walk into the kitchen. | Every API is a door that needs a lock (authentication). |
| Authentication vs authorization | Authentication: proving who you are. Authorization: what you are allowed to do. | Showing your ID at the door versus which rooms your pass opens. | Mixing them up is a very common security hole. |
| Hosting and deployment | Running your program on a computer that is always on and reachable. | Moving from cooking at home to running a restaurant. | Decides cost, speed for far-away users, and HTTPS. |
| Compiled vs interpreted | Compiled code is translated to machine instructions before it runs. Interpreted code is translated while it runs. | Reading a translated book versus having an interpreter beside you. | Compiled is usually much faster on heavy computing and catches mistakes earlier. |
| Static types | The language knows what kind of thing each value is (text, number, date) and refuses mismatches before running. | A form that will not accept letters in the phone-number box. | Catches most mistakes AI makes in seconds, before users see them. |
| Dependency (package) | Someone else's code your project uses. | Buying a ready-made part instead of building it. | Each one can be abandoned, buggy, or malicious. AI sometimes invents names that do not exist. |
| Test | A small program that checks another part of the program works. | A checklist you run after every change. | It is how "done" becomes provable instead of hoped-for. |
| Latency vs throughput | Latency: how long one request takes. Throughput: how many you handle per second. | One fast checkout versus many checkouts open at once. | Different goals, different fixes. Decide which one the project needs. |
| Cache | A saved answer you reuse instead of recomputing. | Writing a phone number on a sticky note. | Big speed-ups, but stale answers are the cost. |
| Profiling | Measuring where a program actually spends its time. | A fitness tracker for code. | Guessing what is slow is usually wrong. Measure first. |
