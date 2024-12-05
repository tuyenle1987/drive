
# **Google Drive Integration Application**

This application integrates with **Google Drive** and provides endpoints for user authentication and file management. It is structured as a modular Flask application with clean separation of concerns for scalability and maintainability.

---

## **Architecture and Structure**

### **Directory Structure**

```
project/
  app.py                     # Main application entry point
  routes/                    # API route handlers
    auth_routes.py           # Handles authentication-related routes
    file_routes.py           # Handles file operations-related routes
  services/                  # Business logic and service integrations
    auth_service.py          # Contains business logic for authentication
    drive_service.py         # Contains business logic for file operations
  config.py                  # Application configuration (dev/prod environments)
  logging_module.py          # Centralized logging with correlation ID support
  correlation.py             # Middleware to generate and manage correlation IDs
  requirements.txt           # Python dependencies
  .env                       # Environment variables for the app
  Dockerfile                 # Docker image for the Flask backend
  docker-compose.yml         # Compose file for multi-service setup
  tests/                     # Unit tests for the application
    test_auth_routes.py      # Tests for authentication routes
    test_auth_service.py     # Tests for authentication service logic
    test_drive_service.py    # Tests for Google Drive service integration
    test_file_routes.py      # Tests for file operation routes
```

---

## **Core Components**

### **1. Authentication**
- **Endpoints:**
  - `/auth/login`: Redirects users to Google's OAuth 2.0 login page.
  - `/auth/callback`: Handles the callback after successful Google authentication.
  - `/auth/status`: Checks if the user is authenticated.
  - `/auth/logout`: Logs the user out by clearing session data.

- **How It Works:**
  1. The user is redirected to Google OAuth 2.0 for authentication.
  2. Upon successful login, a unique token is generated and stored in the session.
  3. The user's authentication status is verified using session data.

---

### **2. File Management**
- **Endpoints:**
  - `/files`: Lists files in the user's Google Drive.
  - `/files/upload`: Allows users to upload a file to their Google Drive.
  - `/files/delete/<file_id>`: Deletes a file from the user's Google Drive.
  - `/files/download/<file_id>`: Downloads a file from the user's Google Drive.

- **How It Works:**
  - **List Files:** Retrieves a paginated list of files using the Google Drive API.
  - **Upload File:** Temporarily saves the file locally, uploads it to Google Drive, and cleans up the temporary storage.
  - **Delete File:** Deletes the specified file from the user's Google Drive by its unique file ID.
  - **Download File:** Streams the file content from Google Drive directly to the client.

---

### **3. Middleware**
- **Correlation ID:**
  - Every request is tagged with a unique correlation ID, either provided by the client (`X-Correlation-ID` header) or auto-generated.
  - The correlation ID is included in all logs for traceability.

---

### **4. Logging**
- Centralized logging is implemented via `logging_module.py`:
  - Logs include timestamps, log levels, module names, and correlation IDs.
  - Supports both console and file logging.

---

### **5. Configuration**
- **`config.py`** dynamically manages environment-specific configurations:
  - `DevelopmentConfig` for local development.
  - `ProductionConfig` for deployment.

---

## **How It Works**

### **1. Authentication Flow**
1. The user initiates login via `/auth/login`.
2. The app redirects the user to Google OAuth 2.0.
3. Upon successful login, Google redirects back to `/auth/callback`.
4. Tokens are stored in the session, and `/auth/status` verifies if the user is authenticated.

### **2. File Operations**
Authenticated users can:
- **List files:** Access `/files` to retrieve a list of files.
- **Upload files:** Use `/files/upload` to send files to Google Drive.
- **Download files:** Use `/files/download/<file_id>` to retrieve files.
- **Delete files:** Use `/files/delete/<file_id>` to remove files.

### **3. Traceability with Correlation ID**
- Every request has a correlation ID, logged with each operation.
- Correlation IDs can be used to trace requests across distributed systems.

### **4. Dockerized Deployment**
- A `Dockerfile` creates a containerized Flask application.
- `docker-compose.yml` integrates multiple services (e.g., Flask backend, database if needed).

---

## **Testing**

### **1. Running Tests**
- Unit tests are implemented to ensure the robustness of the application. The `pytest` framework is used for testing.
- Run the following command to execute all tests:
  ```bash
  pytest
  ```

### **2. Test Coverage**
- **Authentication Tests:**
  - Validate login and callback flows.
  - Ensure session management and logout functionality work correctly.
- **File Operations Tests:**
  - Test file listing, uploading, downloading, and deletion using mock Google Drive API responses.
- **Service Integration Tests:**
  - Mock and validate Google Drive service interactions, including edge cases.
- **Middleware Tests:**
  - Validate correlation ID generation and propagation.

### **3. Example Test Output**
```plaintext
============================= test session starts ==============================
platform linux -- Python 3.8, pytest-8.3.4
rootdir: /app
collected 14 items

tests/test_auth_routes.py .....                                          [ 35%]
tests/test_auth_service.py ..                                            [ 50%]
tests/test_drive_service.py ....                                         [ 78%]
tests/test_file_routes.py ....                                           [100%]

============================== 14 passed in 0.15s ===============================
```

---

## **Benefits**

- **Modular Design:** Separation of routes, services, and middleware ensures maintainability.
- **Scalability:** Middleware and modular architecture allow easy scaling and feature additions.
- **Traceability:** Correlation ID ensures logs can trace requests end-to-end.
- **Security:** OAuth 2.0 ensures secure authentication.

---
