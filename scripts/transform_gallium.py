#!/usr/bin/env python

# 將 QWERTY 倉頡碼表轉換爲 Gallium v1（含符號修改）鍵盤佈局碼表。
#
# 原理：倉頡字根依「實體鍵位」記憶。使用者在系統層使用 Gallium 佈局，
# 故將每個倉頡碼字母（QWERTY 鍵位）改寫爲該實體鍵在 Gallium 下實際送出的字元，
# 令字根停留在原本的實體鍵位上。
#
# 佈局（實體 QWERTY 鍵位 -> Gallium 送出字元）：
#   q w e r t  y u i o p      b l d c v   j y o u ;
#   a s d f g  h j k l ;  ->  n r t s g   p h a e i
#   z x c v b  n m , . /      x q m w z   k f , . /
#
# 注意：實體 i 鍵送出 o（故倉頡碼 i->o）；實體 h 鍵送出 p，故倉頡碼 p->;，
# 分號成爲碼元。字元 i 不再出現於任何倉頡碼中。

import sys
import os

# 倉頡碼字母（QWERTY）-> Gallium 送出字元
GALLIUM = {
    'a': 'n', 'b': 'z', 'c': 'm', 'd': 't', 'e': 'd', 'f': 's', 'g': 'g',
    'h': 'p', 'i': 'o', 'j': 'h', 'k': 'a', 'l': 'e', 'm': 'f', 'n': 'k',
    'o': 'u', 'p': ';', 'q': 'b', 'r': 'c', 's': 'r', 't': 'v', 'u': 'y',
    'v': 'w', 'w': 'l', 'x': 'q', 'y': 'j', 'z': 'x',
}

# 自檢：必須爲雙射（26 個來源對應 26 個相異目標），否則會產生重碼。
assert len(GALLIUM) == 26, "GALLIUM 必須涵蓋 a-z 共 26 個字母"
assert len(set(GALLIUM.values())) == 26, "GALLIUM 目標字元發生碰撞，並非雙射"


def remap(code):
    """僅改寫 a-z 字母；'（構詞碼錨點）、Tab 等其餘字元原樣保留。"""
    return ''.join(GALLIUM[ch] if ch in GALLIUM else ch for ch in code)


def transform_file(input_file):
    if not os.path.exists(input_file):
        print(f"錯誤：找不到文件 {input_file}")
        return False

    # 輸出檔名：cangjie5.base.dict.yaml -> cangjie5_gallium.base.dict.yaml
    out_file = os.path.join(
        os.path.dirname(input_file),
        os.path.basename(input_file).replace('cangjie5.', 'cangjie5_gallium.', 1),
    )
    if out_file == input_file:
        print(f"錯誤：輸出檔名與來源相同，已略過 {input_file}")
        return False

    data_count = 0
    in_header = True

    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(out_file, 'w', encoding='utf-8') as f_out:

        for line in f_in:
            if in_header:
                # 改寫表頭 name： cangjie5.X -> cangjie5_gallium.X
                if line.startswith('name:'):
                    line = line.replace('cangjie5.', 'cangjie5_gallium.', 1)
                f_out.write(line)
                if line.strip() == '...':
                    in_header = False
                continue

            # 數據區：保留空行與註釋
            if not line.strip() or line.startswith('#'):
                f_out.write(line)
                continue

            parts = line.rstrip('\r\n').split('\t')
            # parts[0] = text（不動）; parts[1] = code; parts[2] = stem（若有）
            if len(parts) >= 2:
                parts[1] = remap(parts[1])
                if len(parts) >= 3:
                    parts[2] = remap(parts[2])
                f_out.write('\t'.join(parts) + '\n')
                data_count += 1
            else:
                f_out.write(line)  # 容錯：異常行原樣保留

    print(f"已生成 {out_file}（{data_count} 條）")
    return True


def main(argv):
    if argv:
        targets = argv
    else:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        targets = [
            os.path.join(base, 'cangjie5.base.dict.yaml'),
            os.path.join(base, 'cangjie5.stem.dict.yaml'),
            os.path.join(base, 'cangjie5.extended.dict.yaml'),
        ]

    ok = True
    for f in targets:
        ok = transform_file(f) and ok
    print("轉換完成。" if ok else "轉換過程中發生錯誤。")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
