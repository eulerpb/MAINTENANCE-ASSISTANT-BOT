import time
from pyrogram import Client


def cadastrarDados(nomeVeiculo, nomeCliente, kmVeiculo, dataManutencao, tipoServico, valorRevisao, urlImagem, username):
    doc_ref = db.collection("Revisoes").document(nomeVeiculo.upper())
    doc_ref.set({
        "nome veículo": nomeVeiculo.upper(),
        "registros": firestore.ArrayUnion([{
            "nome cliente": nomeCliente.upper(),
            "KM veiculo": kmVeiculo,
            "data manutencao": dataManutencao,
            "tipo do servico": tipoServico.upper(),
            "valor da manutenção": valorRevisao,
            "Imagem anexada:": urlImagem,
            "cadastrado por": username
        }])
    }, merge=True)

async def upload_photo(photo_bytes):
    filename = f"{time.asctime()}.jpg"

    bucket = storage.bucket()
    blob = bucket.blob(filename)
    blob.upload_from_filename(photo_bytes)

    blob.make_public()
    url = blob.public_url
    return url