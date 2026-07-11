# Retrieval practice

## What it is

The systematic use of low-stakes tests, prompts, or recall activities that make learners actively
pull information from memory, rather than re-exposing them to the material. Unlike passive review
(re-reading, highlighting), retrieval strengthens memory traces by repeatedly reconstructing
knowledge, improving long-term retention and transfer [P1][P2].

## Evidence tier

**High.** A 217-study meta-analysis found robust positive effects of practice testing over restudy
across lab and classroom contexts, including transfer tasks [P1]. Classic experiments show
repeated testing yields substantially better delayed retention than repeated studying [P2], and
retrieval outperforms even elaborative studying with concept mapping [P3]. A 2025 meta-analysis
found both covert (mental) and overt (written/spoken) retrieval enhance learning, with overt
significantly more effective [P4].

## When to use

- Factual and conceptual material where answers can be judged correct/incorrect [P1][P2].
- Effects are larger with at least a day between study and final test, and with mixed-format
  practice (recall + recognition) [P1].
- Holds up in real classrooms; especially helpful for secondary-school students [P1].
- Prefer overt retrieval (typed/written answers) over "think of the answer" prompts [P4].

## Boundary conditions & pitfalls

- **Backfires without feedback on hard items**: questions so difficult that learners repeatedly
  fail without corrective feedback reinforce errors and discourage engagement [P1][P4].
- **High stakes kill the effect**: heavily graded or competitive tests raise anxiety and shift
  attention to performance rather than learning [P1][P2].
- **Learners misjudge it**: restudy *feels* easier, so learners under-use testing unless the
  course structure nudges them into it [P2][P3] — the pipeline must schedule retrieval, not offer
  it as optional extra.

## Worked example

A physiology module introduces cardiac electrophysiology in short expository segments, then
immediately generates 5–7 low-stakes recall questions ("Explain why the AV node delays
conduction") answered in free text. The tool schedules these questions again at increasing
intervals over subsequent lessons, occasionally switching to mixed multiple-choice + short-answer
formats, with brief feedback after each attempt.

## Applying to code-heavy material

Recall prompts become *production* prompts: "write the function signature from memory,"
"predict this snippet's output before running it," or "re-implement yesterday's helper without
looking." Running the code supplies the corrective feedback the boundary conditions require —
cheaper and more reliable than grading free text. Avoid pure syntax trivia; target the API
shapes and failure modes the course actually reuses.
