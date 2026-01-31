This folder contains task descriptions for working with Claude Sonnet via GitHub Copilot.

In the task descriptions, rectangle dimensions are give as width in pixels by height in pixels. Speeds are pixels per frame.

The file naming convention is `yyyy-mm-dd-descriptive-string.md`.

Tasks should be broken into stages that are each simple enough to for the agent to tackle as a single turn. It is OK to assume that earlier parts of the task are still in the model's context window.

When referring to file, use paths relative to the project root, without a leading slash.

When returning to a task with additional instructions, use a horizontal rule, which is three dashes on a line by itself.

Here are a snippet to help with converting Zig game config to Python game config.

> Here are some configuration constants expressed in Zig. Translate them into Python and append them to src/pyginvaders/config.py following the same convention.
> Here are some configurations expressed in Zig that all apply to THING. Translate them into Python, append them to src/pyginvaders/config.py following the same convention, naming them name them `THING_...`.
