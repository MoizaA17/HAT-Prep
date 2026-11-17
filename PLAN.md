# HAT Quant Coach (working title)

An AI-assisted web app that helps graduates prepare for the **Quantitative Reasoning** section of the HEC HAT-I test: learn a topic, practise under time pressure, and get AI feedback on mistakes.

---

## 1. Problem

- HEC HAT is required for MS admissions in Pakistan. HAT-I (Engineering, CS, Maths, Stats, Physics) is 40% Quantitative Reasoning, about 40 of 100 MCQs.
- The test has 100 MCQs in 120 minutes, about **72 seconds per question**. Most candidates cannot solve the quant questions in time without short tricks.
- Students study and still feel unprepared because they cannot tell what they truly know from what only feels familiar, and they do not know if they are fast enough.
- I am facing this problem myself, so I am user number one.

## 2. Goal (one sentence)

> A HAT-I candidate can pick a quantitative topic, learn it with worked examples and a short trick, take a timed confidence test, and get AI feedback on their mistakes and a personal study plan.

## 3. Target user

Graduates (BS holders) preparing for HAT-I, mainly for MS/MPhil admission.

## 4. Scope of the 3-day sprint (v1)

### Must have
- [ ] Topic picker with **2 active topics**: Ratio & Proportion, Percentages
- [ ] Other topics shown as "coming soon" (Algebra, Averages, Profit & Loss, etc.)
- [ ] Lesson per topic: basics, worked examples, short trick (and when it does not work)
- [ ] Timed MCQ test (10 questions per topic) with a **Sure / Not sure tap before each answer**
- [ ] Per-question timer, target 72 seconds
- [ ] Score with a band label and advice (see section 7)
- [ ] Result report: confidence grid and a "correct but too slow" list
- [ ] **AI Feature 1: Mistake Explainer**
- [ ] **AI Feature 2: Personalized Study Advice**
- [ ] Public GitHub repo with README, screenshots, and a 2-3 minute demo video

### Nice to have (only if time is left)
- Saved progress history
- A "retake only my weak questions" button
- Urdu hints

### Not now (roadmap, in this order)
1. **Ask-a-doubt box:** the student asks about the lesson and the AI answers using only the lesson text
2. **Live question generation + verification:** AI writes new questions, Python checks the answers, only verified ones are shown
3. More topics, then Verbal and Analytical sections
4. Login and accounts, mobile app

## 5. User flow (4 screens)

1. **Topic picker:** choose Ratio & Proportion or Percentages (others greyed out)
2. **Lesson:** basics, then worked examples, then the short trick
3. **Test:** question, Sure / Not sure tap, answer, timer, next
4. **Result:** score, band, confidence grid, slow questions, AI explanations of mistakes, AI study advice

## 6. Content design

### Lesson template (same for every topic)
1. What you must know first (basics only, no history)
2. Worked example 1 (normal method, step by step)
3. Worked example 2
4. Short trick, plus when it works and when it fails
5. Two practice questions with answers

### Question format (JSON)
```json
{
  "id": "rp_001",
  "topic": "ratio_proportion",
  "question": "Divide 120 in the ratio 2:3.",
  "options": ["A. 40, 80", "B. 48, 72", "C. 50, 70", "D. 30, 90"],
  "answer": "B",
  "solution_steps": ["Total parts = 5", "120 / 5 = 24", "2 x 24 = 48 and 3 x 24 = 72"],
  "trick": "Divide by the total parts first",
  "difficulty": "easy",
  "target_seconds": 72
}
```

### Question bank rules
- At least 10 questions per topic, original (not copied from past papers or copyrighted books)
- **Every answer is verified with a Python script** before it goes into the JSON
- Exactly one correct option per question
- Every trick is tested on several numbers, and its limits are written down
- I manually review the questions before release

## 7. Scoring and advice

| Score | Label | Advice |
|---|---|---|
| 90-100% | Excellent | Move to the next topic |
| 75-89% | Good | Review the mistakes, then move on |
| 60-74% | Fair | Re-read the lesson, then retake |
| Below 60% | Poor | Re-learn the topic from the basics |

The band is decided by **code**, not by the AI.

### Confidence grid (Sure / Not sure vs right / wrong)

| | Right | Wrong |
|---|---|---|
| **Sure** | Solid | **Danger zone** (thought I knew it) |
| **Not sure** | Shaky (lucky or half-known) | Known gap |

### Time check
A correct answer that took longer than the target (72 seconds) is flagged as **"correct but too slow"**.

## 8. AI features

### AI Feature 1: Mistake Explainer
- **When:** after the test, for each wrong answer
- **Input given to the AI:** question, options, the verified correct answer, the verified solution steps, the student's chosen option, their confidence tap, and time taken
- **Output:** a short explanation (about 80 words) of why the chosen option is wrong, the likely misconception, and a one-line tip
- **Guardrails:**
  - The AI must use only the provided solution steps and must never change the correct answer
  - If it cannot tell why the student erred, it says so
- **Fallback:** if the API fails, show the stored solution steps
- **Evaluation:** I read at least 10 generated explanations and check them for correctness and helpfulness

### AI Feature 2: Personalized Study Advice
- **When:** on the result screen
- **Input given to the AI:** topic, score and band, per-question times, and confidence grid counts
- **Output:** strongest area, main weakness, next action matching the band, and 2-3 specific things to practise
- **Guardrails:**
  - Code decides the band; the AI writes the advice around it
  - It may only refer to the data provided and must not invent numbers
- **Fallback:** a template message per band
- **Evaluation:** test with at least 5 different result patterns (e.g. fast and wrong, slow and right, many "danger zone" answers)

## 9. Architecture

```
Verified question bank + lessons (JSON/Markdown files)
        |
App (Streamlit): topic picker -> lesson -> timed test -> scoring
        |
AI layer: Mistake Explainer + Study Advice  (fallback if AI fails)
```

## 10. Tech stack (proposed, confirm during build)

- Python
- Streamlit for the interface
- An LLM API for the two AI features (API key stored in `.env`, never committed)
- JSON files for questions, Markdown or JSON for lessons
- Git and GitHub for version control

## 11. Risks and how I handle them

| Risk | What I do |
|---|---|
| AI writes wrong math or a wrong trick | Verify all answers with Python; AI features only use verified data |
| AI explanation is wrong or vague | Ground it in the stored solution steps; review 10 outputs; fallback text |
| API fails or is slow during a demo | Fallback to stored steps and band templates |
| Scope grows too big | Only 2 topics, only 2 AI features; extras go to the roadmap |
| API key leaks | `.env` plus `.gitignore`; rotate the key if ever exposed |
| HAT details are outdated | Verify the format and weights on the official ETC portal (etc.hec.gov.pk) |

## 12. Research notes

- HAT format: 100 MCQs, 120 minutes, no negative marking; HAT-I weights are Verbal 30%, Analytical 30%, Quantitative 40% 
- Existing tools: Anki, Brainscape (confidence ratings), Quizlet, RemNote, Khanmigo, NotebookLM, plus HAT prep sites
- My difference: confidence **before** the answer, time per question against the HAT pace, and AI feedback grounded in verified solutions 

## 13. Sprint schedule

| Day | Goal |
|---|---|
| Day 2 | Finish design; build the question bank (draft with AI, verify with Python); app skeleton, lesson screen, test screen |
| Day 3 | Result screen and scoring; both AI features; review 10 AI outputs; polish; README, screenshots, demo video; reflection notes |

**Rule:** no new features after Day 2 evening. If something takes over an hour to fix, simplify it.

## 14. Definition of done

- [ ] Two topics work from lesson to result
- [ ] All questions verified by script
- [ ] Both AI features work, with fallbacks
- [ ] README with screenshots and run instructions
- [ ] 2-3 minute demo video
- [ ] Reflection written: what worked, what was hard, what I would do next
