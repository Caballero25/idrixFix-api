from abc import ABC, abstractmethod
from typing import Dict, Any

class IAuditoriaLogRepository(ABC):
    
    @abstractmethod
    def create_log(self, log_data: Dict[str, Any]) -> bool:
        """Crea un nuevo registro de log de auditoría."""
        pass