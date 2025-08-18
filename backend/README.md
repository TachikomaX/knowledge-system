# 数据库ER图

```markdown
+-----------+        +-------------+        +-------------+
|   users   |        |    notes    |        |    tags     |
+-----------+        +-------------+        +-------------+
| id (PK)   | 1    n | id (PK)     | n    n | id (PK)     |
| username  |--------| user_id (FK)|--------| name        |
| email     |        | title       |        +-------------+
| password  |        | content     |
| created_at|        | summary     |
+-----------+        | created_at  |
                     | updated_at  |
                     +-------------+
                            |
                            | 1
                            n
                    +----------------+
                    |   note_tags    |
                    +----------------+
                    | note_id (FK)   |
                    | tag_id  (FK)   |
                    +----------------+
```
