# Blogging-Platform-API

A Flask-based REST API for a personal blogging platform with full CRUD operations backed by a MySQL database.

## How It Works

```
Request → Validate Input → Connect to MySQL → Execute Query
                                                   ├── Success → Return JSON Response
                                                   └── Error   → Return Error Message
```

- All blog posts are stored in a **MySQL database**
- Tags are stored as **JSON** in the database and parsed on every response
- Supports **wildcard search** across title, content, and category fields

## Prerequisites

- Python 3.8+
- MySQL server running locally

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/MazenHassanDev/Blogging-Platform-API.git
cd Blogging-Platform-API
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up the database**

Open MySQL Workbench and run:
```sql
CREATE DATABASE blog_api;
USE blog_api;

CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(100) NOT NULL,
    tags JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**5. Set up environment variables**
```bash
cp .env.example .env
```
Then open `.env` and fill in your MySQL credentials.

**6. Run the app**
```bash
python app.py
```

## API Endpoints

### Create a Post
```
POST /posts
```
**Body:**
```json
{
    "title": "My First Blog Post",
    "content": "This is the content of my first blog post.",
    "category": "Technology",
    "tags": ["Tech", "Programming"]
}
```
**Response `201 Created`:**
```json
{
    "id": 1,
    "title": "My First Blog Post",
    "content": "This is the content of my first blog post.",
    "category": "Technology",
    "tags": ["Tech", "Programming"],
    "createdAt": "Thu, 12 Mar 2026 23:18:46 GMT",
    "updatedAt": "Thu, 12 Mar 2026 23:18:46 GMT"
}
```

---

### Get All Posts
```
GET /posts
```
**Response `200 OK`:** Array of all blog posts

---

### Search Posts
```
GET /posts?term=tech
```
Wildcard search across `title`, `content`, and `category` fields.

**Response `200 OK`:** Array of matching blog posts

---

### Get a Single Post
```
GET /posts/<id>
```
**Response `200 OK`:** Single blog post or `404 Not Found`

---

### Update a Post
```
PUT /posts/<id>
```
**Body:** Same as Create Post

**Response `200 OK`:** Updated blog post or `404 Not Found`

---

### Delete a Post
```
DELETE /posts/<id>
```
**Response `204 No Content`** or `404 Not Found`

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK — request succeeded |
| 201 | Created — post successfully created |
| 204 | No Content — post successfully deleted |
| 400 | Bad Request — missing or invalid fields |
| 404 | Not Found — post does not exist |
| 500 | Internal Server Error |

## Project Structure

```
blog-api/
├── app.py              # main Flask application
├── .env                # database credentials (not committed to git)
├── .env.example        # template for environment variables
├── .gitignore          # prevents secrets from being committed
├── requirements.txt    # Python dependencies
└── README.md           # this file
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DB_HOST` | MySQL host (default: `localhost`) |
| `DB_USER` | MySQL username (default: `root`) |
| `DB_PASSWORD` | MySQL password |
| `DB_NAME` | Database name (default: `blog_api`) |
