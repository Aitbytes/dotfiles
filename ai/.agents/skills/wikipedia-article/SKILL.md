---
name: wikipedia-article
description: Write a Wikipedia-style encyclopedic article from research findings. Covers lead paragraph, sections, tone conventions, citation formatting, and the infobox pattern.
---

## What I do

Write a formal encyclopedic article modeled on Wikipedia's standards. The output is a well-structured markdown document that could be converted to MediaWiki markup or submitted to Wikipedia for review. Emphasis on neutral tone, encyclopedic structure, inline citations, and balanced coverage of differing viewpoints.

## When to use me

When the user wants a citable, encyclopedic-style reference article suitable for Wikipedia submission, an academic wiki, or a formal knowledge-base entry. Use when the topic is factual, multi-faceted, and benefits from structured presentation with source attribution throughout.

## Tone and Style

- **Neutral point of view (NPOV)**: Present all significant views fairly, without editorial bias. Do not advocate a position.
- **No first person**: Never use "I", "we", "you", "the author", "this article argues". Use third person or passive voice.
- **Informal language prohibited**: Avoid colloquialisms, idioms, emotional language, rhetorical flourishes.
- **Definitive statements need sources**: Every factual claim should have an inline citation `[source]`.
- **Lead first**: Start with a comprehensive definition in the first paragraph (the lead), which summarizes the entire article.

## Article Structure

```
# Article Title

The **lead paragraph** is 2-4 sentences that defines the topic, establishes
context, and summarizes the key points. It should be comprehensible to a
non-expert. No citation in the lead unless the claim is disputed.

## Overview

A brief section providing context, history, or background.
Establishes why the topic matters and what the article covers.

## [Section 1]

### [Sub-section if needed]

## [Section 2]

## [Controversies or Debates]

Present all significant viewpoints fairly. Do not characterize one view
as correct or superior. Use citations from multiple perspectives.

## See also

- [[Related Article 1]]
- [[Related Article 2]]

## References

Citations list here in alphabetical order or numbered format.

## External links

Only links to official sources, databases, or primary resources.
```

## Citation Style

Inline citations go immediately after the claim:

```
Machine learning is a branch of artificial intelligence that enables
systems to learn from data without being explicitly programmed[1].
```

References section format:

```
[1] Author Name. "Title of Work". *Publication*. Publisher. Year. p. X.
```

Or for web sources:

```
[1] Author Name. "[Page Title]". *Website Name*. URL. Published Year.
    Accessed Year.
```

## Infobox pattern (optional)

If the topic is a person, place, or thing with structured attributes:

```markdown
| Parameter | Value |
| --------- | ----- |
| Field 1   | Value |
| Field 2   | Value |
```

## What to avoid

- **Advocacy**: Do not argue for a position. Present evidence and let readers draw conclusions.
- **Novelty language**: Never call something "revolutionary", "game-changing", or "cutting-edge" — this is promotional language.
- **Breach of NPOV**: Statements like "X is the best" or "Y is superior" violate encyclopedic tone.
- **Unverified claims**: If you cannot find a source, say "There is no consensus" or "This claim is disputed" rather than stating it as fact.
- **Incomplete coverage**: If a significant view exists in published sources, it must be represented even if you personally disagree with it.

## Wikipedia-specific notes

- Articles should be "discussions about the topic", not "the topic itself"
- Avoid self-referential language about the article ("This article discusses...")
- Stub articles (very short) are discouraged — aim for at minimum a 4-paragraph lead + 2 substantial sections
- For living persons or current events, maintain strict neutrality and factuality

## Output envelope

The skill produces a single markdown file (`article.md`) with the full article. The agent should write this as a tool result.

## Limitations

- No code execution; purely a writing and formatting skill
- Requires that the research content is already gathered — the skill formats it, it does not conduct research
