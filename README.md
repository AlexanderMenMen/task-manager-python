# Task Manager with Reminder Notifications 🚀

#### Description:
Task Manager with Reminder Notifications is a Python-based application designed to help users manage their daily tasks efficiently. The program allows users to add, remove, list, and modify tasks, as well as send reminders via Gmail or SMS using Twilio. Tasks are stored persistently in a CSV file, and environment variables are used for secure credential management. This project demonstrates skills in data management, integration with external APIs, and handling dates and times—all essential abilities for modern software development.

## Features ✨
- **Add Task:** Create a new task by providing a title, description, category (from a predefined list), and a due date.
- **Remove Task:** Delete an existing task by selecting its number from a list.
- **List Tasks:** Display all tasks in a neatly numbered list for easy reference.
- **Modify Task:** Update details of an existing task, including title, description, category, and due date.
- **Send Reminders:** Send personalized reminders for tasks via SMS (using Twilio) or Gmail.
- **CSV Storage:** Tasks are stored in a CSV file, ensuring data persistence even after the program ends.
- **Secure Credentials:** Uses a `.env` file to manage sensitive information like API keys and passwords.

## Installation 💻
1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/your-repo.git
    cd your-repo
    ```
2. **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration 🔧
Create a file named `.env` in the project root with the following content:

```env
# Twilio Credentials (for sending SMS)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number

# Gmail Credentials (for sending email notifications)
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
