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

{{/each}}
{{/each}}

## Structures
