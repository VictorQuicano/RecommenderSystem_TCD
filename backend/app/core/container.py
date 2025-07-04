"""
Dependency injection container for the application.
"""
from app.core.interfaces import IDataRepository, IKnnService, IDistanceService, IMatrixService
from app.repositories.data_repository import DataRepository
from app.services.knn_service import KnnService
from app.services.distance_service import DistanceService
from app.services.matrix_service import MatrixService
from app.core.distance_factory import DistanceCalculatorFactory
from app.core.config import Config


class Container:
    """Dependency injection container."""
    
    def __init__(self):
        self._config = Config()
        self._distance_factory = DistanceCalculatorFactory()
        self._data_repository: IDataRepository = None
        self._knn_service: IKnnService = None
        self._distance_service: IDistanceService = None
        self._matrix_service: IMatrixService = None
    
    @property
    def config(self) -> Config:
        """Get configuration instance."""
        return self._config
    
    @property
    def distance_factory(self) -> DistanceCalculatorFactory:
        """Get distance factory instance."""
        return self._distance_factory
    
    @property
    def data_repository(self) -> IDataRepository:
        """Get data repository instance."""
        if self._data_repository is None:
            self._data_repository = DataRepository(self._config)
        return self._data_repository
    
    @property
    def knn_service(self) -> IKnnService:
        """Get KNN service instance."""
        if self._knn_service is None:
            self._knn_service = KnnService(self._distance_factory)
        return self._knn_service
    
    @property
    def distance_service(self) -> IDistanceService:
        """Get distance service instance."""
        if self._distance_service is None:
            self._distance_service = DistanceService(self._distance_factory)
        return self._distance_service
    
    @property
    def matrix_service(self) -> IMatrixService:
        """Get matrix service instance."""
        if self._matrix_service is None:
            self._matrix_service = MatrixService()
        return self._matrix_service
