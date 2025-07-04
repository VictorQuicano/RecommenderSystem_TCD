"""
Data-related API routes.
"""
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from app.core.container import Container

router = APIRouter()
container = Container()


@router.get("/", response_model=List[str])
async def get_column_names(dataset: str = Query(...)) -> List[str]:
    """Get column names (users) from a dataset."""
    try:
        return container.data_repository.get_user_columns(dataset)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/matrix")
async def get_matrix(dataset: str = Query(...)):
    """Get matrix representation of a dataset."""
    try:
        df = container.data_repository.get_dataset(dataset)
        matrix_data = container.matrix_service.get_matrix_data(df)
        return matrix_data
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/datasets")
async def get_available_datasets() -> List[str]:
    """Get list of available datasets."""
    try:
        return container.data_repository.get_available_datasets()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/compare")
async def compare_users(
    u1: str = Query(..., description="First user to compare"),
    u2: str = Query(..., description="Second user to compare"),
    metric: str = Query(..., description="Distance metric to use"),
    dataset: str = Query("Movie_Ratings.csv", description="Dataset to use")
):
    """Compare two users using a specified distance metric."""
    try:
        df = container.data_repository.get_dataset(dataset)
        distance = container.distance_service.calculate_distance(df, u1, u2, metric)
        return {"distance": distance}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/knn")
async def knn_neighbors(
    user: str = Query(..., description="Target user"),
    k: int = Query(..., description="Number of neighbors to find"),
    dataset: str = Query("Movie_Ratings.csv", description="Dataset to use"),
    distance: str = Query("euclidean", description="Distance metric to use")
):
    """Find k nearest neighbors for a user."""
    try:
        df = container.data_repository.get_dataset(dataset)
        neighbors = container.knn_service.find_neighbors(df, user, distance, k)
        return neighbors
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/metrics")
async def get_available_metrics() -> List[str]:
    """Get list of available distance metrics."""
    try:
        return container.distance_service.get_available_metrics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
