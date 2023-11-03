from fastapi import FastAPI

app = FastAPI()

índice_invertido = {}

documentos = [
    "Este es el primer documento contiene información de ejemplo.",
    "Este es el segundo documento también contiene información de ejemplo.",
    "El tercer documento contiene datos completamente distintos.",
    "El cuarto documento es este y va con contenido adicional.",
    "El quinto documento es otro ejemplo de texto.",
    "Documento número seis con datos relevantes.",
    "Este documento siete es un ejemplo adicional.",
    "El octavo documento contiene información importante.",
    "Noveno documento con contenido variado.",
    "El décimo y último documento de la colección."
]

titulos = [
    "Documento 1", "Documento 2", "Documento 3", "Documento 4", "Documento 5",
    "Documento 6", "Documento 7", "Documento 8", "Documento 9", "Documento 10"
]

def construir_índice_invertido(documentos):
    índice = {}
    for id_doc, contenido_doc in enumerate(documentos):
        palabras = contenido_doc.lower().split()
        for palabra in palabras:
            if palabra not in índice:
                índice[palabra] = [id_doc]
            else:
                if id_doc not in índice[palabra]:
                    índice[palabra].append(id_doc)
    return índice

índice_invertido = construir_índice_invertido(documentos)

def buscar_en_índice_invertido(consulta, índice, documentos):
    consulta = consulta.lower()
    if consulta in índice:
        ids_docs = índice[consulta]
        resultados = [{"titulo": titulos[id_doc], "contenido": documentos[id_doc]} for id_doc in ids_docs]
        return resultados
    else:
        return []

@app.get("/buscar/{consulta}")
async def buscar(consulta: str):
    consulta = consulta.lower()
    resultados = buscar_en_índice_invertido(consulta, índice_invertido, documentos)
    if resultados:
        return {"resultado": resultados}
    else:
        return {"resultado": "La palabra no fue encontrada en ningún documento."}

@app.get("/")
async def bienvenido():
    return {"mensaje": "¡Bienvenido al motor de búsqueda de documentos!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)