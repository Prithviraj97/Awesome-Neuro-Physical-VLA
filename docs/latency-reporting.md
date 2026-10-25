# Latency reporting standard

A timing number is useful only if a reader can tell what was timed, on what, and how. Every record in [`data/latency.yaml`](../data/latency.yaml) needs the fields below before it can be marked `verified: true`.

| Field | What to write | Why it matters |
| :--- | :--- | :--- |
| `latency_ms` | Value or range in ms | |
| `what_is_timed` | Which stages: preprocessing, vision encoder, backbone, action head, postprocessing, transfer to robot | Papers differ by tens of ms on this alone |
| `statistic` | single, mean, mean±std, or p50/p95/p99 | Control stability depends on the tail, not only the mean |
| `hardware` | Exact device and power mode, e.g. "Jetson AGX Orin 32GB, MAXN, clocks locked" | Desktop and edge numbers differ by several times |
| `precision` | fp32, bf16, fp16, int8, int4 | Quantization changes both speed and memory |
| `origin` | reported or measured | Keeps your measurements separate from claims |
| `source` | Table/section in the paper, or path to a log in `bench/` | Lets anyone check the number |

Recommended extras: batch size (usually 1 for control), number of camera views, image resolution, chunk length, action rate actually sent to the robot, power draw.

## Measured records

If you run a model yourself, commit the script and raw log under `bench/<model>/` and record:

- software versions (JetPack/CUDA/TensorRT or PyTorch),
- warm-up count and number of timed calls (at least 1,000 after warm-up),
- p50, p95 and p99 end to end, plus per-stage times if available.

## What not to report

- A single "real-time" claim without a number.
- Control-loop rate in place of inference latency. A policy can send commands at 50 Hz from a chunk computed once per second.
- "0 ms" for asynchronous methods. They hide latency from the robot; the inference still takes time and the commands are still based on old observations.
