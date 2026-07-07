{{cleanAnchor refid name}}

### {{shortname name}}

{{#if includes}}
```cpp
#include <{{includes}}>
```
{{/if}}

```cpp
{{classSignature}}
```

{{#if basecompoundref}}> **Inherits:** {{#each basecompoundref}}{{linkedName name refid}}{{#unless @last}}, {{/unless}}{{/each}}
{{/if}}
{{#if derivedcompoundref}}> **Subclassed by:** {{#each derivedcompoundref}}{{linkedName name refid}}{{#unless @last}}, {{/unless}}{{/each}}
{{/if}}

{{briefdescription}}

{{detaileddescription}}

{{#each inheritedMemberGroups}}
#### Inherited from {{linkedName name refid}}

| Kind | Name | Description |
|------|------|-------------|
{{#each members}}| `{{kind}}` | {{linkedName name refid}} {{badges}} | {{cell (memberSummary this)}} |
{{/each}}

{{/each}}
{{#each filtered.sections}}
#### {{label}}

{{#if (hasReturnColumn section)}}
| Return | Name | Description |
|--------|------|-------------|
{{#each members}}| {{returnTypeShort}} | [`{{name}}`](#{{cleanId refid name}}) {{badges}} | {{cell (memberSummary this)}} |
{{/each}}
{{else}}
| Name | Description |
|------|-------------|
{{#each members}}| [`{{name}}`](#{{cleanId refid name}}) {{badges}} | {{cell (memberSummary this)}} |
{{/each}}
{{/if}}

{{#each members}}

---

{{cleanAnchor refid name}}

##### {{name}}

{{badges}}

```cpp
{{signature}}
```

{{briefdescription}}

{{detaileddescription}}

{{#if referencedBy}}
###### Referenced by

{{#each referencedBy}}- {{linkedName name refid}}
{{/each}}

{{/if}}
{{#if references}}
###### References

{{#each references}}- {{linkedName name refid}}
{{/each}}

{{/if}}
{{#if reimplements}}
###### Reimplements

{{#each reimplements}}- {{linkedName name refid}}
{{/each}}

{{/if}}
{{#if reimplementedBy}}
###### Reimplemented by

{{#each reimplementedBy}}- {{linkedName name refid}}
{{/each}}

{{/if}}

{{#unless briefdescription}}
{{#unless detaileddescription}}
{{memberSummary this}}
{{/unless}}
{{/unless}}

{{#if (hasDocumentedParams params)}}
| Parameter | Type | Description |
|-----------|------|-------------|
{{#each (documentedParams params)}}| `{{name}}` | `{{type}}` | {{description}} |
{{/each}}
{{/if}}

{{#if enumvalue}}
| Value | Description |
|-------|-------------|
{{#each enumvalue}}| `{{name}}` | {{summary}} |
{{/each}}
{{/if}}

{{/each}}
{{/each}}
