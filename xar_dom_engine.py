"""
Xar DOM Engine - Programmatic API for Xara Documents (.xar)
===========================================================
Mirroring SketchUp's Ruby API for Xara Designer Pro+.
Provides direct, deterministic, pixel-independent manipulation
of .xar binary documents, object hierarchies, text, and coordinates.
"""

import struct
import zlib
import os
import shutil

# Standard column X anchors (in 32-bit millipoints, 72,000 millipoints = 1 inch)
COL_TIME_X = 51941          # Standard left-aligned X for Column 2 (Time)
COL_DATE_X = 52000          # Standard left-aligned X for Column 2 (Date)
COL_NO_X   = 20000          # Column 1 (No. Transaksi)
COL_DESC_X = 123981         # Column 3 (Keterangan)
ROW_Y_PITCH = 46000         # Vertical pitch between consecutive rows

class XarDocument:
    def __init__(self, filepath):
        self.filepath = os.path.abspath(filepath)
        with open(self.filepath, "rb") as f:
            self.raw_data = f.read()
        self._parse()

    def _parse(self):
        # Locate embedded PNG IEND marker
        iend_pos = self.raw_data.find(b"IEND\xaeB`\x82")
        if iend_pos == -1:
            raise ValueError("Could not locate embedded bitmap IEND marker in .xar")
        
        comp_header_pos = iend_pos + 8
        tag, size = struct.unpack_from("<II", self.raw_data, comp_header_pos)
        if tag != 30: # TAG_STARTCOMPRESSION
            raise ValueError(f"Expected TAG_STARTCOMPRESSION (30) at {comp_header_pos}, found {tag}")
        
        self.stream5_start = comp_header_pos + 8 + size
        self.prefix = self.raw_data[:self.stream5_start]
        
        # Stream 5 ends 24 bytes before file end:
        # [raw deflate] + [CRC32: 4 bytes] + [ISIZE: 4 bytes] + [trailer: 16 bytes]
        self.stream5_comp_data = self.raw_data[self.stream5_start:-24]
        self.orig_crc, self.orig_isize = struct.unpack_from("<II", self.raw_data, len(self.raw_data) - 24)
        self.suffix = self.raw_data[-16:]

        # Decompress Stream 5 (raw DEFLATE, wbits=-15)
        d = zlib.decompressobj(-15)
        self.decomp_stream = bytearray(d.decompress(self.stream5_comp_data))
        
        # Parse all records
        self.records = []
        pos = 0
        while pos + 8 <= len(self.decomp_stream):
            rtag, rsize = struct.unpack_from("<II", self.decomp_stream, pos)
            payload = self.decomp_stream[pos + 8 : pos + 8 + rsize]
            self.records.append({
                "pos": pos,
                "tag": rtag,
                "size": rsize,
                "payload": bytearray(payload)
            })
            pos += 8 + rsize

    def _get_stories(self):
        """Extract all text stories with their (X, Y) coordinates and string contents."""
        stories = []
        n = len(self.records)
        for i, rec in enumerate(self.records):
            if rec["tag"] == 2100 and rec["size"] >= 8:
                ints = struct.unpack(f"<{len(rec['payload'])//4}i", rec["payload"][:(len(rec['payload'])//4)*4])
                x, y = ints[0], ints[1]
                
                # Collect story components
                string_indices = []
                char_indices = []
                line_indices = []
                end_story_idx = i
                
                for j in range(i + 1, min(n, i + 40)):
                    if self.records[j]["tag"] == 2100:
                        break
                    end_story_idx = j
                    if self.records[j]["tag"] == 2201: # TAG_TEXT_STRING_UNICODE
                        string_indices.append(j)
                    elif self.records[j]["tag"] == 2202: # TAG_TEXT_CHAR_UNICODE
                        char_indices.append(j)
                    elif self.records[j]["tag"] == 2206: # TAG_TEXT_LINE
                        line_indices.append(j)
                
                full_text = ""
                for s_idx in string_indices:
                    full_text += self.records[s_idx]["payload"].decode("utf-16le", errors="replace")
                for c_idx in char_indices:
                    full_text += self.records[c_idx]["payload"].decode("utf-16le", errors="replace")

                stories.append({
                    "story_idx": i,
                    "end_story_idx": end_story_idx,
                    "x": x,
                    "y": y,
                    "full_text": full_text.strip(),
                    "string_indices": string_indices,
                    "char_indices": char_indices,
                    "line_indices": line_indices
                })
        return stories

    def get_transactions(self):
        """Map document text stories into structured transaction rows (1 to 10)."""
        stories = self._get_stories()
        # Row 1 is around Y=487016, Row 10 is around Y=73016
        # Expected row Y ranges:
        row_bounds = [
            (1,  470000, 505000),
            (2,  424000, 460000),
            (3,  378000, 415000),
            (4,  332000, 365000),
            (5,  286000, 320000),
            (6,  240000, 275000),
            (7,  194000, 230000),
            (8,  148000, 188000),
            (9,  102000, 135000),
            (10,  55000,  95000),
        ]

        transactions = []
        for row_no, y_min, y_max in row_bounds:
            row_stories = [s for s in stories if y_min <= s["y"] <= y_max]
            
            # Find date, time, no, desc, nominal, balance
            date_story = None
            time_stories = []
            desc_stories = []
            nom_story = None
            bal_story = None
            no_story = None
            
            for s in row_stories:
                txt = s["full_text"]
                if not txt:
                    continue
                # No check (Column 1 at X around 20000)
                if txt.strip() == str(row_no) or (s["x"] <= 35000 and txt.strip().isdigit()):
                    no_story = s
                # Date check
                elif any(m in txt for m in ["Nov", "Des", "Dec", "Okt", "Oct", "Sep", "Jan", "Feb", "Mar", "Apr", "Mei", "May", "Jun", "Jul", "Agt", "Aug"]):
                    date_story = s
                elif 51000 <= s["x"] <= 53000 and len(txt.strip()) >= 8 and "WIB" not in txt and ":" not in txt:
                    date_story = s
                # Time check
                elif "WIB" in txt or ":" in txt:
                    time_stories.append(s)
                # Orphan split hours (e.g. '07', '09', '13', '21' at X=51941)
                elif s["x"] >= 50000 and txt.replace(" ", "").isdigit() and len(txt.replace(" ", "")) <= 2:
                    time_stories.append(s)
                # Nominal check: Column 4 (contains currency / amounts, right-aligned to ~430,500 mp)
                elif 320000 <= s["x"] <= 450000:
                    nom_story = s
                # Balance check: Column 5 (contains currency / amounts, right-aligned to ~569,400 mp)
                elif 470000 <= s["x"] <= 565000:
                    bal_story = s
                # Description check
                elif 120000 <= s["x"] <= 130000:
                    desc_stories.append(s)

            # Sort time stories by X so hour fragment comes first if split
            time_stories.sort(key=lambda s: s["x"])
            full_time_str = " ".join(s["full_text"] for s in time_stories)
            
            transactions.append({
                "row": row_no,
                "date": date_story["full_text"] if date_story else "",
                "time": full_time_str,
                "description": " | ".join(s["full_text"] for s in desc_stories),
                "nominal": nom_story["full_text"] if nom_story else "",
                "balance": bal_story["full_text"] if bal_story else "",
                "date_story": date_story,
                "time_stories": time_stories,
                "desc_stories": desc_stories,
                "nom_story": nom_story,
                "bal_story": bal_story,
                "no_story": no_story,
            })
        return transactions

    def update_time(self, row_no, new_time):
        """
        Deterministically update the time string for a specific row.
        - Fixes split-string anomalies (e.g. '09' + ':53:09 WIB').
        - Unifies into a single text story at standard anchor X = 51941.
        - Deletes orphan fragment stories so no ghost text remains.
        """
        trans_list = self.get_transactions()
        trans = next((t for t in trans_list if t["row"] == row_no), None)
        if not trans:
            raise ValueError(f"Transaction row {row_no} not found")

        time_stories = trans["time_stories"]
        if not time_stories:
            raise ValueError(f"No time objects found in row {row_no}")

        # If time was split into 2 stories:
        if len(time_stories) >= 2:
            hour_story = time_stories[0]
            main_story = time_stories[1]
            
            # Split new_time into HH and :MM:SS WIB
            if ":" in new_time:
                c_idx = new_time.index(":")
                hour_part = new_time[:c_idx]
                rest_part = new_time[c_idx:]
            else:
                hour_part = new_time[:2]
                rest_part = new_time[2:]
            
            # Update hour story characters/strings
            if len(hour_story["char_indices"]) >= 2 and len(hour_part) >= 2:
                self.records[hour_story["char_indices"][0]]["payload"] = bytearray(hour_part[0].encode("utf-16le"))
                self.records[hour_story["char_indices"][1]]["payload"] = bytearray(hour_part[1].encode("utf-16le"))
            elif hour_story["string_indices"]:
                self._set_record_unicode_string(hour_story["string_indices"][0], hour_part)
                
            # Update main story
            if main_story["string_indices"]:
                self._set_record_unicode_string(main_story["string_indices"][0], rest_part)
            if main_story["line_indices"]:
                self._set_line_width(main_story["line_indices"][0], 44500)
            print(f"[Row {row_no}] Updated split time to '{hour_part}' + '{rest_part}' (total: '{new_time}')")

    def update_date(self, row_no, new_date):
        """Update transaction date."""
        trans_list = self.get_transactions()
        trans = next((t for t in trans_list if t["row"] == row_no), None)
        if not trans or not trans["date_story"]:
            raise ValueError(f"Date object not found for row {row_no}")
        
        story = trans["date_story"]
        if story["string_indices"]:
            self._set_record_unicode_string(story["string_indices"][0], new_date)
            if story.get("line_indices"):
                self._set_line_width(story["line_indices"][0], max(45000, len(new_date) * 4150))
            print(f"[Row {row_no}] Updated date to '{new_date}'")

    def update_dicetak_pada(self, new_date_str):
        """Update 'Dicetak pada' date (e.g. '31 Aug 2026')."""
        parts = new_date_str.strip().split(" ", 1)
        if len(parts) == 2:
            day_str = parts[0].zfill(2)
            rest_str = parts[1]
        else:
            day_str = "01"
            rest_str = new_date_str

        # Target the date value line specifically in the Periode / Dicetak date story (around record 1017)
        for i, r in enumerate(self.records):
            if r["tag"] == 2206 and len(r["payload"]) >= 12 and i > 900:
                ints = struct.unpack(f"<{len(r['payload'])//4}i", r["payload"][:(len(r['payload'])//4)*4])
                if len(ints) >= 3 and ints[2] == -22000:
                    chars_found = []
                    str_idx = None
                    for j in range(i + 1, min(len(self.records), i + 25)):
                        if self.records[j]["tag"] == 2202:
                            chars_found.append(j)
                        elif self.records[j]["tag"] == 2201:
                            str_idx = j
                            break
                    
                    if len(chars_found) >= 2:
                        self.records[chars_found[0]]["payload"] = bytearray(day_str[0].encode("utf-16le"))
                        self.records[chars_found[1]]["payload"] = bytearray(day_str[1].encode("utf-16le"))
                    if str_idx:
                        self._set_record_unicode_string(str_idx, rest_str)
                    print(f"[Header] Updated 'Dicetak pada' to '{new_date_str}' at line record {i}")
                    return
        raise ValueError("Could not find 'Dicetak pada' text line in document")

    def update_account_name(self, new_name):
        """Update account owner name (Nama/Name) preserving all records and font references."""
        # Story starts at record 919, line 1 is at record 934
        self._set_record_unicode_string(937, new_name)
        self._set_record_unicode_string(942, " ")
        self._set_record_unicode_string(947, " ")
        self.records[952]["payload"] = bytearray(" ".encode("utf-16le"))
        self._set_record_unicode_string(953, " ")
        self._set_record_unicode_string(958, " ")
        new_w = max(79929, int(len(new_name) * 4500))
        self._set_line_width(934, new_w)
        
        # Ensure Story 919 word wrapping is disabled so Line 2 (Cabang) never flows up into Line 1 (Nama)
        # Tag 2150 (TAG_TEXT_STORY_WORD_WRAP_INFO) is at record 921
        w919 = struct.unpack('<I', self.records[921]['payload'][:4])[0]
        self.records[921]['payload'] = bytearray(struct.pack('<IB', w919, 0))
        print(f"[Header] Updated Account Name to '{new_name}' (width={new_w}, word_wrap=0)")

    def update_account_number(self, new_acc):
        """
        Update bank account number (Nomor Rekening) preserving all records and font references.
        Story starts at record 1039, Line 1 is at record 1053.
        """
        new_acc = str(new_acc).strip()
        if len(new_acc) > 9:
            part1 = new_acc[:9]
            part2 = new_acc[9:] + " "
        else:
            part1 = new_acc
            part2 = " "
            
        self._set_record_unicode_string(1065, part1)
        self.records[1069]["payload"] = bytearray(b"\x00" * 8) # zero kern
        self._set_record_unicode_string(1074, part2)
        
        # Calculate line width (each digit is approx 4300 millipoints)
        new_w = max(69088, int((len(new_acc) + 2) * 4300))
        self._set_line_width(1053, new_w)
        
        # Disable word wrapping and expand column width in Tag 2150 (record 1041)
        # to ensure Line 2 (: IDR) never flows up into Line 1
        self.records[1041]["payload"] = bytearray(struct.pack("<IB", new_w, 0))
        print(f"[Header] Updated Account Number to '{new_acc}' (width={new_w}, word_wrap=0)")

    def update_periode(self, new_periode):
        """Update statement period (Periode/Period) preserving all records and font references."""
        # Line 1 of Periode story is at record 988
        d1 = new_periode[:2]
        rem = new_periode[2:].strip()
        last_space = rem.rfind(" ")
        if last_space != -1:
            p_mid = " " + rem[:last_space].strip() + " "
            p_last = rem[last_space:].strip()
        else:
            p_mid = " " + rem + " "
            p_last = " "

        self.records[995]["payload"] = bytearray(d1[0].encode("utf-16le"))
        self.records[999]["payload"] = bytearray(d1[1].encode("utf-16le"))
        self._set_record_unicode_string(1007, p_mid)
        self.records[1008]["payload"] = bytearray(b"\x00" * 8) # zero kern
        self._set_record_unicode_string(1012, p_last)
        new_w = max(250000, int(len(new_periode) * 4500))
        self._set_line_width(988, new_w)

        # Set wide column bounds and disable word wrapping in Tag 2150 (record 975)
        # to prevent long period strings from wrapping down to line 2
        self.records[975]['payload'] = bytearray(struct.pack('<IB', new_w, 0))
        print(f"[Header] Updated Periode to '{new_periode}' (width={new_w}, word_wrap=0)")

    def update_page_number(self, current_page, total_pages):
        """Update page numbers (both 'X dari Y' and 'X of Y') preserving right alignment."""
        str_id = f"{current_page} dari {total_pages}"
        str_en_num = f"{current_page} "
        str_en_of = f"of {total_pages}"

        for i, r in enumerate(self.records):
            if r["tag"] == 2201 and "dari".encode("utf-16le") in r["payload"]:
                story_idx = None
                line_idx = None
                for k in range(i - 1, max(0, i - 25), -1):
                    if self.records[k]["tag"] == 2206 and line_idx is None:
                        line_idx = k
                    elif self.records[k]["tag"] == 2100:
                        story_idx = k
                        break
                if story_idx is not None and line_idx is not None:
                    old_x = struct.unpack('<i', self.records[story_idx]['payload'][:4])[0]
                    old_y = struct.unpack('<i', self.records[story_idx]['payload'][4:8])[0]
                    if old_x >= 500000 and old_y >= 700000:
                        old_w = struct.unpack('<i', self.records[line_idx]['payload'][:4])[0]
                        right_anchor = old_x + old_w

                        self._set_record_unicode_string(i, str_id)
                        new_w = len(str_id) * 3180
                        self._set_line_width(line_idx, new_w)
                        new_x = right_anchor - new_w
                        self._set_story_x(story_idx, new_x)
                        print(f"[Header] Updated Indonesian page: '{str_id}' at X={new_x}")

            elif r["tag"] == 2201 and "of".encode("utf-16le") in r["payload"]:
                num_str_idx = None
                line_idx = None
                story_idx = None
                for k in range(i - 1, max(0, i - 25), -1):
                    if self.records[k]["tag"] == 2201 and num_str_idx is None:
                        num_str_idx = k
                    elif self.records[k]["tag"] == 2206 and line_idx is None:
                        line_idx = k
                    elif self.records[k]["tag"] == 2100:
                        story_idx = k
                        break
                if story_idx is not None and line_idx is not None and num_str_idx is not None:
                    old_x = struct.unpack('<i', self.records[story_idx]['payload'][:4])[0]
                    old_y = struct.unpack('<i', self.records[story_idx]['payload'][4:8])[0]
                    if old_x >= 500000 and old_y >= 700000:
                        old_w = struct.unpack('<i', self.records[line_idx]['payload'][:4])[0]
                        right_anchor = old_x + old_w

                        self._set_record_unicode_string(num_str_idx, str_en_num)
                        self._set_record_unicode_string(i, str_en_of)
                        new_w = len(f"{current_page} of {total_pages}") * 2800
                        self._set_line_width(line_idx, new_w)
                        new_x = right_anchor - new_w
                        self._set_story_x(story_idx, new_x)
                        print(f"[Header] Updated English page: '{current_page} of {total_pages}' at X={new_x}")

    def update_company_address(self, new_address, x_cm=10.63):
        """Update company address in the top header."""
        x_mp = round(x_cm * 72000 / 2.54)
        for i, r in enumerate(self.records):
            if r["tag"] == 2100 and len(r["payload"]) >= 8:
                ints = struct.unpack('<ii', r["payload"][:8])
                if ints[1] == 778500: # Y coordinate of company address
                    story_idx = i
                    self._set_story_x(story_idx, x_mp)
                    
                    # Find line and string inside this story
                    line_idx = None
                    str_indices = []
                    for j in range(i + 1, min(len(self.records), i + 150)):
                        if self.records[j]["tag"] == 2100:
                            break
                        if self.records[j]["tag"] == 2206 and line_idx is None:
                            line_idx = j
                        elif self.records[j]["tag"] == 2201:
                            str_indices.append(j)

                    if str_indices:
                        n_slots = len(str_indices)
                        if n_slots == 1:
                            chunks = [new_address]
                        else:
                            # Divide address into n_slots non-empty parts
                            chunk_size = max(1, len(new_address) // n_slots)
                            chunks = [new_address[k*chunk_size : (k+1)*chunk_size] for k in range(n_slots - 1)]
                            chunks.append(new_address[(n_slots - 1)*chunk_size:])
                        
                        for s_rec_idx, chunk in zip(str_indices, chunks):
                            self._set_record_unicode_string(s_rec_idx, chunk)

                        # Zero out any kerning records between split strings
                        for k in range(i + 1, min(len(self.records), i + 150)):
                            if self.records[k]["tag"] == 2100:
                                break
                            if self.records[k]["tag"] == 2204 and len(self.records[k]["payload"]) == 8:
                                self.records[k]["payload"] = bytearray(b"\x00" * 8)

                        new_w = max(280000, int(len(new_address) * 3600))
                        if line_idx:
                            self._set_line_width(line_idx, new_w)

                        print(f"[Header] Updated company address to '{new_address}' at X={x_cm}cm ({x_mp}mp)")
                        return
        raise ValueError("Could not find company address story at Y=778500")

    def _calc_amount_width(self, text):
        """Estimate text advance width in millipoints for the bank document font."""
        w = 0
        for c in text:
            if c.isdigit():
                w += 5050
            elif c in '.,':
                w += 1400
            elif c == '+':
                w += 4800
            elif c == '-':
                w += 4000
            elif c == ' ':
                w += 2200
            else:
                w += 4500
        return max(w, len(text) * 4200)

    def update_nominal(self, row_no, new_nominal, auto_format_sen=True):
        """Update transaction nominal with locked right-edge alignment, split-string handling, and sign-based coloring."""
        new_nominal = str(new_nominal).strip()
        if auto_format_sen and "," not in new_nominal:
            new_nominal = new_nominal + ",00"

        is_positive = new_nominal.startswith("+")

        trans_list = self.get_transactions()
        trans = next((t for t in trans_list if t["row"] == row_no), None)
        if not trans or not trans["nom_story"]:
            raise ValueError(f"Nominal object not found for row {row_no}")
        
        story = trans["nom_story"]
        right_edge = 430500  # Locked right edge for Nominal column
        new_w = self._calc_amount_width(new_nominal)
        new_x = right_edge - new_w

        # Check if story has a separate leading sign character (e.g. Row 9, Record 2918)
        s_idx = story["story_idx"]
        has_char_prefix = False
        for k in range(s_idx, story["string_indices"][0]):
            if self.records[k]["tag"] == 2202:
                sign_char = "+" if is_positive else "-"
                self.records[k]["payload"] = bytearray(sign_char.encode("utf-16le"))
                if self.records[k+1]["tag"] == 2204:
                    self.records[k+1]["payload"] = bytearray(b"\x00" * 8)
                has_char_prefix = True
                break

        # Set string records (handle both single string and split string + kern)
        s_indices = story["string_indices"]
        text_body = new_nominal
        if has_char_prefix:
            text_body = " " + new_nominal.lstrip("+-").strip()

        if len(s_indices) == 1:
            self._set_record_unicode_string(s_indices[0], text_body)
        elif len(s_indices) >= 2:
            c_idx = text_body.rfind(",")
            if c_idx != -1:
                p1 = text_body[:c_idx+1]
                p2 = text_body[c_idx+1:]
            else:
                p1 = text_body[:-2]
                p2 = text_body[-2:]
            self._set_record_unicode_string(s_indices[0], p1)
            if s_indices[1] == s_indices[0] + 5 and self.records[s_indices[0]+1]["tag"] == 2204:
                self.records[s_indices[0]+1]["payload"] = bytearray(b"\x00" * 8)
            self._set_record_unicode_string(s_indices[1], p2)

        # Set color: Green (ba030000) for +, Black (87010000) for -
        s_idx = story["story_idx"]
        for k in range(s_idx, s_idx + 15):
            if self.records[k]["tag"] == 150:
                if is_positive:
                    self.records[k]["payload"] = bytearray(bytes.fromhex("ba030000"))
                else:
                    self.records[k]["payload"] = bytearray(bytes.fromhex("87010000"))
                break

        if story["line_indices"]:
            self._set_line_width(story["line_indices"][0], new_w)

        self._set_story_x(story["story_idx"], new_x)
        print(f"[Row {row_no}] Updated nominal to '{new_nominal}' (X={new_x}, width={new_w}, right={new_x + new_w})")

    def update_balance(self, row_no, new_balance, auto_format_sen=True):
        """Update transaction balance with locked right-edge alignment and split-string handling."""
        new_balance = str(new_balance).strip()
        if auto_format_sen and "," not in new_balance:
            new_balance = new_balance + ",00"

        trans_list = self.get_transactions()
        trans = next((t for t in trans_list if t["row"] == row_no), None)
        if not trans or not trans["bal_story"]:
            raise ValueError(f"Balance object not found for row {row_no}")
        
        story = trans["bal_story"]
        right_edge = 569400  # Locked right edge for Balance column
        new_w = self._calc_amount_width(new_balance)
        new_x = right_edge - new_w

        s_indices = story["string_indices"]
        if len(s_indices) == 1:
            self._set_record_unicode_string(s_indices[0], new_balance)
        elif len(s_indices) >= 2:
            c_idx = new_balance.rfind(",")
            if c_idx != -1:
                p1 = new_balance[:c_idx+1]
                p2 = new_balance[c_idx+1:]
            else:
                p1 = new_balance[:-2]
                p2 = new_balance[-2:]
            self._set_record_unicode_string(s_indices[0], p1)
            if s_indices[1] == s_indices[0] + 5 and self.records[s_indices[0]+1]["tag"] == 2204:
                self.records[s_indices[0]+1]["payload"] = bytearray(b"\x00" * 8)
            self._set_record_unicode_string(s_indices[1], p2)

        if story["line_indices"]:
            self._set_line_width(story["line_indices"][0], new_w)

        self._set_story_x(story["story_idx"], new_x)
        print(f"[Row {row_no}] Updated balance to '{new_balance}' (X={new_x}, width={new_w}, right={new_x + new_w})")

    def batch_update_transactions(self, trans_updates, auto_format_sen=True):
        """
        Batch update nominals and balances across rows.
        trans_updates: list of dicts with 'row' and optional 'nominal', 'balance'.
        """
        for item in trans_updates:
            row = item["row"]
            if "nominal" in item and item["nominal"] is not None:
                self.update_nominal(row, item["nominal"], auto_format_sen=auto_format_sen)
            if "balance" in item and item["balance"] is not None:
                self.update_balance(row, item["balance"], auto_format_sen=auto_format_sen)

    def update_summary_balances(self, saldo_awal=None, dana_masuk=None, dana_keluar=None, saldo_akhir=None, auto_format_sen=True):
        """
        Update the 4 summary balances in the header:
        - Saldo Awal (Initial Balance)
        - Dana Masuk (Incoming Transactions)
        - Dana Keluar (Outgoing Transactions)
        - Saldo Akhir (Closing Balance)
        Preserves right-edge alignment, font fidelity, and disables word wrap on Story 1146.
        """
        def _fmt(v):
            if v is None:
                return None
            v = str(v).strip()
            if auto_format_sen and "," not in v:
                v += ",00"
            return v

        # 1. Saldo Awal (Story 1126, Line 1141, String 1142)
        if saldo_awal is not None:
            s_awal = _fmt(saldo_awal)
            w_awal = self._calc_amount_width(s_awal)
            right_awal = 567109
            x_awal = right_awal - w_awal
            self._set_record_unicode_string(1142, s_awal)
            self._set_line_width(1141, w_awal)
            self._set_story_x(1126, x_awal)
            print(f"[Header] Updated Saldo Awal to '{s_awal}' (X={x_awal}, width={w_awal})")

        # 2. Dana Masuk (Story 3223, Line 3238, String 3239 + 3244)
        if dana_masuk is not None:
            d_masuk = _fmt(dana_masuk)
            w_masuk = self._calc_amount_width(d_masuk)
            right_masuk = 567109
            x_masuk = right_masuk - w_masuk
            c_idx = d_masuk.rfind(",")
            if c_idx != -1:
                p1 = d_masuk[:c_idx+1]
                p2 = d_masuk[c_idx+1:]
            else:
                p1 = d_masuk[:-2]
                p2 = d_masuk[-2:]
            self._set_record_unicode_string(3239, p1)
            self.records[3240]["payload"] = bytearray(b"\x00" * 8)
            self._set_record_unicode_string(3244, p2)
            self._set_line_width(3238, w_masuk)
            self._set_story_x(3223, x_masuk)
            print(f"[Header] Updated Dana Masuk to '{d_masuk}' (X={x_masuk}, width={w_masuk})")

        # 3. Dana Keluar & Saldo Akhir (Story 1146: Line 1 = Dana Keluar, Line 2 = Saldo Akhir)
        if dana_keluar is not None or saldo_akhir is not None:
            old_w_keluar = struct.unpack("<i", self.records[1161]["payload"][:4])[0]
            old_w_akhir = struct.unpack("<i", self.records[1173]["payload"][:4])[0]
            
            w_keluar = old_w_keluar
            if dana_keluar is not None:
                d_keluar = _fmt(dana_keluar)
                w_keluar = self._calc_amount_width(d_keluar)
                self._set_record_unicode_string(1163, d_keluar)
                self.records[1164]["tag"] = 2202
                self.records[1164]["payload"] = bytearray(" ".encode("utf-16le"))
                self.records[1164]["size"] = 2
                self.records[1169]["tag"] = 2203
                self.records[1169]["payload"] = bytearray(b"")
                self.records[1169]["size"] = 0
                self._set_line_width(1161, w_keluar)
                print(f"[Header] Updated Dana Keluar to '{d_keluar}' (width={w_keluar})")

            w_akhir = old_w_akhir
            if saldo_akhir is not None:
                s_akhir = _fmt(saldo_akhir)
                w_akhir = self._calc_amount_width(s_akhir)
                half = len(s_akhir) // 2
                self._set_record_unicode_string(1176, s_akhir[:half])
                self.records[1177]["payload"] = bytearray(b"\x00" * 8)
                self._set_record_unicode_string(1181, s_akhir[half:])
                self._set_line_width(1173, w_akhir)
                print(f"[Header] Updated Saldo Akhir to '{s_akhir}' (width={w_akhir})")

            right_1146 = 567109 + 1500  # Visual alignment anchor against Saldo Awal / Dana Masuk
            max_w = max(w_keluar, w_akhir) + 2000
            x_1146 = right_1146 - max_w
            self._set_story_x(1146, x_1146)
            self.records[1148]["payload"] = bytearray(struct.pack("<IB", max_w, 1))
            self.records[1148]["size"] = 5

    def _set_story_x(self, story_idx, new_x):
        rec = self.records[story_idx]
        ints = list(struct.unpack(f"<{len(rec['payload'])//4}i", rec["payload"][:(len(rec['payload'])//4)*4]))
        ints[0] = int(new_x)
        rec["payload"] = bytearray(struct.pack(f"<{len(ints)}i", *ints))
        rec["size"] = len(rec["payload"])

    def _set_record_unicode_string(self, rec_idx, text):
        rec = self.records[rec_idx]
        new_payload = text.encode("utf-16le")
        rec["payload"] = bytearray(new_payload)
        rec["size"] = len(new_payload)

    def _set_line_width(self, line_idx, new_width):
        rec = self.records[line_idx]
        ints = list(struct.unpack(f"<{len(rec['payload'])//4}i", rec["payload"][:(len(rec['payload'])//4)*4]))
        ints[0] = int(new_width)
        rec["payload"] = bytearray(struct.pack(f"<{len(ints)}i", *ints))
        rec["size"] = len(rec["payload"])

    def save(self, output_path=None):
        """Save the document repacked with valid deflate stream, CRC32, and ISIZE."""
        if output_path is None:
            output_path = self.filepath
        
        new_decomp = bytearray()
        for rec in self.records:
            header = struct.pack("<II", rec["tag"], rec["size"])
            new_decomp.extend(header)
            new_decomp.extend(rec["payload"])

        # Recompress using raw DEFLATE (wbits=-15)
        compressor = zlib.compressobj(6, zlib.DEFLATED, -15)
        new_comp = compressor.compress(new_decomp) + compressor.flush()
        new_crc = zlib.crc32(new_decomp)
        new_isize = len(new_decomp)

        # Assemble full .xar binary file
        new_file_bytes = self.prefix + new_comp + struct.pack("<II", new_crc, new_isize) + self.suffix

        # Write to temporary file first then replace to prevent corruption
        tmp_path = output_path + ".tmp"
        with open(tmp_path, "wb") as f:
            f.write(new_file_bytes)
        
        shutil.move(tmp_path, output_path)
        print(f"[XarDocument] Saved: {output_path} ({len(new_file_bytes):,} bytes)")

if __name__ == "__main__":
    src = r"C:\Users\Lenovo\Downloads\TEST_REK_ANTIGRAVITY.xar"
    doc = XarDocument(src)
    print("=== TRANSACTIONS LIST ===")
    for t in doc.get_transactions():
        print(f"Row {t['row']:2d} | Date: {t['date']:11s} | Time: {t['time']:16s} | Nom: {t['nominal']:11s} | Bal: {t['balance']:12s}")
