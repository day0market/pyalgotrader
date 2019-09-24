# OES-API Update Guide    {#update_guide}

OES_0.15.9 / 2019-05-31
-----------------------------------

### 1. APIUpdate Summary

  1.  Compatible server v0.15.5.1 versionAPI, Customers can choose not to upgrade (We recommend upgrading, To support business version Kechuang)
  2.  fix: repairAPIWe can not support a value greater than1024File descriptor problem
  3.  New sub-type securities
      - Branch board stock (OES_SUB_SECURITY_TYPE_STOCK_KSH)
      - Branch board Depositary Receipts (OES_SUB_SECURITY_TYPE_STOCK_KCDR)
      - Shanghai and London throughCDR (OES_SUB_SECURITY_TYPE_STOCK_HLTCDR)
  4.  New subscription rights issue corresponding to the type of trading OES_BS_TYPE_ALLOTMENT, To support the placement of business
  5.  Define new product type attribute, And reflected in the following structure:
      - Securities Information (OesStockBaseInfoT/OesStockItemT)
      - Securities issuance information (OesIssueBaseInfoT/OesIssueItemT)
      - Stock holdings information (OesStkHoldingBaseInfoT/OesStkHoldingItemT)
      - Return commission (OesOrdCnfmT/OesOrdItemT)
      - Return on turnover (OesTrdCnfmT/OesTrdItemT)
      - The issuance of securities information query interface(OesApi_QueryIssue)Filters
      - Stock holdings information query interface(OesApi_QueryStkHolding)Filters
  6.  To support Kechuang board, Extended data structures, and the corresponding query result (Compatible with previous versionsAPI)
      - Securities account basic information (OesInvAcctBaseInfoT, OesInvAcctItemT) To add the following fields:
          - Branch board interests (kcSubscriptionQuota)
      - Spot Products basic information (OesStockBaseInfoT, OesStockItemT) To add the following fields:
          - Limit the maximum number of buy (lmtBuyMaxQty)
          - Limit the number of limit buy (lmtBuyMinQty)
          - Sell ​​Limit the maximum number of (lmtSellMaxQty)
          - Limit the number of sell limit (lmtSellMinQty)
          - Market price to buy the maximum number of (mktBuyMaxQty)
          - Limit the number of market price to buy (mktBuyMinQty)
          - Market price to sell the maximum number of (mktSellMaxQty)
          - Limit the number of market sell (mktSellMinQty)
      - Overview client Overview shareholder account information (OesInvAcctOverviewT) To add the following fields:
          - Branch board interests (kcSubscriptionQuota)
  7.  Reconstruction of ups and downs stop price、Price range field is named, Add new aliases for these fields (Compatible with previous versionsAPI)
      - ceilPrice => upperLimitPrice
      - floorPrice => lowerLimitPrice
      - priceUnit => priceTick
  8.  The adjustment delegate type certificate (eOesOrdTypeShT)
      - increase 'Counterparty best price declaration (OES_ORD_TYPE_SH_MTL_BEST)' Types of (Only for Kechuang board)
      - increase 'The party declared the best price (OES_ORD_TYPE_SH_MTL_SAMEPATY_BEST)' Types of (Only for Kechuang board)
  9.  Shareholders' rights to enumerate account transactions(eOesTradingPermissionT)New in
      - Branch board trading privileges (OES_PERMIS_KSH)
  10. New error code1035、1036、1274、1275, Adjustment error code1007、1022Description information
      | error code | description
      | ---- | ---------------
      | 1007 | Non-service opening hours
      | 1022 | Not yet supported or not yet opened this business
      | 1035 | Illegal product type
      | 1036 | Black and white list check failed
      | 1274 | Shareholder account no trading rights through depositary receipts of Shanghai and London
      | 1275 | Shareholder account no trading rights Kechuang board

### 2. Server update summary

  1. Support the rights issue subscription service
  2. Support for the customer to set restrictions prohibit buying and selling securities of a branch
  3. Support reverse repurchase delayed until closing time15:30
  4. Support Branch board business
  5. Other repair system defects, Improve security

### 3. Branch board market order price protection explanation

  1. During Kechuang board market order trade, Protection limit fill in the delegation requestordPriceIn the field (For the motherboard market order, Commission requestordPriceFields meaningless)
  2. For five days prior to listing、No price limit of Securities on the Branch, Protection of market order required limit, And the protective unit price subject to price changes
  3. For five days after the listing、There are price limits of Securities on the Branch, Market Order An order of protection can fill in a valid value or price0
     - For the price of buying commission, Commission requestordPricefill0It will be used as a protective limit price limit
     - For the market to sell commission, Commission requestordPricefill0It will be used as a lower limit price limit protection
  4. For Kechuang plate securities have price limits:
     - When the market price is higher than the limit buy entrusted the protection limit price, The use of funds trading limit price freeze, Commissioned by normal processing
     - When the market price is lower than buying commission protection limit price, The use of protective transaction price freeze funds
     - When the market price is lower than buying commission protection limit price, Commission will be rejected
     - When the market price is lower than the selling commission protection limit price, Commissioned by normal processing
     - When the market price is higher than the selling price protection delegate limit price, Commission will be rejected


---

OES_0.15.7.4 / 2018-09-28
-----------------------------------

### 1. APIUpdate Summary

  1. Compatible server v0.15.5.1 versionAPI，Customers can choose not to upgrade (We recommend upgrading)
  2. fix: When multiple threads simultaneously fix initializationAPIThe log, Cause problems with duplicate log information output
  3. APIAdd the following interfaces
    | API                          | description
    | ---------------------------- | ---------------
    | OesApi_SendBatchOrdersReq    | Batch commission
    | OesApi_SendBatchOrdersReq2   | Batch commission
    | OesApi_SendChangePasswordReq | Modify client login password，Only supports15:00After modifying
    | OesApi_SetLastError          | Set the current threadAPIError number
    | OesApi_GetLastError          | Get the current thread LastAPICall the wrong number failed
    | OesApi_SetCustomizedDriverId | Obtain the device serial number has been set
    | OesApi_GetCustomizedDriverId | Device serial number is provided
    | OesApi_GetClientOverview     | Overview obtain client information
    | OesApi_QueryCounterCash      | Queries Cabinet fund information(Supports only part of the main counter)
    | OesApi_QueryMarketState      | Query state of the market(Shenzhen currently only get to market conditions)
    | OesApi_HasMoreCachedData     | Not return channel acquisition data buffer callback processing length
    | OesApi_SetThreadUsername     | Set the login user name for the current thread
    | OesApi_SetThreadPassword     | Set login password of the current thread
    | OesApi_SetThreadEnvId        | Set the client environment number of the current thread
  4. New analogy to send a return message channel: State of the market push(Currently only push the Shenzhen market status)，Subscribe default conditions do not subscribe to this message
  5. New Securities Depositary Receipts corresponding sub-categories OES_SUB_SECURITY_TYPE_STOCK_CDR
  6. Return header structure(OesRptMsgHeadT)Increase execType Field，It is used to indicate the type of return on execution(referenceeOesExecTypeTdefinition)。
  7. Query Interface Security Information(OesApi_QueryStock)In Add new filter“Type of securities”、“Securities subcategories”
  8. Interface inquiry commission(OesApi_QueryOrder)In Add new filter“Type of securities”、“Business type”
  9. Query Interface turnover(OesApi_QueryTrade)In Add new filter“Type of securities”、“Business type”
  10. Check stock holdings Interface(OesApi_QueryStkHolding)In Add new filter“Type of securities”
  11. Adjust the access to payment commission request interface, Support Yinzhengzhuanzhang between banks and Cabinet
  12. Customer funds increased information identifies whether to ban access to gold
  13. Shareholders customer information to identify whether an increase in prohibited transactions
  14. Securities transaction information in an increase subtype、The original number of commission、Original order price
  15. New section error code
    | error code | description
    | ---- | ---------------
    | 1029 | Password unchanged
    | 1030 | Illegal source categories
    | 1031 | Illegal type of encryption
    | 1032 | Illegal client device serial number
    | 1033 | No available node
    | 1271 | Shareholder account no trading authority Depositary Receipts
    | 1272 | Permissions shareholder accounts did not trade stock enterprise innovation
    | 1273 | Illegal access to payment transfer type

### 2. Server update summary

  1. Support Change Password
  2. Support batch commission
  3. stand byCDRtransaction、Innovative companies stock trading
  4. New features in emergency withdrawals end monitoring and management
  5. Disk before the system starts to increase, and the late knock operation。Pre-construction（9:00）You can query data，But the transaction will not be accepted and access to payment。After the call it a day（15:10）Trading will not be accepted，But it can be performed out of gold、Change Password and query data。
  6. Repair system defects，Improve the management and fault recovery processing


---

OES_0.15.5.16 / 2018-09-28
-----------------------------------

### 1. APIUpdate Summary

  1. Compatible server v0.15.5.1 versionAPI, Customers can choose not to upgrade (We recommend upgrading)
  2. fix: When multiple threads simultaneously fix initializationAPIThe log, Cause problems with duplicate log information output
  3. increase OesApi_HasMoreCachedData interface, A return has been received but not yet cached data length processed callback
  4. increase OesApi_GetLastError interface, Return for the lastAPICall the wrong number failed
  5. increase OesApi_QueryCounterCash interface, Funds for information query the main cabinet (Supports only part of the main cabinet)
  6. increase OesApi_GetClientOverview interface, Summary information for the client query
  7. Set current thread to increase user login name/login password/Interface number of the client environment
  8. Spot filter criteria query interface product information in new types of securities、Securities sub-type filters
  9. Adjust the access to payment commission request interface, Support Yinzhengzhuanzhang between banks and Cabinet
  10. Customer funds increased information identifies whether to ban access to gold
  11. Shareholders customer information to identify whether an increase in prohibited transactions
  12. Securities transaction information in an increase subtype、The original number of commission、Original order price

### 2. Server update summary

  1. stand byCDRtransaction、Innovative companies stock trading
  2. New emergency cancellation function monitoring and management side
  3. Repair system defects, Improve the management and fault recovery processing


---

OES_0.15.5.11 / 2018-06-20
-----------------------------------

### 1. APIUpdate Summary

  1. APIno change
  2. Compatible server v0.15.5.1 versionAPI, Customers can choose not to upgrade (We recommend upgrading)

### 2. Server update summary

  1. Repair system defects
  2. Improve fault tolerance
  3. Other functional updates


---

OES_0.15.5.4 / 2018-02-22
-----------------------------------

### 1. APIUpdate Summary

  1. Compatible server v0.15.5.1 versionAPI, Customers can choose not to upgrade
  2. fix: ResolvedWindowsCompatibility issues under
  3. fix: Notes error correction information ('Commission results (OesCommissionRateItemT)' in feeRate Incorrect field precision Description)
  4. APIPriority will automatically get to useip/macinformation，Only automatically acquiredip/macWhen information is illegal，We will use the client's ownip/mac
  5. CorrectionETFProduct information fields spelling errors (preTrdaingDay => preTradingDay)
  6. increase OesApi_GetLastRecvTime、OesApi_GetLastSendTime interface, Get the latest channel for sending/Time to accept the message
  7. When the login fails, able to pass errno/SPK_GET_ERRNO() Get to the specific cause of failure

### 2. Server update summary

  1. fix: Optimize return Push，Improve the fairness of the push service
  2. fix: There is no backfill repair at the time of commission confirmed exchOrdId The problem
  3. The server will reject from the local loopback address as well as illegalIP/MACLogin address


---

OES_0.15.5 / 2017-11-12
-----------------------------------

### 1. Update Summary

  1. APINo increase in the client environment(clEnvId)，Number of different client environments(clEnvId)Commissioned by the sequence number in the(clSeqNo)Sequences independently of each other
  2. Increase independent withdrawals Interface，Supported by clEnvId+clSeqNo Carried out withdrawals
  3. Return channel support messaging subscriptions，Subscribe to return all types of messages by default
  4. New types of return messages：Notify capital changes、Position change notification
  5. After the withdrawals, commissioned successfully executed，Supplementary status is withdrawn commissioned push
  6. Query interface type callback methods defined adjustment，Query Callback Interface increase isEnd Mark
  7. Open interest positions increased costs related information field，It will affect the structure and open interest positions returned by the query structure change notification
  8. APIIn the log output delay statistics on exit

### 2. For more updates

#### 2.1 APINo increase in the client environment(clEnvId)

  - clEnvId No client environment，It is used to distinguish client instance reported delegate。For each client to assign different instance clEnvId，Such examples of these clients can maintain their own clSeqNo Without interfering with each other
  - The client can use different instances of the same clEnvId Login server。These use the same this time clEnvId The client instances share the same clSeqNo sequence
  - clEnvId The client is the range __[0~99]__ ([100~127] A reserved section，The client should be avoided)
  - able to pass OesApi_GetClEnvId() The client interface to obtain this instance is bound clEnvId
  - Service maintained by the information commission，Will record the transmission source client end of this delegate instance is bound clEnvId。Commissioned report message(OesOrdCnfmT.clEnvId) with Commissioned inquiry response(OesOrdItemT.clEnvId) This information will carry
  - Please refer to the configuration file settings oes_client_sample.conf in [oes_client].clEnvId Setting parameters

#### 2.2 Increase independent withdrawals Interface

  - Increase independent withdrawals Interface OesApi_SendOrderCancelReq()
  - Interface pCancelReq Parameters pCancelReq->mktId Mandatory
  - Interface pCancelReq Parameters pCancelReq->invAcctId、pCancelReq->securityId Optional。If you fill in will be withdrawn and the match delegate to make
  - It remains to be withdrawn by commission clOrdId Carried out withdrawals way。If the interface pCancelReq->origClOrdId > 0，Then by prioritypCancelReq->origClOrdId It was commissioned to match the withdrawal of cancellation
  - It was commissioned by withdrawal clEnvId+clSeqNo Carried out withdrawals scene，If the interface pCancelReq->origClEnvId = 0，Then the current instance is bound client default clEnvId As the withdrawal of commission clEnvId Carried out withdrawals。That，For cancellation commissioned for example given client，When withdrawals pCancelReq->origClEnvId You can write0； __If you want to withdrawals of other customers entrust instance issues of end，You need to write accurate withdrawals interface pCancelReq->origClEnvId Field__

#### 2.3 Return channel support messaging subscriptions

  - by default，Subscribe to all types of return messages
  - Please refer to the configuration file settingsoes_client_sample.conf in [oes_client].rpt.subcribeRptTypes  Setting parameters

#### 2.4 New capital changes、Position change notification

  - Two new push message return：OESMSG_RPT_CASH_ASSET_VARIATION (Notify capital changes)、OESMSG_RPT_STOCK_HOLDING_VARIATION (Position change notification)
  - As a result of delegation request、Principal transactions、Commissioned caused cancellation of funds available、Changes in available positions，Will trigger capital changes return channel/Position change notification
  - To buy a sum of commission, for example，OESThe server will in turn push the following message：
    1. OESMSG_RPT_ORDER_INSERT News (The new commission trigger)
    2. OESMSG_RPT_CASH_ASSET_VARIATION News（Due to the freezing of funds triggered）
    3. OESMSG_RPT_ORDER_REPORT News（Because the exchange commission in return trigger）
    4. OESMSG_RPT_TRADE_REPORT News（Exchange traded due to return trigger）
    5. OESMSG_RPT_CASH_ASSET_VARIATION News（Traded funds caused due to deductions trigger）
    6. OESMSG_RPT_STOCK_HOLDING_VARIATION News（Due to the increase in turnover caused by trigger positions）

#### 2.5 Supplementary status is withdrawn commissioned push

  - Was successfully commissioned in order to buy a sum of withdrawals, for example，Return return channel will in turn push follows news：
    1. Cancellation of commission OESMSG_RPT_ORDER_INSERT News
    2. Cancellation of commission OESMSG_RPT_ORDER_REPORT News
    3. __Be withdrawn__ Entrusted OESMSG_RPT_ORDER_REPORT News
    5. OESMSG_RPT_CASH_ASSET_VARIATION News（Due to trigger the release of frozen funds）

#### 2.6 Query interface type callback methods defined adjustment

  - Adjust the query interface callback method type definition F_OESAPI_ONMSG_T => F_OESAPI_ON_QRY_MSG_T
  - Query interface callback method to increase parameters OesQryCursorT *pQryCursor，use pQryCursor->isEnd Determine whether it is the last query

#### 2.7 Open interest positions increased costs related information field

  - 'Stock holdings information (OesStkHoldingItemT)' Struct field increases:
    1. Richu total cost of carry (originalCostAmt)
    2. Japan total purchase amount (totalBuyAmt)
    3. Japan sold a total amount (totalSellAmt)
    4. Japan total purchase cost (totalBuyFee)
    5. Japan sold a total cost (totalSellFee)
    6. Cost of carry price (costPrice)

#### 2.8 Interface callback method returns type definitions adjustment

  - Interface callback method returns type definitions adjustment F_OESAPI_ONMSG_T => F_OESAPI_ON_RPT_MSG_T
  - Interface callback method returns the actual parameter list does not change

#### 2.9 Other adjustments

  - Commissioned an independent increase in the return on information exchange error code field
    1. The original error code field OesOrdCnfmT.ordRejReason constant
    2. When the commission was beaten back to waste a single Exchange，OesOrdCnfmT.ordRejReason Interpretation is “Exchange rejected”，At this point you need to refer to the specific cause of error OesOrdCnfmT.exchErrCode，This field carries the exchange defined error code
  - Adjust the definition of the state commission
    1. delete 'OES_ORD_STATUS_DECLARING (Positive News)' status
    2. Heavy naming OES_ORD_STATUS_NORMAL => OES_ORD_STATUS_NEW (new order)
    3. Retention OES_ORD_STATUS_NORMAL Defined as a compatible version switch
  - Return a message type definition adjustment
    1. Rename the return message type OESMSG_RPT_ORDER_REJECT => OESMSG_RPT_BUSINESS_REJECT (OESBusiness refusal, Entrust/Withdrawals and the like check failed wind control)
    2. Retention OESMSG_RPT_ORDER_REJECT Defined as a compatible version switch
  - Adjustment 'Financial information(OesCashAssetItemT)' Some of the fields in:
    3. 'current balance'Rename the field currentBal => currentTotalBal
  - NewAPIinterface 'ObtainAPIThe release number (OesApi_GetApiVersion)'
  - NewAPIinterface 'Get the current trading day (OesApi_GetTradingDay)'
  - Adjusting commissions query resultsfeeRateAccuracy field，When the calculation mode is the commission ‘By Amount’ Time，feeRate Field represents the ratio of precision by 'millionth' => 'One ten-millionth'


---

OES_0.15.3 / 2017-08-14
-----------------------------------

### update content

  1. Spot Products basic information(OesStockBaseInfoT) in
    - Adjustment field isQualificationRequired => qualificationClass,
        Please refer to the value eOesQualificationClassT
    - New field Product risk level(securityRiskLevel)，Please refer to the value eOesSecurityRiskLevelT
    - New field Reverse repurchase deadline(repoExpirationDays)
    - New field Models accounting for the number of days(cashHoldDays) Field
  2. Customer funds basic information(OesCashAssetBaseInfoT) in
    - Rename the field Opening Balance(originalBal => beginningBal)
    - New field Beginning available balance(beginningAvailableBal)
    - New field Beginning desirable balance(beginningDrawableBal)
    - New field Current Reversal Amount(Net capital red red blue complement, reversalAmt)
    - New field current balance(currentBal)
    - Rename the field The current available balance(tradeAvlAmt => currentAvailableBal)
    - Rename the field Current desirable balance(withdrawAvlAmt => currentDrawableBal)
  3. Customer base information(OesCustBaseInfoT) in
    - New Agency logo(institutionFlag) Field
    - New Investors Category(investorClass) Field
  4. Securities account basic information(OesInvAcctBaseInfoT) in
    - Adjustment field '(Shareholder account access restrictions, acctLimit)'
        - Types of uint32 => uint64
        - Heavy naming acctLimit => Limits
    - Adjustment field '(Shareholders' rights/Client privilege, acctRight)'
        - Types of uint32 => uint64
        - Heavy naming acctRight => permissions
  5. APINew Interface Send request access to payment commission(OesApi_SendFundTrsfReq) interface
  6. APINew Interface Query with the number of new shares、In the ballot information(OesApi_QueryLotWinning) interface
  7. New ‘IPO、In the ballot information inquiry’ Relevant messages defined
    - New field Query IPO、Information filtering conditions in the ballot(OesQryLotWinningFilterT)
    - New field IPO、Winning content(OesLotWinningItemT)
    - New field Query IPO、In the ballot information request(OesQryLotWinningReqT)
    - New field Query IPO、Response in the ballot information(OesQryLotWinningRspT)
  8. Access to payment service reject message type changes OesFundTrsfReqT => OesFundTrsfRejectT
  9. Access to payment of commission rewards structure(OesFundTrsfReportT) In new fields Error code information(errorInfo)
  10. Access to payment commissioned by state(eOesFundTrsfStatusT) in
    - Adjust the macro definition OES_FUND_TRSF_STS_RECV => OES_FUND_TRSF_STS_UNDECLARED
    - Adjust the macro definition OES_FUND_TRSF_STS_DCLR => OES_FUND_TRSF_STS_DECLARED
    - New state Cabinet to report before the instruction has to be rolled back(OES_FUND_TRSF_STS_UNDECLARED_ROLLBACK)
    - New state After the instruction has to be rolled back to report Cabinet(OES_FUND_TRSF_STS_DECLARED_ROLLBACK)
    - New state Access to payment instruction is completed，Waiting for the end of the transaction(OES_FUND_TRSF_STS_WAIT_DONE)
    - New state Pending the implementation of the access to payment(OES_FUND_TRSF_STS_SUSPENDED)
  11. Error code when a transaction fails to insufficient permissions subdivision(For details, see README Error code table section)


---

OES_0.12.9 / 2017-06-06
-----------------------------------

### update content

  1. useAPIWhen initiating IPO，Subscription commissionbsTypeNeed to fill ‘OES_BS_TYPE_SUBSCRIPTION’
  2. can useAPIQuery Interface shareholder accounts(OesApi_QueryInvAcct)IPO shareholders to obtain the amount of the account(OesInvAcctItemT.subscriptionQuota)
  3. can useAPIQuery securities issuance Product Information Interface(OesApi_QueryIssue)To subscribe new shares to obtain information on the date of(OesIssueItemT)
  4. can useAPISpot product information query interfaces(OesApi_QueryStock)Bonds acquired every hundred dollars the amount of interest accrued(OesStockItemT.bondInterest)，
    This field is accurate to eight membered after，which is123400000Equivalent to a third of four per cent $ 1.2
  5. Commissioned by the sale of government bonds interest involved，You can refer to‘The delegate confirms information(OesOrdCnfmT)’Medium manner‘Freeze Interest(frzInterest)’、‘Interest has occurred(cumInterest)’Field
  6. Interest related to the sale of bond transactions，You can refer to‘Transaction confirmation information(OesTrdCnfmT)’Medium manner‘Interest has occurred(cumInterest)’Field
  7. ‘Business type’Rename the macro definition，For details, seeOES_0.12.8.2Modified version history。Original macro definition will be discarded after the next version


---

OES_0.12.7 / 2017-04-13
-----------------------------------

### 1. The main updates
  1. useAPIWhen the reverse repurchase commission issued，Reverse repurchase commissionbsTypeThe need to assign ‘OES_BS_TYPE_CS’，Instead of the usual‘Sell’。
  2. useAPIWhen the reverse repurchase commission issued，ordQty Units field represents‘Zhang’Instead of‘hand’。
  3. Return channel expansion in both categories news：‘Access to payment commissioned response-Business refusal（OESMSG_RPT_FUND_TRSF_REJECT）’
    with‘Access to payment reports commissioned by the Executive(OESMSG_RPT_FUND_TRSF_REPORT)’ 。
    - Access to payment services commission refused to return messages return a message body structure OesFundTrsfReqT，
    - Return messages to and from the implementation of the report commissioned by gold return a message body structure OesFundTrsfReportT，
    - If you do notoesMake a deposit can ignore these two types of return messages within the system
  4. inmds_api.h、oes_api.hIncreasesutilReference library header files，APIUsers only need to referencemds_api.h、oes_api.h，
    No longer need to explicitly referencesutilLibrary header files

### 2. Other adjustments：
  1. There are no independent access to payment channels，clientConfiguration can be removed62**Ports configured
  2. Adjusting commissions query resultsfeeRateAccuracy field，When the calculation mode is the commission ‘By Amount’ Time，
     feeRate Field represents the ratio of precision by 'One hundred thousandth' => 'millionth'
  3. ‘Cost calculation model’ The name of the macro definition adjustment eOesCalFeeModeT => eOesCalcFeeModeT
  4. New Bond、Fund securities category，AdjustmentETFType of securities macro definition of value
  5. New securities sub-category definitions
  6. Spot products to increase basic information“Securities subcategories”Field，And renaming“Buy Units”、“Sell ​​Unit”Field
  7. ETFProduct basic information added“Type of securities”、“Securities subcategories”Field
  8. ETFStocks increased basic information“Securities subcategories”Field
