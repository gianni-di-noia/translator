# Use an official Node runtime as a parent image
FROM node:14

# Set the working directory in the container
WORKDIR /app

COPY . /app/

# Copy package.json and package-lock.json to the working directory
# COPY package*.json ./

# Install app dependencies
RUN npm install

# Copy your application files to the container

# Expose the port on which your app will run
EXPOSE 3000

RUN ls

# Define the command to run your app
CMD ["node", "app.js"]
