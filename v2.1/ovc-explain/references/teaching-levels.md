# Teaching at each level, and designing the check-yourself questions

Load this when writing the guide. The goal is not a long document. It is that
the builder can **explain what exists, change it safely, and know what is and
is not proven**.

## Why the guide is built this way

A randomized trial of developers learning a new library (Shen and Tamkin,
arXiv 2601.20245, 2026; the authors work at an AI developer, so read the
limitations) found that 52 mostly junior developers using AI averaged 50% on a
comprehension quiz against 67% for hand-coders: 17 percentage points lower,
with the biggest gap in debugging. Within the AI group, the best results (65%
or higher) came from people who asked conceptual questions, asked for
explanations alongside code, or used the AI to check their own understanding.
The worst (under 40%) came from handing everything over. The subgroups were
tiny (2 to 7 people), the quiz came minutes after the task, the assistant was a
chat sidebar, and the analysis does not establish cause. It is a strong hint,
not a law.

So the guide: ties every explanation to real code, asks the reader questions,
and never lets "the AI built it" stand in for "I can explain it".

## Beginner

- Everyday words. One new idea at a time. Define a term the first time it
  appears, with a picture from daily life (a kitchen, a library, a post office).
- Follow **one real action** from click to result before showing structure.
  Orientation first ("here is what happens when you press Start"), then the map.
- Say what each file is *for* and when you would open it. Never list a file
  without a purpose.
- After each major section in the interactive tour, ask one small question and
  wait.
- Be honest and calm about gaps: "this part is written but not tested in a
  browser yet" is useful, not shameful.
- End with 3 "what to learn next" pointers tied to what they just saw.

## Intermediate

- Assume they know the language. Explain the architecture, the data flow, and
  the *reasons* for choices, and the trade-offs (what each choice costs).
- Call out the 2 to 3 places most likely to cause trouble.
- Link to the decision log for each non-obvious choice.

## Expert

- Skip tutorials. Give the map, the invariants (things that must stay true), the
  contracts between parts, the runbook (build, test, deploy, debug), measured
  performance, and the list of known gaps and unverified claims.
- Use file:line pointers instead of prose wherever possible.

## Designing "Check yourself" questions

Write questions about **this project**, answerable by reading the guide and the
named files. Mix types, and make each answer checkable with a `file:line`:

| Type | Example | Tests |
|---|---|---|
| Locate | "Which file decides when focus switches to break?" | Can they find things |
| Predict | "If the browser tab sleeps for 10 minutes, what does the timer show and why?" | Do they understand the design |
| Change | "You want a 15-minute break after four sessions. Which files change, and which tests?" | Can they modify safely |
| Debug | "The count resets at midnight, which you did not want. Where do you look first?" | The skill the study found weakest |
| Evidence | "Which requirement is only Partial, and what would make it Done?" | Do they know what is proven |

Counts: beginner 5 to 8, intermediate 3 to 5, expert optional. Avoid trivia
("what colour is the button") and avoid yes/no. Answers never repeat the
question; they explain and point to code.

## Interactive tour and quiz mode (offer it to beginners and intermediates)

1. Offer: "Want me to walk you through it one part at a time, and ask you a
   question after each?"
2. Present one section, then one question. Wait for the answer.
3. If right: confirm and add one detail they might not have noticed. If
   partly right: say what was right, then give the missing piece with a file
   pointer. If wrong: explain gently, show the code, ask a simpler follow-up.
4. Never reveal the stored answers early; use them as your reference.
5. At the end, summarise strengths, the two ideas to revisit, and where to read.
