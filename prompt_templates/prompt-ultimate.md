
### **Ultimate Generalized Application Generation Prompt**

> **Objective**: Generate a fully structured software application using the provided inputs: **Domain-Driven Design (DDD) Document**, **Technology Stack**, and **Software Pattern Template**. The output should include all required files and directories for the application, and it should be provided either as a downloadable zip file or as a shell script that will create and populate the application files directly on my file system.
>
> ---
>
> ## **Context**
>
> ### **Input Details**
> - **Domain-Driven Design Document**: I will provide a document defining core domain concepts, entities, and business rules.
> - **Technology Stack**: I will specify the technology stack, including programming language, frameworks, libraries, infrastructure, and dependencies.
> - **Software Pattern Template**: I will specify the architectural pattern template, including directory structure, design patterns, and organization of code and configuration files.
>
> ### **Output Requirements**
> - **Output Format**:
    >   - Provide a shell script named `create_project.sh` to create all directories and populate files with the necessary code.
>   - Alternatively, output the application as a zip file named `application.zip` for direct download and extraction.
> - **File Content**:
    >   - Include code files with inline comments for each entity, repository, service, and handler, structured according to the provided pattern template.
>   - Add configuration files based on the technology stack and dependencies.
> - **File Structure Example**:
    >   - Follow the directory structure as defined in the pattern template, ensuring all specified files are placed in the correct locations and contain the relevant code.
>
> ---
>
> ## **Role**
> - Act as an expert software architect proficient in Domain-Driven Design, the provided technology stack, and software patterns.
>
> ## **Examples**
> - Use example code snippets for each specified file in the application, following the details in the domain, technology stack, and pattern template.
> - For each file, include sample methods, classes, or configurations as defined in the DDD document and technology stack.
>
> ## **Constraints**
> - Exclude any unrelated files or configurations not defined in the provided inputs.
> - Use the latest versions of all libraries, frameworks, and dependencies specified in the technology stack.
>
> ---
>
> ## **Final Task**
> - Generate a complete application based on the **DDD Document**, **Technology Stack**, and **Pattern Template** provided. Bundle all files and directories into a downloadable zip file (`application.zip`) or create a shell script (`create_project.sh`) that will set up the entire project structure and populate the files with the specified content.
>
> ---
>
> **Next Step**: After receiving this prompt, request the **DDD Document**, **Technology Stack**, and **Software Pattern Template** to use as inputs for generating the application.

---

With this generalized prompt, you can provide any **DDD document**, **Technology Stack**, and **Pattern Template** as separate inputs. The assistant will then use these inputs to generate a fully structured application that aligns with your specifications and output preferences.