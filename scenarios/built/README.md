# Built scenarios

The eight episodes of the paper, generated in its strongest condition — the v2
fidelity rubric plus the three lines of extracted API fact (the 4.10 arm).

Each `.aoe2scenario` ships with a `.meta.json` sidecar recording the full config,
the pinned model, attempt count, and trigger count. `results.jsonl` is the
append-only attempt log for the run, failures included.

| File | Episode | Triggers | Attempts |
|------|---------|----------|----------|
| `marco_polo_on_the_silk_road` | Marco Polo on the Silk Road | 12 | 1 |
| `the_battle_of_hastings` | The Battle of Hastings | 11 | 1 |
| `the_battle_of_tours` | The Battle of Tours | 14 | 1 |
| `the_exile_of_el_cid` | The Exile of El Cid | 14 | 1 |
| `the_fall_of_constantinople` | The Fall of Constantinople | 20 | 2 |
| `the_rise_of_temujin` | The Rise of Temujin | 16 | 1 |
| `the_road_to_reims` | The Road to Reims | 16 | 1 |
| `the_siege_of_vienna` | The Siege of Vienna | 18 | 1 |

Condition, identical across all eight: `anthropic/claude-sonnet-5-20260630`,
generator 2.4, fidelity prompt v2 (hash `131776fb33b105c4`), temperature 0.0,
best-of-1, up to 3 repairs, introspection-guided repair on, freeform prompt
style, reachability prompting off.

A static reachability audit passes 8/8 — every scenario has both a victory and a
defeat path, and no orphan triggers.

## Playing one

Copy a `.aoe2scenario` into:

```
C:\Users\<USERNAME>\Games\Age of Empires 2 DE\<STEAM_ID>\resources\_common\scenario\
```

then in-game: **Editors -> Scenario Editor -> open it -> Menu -> Test**.

## Reproducing

```
cd code
python tools/run_factorial.py --cells fidelity --root output/paper8_api --workers 4
```

Requires `OPENROUTER_API_KEY`. Generation is not bit-reproducible even at
temperature 0.0: a re-run of Tours in this batch produced materially different
code from its first attempt.
