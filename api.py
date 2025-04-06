import logging
import os
import json
from fastapi import FastAPI, Request, Response, logger
from pydantic import BaseModel

# TODO: Ovo nam ovdje ne treba
from services.mongodb_services import add_message, delete_phone_number_data, get_chat_history
from services.woocomerce_service import get_woocomerce_products
from utils import generate_response, process_message

app = FastAPI()
logger = logging.getLogger("uvicorn")


@app.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

    logger.info(
        f"Verify webhook: mode={mode}, token={token}, challenge={challenge}")
    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return Response(content=challenge, media_type="text/plain")
        else:
            return Response(content="Forbidden", status_code=403)
    return Response(content="Not Found", status_code=404)


@app.post("/webhook")
async def webhook(request: Request):
    body_bytes = await request.body()
    body = json.loads(body_bytes)

    logger.info(f"Received webhook event: {body}")
    if body.get("object") == "whatsapp_business_account":
        for entry in body.get("entry", []):
            for change in entry.get("changes", []):
                if change.get("field") == "messages":
                    value = change.get("value", {})
                    if "messages" in value:
                        for message in value.get("messages", []):
                            await process_message(message)
    return {"status": "ok"}


@app.get("/delete")
async def delete():
    await delete_phone_number_data("+38763534038")


@app.get("/health")
async def health_check():
    # res = await generate_response("Nemam neki budžet", "+38763534038")
    # mocked_data = [
    #     {
    #         "role": "user",
    #         "content": "Pozdrav, započeo sam malo trenirati i što mi preporučujete da uzmem, kreatin proteine ili tako nešto jer se ne razumijem u to"
    #     },
    #     {
    #         "role": "assistant",
    #         "content": "Pozdrav! Drago mi je da si započeo s treninzima, to je sigurno veliki korak prema zdravijem načinu života! Da bih ti mogao bolje pomoći, mogu li te pitati nekoliko pitanja?\n\nKakvi su tvoji ciljevi s treninzima? Pokušavaš li izgraditi mišiće, izgubiti težinu ili možda nešto drugo?"
    #     },
    #     {
    #         "role": "user",
    #         "content": "izgubiti težinu"
    #     },
    #     {
    #         "role": "assistant",
    #         "content": "Odlično! Gubitak težine je sjajan cilj. Možeš li mi reći koju vrstu treninga prakticiraš? Je li to teretana, aerobik, ili možda nešto treće? Također, koliko često treniraš?"
    #     },
    #     {
    #         "role": "user",
    #         "content": "uglavnom trčanje"
    #     },
    #     {
    #         "role": "assistant",
    #         "content": "Super, trčanje je odličan način za sagorijevanje kalorija! S obzirom na tvoj cilj gubitka težine i tip treninga, razmišljam o dodacima koji ti mogu pomoći. \n\nImate li kakva ograničenja ili alergije, posebno u vezi s dodacima prehrani? Također, koji je tvoj budžet za ovu vrstu proizvoda?"
    #     },
    #     {
    #         "role": "user",
    #         "content": "Nemam nikakve alergije, što se tie cijene gledao bih nešto što nije preskupo ipak"
    #     },
    #     {
    #         "role": "assistant",
    #         "content": "Razumijem, hajde da pronađemo nešto u tvom cjenovnom rangu. \n\nS obzirom na to da želiš izgubiti težinu, preporučio bih ti mogućnost uzimanja fat burnera, koji mogu pomoći u ubrzavanju metabolizma i sagorijevanju masti. \n\nImam jedan proizvod koji bi mogao biti dobar za tebe:\n\nThermogenic Fat Burner 120 kapsula  \nCijena: 54.90 KM  \nStanje: Dostupno na skladištu  \n\nZašto je ovo savršen izbor za tebe:  \nOvaj fat burner pomaže u ubrzavanju metabolizma i sagorijevanju masnih naslaga, što može pridonijeti tvom cilju gubitka težine dok trčiš. Sadrži L-karnitin, zeleni čaj i kofein koji pomažu u definiciji mišića i regulaciji apetita.\n\nKako koristiti:  \nPreporučuje se uzeti 2 kapsule dnevno, najbolje prije obroka ili treninga.\n\nLink: Thermogenic Fat Burner\n\nŽeliš li još informacija o ovom proizvodu ili da preporučim nešto drugo?"
    #     },
    #     {
    #         "role": "user",
    #         "content": "Postoje li neke posljedice od uzimanja ovoga?"
    #     },
    #     {
    #         "role": "assistant",
    #         "content": "Dobar upit! Kao i kod svih dodataka prehrani, mogu se pojaviti određene individualne reakcije. Evo nekoliko općenitih informacija:\n\n1. Kofein: Može izazvati nervozu, nesanicu ili povećanu otkucaje srca, posebno ako si osjetljiv na njega.\n2. L-karnitin: Obično se smatra sigurnim, ali može izazvati probavne smetnje kod nekih ljudi.\n3. Zeleni čaj: U umjerenim količinama je obično bezopasan, ali velike doze mogu uzrokovati probleme s jetrom kod nekih osoba.\n\nPreporučujem da se posavjetuješ s liječnikom ili nutricionistom prije nego što započneš uzimanje dodataka, pogotovo ako imaš drugih zdravstvenih problema.\n\nJe li to sve što bi te zanimalo o ovome proizvodu ili možda želiš više informacija?"
    #     },
    # ]
    # # for data in mocked_data:
    # #     await add_message("+38763534038", data["role"], data["content"])

    # res = await get_chat_history("+38763534038")

    # return {"status": "healthy"}
    res = await get_woocomerce_products()
    return {"response": res}


def start_api():
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
