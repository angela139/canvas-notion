import discord
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from user import User
import random

load_dotenv()
# Grab the API token from the .env file.
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
USER_ID = os.environ["DISCORD_USER"]

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

client = discord.Client(intents=intents)

canvasKey = os.environ["CANVAS_KEY"]
notionToken = os.environ["NOTION_TOKEN"]
notionPageId = os.environ["NOTION_PAGE_ID"]
schoolAb = os.environ["SCHOOL_URL"]
database_id = os.environ["DATABASE_ID"]

ucdavis_user = User(canvasKey, notionToken, notionPageId, schoolAb, database_id)
existing_assignments = ucdavis_user.notionProfile.getDetailAssignments()

message_sent = False


async def send_reminder(user_id, assignment_name, hours, minutes):
    global message_sent
    message_sent = True
    user = await client.fetch_user(user_id)
    reminder_string = f"Reminder: Assignment '{assignment_name}' is due in {hours} hours and {minutes} minutes!"
    await user.send(reminder_string)


async def send_urgent_reminder(user_id, assignment_name, hours, minutes):
    global message_sent
    message_sent = True
    user = await client.fetch_user(user_id)
    reminder_string = f"{user.mention} Homie hurry up: Assignment '{assignment_name}' is due in {hours} hours and {minutes} minutes!"
    await user.send(reminder_string)


async def check_assignments():
    while True:
        current_time = datetime.now(timezone.utc)
        for assignment in existing_assignments:
            due_date = datetime.strptime(assignment["date"], "%Y-%m-%dT%H:%M:%S.%f%z")
            remaining_time = due_date - current_time
            total_seconds = remaining_time.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            if timedelta(hours=2) > remaining_time > timedelta(hours=0):
                await send_urgent_reminder(USER_ID, assignment["name"], hours, minutes)
            elif timedelta(hours=28) > remaining_time > timedelta(hours=0):
                await send_reminder(USER_ID, assignment["name"], hours, minutes)

        if message_sent is True:
            angela_quotes_of_the_day = ["'You're an alcoholic every weekend'",
                                        "'I'm just better than you at this stuff'",
                                        "'What race of individuals r they'", "'Fuck it, we ball'",
                                        "'In Canada drinking age is 18'",
                                        "'Your top level is my bottom level'", "'I'm cooking chill'",
                                        "'Menace behavior'"]
            wisdom_string = f"Chun-ho-related quote: {angela_quotes_of_the_day[random.randint(0, len(angela_quotes_of_the_day) - 1)]}"
            user = await client.fetch_user(USER_ID)
            await user.send(wisdom_string)
        # Sleep for an extended period after checking assignments
        print("Exited")
        await client.close()


@client.event
async def on_ready():
    print("Bot connected to Discord.")
    client.loop.create_task(check_assignments())


client.run(DISCORD_TOKEN)
