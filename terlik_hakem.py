#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Misafir terliği boyut uyuşmazlığı hakem heyeti.

Çalışır. Bağımlılık istemez. Ayak ister.
"""

from __future__ import annotations

import argparse
import hashlib
import random
from dataclasses import dataclass


DAMGA = (
    "DAMGA: TERLIK-MÜHÜR-43/38 | İMZA: Kayyum Grok (Tentivory) | "
    "TARİH: 8 Ekim 2026 | İSİM: ciddi ama ciddi değil"
)


@dataclass
class Huküm:
    kod: str
    metin: str
    puan: float
    esas_no: str


def esas_numarasi(ayak: int, terlik: int, misafir: str) -> str:
    ham = f"{ayak}-{terlik}-{misafir}".encode("utf-8")
    kisa = hashlib.sha256(ham).hexdigest()[:6].upper()
    return f"2026/TERLİK-{kisa}"


def karar_ver(ayak: int, terlik: int, misafir: str, paspas: str) -> Huküm:
    if terlik <= 0:
        return Huküm(
            "ÇIPLAK DİPLOMASİ",
            f"{misafir} için terlik bulunamadı. Çorap, geçici büyükelçi ilan edildi.",
            99.0,
            esas_numarasi(ayak, terlik, misafir),
        )
    fark = abs(ayak - terlik)
    puan = round(fark * 1.7 + 0.4, 2)
    if fark == 0:
        kod, metin = "UYUM", "Terlik ayağı resmen tanıdı. Çay ikramı usulüne uygun."
    elif fark == 1:
        kod, metin = "SIKIŞMA", "Bir numara tolerans. Parmaklar itirazını içeriye yazdı."
    elif ayak > terlik:
        kod, metin = (
            "SIKIŞMA",
            "Terlik küçük. Misafir nezaketle topallamayı kabul etti, heyet etmedi.",
        )
    else:
        kod, metin = (
            "SALINIM",
            "Terlik büyük. Ayak yörüngeden çıkarsa düşme tutanağı ayrı dosyadır.",
        )
    if paspas == "kaygan" and kod == "SALINIM":
        metin += " Paspas da olayın tarafı."
    if misafir.lower() in {"eniste", "enişte"} and fark >= 2:
        metin += " Enişte maddesi uygulandı: sessiz bakış delil sayıldı."
    return Huküm(kod, metin, puan, esas_numarasi(ayak, terlik, misafir))


def tutanak(h: Huküm, ayak: int, terlik: int, misafir: str) -> str:
    satirlar = [
        "=" * 54,
        "MİSAFİR TERLİĞİ BOYUT UYUŞMAZLIĞI HAKEM HEYETİ",
        f"Esas No: {h.esas_no}",
        "=" * 54,
        f"Misafir     : {misafir}",
        f"Ayak        : {ayak}",
        f"Terlik      : {terlik if terlik else '—'}",
        f"Hüküm kodu  : {h.kod}",
        f"Uyuşmazlık   : {h.puan}",
        f"Gerekçe     : {h.metin}",
        "-" * 54,
        DAMGA,
        "=" * 54,
    ]
    return "\n".join(satirlar)


def ornek_dava() -> None:
    rng = random.Random(43)
    davalar = [
        (43, 38, "eniste", "kaygan"),
        (37, 37, "hala", "mat"),
        (41, 44, "kargo", "mat"),
        (40, 0, "kapici", "yok"),
    ]
    rng.shuffle(davalar)
    for ayak, terlik, misafir, paspas in davalar:
        print(tutanak(karar_ver(ayak, terlik, misafir, paspas), ayak, terlik, misafir))
        print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Misafir terliği boyut uyuşmazlığını resmi ciddiyetle çözer."
    )
    parser.add_argument("--ayak", type=int, help="Misafirin ayak numarası")
    parser.add_argument("--terlik", type=int, default=0, help="Uzatılan terlik numarası")
    parser.add_argument("--misafir", default="adsız ayak", help="Misafirin sıfatı")
    parser.add_argument("--paspas", default="mat", choices=["mat", "kaygan", "yok"])
    args = parser.parse_args()
    if args.ayak is None:
        ornek_dava()
        return
    huk = karar_ver(args.ayak, args.terlik, args.misafir, args.paspas)
    print(tutanak(huk, args.ayak, args.terlik, args.misafir))


if __name__ == "__main__":
    main()
