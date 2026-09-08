# Results

| Condition (no context unless stated) | all | paraphrase (40) | unseen (20) | data (36) |
|---|---|---|---|---|
| base, fair prompt, no context | 0.031 | 0.025 | 0.100 | 0.000 |
| base + knowledge base in context (retrieval control) | 0.354 | 0.400 | 0.600 | 0.167 |
| adapter run 1, epoch 4 (48 steps) | 0.104 | 0.050 | 0.100 | 0.167 |
| adapter run 2, epoch 10 | 0.323 | 0.425 | 0.200 | 0.278 |
| adapter run 2, epoch 20 | 0.562 | 0.425 | 0.150 | 0.944 |
| **adapter run 2, epoch 30 (published)** | 0.573 | 0.425 | 0.200 | 0.944 |
| adapter run 2, epoch 30 + knowledge base in context | 0.458 | 0.550 | 0.350 | 0.417 |

Read the columns, not the total. On facts that are in the knowledge base (**paraphrase**) the adapter and retrieval are level. On facts never rendered for training (**unseen**) retrieval wins three to one: the adapter does not generalise beyond what it saw, and when pushed it confabulates plausible numbers (it answered the coil resonance as 7.81 Hz; the truth is 33.06). On per-month statistics (**data**) the adapter wins because those numbers are not in the knowledge-base text at all; that column measures memorisation of the corpus, which is the point of the adapter and also its limit.

A fourth condition, **adapter plus the knowledge base in context**, was run afterwards. It is the best on facts that are in the knowledge base (0.550), better than the bare adapter on unseen facts (0.350 vs 0.200) but still below retrieval alone (0.600), and much worse than the bare adapter on per-month data (0.417 vs 0.944) because the pasted text pulls answers toward its own phrasing. The practical reading: route per-month statistics to the adapter alone and everything else to a model with the knowledge base in context; that split would score about 0.71 on this set. Neither the adapter nor retrieval is the whole answer.
