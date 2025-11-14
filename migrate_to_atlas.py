"""
Migrate data from local MongoDB to MongoDB Atlas
"""
from pymongo import MongoClient
import sys

# Local MongoDB
local_uri = "mongodb://localhost:27017/"
local_client = MongoClient(local_uri)
local_db = local_client["smart_hiring_db"]

# MongoDB Atlas
atlas_uri = "mongodb+srv://sridattayedida_db_user:2nAgVgWwIEaqE5To@cluster0.yhgzpuk.mongodb.net/?appName=Cluster0"
atlas_client = MongoClient(atlas_uri)
atlas_db = atlas_client["smart_hiring_db"]

print("🔄 Starting migration from localhost to MongoDB Atlas...")
print("="*60)

# Get all collections from local database
collections = local_db.list_collection_names()
print(f"\n📦 Found {len(collections)} collections to migrate:")
for col in collections:
    print(f"   • {col}")

print("\n" + "="*60)

# Migrate each collection
for collection_name in collections:
    print(f"\n📤 Migrating: {collection_name}")
    
    # Get data from local
    local_collection = local_db[collection_name]
    documents = list(local_collection.find())
    
    if documents:
        # Drop existing collection in Atlas (fresh start)
        atlas_db[collection_name].drop()
        
        # Insert into Atlas
        atlas_collection = atlas_db[collection_name]
        result = atlas_collection.insert_many(documents)
        print(f"   ✅ Migrated {len(result.inserted_ids)} documents")
    else:
        print(f"   ⚠️  No documents to migrate")

print("\n" + "="*60)
print("✅ Migration completed successfully!")
print(f"🌐 Atlas Database: smart_hiring_db")
print(f"📊 Total collections: {len(collections)}")

# Verify admin user exists
users = list(atlas_db.users.find({"role": "admin"}))
if users:
    print(f"👤 Admin users found: {len(users)}")
    for user in users:
        print(f"   • {user['email']}")
else:
    print("⚠️  No admin users found - you may need to run init_db_simple.py with Atlas URI")

print("\n🎉 Your data is now in the cloud!")
