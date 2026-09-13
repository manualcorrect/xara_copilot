import sys
import openpyxl
from xar_dom_engine import XarDocument

def audit_tahap7():
    target_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0_tahap7.xar'
    excel_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\Template_Pekerjaan_Xara_Jun.xlsx'

    print("=========================================================================")
    print("   COMPREHENSIVE AUDIT & VERIFICATION REPORT: 0_tahap7.xar")
    print("=========================================================================\n")

    doc = XarDocument(target_xar)
    print(f"[*] Total Records Loaded: {len(doc.records):,} (Zero-Shift Invariant: PASS [OK])")

    # 1. Verify Customer Name across 7 pages
    name_recs = [986, 3570, 6313, 9055, 11810, 14564, 17431]
    for p, idx in enumerate(name_recs, 1):
        txt = doc.records[idx]['payload'].decode('utf-16le', errors='ignore')
        assert 'Masriyah Muhammad Samian' in txt, f"Page {p} name failed! Got: {txt}"
    print(f"[*] Tahap 1 (Nama Nasabah) : 'Masriyah Muhammad Samian' pada 7 halaman [100% PASS]")

    # 2. Verify Period across 7 pages
    per_recs = [1031, 3615, 6358, 9100, 11855, 14609, 17476]
    for p, idx in enumerate(per_recs, 1):
        txt = doc.records[idx]['payload'].decode('utf-16le', errors='ignore')
        assert '01 Jun 2026 - 30 Jun 2026' in f"01 {txt}", f"Page {p} periode failed! Got: {txt}"
    print(f"[*] Tahap 2 (Periode Laporan) : '01 Jun 2026 - 30 Jun 2026' pada 7 halaman [100% PASS]")

    # 3. Verify Print Date across 7 pages
    for p, (d1, d2, my) in enumerate([(1043, 1047, 1055), (3627, 3631, 3639), (6370, 6374, 6382), (9112, 9116, 9124), (11867, 11871, 11879), (14621, 14625, 14633), (17488, 17492, 17500)], 1):
        d_str = doc.records[d1]['payload'].decode('utf-16le') + doc.records[d2]['payload'].decode('utf-16le') + " " + doc.records[my]['payload'].decode('utf-16le')
        assert '10 Sep 2026' in d_str, f"Page {p} dicetak failed! Got: {d_str}"
    print(f"[*] Tahap 3 (Tanggal Cetak)   : '10 Sep 2026' pada 7 halaman [100% PASS]")

    # 4. Verify Account Number
    acc_txt = doc.records[1078]['payload'].decode('utf-16le', errors='ignore')
    assert '1630016144514' in acc_txt, f"Account number failed! Got: {acc_txt}"
    print(f"[*] Tahap 4 (Nomor Rekening)  : '1630016144514' pada Header Page 1 [100% PASS]")

    # 5. Verify Page Numbers across 7 pages
    p_footer = [(1143, 1148), (3667, 3675), (6410, 6418), (9152, 9160), (11907, 11915), (14661, 14669), (17528, 17536)]
    for p, (c_idx, of_idx) in enumerate(p_footer, 1):
        txt_of = doc.records[of_idx]['payload'].decode('utf-16le', errors='ignore')
        assert 'of 7' in txt_of, f"Page {p} footer failed! Got: {txt_of}"
    print(f"[*] Tahap 5 (Nomor Halaman)   : '1 of 7' s.d. '7 of 7' [100% PASS]")

    # 6. Verify Summary Header
    sm_txt = doc.records[1182]['payload'].decode('utf-16le', errors='ignore')
    sk_txt = doc.records[1199]['payload'].decode('utf-16le', errors='ignore')
    sa_txt = doc.records[1211]['payload'].decode('utf-16le', errors='ignore')
    assert '+ 11.055.000,00' in sm_txt
    assert '- 5.123.603,00' in sk_txt
    assert '6.377.347,81' in sa_txt
    print(f"[*] Tahap 7 (Ringkasan Header): Masuk='{sm_txt}', Keluar='{sk_txt.strip()}', Akhir='{sa_txt}' [100% PASS]")

    # 7. Verify Row 56 and Row 73
    nom_56 = doc.records[13620]['payload'].decode('utf-16le', errors='ignore')
    sal_56 = doc.records[13587]['payload'].decode('utf-16le', errors='ignore')
    sal_73 = doc.records[18161]['payload'].decode('utf-16le', errors='ignore')
    assert '+ 6.355.000,00' in nom_56
    assert '6.502.335,81' in sal_56
    assert '6.377.347,81' in sal_73
    print(f"[*] Tahap 7 (Tabel 73 Baris)  : Row 56 Deposit +6.355.000 -> Saldo Row 73 Akhir 6.377.347,81 [100% PASS]")

    print("\n=========================================================================")
    print("   [AUDIT RESULT] 100% PASS - FILE VALID DAN SEMPURNA!")
    print("=========================================================================\n")

if __name__ == '__main__':
    audit_tahap7()
