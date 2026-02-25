# AI rules for Versioned Notes System

- **Never overwrite versions**: Immutability is the core concept. Updates to a note must create a new version.
- **Always use the service layer**: Do not put business logic in routes. Routes should only handle HTTP layers.
- **Strict Version Logic**: Version must ALWAYS be `last_version + 1`. Never calculate based on the count of versions, and NEVER accept a version number from the frontend. This logic must be centralized in the service layer and cannot be bypassed.
- **Validation**: Always validate inputs (schemas) prior to passing processing to the service layer.
- **Keep it simple**: Avoid complex abstractions. Keep functions small, readable, and easy to explain.
