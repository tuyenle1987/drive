
# Google Drive Integration (Modular)

## Setup Instructions

1. **Create Environment Files**:
   - For the backend, use `.env.example` as a template to create a `.env` file. Ensure the following variables are set:
     - `GOOGLE_CLIENT_SECRET`
     - `GOOGLE_CLIENT_ID`
     - (Other variables can be omitted.)
   - For the frontend, create a `.env` file with the following content:
     ```
     REACT_APP_API_BASE_URL=http://localhost:5000
     ```

2. **Install Docker Compose**: Ensure Docker Compose is installed on your system.

3. **Run the Application**:
   ```bash
   docker-compose up
   ```

   - The **frontend** will be available at: [http://localhost:3000](http://localhost:3000).
   - The **backend** will run at: [http://localhost:5000](http://localhost:5000).

For additional details, refer to the README files located in the `backend` and `frontend` folders.
