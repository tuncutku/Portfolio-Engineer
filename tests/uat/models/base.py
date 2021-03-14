import os


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    @property
    def url(self):
        return os.environ["APP_URI"]
    
    @property
    def title(self):
        
