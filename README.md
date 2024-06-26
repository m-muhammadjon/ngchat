## Setting Up the Project

### Setting Up the Project via Virtual Environment

1. Install project requirements:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements/develop.txt
   ```

2. Create a `.env` file:
   ```bash
   cp .env.example .env
   ```
   Modify `DJANGO_SETTINGS_MODULE` to `config.settings.develop` and `DB_HOST` to `localhost` in the `.env` file.

3. Create the database:
   ```bash
   sudo -u postgres psql
   CREATE DATABASE my_db;
   ```

   If you prefer not to use the `postgres` user, create a new user and grant all privileges:
   ```bash
   CREATE USER my_user WITH PASSWORD 'password';
   GRANT ALL PRIVILEGES ON DATABASE my_user TO my_db;
   ```

4. Set up the `.env` file with your database credentials:
   ```bash
   nano .env
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```


6. Run the server:
   ```bash
   python manage.py runserver
   ```

## Setting Up with Docker

1. Create a `.env` file:
   ```bash
   cp .env.example .env
   ```


2. Build and run Docker:
   ```bash
   docker-compose up --build
   ```

Open a browser and go to `http://localhost:8000/`. Use the following superuser credentials: `admin`/`admin`.

### Additional Steps

- **Recaptcha:**

  You can get key for recaptcha from [here](https://www.google.com/recaptcha/admin/create) and add it to the `.env`
  file. Then add keys to the `.env` file:
  ```bash
  RECAPTCHA_SITE_KEY=your_site_key
  RECAPTCHA_SECRET_KEY=your_secret_key
  ```

- **Pre-commit Hook:**

  Install and configure pre-commit hook:
  ```bash
  pip install pre-commit
  pre-commit install
  ```

- **Running Tests:**
  Execute tests with the following command:
  ```bash
  python manage.py test
  ```

## API Documentation

API documentation is available at `http://localhost:8000/swagger/`

- /login/ - Login API. You can get your token by providing your username and password.
- /users/ - User API. You can get other users list from here.
- /conversation-create/ - Create a conversation with another user.

After creating a conversation, you can send messages to that conversation through websocket.
Every user should connect to the websocket with auth token. Example:
```bash
ws://localhost:8000/ws/users/?token=TOKEN
```
After connecting to the websocket, you can send messages to the conversation by providing the conversation id and message.
Example for sending messages:
```bash
{
    "socket_type": "chat_message",
    "conversation": $conversation_id,
    "text": "Hi! How are you?"
}
```
Example for read a message:
```bash
{
    "socket_type": "read_message",
    "message_id": $message_id
}
```

You can get conversations list and messages list from the API.
- /conversations/ - Get conversations list.
- /message-history/{conversation_id}/ - Get messages list of the conversation.
