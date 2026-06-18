<span style="font-size: 20px;">

# BDT Training AUC Analysis

**User:** Anonymous  
**Created:** 6/6/2026 13:05:13  
**Updated:** 6/6/2026 13:20:47  
**Exported:** 6/6/2026 13:26:06  
**Link:** [https://chatgpt.com/g/g-p-68bc1f6445088191b4003a694b28baf3-fcc-ee/c/6a23f0d7-85c0-83ed-a942-e77e3f07782b](https://chatgpt.com/g/g-p-68bc1f6445088191b4003a694b28baf3-fcc-ee/c/6a23f0d7-85c0-83ed-a942-e77e3f07782b)  

## Prompt:
6/6/2026, 1:20:17 PM

> params \= {  
> 'objective': 'binary:logistic',  
> 'eval\_metric': 'auc',  
> 'learning\_rate': 0.05,  
> 'max\_depth': 3,  
> 'n\_estimators': 150,  
> 'subsample': 0.8,  
> 'colsample\_bytree': 0.8,  
> 'min\_child\_weight': 20,  
> 'gamma': 5,  
> 'seed': 42,  
> }

can you explain the different hyperparamters?

## Response:
6/6/2026, 1:20:18 PM

For XGBoost, the hyperparameters can roughly be divided into three categories:

1. **How complex each tree can become**
2. **How many trees are built**
3. **How strongly you regularise (prevent overfitting)**

I'll focus on the parameters in your example and explain their impact in the context of an FCC-ee HEP analysis.

---

## `max_depth`

```python
max_depth = 3
```

This is the maximum depth of each decision tree.

A depth-1 tree makes only one split:

```text
if recoil_mass > 120:
    signal
else:
    background
```

A depth-3 tree can make a sequence of splits:

```text
if recoil_mass > 120:
    if WW_mass > 70:
        if miss_energy > 30:
            signal
```

A depth-8 tree can learn extremely complicated regions.

### Effect

- Larger depth:
  - more powerful
  - more likely to overfit
  - can memorise rare events

- Smaller depth:
  - simpler model
  - more robust
  - often preferred in HEP

Typical values:

```text
2–4  conservative
5–8  aggressive
>10  usually excessive
```

For your sample size (~40k events), I'd start with:

```python
max_depth = 3
```

---

## `n_estimators`

```python
n_estimators = 150
```

Number of trees.

A BDT works by building trees sequentially.

Tree 1:
- separates signal/background

Tree 2:
- focuses on mistakes made by Tree 1

Tree 3:
- focuses on remaining mistakes

etc.

### Effect

More trees:

- higher capacity
- longer training
- higher overfitting risk

Typical range:

```text
50–200    modest
200–500   common
>1000     usually requires strong regularisation
```

---

## `learning_rate`

```python
learning_rate = 0.05
```

Also called `eta`.

This controls how much each new tree contributes.

Imagine Tree 1 says:

```text
signal probability = 0.9
```

With

```python
learning_rate = 1.0
```

you take the full correction.

With

```python
learning_rate = 0.05
```

you only take 5% of the correction.

### Effect

Small learning rate:

- slower learning
- smoother model
- less overfitting

Large learning rate:

- faster learning
- more unstable
- more overfitting

Typical values:

```text
0.01–0.05 very conservative
0.05–0.10 common
0.20–0.30 aggressive
```

Your original

```python
learning_rate = 0.20
```

is quite aggressive.

---

## `subsample`

```python
subsample = 0.8
```

For each tree, use only a random fraction of events.

Example:

```python
subsample = 0.8
```

means:

- randomly choose 80% of training events
- build the next tree using only those

### Effect

This introduces randomness.

Benefits:

- reduces overfitting
- reduces correlation between trees

Typical values:

```text
0.6–0.9
```

---

## `colsample_bytree`

```python
colsample_bytree = 0.8
```

Same idea, but for variables.

You have about 35 variables.

With:

```python
colsample_bytree = 0.8
```

each tree sees only ~28 randomly chosen variables.

### Effect

- prevents over-reliance on one feature
- reduces overfitting
- often improves generalisation

Especially useful when variables are highly correlated.

In your analysis:

```text
lep0_p
lep1_p
zll_p
WW_p
...
```

many variables are correlated.

---

## `min_child_weight`

```python
min_child_weight = 20
```

One of the strongest anti-overtraining parameters.

Suppose a split creates a leaf containing only:

```text
5 events
```

The tree might learn a completely accidental fluctuation.

`min_child_weight` forbids such tiny leaves.

Higher value:

```python
min_child_weight = 20
```

means:

> Don't create leaves unless they contain enough statistics.

### Effect

Large value:

- smoother classifier
- less overtraining

Small value:

- more detailed structure
- higher risk of memorisation

For HEP analyses:

```text
1–5     flexible
10–30   conservative
```

---

## `gamma`

```python
gamma = 5
```

Another anti-overfitting parameter.

A split is only accepted if it improves the loss function by at least `gamma`.

Think of it as:

> "How much improvement must a split provide before I allow it?"

### Effect

Small gamma:

```python
gamma = 0
```

accept almost every split.

Large gamma:

```python
gamma = 5
```

only keep important splits.

Typical values:

```text
0     no penalty
1–5   moderate
>10   very restrictive
```

---

## `objective`

```python
objective = "binary:logistic"
```

You're doing binary classification:

```text
signal = 1
background = 0
```

The output becomes:

```text
0 → background-like
1 → signal-like
```

This is exactly what you want.

---

## `eval_metric`

```python
eval_metric = "auc"
```

Metric monitored during training.

Common choices:

```python
"auc"
"logloss"
"error"
```

For HEP classification I usually prefer:

```python
eval_metric = "auc"
```

because ultimately you care about signal/background separation.

---

## Which parameters matter most for your overtraining?

In your case I would focus on:

```python
max_depth
n_estimators
learning_rate
min_child_weight
```

These have the biggest impact.

A good conservative starting point would be:

```python
params = {
    'objective': 'binary:logistic',
    'eval_metric': 'auc',

    'max_depth': 3,
    'n_estimators': 150,
    'learning_rate': 0.05,

    'subsample': 0.8,
    'colsample_bytree': 0.8,

    'min_child_weight': 20,
    'gamma': 5,

    'seed': 42,
}
```

Then monitor:

- Training AUC
- Validation AUC
- KS test or train-vs-validation score distributions

A model with training AUC ≈ 0.98 and validation AUC ≈ 0.96 is generally preferable to a model with training AUC = 1.00 and validation AUC = 0.96, because it is usually more stable when applied to independent Monte Carlo samples or real data.



---
Powered by [ChatGPT Exporter](https://www.chatgptexporter.com)
</span>