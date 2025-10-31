# RelaySMS CAPTCHA Server

## Configuration

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/smswithoutborders/RelaySMS-CAPTCHA-Server.git
   cd RelaySMS-CAPTCHA-Server
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   ```bash
   cp .env.example .env
   ```

   Edit the `.env` file with your configuration settings.

5. **Run the server**
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

The server will be available at `http://localhost:8000`

## API Documentation

### Base URL

```
http://localhost:8000/v1
```

### Authentication

All endpoints require authentication using either:

- `client_id` (for CAPTCHA operations)
- `client_secret` (for token verification)

### Endpoints

#### 1. Request New CAPTCHA

**POST** `/v1/new`

Generate a new CAPTCHA challenge.

**Request Body:**

```json
{
  "client_id": "your_client_id"
}
```

**Response:**

```json
{
  "challenge_id": "unique_challenge_id",
  "image": "base64_encoded_captcha_image"
}
```

**Status Codes:**

- `200` - Success
- `401` - Invalid client ID
- `503` - CAPTCHA service unavailable

---

#### 2. Solve CAPTCHA

**POST** `/v1/solve`

Submit an answer to a CAPTCHA challenge.

**Request Body:**

```json
{
  "client_id": "your_client_id",
  "challenge_id": "challenge_id_from_new_endpoint",
  "answer": "captcha_solution"
}
```

**Response:**

```json
{
  "success": true,
  "message": "CAPTCHA solved successfully.",
  "token": "challenge_id-verification_token"
}
```

**Status Codes:**

- `200` - Success (check `success` field for actual result)
- `400` - Missing required fields or challenge already used
- `401` - Invalid client ID
- `404` - Challenge ID not found or expired

---

#### 3. Verify Token

**POST** `/v1/verify`

Verify a CAPTCHA token obtained from solving a challenge.

**Request Body:**

```json
{
  "client_secret": "your_client_secret",
  "token": "challenge_id-verification_token"
}
```

**Response:**

```json
{
  "success": true,
  "message": "Token verified successfully."
}
```

**Status Codes:**

- `200` - Success (check `success` field for actual result)
- `400` - Missing required fields
- `401` - Invalid client secret

## Usage Flow

1. **Request a CAPTCHA**: Call `/v1/new` with your `client_id` to get a challenge ID and image
2. **Display the CAPTCHA**: Show the base64-encoded image to the user
3. **Collect user input**: Get the CAPTCHA solution from the user
4. **Solve the CAPTCHA**: Call `/v1/solve` with the challenge ID and answer to get a verification token
5. **Verify the token**: Use `/v1/verify` with your `client_secret` and the token to confirm completion

## License

This project is licensed under the GPL-3.0-only License. See the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request
