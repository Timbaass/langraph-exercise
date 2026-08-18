from langchain.tools import tool
import json

from app_agents.mcp_tools.EnuygunMCP import EnuygunMCP


def create_flight_search_tool(mcp: EnuygunMCP):

    @tool
    async def search_flights(
        origin: str,
        destination: str,
        departure_date: str,
        return_date: str | None = None,
        adults: int = 1,
        children: int = 0,
        infants: int = 0,
        cabin_class: str = "ECONOMY",
        direct_flight: bool = False,
    ):
        """
        Search for available flights between an origin and destination.

        Use this tool when the user wants to search, find, compare,
        or list available flights.

        Infer all parameters from the user's request.

        Required:
        - origin: Departure city or airport.
        - destination: Arrival city or airport.
        - departure_date: Departure date in DD.MM.YYYY format.

        Optional:
        - return_date: Return date for round-trip searches.
        - adults: Number of adults. Defaults to 1.
        - children: Number of children aged 2-12. Defaults to 0.
        - infants: Number of infants under 2. Defaults to 0.
        - cabin_class: ECONOMY, BUSINESS, PREMIUM_ECONOMY, or FIRST.
        - direct_flight: True only if the user explicitly requests
          a direct/non-stop flight.

        Return only concise flight information.
        Do not expose raw MCP/API response data.
        """

        input_data = {
            "origin": origin,
            "destination": destination,
            "departure_date": departure_date,
            "return_date": return_date,
            "adults": adults,
            "children": children,
            "infants": infants,
            "cabin_class": cabin_class,
            "direct_flight": direct_flight,
        }

        response = await mcp.call_tool("flight_search", input_data)
        payload = extract_mcp_payload(response)

        return compact_flight_response(payload)

    return search_flights


def extract_mcp_payload(response) -> dict:
    if isinstance(response, list) and response:
        first_item = response[0]
        if isinstance(first_item, dict) and "text" in first_item:
            payload = json.loads(first_item["text"])
        else:
            raise ValueError(f"Unexpected list item format: {first_item!r}")

    elif isinstance(response, dict):
        payload = response

    elif isinstance(response, str):
        payload = json.loads(response)

    elif hasattr(response, "content") and response.content:
        first_content = response.content[0]
        raw_text = getattr(first_content, "text", None)
        if not raw_text:
            raise ValueError("In MCP tool response, first content item has no 'text' attribute.")
        payload = json.loads(raw_text)

    else:
        raise ValueError(f"Unexpected MCP tool response format: {type(response)} — {response!r}")

    if not payload.get("success", True):
        raise ValueError(payload.get("error", "MCP tool returned an error."))

    return payload["data"]

def compact_flight_response(data: dict) -> dict:
    flights = []

    # ✅ DÜZELTME 2: departure verisini data["flights"]["departure"] içinden çekiyoruz
    flights_data = data.get("flights", {})
    departure_flights = flights_data.get("departure", [])

    for flight in departure_flights:
        segment = flight["segments"][0]
        price = flight["price_breakdown"]
        infos = flight["infos"]

        flights.append(
            {
                "id": flight["enuid"],
                "airline": segment["marketing_airline"],
                "flight_number": segment["flight_number"],
                "origin": segment["origin"],
                "destination": segment["destination"],
                "departure": segment["departure_datetime"]["time"],
                "arrival": segment["arrival_datetime"]["time"],
                "duration_minutes": segment["duration"]["total_minutes"],
                "price": price["total"],
                "currency": price["currency"],
                "available_seats": segment["available_seats"],
                "baggage": {
                    "carry_on_kg": infos["baggage_info"]["carryOn"]["allowance"],
                    "checked_kg": (
                        infos["baggage_info"]["firstBaggageCollection"][0]["allowance"]
                    ),
                },
            }
        )

    return {
        "flights": flights,
        "cheapest": min(flights, key=lambda x: float(x["price"])) if flights else None,
        "fastest": (
            min(flights, key=lambda x: float(x["duration_minutes"]))
            if flights
            else None
        ),
        # ✅ ARTIK DÜZGÜN ÇALIŞIYOR: Bunlar ana "data" objesinin içinden okunuyor
        "search_params": data.get("search_params"),
        "search_url": data.get("search_url"),
        "short_search_url": data.get("short_search_url"),
        "request_id": data.get("request_id"),
    }