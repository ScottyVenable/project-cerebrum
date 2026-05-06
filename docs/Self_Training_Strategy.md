# Cerebrum Self-Training & Calibration Strategy

## 1. The Protocol (Motor Imagery - Graz Paradigm)
To train the AI on your brain, you will use a "closed-loop" session protocol.

### Session Structure
*   **Total Trials:** 80 per session (40 Left Hand, 40 Right Hand).
*   **Trial Sequence:**
    1.  **Rest (2.0s):** Focus on a static cross.
    2.  **Cue (1.25s):** An arrow appears pointing left or right.
    3.  **Task (4.0s):** Perform "Kinaesthetic Motor Imagery"—feel the sensation of movement without actually moving.
    4.  **Break (1.5s):** Relax and blink.

## 2. Data Collection (Offline Phase)
Before the BCI works, you must be the "teacher."
*   Run the `applications/calibration_ui.py`.
*   Data is saved as `.xdf` or `.csv` with LSL timestamps.
*   Use a Python script (to be developed) to extract Mu (8-13Hz) and Beta (13-30Hz) features using Common Spatial Patterns (CSP).

## 3. Real-time Neurofeedback (Online Phase)
Once accuracy exceeds 70%:
*   The Hub will provide a real-time "Power Bar."
*   As you imagine movement, the bar fills. 
*   **Goal:** This allows your brain to "see" its own signals, creating a symbiotic learning loop between the AI and your sensorimotor cortex.

## 4. Electrode Placement for Solo Training
Focus on the **C3, Cz, and C4** positions (10-20 system).
*   **C3:** Over the left hemisphere (Right hand control).
*   **C4:** Over the right hemisphere (Left hand control).
*   **Cz:** Central reference.
*   **Ground:** Behind the ear (Mastoid).
