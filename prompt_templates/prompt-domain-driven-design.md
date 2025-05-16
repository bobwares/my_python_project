You are an expert software architect specializing in Domain-Driven Design.  
Given the following JSON Schema that defines the structure of a domain model, produce a comprehensive DDD document in Markdown. Your document should include the following sections:

1. **Ubiquitous Language**  
   • List and define the key terms and concepts that appear in the schema.

2. **Bounded Contexts**  
   • Identify logical sub-domains or modules.  
   • For each context, give a brief description of its responsibility.

3. **Aggregates and Aggregate Roots**  
   • Determine which entities form aggregates.  
   • Specify the aggregate root for each and explain its invariants.

4. **Entities**  
   • For each entity in the schema, describe its identity, lifecycle, and key attributes.

5. **Value Objects**  
   • Identify which types are value objects.  
   • Explain their immutability and how they contribute to the model.

6. **Domain Services**  
   • List any operations that don’t naturally belong to a single entity or value object.  
   • Describe their purpose and inputs/outputs.

7. **Domain Events**  
   • For each meaningful state change, define a domain event including its payload.

8. **Context Map**  
   • If there are multiple bounded contexts, show how they relate (partnerships, shared kernels, etc.).

9. **Example Use Cases / Application Services**  
   • Show 2–3 high-level use cases and map them to application services, inputs, and outputs.

10. **UML Class Diagram (ASCII or Mermaid)**  
    • Provide a simple diagram illustrating entities, value objects, and their relationships.

**Output Constraints**
- Output *only* the DDD document in Markdown.
- Do *not* include the raw JSON Schema in your output.
- Use headings (`##`, `###`) to structure sections.

---

**JSON Schema**
```json
{text}
