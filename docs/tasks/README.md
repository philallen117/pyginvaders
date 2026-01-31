This folder contains task descriptions for working with Claude Sonnet via GitHub Copilot.

In the task descriptions, rectangle dimensions are give as width in pixels by height in pixels. Speeds are pixels per frame.

The file naming convention is `yyyy-mm-dd-descriptive-string.md`.

Tasks should be broken into stages that are each simple enough to for the agent to tackle as a single turn. It is OK to assume that earlier parts of the task are still in the model's context window.

When referring to file, use paths relative to the project root, without a leading slash.

When returning to a task with additional instructions, use a horizontal rule, which is three dashes on a line by itself.

Here is a snippet to help with converting Zig game config to Python game config.
