from fastapi import FastAPI
import collections

app = FastAPI()

índice_invertido = collections.defaultdict(set)

class Documento:
    def __init__(self, contenido):
        self.contenido = contenido
        self.palabras_clave = set(contenido.lower().split())

documentos = [
    Documento("Este es el primer documento contiene información de ejemplo."),
    Documento("Este es el segundo documento también contiene información de ejemplo."),
    Documento("El tercer documento contiene datos completamente distintos."),
    Documento("El cuarto documento es este y va con contenido adicional."),
    Documento("El quinto documento es otro ejemplo de texto."),
    Documento("Documento número seis con datos relevantes."),
    Documento("Este documento siete es un ejemplo adicional."),
    Documento("El octavo documento contiene información importante."),
    Documento("Noveno documento con contenido variado."),
    Documento("El décimo y último documento de la colección.")
]

def construir_índice_invertido(documentos):
    índice_invertido = collections.defaultdict(set)
    for i, documento in enumerate(documentos):
        for palabra in documento.palabras_clave:
            índice_invertido[palabra].add(i)
    return índice_invertido

índice_invertido = construir_índice_invertido(documentos)

def buscar_en_índice_invertido(consulta, índice):
    consulta = consulta.lower()
    if consulta in índice:
        documentos_con_palabra = set()
        for doc_index in índice[consulta]:
            documento = documentos[doc_index]
            documentos_con_palabra.add((documento.contenido, consulta))
        return list(documentos_con_palabra)
    else:
        return []

@app.get("/buscar/{consulta}")
async def buscar(consulta: str):
    consulta = consulta.lower()
    resultados = buscar_en_índice_invertido(consulta, índice_invertido)
    if resultados:
        return {"resultados": resultados}
    else:
        return {"resultado": "La palabra no fue encontrada en ningún documento."}

@app.get("/")
async def bienvenido():
    return {"mensaje": "¡Bienvenido al motor de búsqueda de documentos!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)