"""
Xara Document CLI - Quick programmatic manipulation for Xara files
Usage examples:
    python xar_cli.py --file "path.xar" --list
    python xar_cli.py --file "path.xar" --row 1 --time "07:15:20 WIB"
    python xar_cli.py --file "path.xar" --row 3 --time "09:03:43 WIB"
    python xar_cli.py --file "path.xar" --row 10 --time "23:05:11 WIB" --nominal "-15.000,00"
"""

import argparse
import os
import sys
from xar_dom_engine import XarDocument

def main():
    parser = argparse.ArgumentParser(description="Xara Document Programmatic DOM Controller")
    parser.add_argument("--file", default=r"C:\Users\Lenovo\Downloads\TEST_REK_ANTIGRAVITY.xar", help="Path to .xar file")
    parser.add_argument("--list", action="store_true", help="List all parsed transactions")
    parser.add_argument("--row", type=int, help="Transaction row number (1-10)")
    parser.add_argument("--time", type=str, help="New time string (e.g. '07:15:20 WIB')")
    parser.add_argument("--date", type=str, help="New date string (e.g. '01 Nov 2025')")
    parser.add_argument("--nominal", type=str, help="New nominal string (e.g. '-50.000,00')")
    parser.add_argument("--balance", type=str, help="New balance string (e.g. '970.834,00')")
    parser.add_argument("--dicetak", type=str, help="New 'Dicetak pada' date (e.g. '31 Aug 2026')")
    parser.add_argument("--page", nargs=2, type=int, metavar=('CURRENT', 'TOTAL'), help="Update page number (e.g. --page 2 10)")
    parser.add_argument("--address", type=str, help="New company address string")
    parser.add_argument("--address-x", type=float, default=10.63, help="New X position in cm for company address (default: 10.63)")
    parser.add_argument("--name", type=str, help="New account name string (e.g. 'ASEP')")
    parser.add_argument("--account", "--acc", dest="account", type=str, help="New account number string (e.g. '1630000000020')")
    parser.add_argument("--periode", type=str, help="New period string (e.g. '01 Dec 202020 -31 Dec 202020')")
    parser.add_argument("--saldo-awal", type=str, help="New Saldo Awal string (e.g. '10.000')")
    parser.add_argument("--dana-masuk", type=str, help="New Dana Masuk string (e.g. '+ 100.000.000')")
    parser.add_argument("--dana-keluar", type=str, help="New Dana Keluar string (e.g. '- 3.000.321')")
    parser.add_argument("--saldo-akhir", type=str, help="New Saldo Akhir string (e.g. '15.321.974')")
    parser.add_argument("--out", type=str, help="Output path (default: overwrite source)")

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: File not found: {args.file}")
        sys.exit(1)

    doc = XarDocument(args.file)

    has_balance_mods = args.saldo_awal or args.dana_masuk or args.dana_keluar or args.saldo_akhir
    if args.list or (not args.row and not args.time and not args.nominal and not args.dicetak and not args.page and not args.address and not args.name and not args.periode and not args.account and not has_balance_mods):
        print(f"\nDocument: {args.file}")
        print("=" * 80)
        print(f"{'Row':4s} | {'Date':11s} | {'Time':16s} | {'Nominal':14s} | {'Balance':14s} | {'Status Jam'}")
        print("-" * 80)
        for t in doc.get_transactions():
            status = "Pecah (2 Objek)" if len(t["time_stories"]) > 1 else "Utuh (1 Objek)"
            print(f"{t['row']:4d} | {t['date']:11s} | {t['time']:16s} | {t['nominal']:14s} | {t['balance']:14s} | {status}")
        print("=" * 80 + "\n")
        return

    modified = False
    if args.dicetak:
        doc.update_dicetak_pada(args.dicetak)
        modified = True

    if args.page:
        doc.update_page_number(args.page[0], args.page[1])
        modified = True

    if args.address:
        doc.update_company_address(args.address, x_cm=args.address_x)
        modified = True

    if args.name:
        doc.update_account_name(args.name)
        modified = True

    if args.account:
        doc.update_account_number(args.account)
        modified = True

    if args.periode:
        doc.update_periode(args.periode)
        modified = True

    if has_balance_mods:
        doc.update_summary_balances(
            saldo_awal=args.saldo_awal,
            dana_masuk=args.dana_masuk,
            dana_keluar=args.dana_keluar,
            saldo_akhir=args.saldo_akhir
        )
        modified = True

    if args.row:
        if args.time:
            doc.update_time(args.row, args.time)
            modified = True
        if args.date:
            doc.update_date(args.row, args.date)
            modified = True
        if args.nominal:
            doc.update_nominal(args.row, args.nominal)
            modified = True
        if args.balance:
            doc.update_balance(args.row, args.balance)
            modified = True

    if modified:
        out_path = args.out if args.out else args.file
        doc.save(out_path)
        print(f"\n[OK] Selesai memperbarui dokumen pada file {out_path}.")

if __name__ == "__main__":
    main()
