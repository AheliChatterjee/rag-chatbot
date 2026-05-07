import json
import os
import uuid
from datetime import datetime


# folder where all sessions will be stored
SESSIONS_DIR = "sessions"

#Create the sessions directory if it doesn't exist
os.makedirs(SESSIONS_DIR, exist_ok=True)

# ----------------------- Create new sessions -----------------------
def create_new_session():
    
    session_id = str(uuid.uuid4())  # Generate a unique session ID
    
    session_data = {
    
        "session_id": session_id,

        "title": "New Chat",
        
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    
        "messages": []
    }
    save_session(session_data)
    
    return session_data

# ----------------------- Save session -----------------------

def save_session(session_data):
    
    session_path = os.path.join(
        SESSIONS_DIR,
        
        f"{session_data['session_id']}.json"
    )
    with open(session_path, "w") as file:
        json.dump(session_data, file, indent=4)
        
        
# ----------------------- Load session -----------------------

def load_session(session_id):
    
    session_path = os.path.join(
        SESSIONS_DIR, 
        f"{session_id}.json"
    )
    
    if not os.path.exists(session_path):
        
        raise FileNotFoundError(f"Session with ID {session_id} not found.")
    
    with open(session_path, "r") as file:
        session_data = json.load(file)
    
    return session_data

#----------------------- List all sessions -----------------------

def get_all_sessions():
    
    sessions = []
    
    for filename in os.listdir(SESSIONS_DIR):
        
        if filename.endswith(".json"):
            
            file_path = os.path.join(SESSIONS_DIR, filename)
            
            with open(file_path, "r") as file:
                
                session_data = json.load(file)
                sessions.append(session_data)
                
    sessions = sorted(
        sessions,
        key = lambda x: x["created_at"],
        
        reverse = True
    )
    return sessions

# ---------------- UPDATE SESSION TITLE ----------------

def update_session_title(session_data):

    if (
        session_data["title"] == "New Chat"
        and len(session_data["messages"]) > 0
    ):

        first_message = session_data["messages"][0]["content"]

        session_data["title"] = first_message[:40]

    return session_data

# ---------------- DELETE SESSION ----------------

def delete_session(session_id):

    session_path = os.path.join(

        SESSIONS_DIR,

        f"{session_id}.json"
    )

    if os.path.exists(session_path):

        os.remove(session_path)
        

# ---------------- RENAME SESSION ----------------

def rename_session(session_id, new_title):

    session_data = load_session(session_id)

    if session_data is not None:

        session_data["title"] = new_title

        save_session(session_data)