# Changelog

### Added

- **Activity Logs** feature:

  - `GET /activity-logs`: Fetch all activity logs (admin only).
  - `GET /activity-logs/user`: Fetch activity logs for the authenticated user.
  - `GET /activity-logs/{id}`: Fetch a single activity log by ID.
  - `POST /activity-logs`: Create a new activity log.
  - `PUT /activity-logs/{id}`: Update an existing activity log.
  - `DELETE /activity-logs/{id}`: Delete an activity log.
  - JWT-based authentication required for protected routes.

- **Unit Tests** using **pytest**:
  - Added tests for all **Activity Log endpoints**.
  - Included **positive and negative test cases** for:
    - Creation
    - Retrieval (single and all)
    - Update
    - Deletion
  - Achieved **100% test coverage** for Activity Logs feature.

### Changed

- Updated **Swagger/OpenAPI documentation** to include Activity Log paths and schemas.
- Modified `components.securitySchemes` to ensure bearer token authentication is clearly defined.

---
