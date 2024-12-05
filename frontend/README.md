
# Frontend Application

This folder contains the source code for a React-based frontend application. It is designed for scalability and includes configurations for local development, testing, and production deployment.

## Features

- **React 18**: Built with the latest version of React for modern UI development.
- **Axios**: For handling API requests.
- **SCSS Support**: Utilizes `Sass` for advanced styling.
- **Jest Testing**: Includes testing capabilities with `jest` and `@testing-library/react`.
- **Docker Support**: Configured for containerized deployment.

---

## Prerequisites

Before you begin, ensure you have the following installed:

- Node.js (v14 or later)
- npm or yarn
- Docker (for containerized deployment)

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

---

## Development

To start the development server:

```bash
npm start
```

The app will be accessible at [http://localhost:3000](http://localhost:3000).

---

## Build

To create a production build:

```bash
npm run build
```

This will generate optimized static files in the `build/` directory.

---

## Testing

Run tests using Jest:

```bash
npm test
```

---

## Deployment

The app is Dockerized for seamless deployment. Use the `Dockerfile` provided to build and run a containerized version of the app.

1. **Build the Docker image**:
   ```bash
   docker build -t frontend-app .
   ```

2. **Run the container**:
   ```bash
   docker run -p 3000:3000 frontend-app
   ```

The application will be accessible at [http://localhost:3000](http://localhost:3000).

---

## Project Structure

- **`src/`**: Contains all the source code, including React components, styles, and assets.
- **`public/`**: Contains static files such as `index.html`.
- **`Dockerfile`**: Docker configuration for containerizing the app.
- **`package.json`**: Project dependencies and scripts.

---

## Scripts

| Script       | Description                                    |
|--------------|------------------------------------------------|
| `start`      | Runs the app in development mode.             |
| `build`      | Builds the app for production.                |
| `test`       | Runs the test suite using Jest.               |
| `eject`      | Ejects the app from `create-react-app` (use with caution). |

---

## Dependencies

### Production
- **React**: ^18.3.1
- **Axios**: ^0.24.0
- **Sass**: ^1.81.0

### Development
- **Jest**: ^26.6.0
- **@testing-library/react**: ^16.0.1
- **axios-mock-adapter**: ^2.1.0

---

## Browsers Support

- **Production**: Latest versions of all major browsers.
- **Development**: Latest version of Chrome, Firefox, and Safari.
