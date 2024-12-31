# Base image
FROM node:18-alpine

# Install bash and create app directory
RUN apk update && apk add --no-cache bash && mkdir -p /app

# Set working directory
WORKDIR /app

# Copy backend dependencies and install
COPY ./backend/package*.json ./backend/
RUN cd ./backend && npm install

# Copy the entire frontend directory
COPY ./frontend ./frontend

# Copy frontend dependencies and install
RUN cd ./frontend && npm install && npm run build

# Copy the rest of the application code
COPY . .

# Expose ports for frontend and backend
EXPOSE 3000 3001

# Install process manager to run both services
RUN npm install -g concurrently

# Command to run frontend and backend
CMD ["concurrently", "-n", "frontend,backend", \
     "npm --prefix ./frontend start", \
     "node ./backend/server.js"]