---
description: 'Industry-standard PyTorch conventions for writing clear, reproducible ML code'
applyTo: '**/*.py'
---

# PyTorch Coding Conventions

These rules reflect how PyTorch code is written on professional ML teams. The goal is
readable, reproducible, and debuggable models — not the shortest possible code.

## 1. Always Document Tensor Shapes

Write the shape of every non-obvious tensor in a comment next to where it's created or
transformed. This saves enormous debugging time.

```python
# x: (batch_size, in_features)
x = self.fc1(x)
# x: (batch_size, hidden_size)  ← shape changed, document it
```

## 2. Explicit Device Placement

Never hardcode `"cuda"` or `"cpu"`. Always select the device at the top of the script
and pass it down explicitly. This makes the code portable.

```python
# Good: device is selected once and passed everywhere
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = MyModel().to(device)
inputs = inputs.to(device)

# Bad: scattered and brittle
model = MyModel().cuda()
```

## 3. Use `torch.utils.data.Dataset` and `DataLoader`

Do not load all data into tensors manually. Always wrap your data in a `Dataset`
subclass and use `DataLoader`. This gives you batching, shuffling, and multi-process
loading for free, and it's the standard pattern in any production codebase.

```python
class MyDataset(torch.utils.data.Dataset):
    def __init__(self, data, labels):
        self.data = data        # assumes data is already loaded into memory (list or array)
        self.labels = labels

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, idx: int):
        return self.data[idx], self.labels[idx]

loader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)
```

## 4. Write Explicit Training Loops

Do not abstract the training step behind a base class or framework (e.g. avoid PyTorch
Lightning unless the project specifically uses it). An explicit loop is easier to
read, debug, and modify:

```python
for epoch in range(num_epochs):
    model.train()                       # enable dropout / batch norm training mode
    for inputs, targets in train_loader:
        inputs, targets = inputs.to(device), targets.to(device)

        optimizer.zero_grad()           # clear gradients from previous step
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()                 # compute gradients
        optimizer.step()                # update weights
```

## 5. Set Random Seeds for Reproducibility

Any script that trains or evaluates a model must set seeds at the top. This ensures
that two runs on the same machine produce the same result — critical for debugging.

```python
import random
import numpy as np

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)
```

## 6. Separate `train()` and `eval()` Modes

Always call `model.train()` before the training loop and `model.eval()` before
validation/inference. Forgetting this causes subtle bugs with dropout and batch
normalisation layers that produce different outputs during training vs. inference.

```python
# Validation — no gradient computation needed
model.eval()
with torch.no_grad():
    for inputs, targets in val_loader:
        outputs = model(inputs.to(device))
        ...
```

## 7. Save and Load Checkpoints Properly

Save only the `state_dict` (the model weights), not the entire model object. Loading
the full object creates coupling to the exact file path and class definition.

```python
# Save
torch.save(model.state_dict(), "checkpoint.pth")

# Load
model = MyModel()
model.load_state_dict(torch.load("checkpoint.pth", map_location=device))
model.to(device)
```

## 8. Choose Loss and Optimizer Deliberately

Do not pick `MSELoss` and `SGD` by default. Comment on why you chose them:

```python
# CrossEntropyLoss: standard for multi-class classification.
# It combines LogSoftmax + NLLLoss in one step, which is numerically stable.
criterion = nn.CrossEntropyLoss()

# Adam: adaptive learning rates per parameter, works well without tuning lr.
# SGD with momentum is often better for CNNs once you have a tuned lr schedule:
# its fixed step size produces more consistent gradient updates across layers,
# which tends to generalise better than Adam for image classification tasks.
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
```

## 9. Model Definition Conventions

- Define all layers in `__init__`, not in `forward`.
- `forward` should only describe the data flow.
- Use `nn.Sequential` only for simple linear stacks; for anything branched, write the
  forward pass explicitly so it is easy to follow.

## 10. Track Metrics During Training

Always print or log the loss (and relevant metrics) every N steps or every epoch.
Silent training loops are undebuggable.

```python
if (epoch + 1) % 10 == 0:
    print(f"Epoch [{epoch+1}/{num_epochs}]  Loss: {loss.item():.4f}")
```
