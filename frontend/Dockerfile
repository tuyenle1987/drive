# Use a lightweight Node.js image
FROM node:16-alpine

# Set the working directory in the container
WORKDIR /app

# Copy only package.json and package-lock.json first to leverage Docker caching
COPY frontend/package.json frontend/package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY frontend/ ./

# Expose the port the React application will run on
EXPOSE 3000

# Start the React application
CMD ["npm", "start"]
