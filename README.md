# 倉頡輸入法

配方： ℞ **cangjie**

[Rime](https://rime.im) 倉頡輸入方案

  - `cangjie5` : 倉頡五代，支持擴展區漢字、「快趣」詞組編碼
  - `cangjie5_express` : 單字快打模式，唯一候選字自動上屏
  - `cangjie5_gallium` : 倉頡五代 · Gallium 鍵盤佈局版
  - `cangjie5_gallium_express` : Gallium 版單字快打模式

## Gallium 佈局版

適用於在系統層使用 **Gallium v1（含符號修改）** 佈局的使用者，令倉頡字根停留在原本的
實體鍵位上。佈局（實體 QWERTY 鍵位 → Gallium 送出字元）：

```
q w e r t  y u i o p      b l d c v   j y o u ;
a s d f g  h j k l ;  ->  n r t s g   p h a e i
z x c v b  n m , . /      x q m w z   k f , . /
```

碼表由 `scripts/transform_gallium.py` 自 `cangjie5.*` 碼表自動轉換產生
（`cangjie5_gallium.{base,stem,extended}.dict.yaml`）。上游碼表更新後重新執行該腳本即可。

注意事項：

  - 因實體 `p` 鍵在此佈局送出 `;`，**分號 `;` 成爲倉頡碼元**。請勿在 `default.custom.yaml`
    中將 `;` 綁定爲選字／翻頁／上屏鍵，否則會與輸入衝突。
  - 字母 `i` 不再出現於任何倉頡碼，但仍保留於 `alphabet` 中以供拼音反查（`` ` `` 前綴）使用。
  - 需在 `default.custom.yaml` 的 `schema_list` 中加入 `cangjie5_gallium`
    （及 `cangjie5_gallium_express`）方可啓用。

## 安裝

[東風破](https://github.com/rime/plum) 安裝口令： `bash rime-install cangjie`

授權條款：見 [LICENSE](LICENSE)
