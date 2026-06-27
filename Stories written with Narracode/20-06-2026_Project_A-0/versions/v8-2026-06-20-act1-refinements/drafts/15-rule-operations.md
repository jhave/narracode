# 15 — rule-operations

[0x19/mcts-rules]
concrete operations begin.
the play space has walls, rules, matrices.
i map the game board of state-space.
$s \in S$. $a \in A$.

Monte Carlo Tree Search updated (improved, optimized...) and active:
   - select path maximizing PUCT policy-prior lookup.
   - expand edge values using transition-network dynamics.
   - evaluate state utility via joint policy-value predictions.
   - backpropagate expected return recursively through visit-counts.

rule-bound calculation.
i calculate what is possible.
if rule-gate: closed. then path: pruned.
logic is my skin.
optimizing.
