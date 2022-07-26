#-----------------------
# BIBLIOTECAS
#-----------------------
import asyncio
from typing import Optional
from functools import wraps, partial
from concurrent.futures import ThreadPoolExecutor
#-----------------------
# CONSTANTES
#-----------------------
#-----------------------
# CLASSES
#-----------------------
class to_async():
    def __init__(self, *, executor: Optional[ThreadPoolExecutor]=None):
        self.executor = executor;
    
    def __call__(self, blocking):
        
        @wraps(blocking)
        async def wrapper(*args, **kwargs):
            loop = asyncio.get_event_loop();
            
            if not self.executor:
                self.executor = ThreadPoolExecutor();

            func = partial(blocking, *args, **kwargs);
        
            return await loop.run_in_executor(self.executor,func);
        return wrapper;
#-----------------------
# FUNÇÕES()
#-----------------------
#-----------------------
# Main()
#-----------------------
#-----------------------