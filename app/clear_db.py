from firebase_setup import db

def clear_survey_responses():
    collection_ref = db.collection("survey_responses")
    docs = list(collection_ref.stream())  # convert to list to reuse

    if not docs:
        print("ℹ️ No documents found in 'survey_responses' collection.")
        return

    deleted = 0
    for doc in docs:
        print(f"🗑️ Deleting: {doc.id}")
        doc.reference.delete()
        deleted += 1

    print(f"✅ Deleted {deleted} documents from 'survey_responses'.")

if __name__ == "__main__":
    clear_survey_responses()
    print("✅ All survey responses cleared.")