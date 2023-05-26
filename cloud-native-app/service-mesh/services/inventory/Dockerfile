# Official Node.js runtime as the base image
FROM node:14

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the package.json and package-lock.json files to the working directory
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the application source code to the working directory
COPY . .

# Expose a port for the application to listen on
EXPOSE 3000

# Specify the command to run the application
CMD ["npm", "start"]
