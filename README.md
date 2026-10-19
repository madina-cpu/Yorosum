# Yorosum

Customizations for the Yorosum Cafe24 store (yorosum.com).

## Language switcher (한국어 / English / O‘zbekcha)

`cafe24/language-switcher.html` adds three language buttons to the store header.

1. Cafe24 admin → 쇼핑몰 설정 → 다국어 쇼핑몰: add an English shop. For Uzbek,
   add another shop (based on English) and translate its texts into Uzbek.
2. Connect a domain to each shop (e.g. `en.yorosum.com`, `uz.yorosum.com`) and
   put those addresses in the three `href`s in the file.
3. Paste the file's contents into the header of every shop's skin
   (디자인 → 디자인 편집 → `layout/basic/layout.html` or the header include).
