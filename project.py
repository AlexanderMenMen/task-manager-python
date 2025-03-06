"""
Task Manager with Reminder Notifications

This program allows users to manage their tasks, including adding, removing,
listing, and sending reminders via email (Gmail) or SMS.
"""

# Import necessary libraries
import csv
import sys
import smtplib
import os
import re
from datetime import datetime
from twilio.rest import Client
from email.message import EmailMessage
from dotenv import load_dotenv # To load enviroment variables

# Load enviroment variables from an .env file
load_dotenv()

# Twilio credentials loaded from environment variables
ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

# Gmail credentials loaded from environment variables
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')


def main():
    """
    Main function that presents a menu to the user.

    Allows user to add, remove, list tasks, modify tasks and send reminders via SMS or email.
    """

    while True:
        print("╔══════════════════╗")
        print("║   Task Manager   ║")
        print("╠══════════════════╣")
        print("║ 1. Add Task      ║")
        print("║ 2. Remove Task   ║")
        print("║ 3. List Tasks    ║")
        print("║ 4. Modify Task   ║")
        print("║ 5. Send Reminders║")
        print("║ 6. Exit          ║")
        print("╚══════════════════╝")

        option = input("\nChoose an option: ")

        # Menu selection
        match option:
            case "1":
                add_task()
            case "2":
                remove_task()
            case "3":
                list_tasks()
            case "4":
                modify_task()
            case "5":
                send_reminder()
            case "6":
                sys.exit(0)
            case _:
                print("Invalid option.\nPlease try again.")


def add_task():
    """
    Adds a new task to the CSV file.

    Prompts the user for task details like title, description, category, and due date.
    :raises ValueError: if the due date format is incorrect.
    """

    title = input("Enter task title: ")
    description = input("Enter task description: ")

    # Category selection
    print("\nSelect a category: ")
    categories = ["Medical Appointment", "Business Meeting", "Work Project","Household Chores", "Study", "Shopping", "Social Events", "Other"]
    for i, category in enumerate(categories):
        print(f"{i + 1}. {category}")

    try:
        category_final = int(input("Choose category: ")) - 1
        if 0 <= category_final < len(categories):
            category = categories[category_final]
        else:
            category = "Other"
    except ValueError:
        category = "Other"

    # Date format
    due_date = input("Enter due date (YYYY-MM-DD): ")
    try:
        due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format.")
        return

    # Save task to CSV
    with open("tasks.csv", "a") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "description", "category", "due_date"])

        # Check if the file is empty, write the header if needed
        file.seek(0, 2)

        # Go to the end of the file
        if file.tell() == 0:
            writer.writeheader()

        # Write the task dictionary to the CSV
        writer.writerow({"title": title, "description": description, "category": category, "due_date": due_date})

    print("\nTask added successfully.")


def remove_task():
    """
    Removes a task from the CSV file.

    Prompts the user for the task number to remove.
    :raises ValueError: if the selected task number is out of range.
    """

    tasks = list_tasks(return_tasks=True)

    if tasks:
        try:
            task_number = int(input("\nEnter task number to remove: ")) - 1
            if 0 <= task_number < len(tasks):
                # Remove elements from a dictionary
                del tasks[task_number]

                # Updated task list to the CSV
                with open("tasks.csv", "w") as file:
                    writer = csv.DictWriter(file, fieldnames=["title", "description", "category", "due_date"])
                    writer.writeheader()
                    writer.writerows(tasks)

                print("\nTask removed successfully.")
            else:
                print("Invalid task number.")
        except ValueError:
            print("Invalid input.")
    else:
        print("No tasks to remove.")


def list_tasks(return_tasks=False):
    """
    Lists all tasks saved in the CSV file.

    :param return_tasks: If True, the function returns the list of tasks instead of printing them.
    :return: List of task dictionaries if return_tasks is True.
    """

    tasks = []

    try:
        with open("tasks.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                tasks.append({"title": row["title"], "description": row["description"],"category": row["category"], "due_date": row["due_date"]})
    except FileNotFoundError:
        print("No tasks available.")
        return []

    if not tasks:
        print("No tasks to display.")
    else:
        print("\nList of tasks:")
        for i, task in enumerate(tasks, start=1):
            print(f"\nTask {i}:\nTitle: {task['title']}\nDescription: {task['description']}\nCategory: {task['category']}\nDue date: {task['due_date']}\n")

    if return_tasks:
        return tasks


def modify_task():
    """
    Modifies an existing task in the CSV file.

    Prompts the user for the task number to modify, then allows modification of title, description, category, and due date.
    """

    tasks = list_tasks(return_tasks=True)

    if tasks:
        try:
            task_number = int(input("\nEnter task number to modify: ")) - 1
            if 0 <= task_number < len(tasks):
                # Modify task details
                task = tasks[task_number]

                print("\nModify the task details (leave blank to keep current value):")

                # We use or because if we leave it blank, the input function takes the current element
                new_title = input(f"Enter new title [{task['title']}]: ") or task["title"]
                new_description = input(f"Enter new description [{task['description']}]: ") or task["description"]

                # Category selection
                print("\nSelect a new category (leave blank to keep current):")
                categories = ["Medical Appointment", "Business Meeting", "Work Project","Household Chores", "Study", "Shopping", "Social Events", "Other"]
                for i, category in enumerate(categories):
                    print(f"{i + 1}. {category}")

                try:
                    category_final = input(f"Choose category [{task['category']}]: ")
                    if category_final:
                        category_final = int(category_final) - 1
                        if 0 <= category_final < len(categories):
                            task["category"] = categories[category_final]
                        else:
                            task["category"]
                except ValueError:
                    pass  # Keep the current category if input is invalid

                # Due date
                new_due_date = input(f"Enter new due date (YYYY-MM-DD) [{task['due_date']}]: ")
                try:
                    if new_due_date:
                        task["due_date"] = datetime.strptime(new_due_date, "%Y-%m-%d").date()
                    else:
                        task["due_date"]
                except ValueError:
                    print("Invalid date format, keeping current due date.")

                # Update the task in the list
                tasks[task_number] = {"title": new_title, "description": new_description,"category": task["category"], "due_date": task["due_date"]}

                # Updated task list to the CSV
                with open("tasks.csv", "w") as file:
                    writer = csv.DictWriter(file, fieldnames=["title", "description", "category", "due_date"])
                    writer.writeheader()
                    writer.writerows(tasks)

                print("\nTask modified successfully.")
            else:
                print("Invalid task number.")
        except ValueError:
            print("Invalid input.")
    else:
        print("No tasks to modify.")


def send_reminder():
    """
    Prompts the user to choose between sending a reminder via SMS or Gmail.
    """

    list_tasks()

    # Select a task to send as a reminder
    task_num = int(input("Enter the task number to send a reminder for: ")) - 1

    tasks = []
    with open("tasks.csv", "r") as file:
        reader = csv.DictReader(file)
        tasks = list(reader)

    if task_num < 0 or task_num >= len(tasks):
        print("Invalid task number.")
        return

    task = tasks[task_num]
    message = f"""
    Hi there,

    This is a reminder for your upcoming task:

    Title: {task['title']}
    Description: {task['description']}
    Category: {task['category']}
    Due Date: {task['due_date']}

    Make sure to complete it on time!

    Best regards,
    Your Task Manager
    """

    option = input("Do you want an SMS or Gmail reminder? (Enter 'sms' or 'gmail'): ").strip().lower()

    if option == 'sms':
        send_sms_notification(message)
    elif option == 'gmail':
        send_gmail_notification(message)
    else:
        print("Invalid option. Please choose either 'sms' or 'gmail'.")


def send_sms_notification(message):
    """
    Sends a SMS notification using Twilio's API

    :param message: The message cotent to be sent via SMS
    :type message: str
    """

    # Create Twilio client
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    user_phone_number = input("Enter your phone number (with country code, e.g., +12345679): ")

    # Send the message
    try:
        sms = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=user_phone_number
        )
        print(f"SMS sent successfully! SID: {sms.sid}")
    except Exception as e:
        print(f"Failed to send SMS: {str(e)}")


def send_gmail_notification(message):
    """
    Sends an email notification using SMTP with Gmail.

    :param message: The message cotent to be sent via email
    :type message: str
    """

    # Prompt for recipient email and validate it
    while(True):
        recipient_email = input("Enter the recipient's email address: ")
        if not re.search(r"^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$", recipient_email):
            print("Invalid email format.\nPlease try again.")
        else:
            break

    # Set up the email content
    email = EmailMessage() # Create a instance of the email message
    email["From"] = SENDER_EMAIL # Set the sender's email
    email["To"] = recipient_email # Set the recipient's email
    email["Subject"] = "Task Reminder" # Assign the email subject
    email.set_content(message) # Add the body of the email

    # Create the Gmail STMP connection
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp: # Connect to Gmail's SMTP server using SSL on port 465
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD) # Log in with the sender's email and password
            smtp.send_message(email) # Send the email
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")


if __name__ == "__main__":
    main()
