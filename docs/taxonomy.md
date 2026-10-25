# Taxonomy

The list uses four axes, one for each part of the loop in the README diagram, plus two support sections. The codes are defined in [`data/taxonomy.yaml`](../data/taxonomy.yaml); this page explains how to use them.

## Scope rule

A paper belongs here if it changes at least one of:

1. the rate at which a learned model produces robot commands,
2. the delay between observation and actuation,
3. how a delayed or stale command is corrected before execution, or
4. how systems are evaluated under motion or delay.

Spatial representations, world models and compression methods enter through this rule. A 3D tokenizer is in scope because it changes encoding cost and robustness to scene motion; a 3D tokenizer evaluated only on static question answering is not.

## Assigning codes

- **Primary code** decides where the paper is listed. Pick the mechanism the paper contributes, not the model it builds on. Example: Real-Time Chunking is `2C` even though it is demonstrated on π0, which is `2A`.
- **Secondary codes** (up to three) record other axes the paper touches.
- **Classify by mechanism, not by name.** SpatialVLA has "spatial" in its name but adds 3D position encodings to 2D tokens without persistent 3D structure, so it is `1C`, not `1D`.
- **Offline vs online.** For `1D` and Axis III, say in the note whether the representation or model is used inside the control loop, for offline planning, or for generating training data. SplatSim uses Gaussian splatting for data generation, not as a runtime memory.

## Borderline cases

| Situation | Decision |
| :--- | :--- |
| Execution method demonstrated on an existing policy (RTC on π0) | Code the method (`2C`); the policy keeps its own entry |
| Industrial system with only a blog post (Helix) | Include with venue "Blog"; the note says it is not peer reviewed |
| Driving-only method | Exclude unless its delay handling transfers to manipulation and the note says how |
| General LLM quantization method (AWQ, SmoothQuant) | Include in `4A` when it is used for VLA or VLM backbones in robotics; the note says so |
| Survey | `S1` |

## Relation to the survey

The codes match the extraction schema of the planned survey on the timescale gap in embodied foundation models, so this repository can be released as that survey's data.
