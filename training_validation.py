from datetime import datetime
import os
from application_logging import logger

class train_validation:
    def __init__(self, path):
        self.log_writer = logger.App_Logger()
    

    def train_validation(self):
        try:
            self.log_writer.log(self.fileobj, 'Start of training validation')
            
