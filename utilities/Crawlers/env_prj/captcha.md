
- 連結網頁、截圖、解讀、填入空格、下載檔案、重新命名。

![](../../../attachments/2023-12-01-16-56-54.png)

Current source:	https://epq.moenv.gov.tw/ProjectDoc/GetCaptchaImage/

```html
<div class="form-group">
    <div class="input-group">
        <label for="CaptchaCode">驗證碼(點擊驗證碼可重新產生驗證碼)</label>
    </div>
    <div class="input-group">
        <a href="javascript:void(0);" title="重新顯示新的驗證碼" onclick="resetCaptchaImage()"><img title="重新顯示新的驗證碼" id="img-captcha" src="./g3_files/saved_resource" alt="重新顯示新的驗證碼" style="width: 100%; height: 100%;"></a>
        <button style="border:0;background:none;text-align:center" title="驗證碼語音播放" onclick="VoicePlay()" type="button">
            <i class="lnr lnr-volume-high" style="font-size: 1.3rem; line-height: 2rem; vertical-align: middle;"></i><span>▒~R▒▒~T▒</span>
        </button>
        <input type="text" class="form-control" placeholder="請輸入驗證碼" maxlength="4" data-val="true" data-val-length="驗證碼(點擊驗證碼可重新產生驗證碼)超過字數4" data-val-length-max="4" id="CaptchaCode" name="CaptchaCode" value="">
        <span class="text-danger field-validation-valid" data-valmsg-for="CaptchaCode" data-valmsg-replace="true"></span>
    </div>
</div>
```