from fastapi import FastAPI

app = FastAPI()

índice_invertido = {}

documento1 = "Este es el primer documento. Contiene información de ejemplo."
documento2 = "Este es el segundo documento. También contiene información de ejemplo."
documento3 = "Otro documento diferente con datos distintos."

def construir_índice_invertido(documentos):
    índice = {}
    for id_doc, contenido_doc in enumerate(documentos):
        palabras = contenido_doc.split()
        for palabra in palabras:
            palabra = palabra.lower()
            if palabra not in índice:
                índice[palabra] = [id_doc]
            else:
                índice[palabra].append(id_doc)
    return índice

documentos = [documento1, documento2, documento3]
índice_invertido = construir_índice_invertido(documentos)

def buscar_en_índice_invertido(consulta, índice, documentos):
    consulta = consulta.lower()
    if consulta in índice:
        ids_docs = índice[consulta]
        resultado = [documentos[id_doc] for id_doc in ids_docs if id_doc < len(documentos)]
        return resultado
    else:
        return []

@app.post("/agregar_documento/{id_documento}")
async def agregar_documento(id_documento: str, texto: str):
    global índice_invertido

    palabras = texto.split()
    for palabra in palabras:
        palabra = palabra.lower()
        if palabra not in índice_invertido:
            índice_invertido[palabra] = []
        índice_invertido[palabra].append(id_documento)
    return {"mensaje": f"Documento {id_documento} agregado al índice invertido"}

@app.get("/buscar/{consulta}")
async def buscar(consulta: str):
    consulta = consulta.lower()
    resultado = buscar_en_índice_invertido(consulta, índice_invertido, documentos)
    return {"resultado": resultado}

@app.get("/")
async def bienvenido():
    return {"mensaje": "¡Bienvenido al motor de búsqueda de documentos!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8300)


