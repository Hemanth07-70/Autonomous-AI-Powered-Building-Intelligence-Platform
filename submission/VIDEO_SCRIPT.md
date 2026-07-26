# PoC Demo Video Script (<= 3:00)

Target duration: 2:40 to 2:55

## 0:00 - 0:20 | Problem + Goal
Narration:
- "This is IntelliBuild AI, an autonomous building intelligence platform."
- "Our goal is to reduce total building energy consumption while maintaining thermal comfort boundaries."

Screen:
- Show dashboard landing view and system status.

## 0:20 - 0:55 | Live Telemetry and Context
Narration:
- "We begin with live building context in the Digital Twin and Buildings views."
- "The selected building context is shared across modules so decisions remain scoped and traceable."

Screen:
- Open Buildings page.
- Open one building details view.
- Open Digital Twin page and select building context.

## 0:55 - 1:35 | AI Decision Generation
Narration:
- "In AI Copilot, we submit an operational goal, for example optimizing HVAC scheduling."
- "The backend returns a structured decision goal with priority and building scope."

Screen:
- Open AI Copilot.
- Show prompt submission.
- Show returned structured goal fields.

## 1:35 - 2:15 | Closed-Loop Execution
Narration:
- "The decision is translated into an execution plan and simulation jobs."
- "EnergyPlus simulation runs asynchronously through the scheduler."
- "This loop allows us to evaluate control updates safely before real-world rollout."

Screen:
- Show simulation queue/job lifecycle.
- Show decision/execution status transitions.

## 2:15 - 2:45 | Quantitative Savings Proof
Narration:
- "Here we compare baseline and optimized operation."
- "Energy use drops by X percent while comfort remains inside accepted temperature bands."

Screen:
- Show your chart/table from submission/QUANT_SAVINGS_TEMPLATE.csv populated with real run data.
- Highlight baseline kWh, optimized kWh, reduction %, comfort compliance %.

## 2:45 - 2:55 | Wrap-up
Narration:
- "IntelliBuild AI demonstrates a robust autonomous control loop combining LLM reasoning, digital twin validation, and measurable energy savings."

Screen:
- Return to architecture slide or final dashboard summary.

## Recording Checklist
- Keep video under 3 minutes.
- Use readable zoom and large fonts.
- Avoid dead time while waiting for jobs; prepare one pre-run and one completed example.
- Mention constraints explicitly: energy + comfort.
