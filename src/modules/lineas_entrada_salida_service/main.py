from fastapi import FastAPI

from src.modules.lineas_entrada_salida_service.infrastructure.api.routers.lineas_entrada_router import router as lineas_entrada_router
from src.shared.cors_config import configure_cors

app = FastAPI(
    #TODO preguntarle a david el nombre y la descripcion
    title="Lineas Entrada-Salida API",
    description="Microservicio para la modificación de lineas de entrada-salida",
    version="1.0.0",
)

# Configurar CORS}
# TODO preguntarle a david el nombre
configure_cors(app, "Linea Entrada-Salida Service")

app.include_router(lineas_entrada_router, prefix="/api/lineas-entrada", tags=["Lineas Entrada"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "lineas_entrada_salida_service"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8003)

    #TODO preguntar sobre como se llaman las lineas o algo asi, para no poner literalmente lineas, porque en la linea hay algo, bueno que hay en esa linea o nque se hace o que, porque si pongo lineas, se asume que se toman las lineas del 1 al 6, y en realidad se están tomando lo que hay dentro de cada linea