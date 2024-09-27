


```
pip install -r requirements.txt
```

```sql
CREATE DATABASE IF NOT EXISTS demodb;
USE demodb;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL
);

INSERT INTO users (name, age) VALUES ('Alice', 30), ('Bob', 25);
```


```
http://127.0.0.1:5000/api/user?name=Alice
```