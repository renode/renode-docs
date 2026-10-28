{{#each filtered.sections}}
## {{label}}

{{#each members}}

{{cleanAnchor refid name}}

### {{name}}

```cpp
{{signature}}
```

{{briefdescription}}

{{#if enumvalue}}
| Value | Description |
|-------|-------------|
{{#each enumvalue}}| `{{name}}` | {{summary}} |
{{/each}}
{{/if}}

{{detaileddescription}}

{{#if (hasDocumentedParams params)}}
{{headingMarker 4}} Parameters

{{#each (documentedParams params)}}* `{{name}}` {{description}}
{{/each}}
{{/if}}

{{/each}}
{{/each}}

## Structures
