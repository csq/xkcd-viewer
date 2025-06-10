
class Comic:
    def __init__(self, id=int, month=str, day=str, year=str, title=str, alt=str, image_url=str):
        self.id = id
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
    
    def get_id(self):
        return self.id
    
    def __str__(self):
        return f"Comic {self.id} | Title: {self.title} | Date: {self.get_date()} | image: {self.image_url}\n"
