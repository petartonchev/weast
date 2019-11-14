db.createUser(
    {
        user: "debug",
        pwd: "debug",
        roles: [
            {
                role: "readWrite",
                db: "moodstock_nosql_db"
            }
        ]
    }
)

