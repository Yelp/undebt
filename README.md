# Undebt

Undebt is a tool for automatically refactoring massive code bases, like the one we have [@Yelp](https://github.com/Yelp).

Every developer knows that [technical debt](https://en.wikipedia.org/wiki/Technical_debt) is bad. Like financial debt, it incurs interest payments over time in the form of long developer hours fixing the sins of the past. Worse, we write code by learning (and copy-and-pasting) from existing code. Thus, if the existing code is full of debt, the debt will only perpetuate itself.

Nevertheless, technical debt keeps growing. Every developer has felt the drive to create and deliver new code quickly, and because of this we ignore the technical debt created in the process. We tell ourselves that we don't have time to refactor code, and should be focusing on building new things instead. In some sense, that's true—there's only so much time available to write code, and the more spent refactoring old code to get rid of debt, the less spent shipping new features—but that just means we need a solution that's fast.

Undebt is the solution to the problem of technical debt. Undebt is a fast and reliable way to refactor your code. Undebt lets you define complex find-and-replace rules using simple, straightforward Python that can be applied quickly to an entire codebase with a simple command.

To get started using Undebt, head over to our [documentation](http://undebt.readthedocs.io/en/latest/).
