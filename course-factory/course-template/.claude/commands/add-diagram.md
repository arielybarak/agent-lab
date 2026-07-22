---
description: Add a generated diagram for a lesson and wire it into the course's visualization pipeline. Use when a lesson needs a diagram or its image reference does not resolve. Requires the diagrams module.
argument-hint: "<lesson name and unit>"
---

Add the diagram for: **$ARGUMENTS**

> Requires the **diagrams** module. If this course did not enable it, stop and say so.

Follow skill `diagrams`.

1. **Check it earns its place.** Diagrams are for structural, spatial, or over-time ideas. If the
   lesson's point is a definition, a comparison, or a list of steps, say so and stop — prose or a
   table is the better artifact.
2. **Add the generator function** in the course's visualization script, mirroring an existing one so
   the new diagram matches its siblings: same shapes, same layout direction, same colour scheme.
3. **Output to the lesson's own image directory**, under the **exact filename the lesson
   references**.
4. **Wire it into the script's driver and run it.** Confirm the image renders.
5. **Confirm the lesson's reference resolves** — a reference to a missing image is a Critical
   finding at review time.

Label the diagram with the running example's parts, named exactly as the lesson's prose names them.
Do not break the script's platform-specific path handling — guard it, do not delete the working
case.
