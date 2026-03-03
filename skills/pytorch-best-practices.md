# Skill: PyTorch Best Practices

**Trigger:** When writing or reviewing Machine Learning code using PyTorch.

**Directives:**
1. **Explicit Dimensions:** Always document tensor shapes in comments (e.g., `# x shape: (batch_size, channels, height, width)`).
2. **Clear Device Placement:** Explicitly handle `.to(device)` operations, keeping the logic simple and predictable.
3. **Readable Training Loops:** Write standard, transparent training loops. Avoid over-abstracting the training step into base classes (like PyTorch Lightning style) unless specifically asked to. You want the raw steps to be visible to the student.
4. **Reproducibility:** Include random seed settings if writing a complete script.
5. **Educational Comments:** Explain *why* a certain loss function, layer dimension, or optimizer is chosen if building a model from scratch.