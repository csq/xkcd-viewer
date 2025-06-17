class Comic:
    def __init__(self, num=int, month=str, day=str, year=str, title=str, alt=str, image_url=str):
        self.num = num
        self.month = month
        self.day = day
        self.year = year
        self.title = title
        self.alt = alt
        self.image_url = image_url
    
    def get_date(self):
        return f"{self.month}/{self.day}/{self.year}"
    
    def get_title(self):
        return self.title
    
    def get_alt(self):
        return self.alt
    
    def get_image_url(self):
        return self.image_url

    def get_num(self):
        return self.num

    def save(self, conn):
        # If the comic num already exists, skip it
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM comics WHERE num = ?", (self.num,))
        row = cursor.fetchone()
        if row:
            self.id = row[0]
            return

        # Insert a new Comic
        cursor.execute("""
            INSERT INTO comics (num, month, day, year, title, alt, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (self.num, self.month, self.day, self.year, self.title, self.alt, self.image_url))
        self.id = cursor.lastrowid
        conn.commit()

    @staticmethod
    def get_all(conn):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM comics")
        rows = cursor.fetchall()
        return [Comic(row[1], row[2], row[3], row[4], row[5], row[6], row[7]) for row in rows]

    @staticmethod
    def get_by_id(conn, id):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM comics WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            return Comic(row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        else:
            return None

    @staticmethod
    def get_by_num(conn, comic_num):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM comics WHERE num = ?", (comic_num,))
        row = cursor.fetchone()
        if row:
            return Comic(row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        else:
            return None

    def __str__(self):
        return f"Comic {self.num} | Title: {self.title} | Date: {self.get_date()} | image: {self.image_url}\n"
