"""Public tariff references for common German charging providers.

Prices are indicative public ad-hoc AC/DC tariffs (EUR/kWh) gathered from provider
pricing pages and can change at any time.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Tariff:
    provider: str
    ac_eur_kwh: float | None
    dc_eur_kwh: float | None
    source_url: str
    note: str = ""


TARIFFS_BY_PROVIDER = {
    "enbw": Tariff(
        provider="EnBW mobility+",
        ac_eur_kwh=0.59,
        dc_eur_kwh=0.69,
        source_url="https://www.enbw.com/elektromobilitaet/unterwegs-laden/tarife",
        note="Ad-hoc Richtwert",
    ),
    "shell": Tariff(
        provider="Shell Recharge",
        ac_eur_kwh=0.64,
        dc_eur_kwh=0.79,
        source_url="https://shellrecharge.com/de-de/tarife",
        note="Ad-hoc Richtwert",
    ),
    "ewe": Tariff(
        provider="EWE Go",
        ac_eur_kwh=0.62,
        dc_eur_kwh=0.74,
        source_url="https://www.ewe-go.de/ladetarif",
        note="Ad-hoc Richtwert",
    ),
    "mainzer": Tariff(
        provider="Mainzer Stadtwerke / ladenetz.de",
        ac_eur_kwh=0.55,
        dc_eur_kwh=0.69,
        source_url="https://www.mainzer-stadtwerke.de",
        note="Richtwert aus öffentlichen Stadtwerketarifen",
    ),
    "ionity": Tariff(
        provider="IONITY",
        ac_eur_kwh=None,
        dc_eur_kwh=0.69,
        source_url="https://ionity.eu/de/tarife",
        note="HPC-Preis ohne Abo",
    ),
}


def infer_tariff(operator_name: str | None) -> Tariff | None:
    if not operator_name:
        return None

    normalized = operator_name.lower()
    for key, tariff in TARIFFS_BY_PROVIDER.items():
        if key in normalized:
            return tariff
    return None
