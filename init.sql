-- Create the database
CREATE DATABASE $POSTGRES_DB;

-- Create the user and set the password
CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';

-- Grant privileges to the user on the database
GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;
