---
layout: default
title:  環評書件摘要內容之下載
parent: PDF檔案之下載與整理
grand_parent: Crawlers
nav_order: 6
last_modified_date: 2023-12-19 16:04:26
tags: Crawlers pdf
---

# 環評書件摘要內容之下載
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>
---

## 背景

```html
<!-- 書件摘要 -->
<div role="tabpanel" class="tab-pane active" id="divTabAbstract">
    <div class="table-responsive" style="margin: 2px 2px 2px 2px;">
        <table class="table table-condensed table-hover">
            <tbody>
                <tr class="active">
                    <th id="a" style="width: 15%;">
                        <label for="lbDOCTY">書件類別</label>
                    </th>
                    <td headers="a">
                        <span id="lbDOCTYP" tabindex="700" Name="lbDOCTY" class="form-control input-sm" style="width: 150px;">說明書</span>
                    </td>
                    <th id="l" style="width: 15%;">
                        <label for="txDST">基地行政區</label>
                    </th>
                    <td headers="l">
                        <input name="ctl00$txDST" type="text" value="高雄市" readonly="readonly" id="txDST" tabindex="711" Name="txDST" class="form-control input-sm" />
                    </td>
                </tr>
                <tr>
                    <th id="b">
                        <label for="txDEPN">開發單位名稱</label>
                    </th>
                    <td headers="b" colspan="3">
                        <input name="ctl00$txDEPN" type="text" value="國巨股份有限公司" id="txDEPN" tabindex="701" Name="txDEPN" class="form-control input-sm" />
                    </td>
                </tr>
                <tr class="active">
                    <th id="c">
                        <label for="txDIRORG">目的事業主管機關</label>
                    </th>
                    <td headers="c" colspan="3">
                        <input name="ctl00$txDIRORG" type="text" value="高雄市政府經濟發展局" id="txDIRORG" tabindex="702" Name="txDIRORG" class="form-control input-sm" />
                    </td>
                </tr>
                <tr>
                    <th id="d" style="width: 15%;">

                        <label id="lbCONSULTI" for="txCONSULTI">顧問機構名稱</label>
                    </th>
                    <td headers="d" colspan="3" id="d1">
                        <input name="ctl00$txCONSULTI" type="text" value="傳閔工程顧問有限公司" id="txCONSULTI" tabindex="703" Name="txCONSULTI" class="form-control input-sm" />
                    </td>
                </tr>
                <tr class="active">
                    <th id="e">
                        <label for="txDAREA">基地面積</label>
                    </th>
                    <td headers="e">
                        <input name="ctl00$txDAREA" type="text" value="0.1582公頃" id="txDAREA" tabindex="704" Name="txDAREA" class="form-control input-sm" />
                    </td>
                    <th id="m">
                        <label for="txDSIZE">開發規模</label>
                    </th>
                    <td headers="m">
                        <input name="ctl00$txDSIZE" type="text" value="1582平方公尺" id="txDSIZE" tabindex="712" Name="txDSIZE" class="form-control input-sm" />
                    </td>
                </tr>
                <tr>
                    <th id="f">
                        <label for="txDECAL">開發計畫類別</label>
                    </th>
                    <td headers="f" colspan="3">
                        <input name="ctl00$txDECAL" type="text" value="工廠之設立" id="txDECAL" tabindex="705" Name="txDECAL" class="form-control input-sm" />
                    </td>
                </tr>
                <tr class="active">
                    <th id="g">
                        <label for="txDSTNAME">環保主管機關</label>
                    </th>
                    <td headers="g">
                        <input name="ctl00$txDSTNAME" type="text" value="高雄市" id="txDSTNAME" tabindex="706" Name="txDSTNAME" class="form-control input-sm" />
                    </td>
                    <th id="n">                              
                    </th>
                    <td headers="n">                              
                    </td>
                </tr>
                <tr>
                    <th id="h">
                        <label for="txSEDAT">繳費日期</label>
                    </th>
                    <td headers="h">
                        <input name="ctl00$txSEDAT" type="text" value="0831215" id="txSEDAT" tabindex="707" Name="txSEDAT" class="form-control input-sm" />
                    </td>
                    <th id="o">
                        <label for="txPORCS">處理情形</label>
                        <label for="txMSNO" style="color: white; opacity: 0.1;">處理情形</label>
                    </th>
                    <td headers="o">
                        <input name="ctl00$txPORCS" type="text" value="辦理結案" id="txPORCS" tabindex="714" Name="txPORCS" class="form-control input-sm" />                              
                    </td>
                </tr>
                <tr class="active">
                    <th id="i">
                        <label for="txTRIA">初審會日期</label>
                    </th>
                    <td headers="i">
                        <input name="ctl00$txTRIA" type="text" value="-" id="txTRIA" tabindex="708" Name="txTRIA" class="form-control input-sm" />
                    </td>
                    <th id="p">
                        <label for="txEXTP">審查結論別</label>
                        <label for="Comment2" style="color: #f5f2f2; opacity: 0.1;">我有意見</label>
                    </th>
                    <td headers="p">
                        <div>
                            <div class="FloatLeft">
                                <input name="ctl00$txEXTP" type="text" value="通過環境影響評估審查" id="txEXTP" tabindex="716" Name="txEXTP" class="form-control input-sm" />
                            </div>
                            <div class="pull-right">
                                <p>
                                    <a id="Comment2" href="#" class="btn btn-primary" data-toggle="modal" data-target="#modalComment2" tabindex="717">
                                        <span class="glyphicon glyphicon-envelope"></span>&nbsp;&nbsp;我有意見
                                    </a>
                                </p>
                            </div>
                        </div>
                    </td>
                </tr>
                <tr>
                    <th id="j">
                        <label for="txCOMIT">委員會日期</label>
                    </th>
                    <td headers="j" colspan="3">
                        <input name="ctl00$txCOMIT" type="text" value="-" id="txCOMIT" tabindex="709" Name="txCOMIT" class="form-control input-sm" style="width: 150px;" />
                    </td>
                </tr>
                <tr class="active">
                    <th id="k">
                        <label for="txNOTES">備註</label>
                    </th>
                    <td headers="k" colspan="3">
                        <input name="ctl00$txNOTES" type="text" value="定稿本 84.10" id="txNOTES" tabindex="710" Name="txNOTES" class="form-control input-sm" />
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</div>
<!-- 審查結論 -->
<div role="tabpanel" class="tab-pane" id="divTabExct">
    <div class="table-responsive" style="margin: 5px 5px 5px 5px;">
        <table class="table table-condensed table-hover">
            <tbody>
                <tr class="active">
                    <td>
                        <div>
                            <label for="txEXCT" style="color: #f5f2f2; opacity: 0.1;">審查結論</label>
                        </div>
                        <div>
                            <textarea name="ctl00$txEXCT" rows="2" cols="20" id="txEXCT" tabindex="717" Name="txEXCT" class="form-control input-sm" style="height:245px;width:99%;">
「國巨股份有限公司高雄廠毗鄰地變更擴建計畫環境影響說明書」審查結論

發文日期:中華民國85年9月7日
發文字號:(85)府環一字第172491號

一、請補充開發前後廢棄物（含污泥、廢液、溶劑）之排放量及其比較表，並說明處理方案，以不增加污染排放量為原則。
二、圖3.3-1 請將基地現況（含警衛室、廠內之道路、增建廠房部分）明確標示。
三、同意開發公司開發後，遇有三級以上地震震度十(即定期)，請合格公司檢查是否變形或發生傾斜等狀況，並將結果送環保局及隨時備查。
四、建議依意見補充說明後，同意開發。
五、位置圖要列出比例，施工、營運路線（用顏色表示）。
六、噪音、振動現況在文章內也要說明，同時要列出使用儀器及校正方法；又噪音、振動的測定值有特別變化的時段要說明其原因，如 P.4-26 噪音 8: 00、振動 11: 00（此時段的噪音沒有特別變化，為什麼只有振動特別大），P.4-27振動 7 : 00（此時段的噪音不足特別低，但振動特別小）等等，以後請注意。
七、請列出 PCU 計算之參考文獻。
八、參考文獻中有著作者姓名的要列出著作者姓名（如P.6-6)。
九、振動的預估須加施工道路的部份，使用△Ldn之變化評估。
十、噪音、振動的實測日期（表內有，文章內沒有）及開始時問要列在文章內。
十一、監測計畫表（(P.7-10)之監測頻率，營運期間內要加幾年內（如一年內、二年內等等，不然如工廠運轉期間永久要做）。
十二、噪音量測定值之表內，由下第一行，夜間時間 22:00-05:00 請改 00:00-05:00 及 22:00-24:00。(附件六) 十三、本案如前次意見及本次意見確實有修改時，不必再審，但通知時請加承諾事項確實實行，監測報告按期送環保局，不然依環境影響評估法第十七條，第二十三條處分。
十四、本計畫如予執行，應依環境影響說明書承諾事項，歷次審查意見辦理。若有差異部份，以本府審查意見為主。
十五、本案如經許可，應依環評法第七條及同法施行細則第十八條、第二十二條規定於動工前在當地適當地點舉行公開 說明會。
十六、本案於取得目的事業主管機關核發之開發單位許可後，逾三年始實施開發行為應依環境影響評估法施行細則第四十二條規定辦理。</textarea>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</div>                                                
```

