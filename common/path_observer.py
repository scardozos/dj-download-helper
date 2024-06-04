import time
import watchdog.events
from .constants import SUPPORTED_AUDIO_EXTENSIONS

class Handler(watchdog.events.RegexMatchingEventHandler):
    def __init__(self, controller):
        
        watchdog.events.RegexMatchingEventHandler.__init__(
            self,
            regexes=[f'.*{extension}$' for extension in SUPPORTED_AUDIO_EXTENSIONS],
            #ignore_regexes=".*crdownload$",
            ignore_directories=True, 
            case_sensitive=False
        )

        self.controller = controller
    
        
    #def on_any_event(self, event: watchdog.events.FileSystemEvent): self.controller.notify(event)
    def on_created(self, event): self.controller.notify(event)
    def on_modified(self, event): self.controller.notify(event)
    
    #def on_moved(self, event): self.controller.notify(event)