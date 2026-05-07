from rag.session_manager import (
    create_new_session,
    save_session,
    load_session,
    get_all_sessions,
    delete_session
)

# Create session
session = create_new_session()

# Add messages
session["messages"].append(
    {
        "role": "user",
        "content": "What is AI?"
    }
)

save_session(session)

print("Before delete:")
print(get_all_sessions())

# Delete session
delete_session(session["session_id"])

print("\nAfter delete:")
print(get_all_sessions())