# OES-API Change Log    {#changelog}

OES_0.15.9_RC1 / 2019-04-28
==============================================

  * New sub-type securities
    - Branch board stock (OES_SUB_SECURITY_TYPE_STOCK_KSH)
    - Branch board Depositary Receipts (OES_SUB_SECURITY_TYPE_STOCK_KCDR)
  * To support Kechuang board, Extended data structures, and the corresponding query result (Compatible with previous versionsAPI)
    - Securities account basic information (OesInvAcctBaseInfoT, OesInvAcctItemT) To add the following fields:
        - Branch board interests (kcSubscriptionQuota)
  * Spot Products basic information (OesStockBaseInfoT, OesStockItemT) To add the following fields:
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
  * Reconstruction of ups and downs stop price、Price range field is named, Add new aliases for these fields (Compatible with previous versionsAPI)
    - ceilPrice => upperLimitPrice
    - floorPrice => lowerLimitPrice
    - priceUnit => priceTick
  * The adjustment delegate type certificate (eOesOrdTypeShT)
    - increase 'Counterparty best price declaration (OES_ORD_TYPE_SH_MTL_BEST)' Types of (Only for Kechuang board)
    - increase 'The party declared the best price (OES_ORD_TYPE_SH_MTL_SAMEPATY_BEST)' Types of (Only for Kechuang board)
  * Shareholders' rights to enumerate account transactions(eOesTradingPermissionT)New in
    - Branch board trading privileges (OES_PERMIS_KSH)
  * New error code
    - 1275, Shareholder account no trading rights Kechuang board
    - 1036, Black and white list check failed

OES_0.15.8 / 2019-02-22
==============================================

  * fix: repairAPIWe can not support a value greater than1024File descriptor problem（becauseselectlimits，When the value is larger than the file descriptor1024Time，It causes a stack overflow）

OES_0.15.8_RC3 / 2019-01-14
==============================================

  * Commissioned returns and returns in new supply dealOESInternal use 'Trading Gateway platform partition number(__tgwPartitionNo)' Field (Protocol compatibility)
  * Adjustment error description
    - 1007, Non-service opening hours（OESERR_NOT_TRADING_TIME）
    - 1022, Not yet supported or not yet opened this business（OESERR_NOT_SUPPORT）

OES_0.15.7.6_RC2 / 2018-11-22
==============================================

  * increase 'Structures in accordance with the configuration information to initialize the client environment' interface
    - OesApi_InitAllByCfgStruct
  * increase 'Once only receive a return message' interface
    - OesApi_RecvReportMsg
  * increase 'Set up/Get the client environment number of threads used in the current subscription in return' interface
    - OesApi_SetThreadSubscribeEnvId
    - OesApi_GetThreadSubscribeEnvId

OES_0.15.7.6 / 2018-11-03
==============================================

  * 'Business type(eOesBuySellTypeT)' New in:
    - 'Subscription rights issue (OES_BS_TYPE_ALLOTMENT)' Types of
  * New 'product type (eOesProductTypeT)' definition, As a high-level product category definitions and positions
  * In the following structural body increases 'product type (productType)' Field
    - Securities Information(OesStockBaseInfoT/OesStockItemT)
    - Securities issuance information (OesIssueBaseInfoT/OesIssueItemT)
    - Stock holdings information (OesStkHoldingBaseInfoT/OesStkHoldingItemT)
    - Return commission (OesOrdCnfmT/OesOrdItemT)
    - Return on turnover (OesTrdCnfmT/OesTrdItemT)
  * The issuance of securities product information query interface(OesApi_QueryIssue)Filters increase:
    - ‘product type(productType)’ condition
  * Stock holdings information query interface(OesApi_QueryStkHolding)Filters increase:
    - ‘product type(productType)’ condition
  * 'Securities subtype(eOesSubSecurityTypeT)'New in:
    - Shanghai and London throughCDRLocal products trading business(OES_SUB_SECURITY_TYPE_STOCK_HLTCDR)
  * New error code definitions
    - 1035, Illegal product type（OESERR_ILLEGAL_PRODUCT_TYPE）
    - 1274, Shareholder account no trading rights through depositary receipts of Shanghai and London（OESERR_NO_HLTCDR_PERM）

OES_0.15.7.5 / 2018-08-31
==============================================

  * repairWindowsUnder platform OesApi_GetErrorMsg Error message returned interface is not accurate

OES_0.15.7.4 / 2018-09-28
==============================================

  * fix: When multiple threads simultaneously fix initializationAPIThe log, Cause problems with duplicate log information output
  * Query filters to delegate the interface changes:
    - increase 'Type of securities(securityType)' Query conditions
    - increase 'Business type(bsType)' Query conditions
  * Query Interface transaction information filtering conditions change:
    - increase 'Type of securities(securityType)' Query conditions
    - increase 'Business type(bsType)' Query conditions
  * Stock holdings query interface filters change:
    - increase 'Type of securities(securityType)' Query conditions
  * Return on turnover information(OesTrdCnfmT/OesQryTrdRspT)Increased field:
    - Securities subtype (subSecurityType)
    - The original number of commission (origOrdQty)
    - Original order price (origOrdPrice)
  * increase 'Overview obtain client information (OesApi_GetClientOverview)' interface
  * increase 'Queries Cabinet fund information (OesApi_QueryCounterCash)' interface
  * Adjustment 'Access to payment delegation request (OesApi_SendFundTransferReq)' interface, Added support only between the main cabinet and the bank access to payment
  * 'Client Funds Information(OesCashAssetItemT)' Structures increased field:
    - Prohibit access to payment (isFundTrsfDisabled)
  * 'Securities account information(OesInvAcctItemT)' Structures increased field:
    - Prohibit trading (isTradeDisabled)
  * 'Transaction query response packet(OesQryTrdRspT)' with 'Return on turnover reply message(OesTrdCnfmT)' Struct field increases:
    - Securities subtype (subSecurityType)
  * 'Registration response message(OesLogonRspT)' Struct field increases:
    - Client Type (clientType)
    - Client state (clientStatus)

OES_0.15.6.13 / 2018-07-16
==============================================

  * Increased modify client login password Interface (OesApi_SendChangePasswordReq)
  * Set current thread to increase user login name/login password/Interface number of the client environment
    - OesApi_SetThreadUsername
    - OesApi_SetThreadPassword
    - OesApi_SetThreadEnvId
  * Increased quantities commissioned Interface (In the form of a batch at the same time send multiple pen delegate declaration)
    - OesApi_SendBatchOrdersReq
    - OesApi_SendBatchOrdersReq2
  * Increase returns the current thread lastAPIInterface error numbers call failed
    - OesApi_GetLastError
    - OesApi_SetLastError
  * New 'Market status query(OesApi_QueryMarketState)' interface，This interface to obtain information about the state of the market type is defined as 'OesMarketStateItemT'
  * Set to increase/Get the serial number of the interface device client custom
    - OesApi_SetCustomizedDriverId
    - OesApi_GetCustomizedDriverId
  * Spot product information query interface to change the filter conditions:
    - increase 'Type of securities(securityType)' Query conditions
    - increase 'Securities subcategories(subSecurityType)' Query conditions
  * Return header(OesRptMsgHeadT) Increased field Execution Type(execType), Return to perform the type of distinction(referenceeOesExecTypeTdefinition）
  * Increase the default message type returns OES_SUB_RPT_TYPE_DEFAULT
  * Return new message types 'Market status information (OESMSG_RPT_MARKET_STATE)'
  * Login request message(OesLogonReqT) Increased field Client device serial number(clientDriverId)
  * New Trading Platform Type Definition(eOesPlatformIdT)
  * New Market status information structure definition(OesMarketStateInfoT)
  * New Depositary Receipts corresponding securities subtype (OES_SUB_SECURITY_TYPE_STOCK_CDR)
  * Shareholders' rights to enumerate account transactions(eOesTradingPermissionT)New in
    - Depositary Receipts trading privileges (OES_PERMIS_CDR)
    - Innovative companies stock trading privileges (OES_PERMIS_INNOVATION)
  * increase OesApi_HasMoreCachedData interface, A return has been received but not yet cached data length processed callback
  * See additional error number oes_errors.h

OES_0.15.5.17 / 2018-08-31
==============================================

  * repairWindowsUnder platform OesApi_GetErrorMsg Error message returned interface is not accurate

OES_0.15.5.16 / 2018-09-28
==============================================

  * fix: When multiple threads simultaneously fix initializationAPIThe log, Cause problems with duplicate log information output
  * increase 'Overview obtain client information (OesApi_GetClientOverview)' interface
  * increase 'Queries Cabinet fund information (OesApi_QueryCounterCash)' interface
  * Adjustment 'Access to payment delegation request (OesApi_SendFundTransferReq)' interface, Added support only between the main cabinet and the bank access to payment
  * 'Client Funds Information(OesCashAssetItemT)' Structures increased field:
    - Prohibit access to payment (isFundTrsfDisabled)
  * 'Securities account information(OesInvAcctItemT)' Structures increased field:
    - Prohibit trading (isTradeDisabled)
  * 'Transaction query response packet(OesQryTrdRspT)' with 'Return on turnover information(OesTrdCnfmT)' Struct field increases:
    - Securities subtype (subSecurityType)
    - The original number of commission (origOrdQty)
    - Original order price (origOrdPrice)
  * 'Registration response message(OesLogonRspT)' Struct field increases:
    - Client Type (clientType)
    - Client state (clientStatus)
  * Set current thread to increase user login name/login password/Interface number of the client environment
    - OesApi_SetThreadUsername
    - OesApi_SetThreadPassword
    - OesApi_SetThreadEnvId
  * Increase return lastAPIInterface error numbers call failed
    - OesApi_GetLastError
  * 'Spot product information query filter condition(OesQryStockFilterT)' In new fields:
    - Type of securities(securityType)
    - Securities subcategories(subSecurityType)
  * increase OesApi_HasMoreCachedData interface, A return has been received but not yet cached data length processed callback
  * Securities subcategory enumeration(eOesSubSecurityTypeT) New in Depositary Receipts(OES_SUB_SECURITY_TYPE_STOCK_CDR) Sub-category definitions
  * Account Permissions enumeration(eOesTradingPermissionT) in:
    - New Depositary Receipts trading privileges(OES_PERMIS_CDR) definition
    - New Innovative companies stock trading privileges(OES_PERMIS_INNOVATION) definition

OES_0.15.5.4 / 2018-02-22
==============================================

  * APIPriority will automatically get to useip/macinformation，Only automatically acquiredip/macWhen information is illegal，We will use the client's ownip/mac
  * The server will reject from the local loopback address as well as illegalip/macLogin address
  * CorrectionETFProduct information fields spelling errors
    - Correction 'ETFSecurities basic information (OesEtfBaseInfoT)' in 'The previous day (preTradingDay)' Fields spelling errors
    - Correction 'ETFShen redemption Product Information (OesEtfItemT)' in 'The previous day (preTradingDay)' Fields spelling errors
  * Merge OES_0.15.5.2
    - fix: ResolvedWindowsCompatibility issues under
    - fix: Notes error correction information ('Commission results (OesCommissionRateItemT)' in feeRate Incorrect field precision Description)
    - increase OesApi_GetLastRecvTime、OesApi_GetLastSendTime interface, Get the latest channel for sending/Time to accept the message
    - When the login fails, able to pass errno/SPK_GET_ERRNO() Get to the specific cause of failure

OES_0.15.5.2 / 2018-01-29 (solveWindowsCompatibility issuesAPIupdated version)
==============================================

  * fix: ResolvedWindowsCompatibility issues under。include:
    - fix: inWindowsunder, APIofSocketNon-blocking mode in question, Only works in blocking mode
    - fix: inWindowsunder, When there is no market data, Quotes Subscribe transmission process will live long ram, Until heartbeat messages are triggered not return
    - fix: inWindowsunder, When run in debug mode, If the network connection, then an exception, On exit(shut downsocketConnection)An exception will be reported
    - fix: inWindowsunder, Can not be acquiredIPwithMACaddress, We need to explicitly provided local to the clientIPwithMAC
  * fix: Notes error correction information ('Commission results (OesCommissionRateItemT)' in feeRate Incorrect field precision Description)
  * increase OesApi_GetLastRecvTime、OesApi_GetLastSendTime interface, Get the latest channel for sending/Time to accept the message
  * When the login fails, able to pass errno/SPK_GET_ERRNO() Get to the specific cause of failure

OES_0.15.5.1 / 2017-11-22
==============================================

  * Increase the value of the type of protocol version number OES_APPL_VER_VALUE, To facilitate alignment version
  * increase OesApi_IsValidOrdChannel、OesApi_IsValidRptChannel And other interfaces, For determining whether a channel has been connected and effective

OES_0.15.5 / 2017-11-03
==============================================

  * The current protocol version used(OES_APPL_VER_ID) upgrade to 0.15.5
  * The minimum compatible version of the protocol(OES_MIN_APPL_VER_ID) upgrade to 0.15.5
  * Adjust the state commission eOesOrdStatusT:
        - delete 'OES_ORD_STATUS_DECLARING (Positive News)' status
        - Heavy naming OES_ORD_STATUS_NORMAL => OES_ORD_STATUS_NEW (new order)
  * Delete structure 'Cancellation refused (OesOrdCancelRejectT)', And content into 'Commission rejected (OesOrdRejectT)' Struct
  * 'Commission rejected (OesOrdRejectT)' Struct field increases:
        - Client number (clientId)
        - Client Environment No. (clEnvId)
        - Original order, commissioned by serial number (origClSeqNo)
        - Original order number of the client environment (origClEnvId)
  * 'Access to payment refused (OesFundTrsfRejectT)' Struct field increases:
        - Client number (clientId)
        - Client Environment No. (clEnvId)
  * 'Stock holdings basic information (OesStkHoldingBaseInfoT)' Struct field increases:
        - Security Type (securityType)
        - Securities subtype (subSecurityType)
  * 'Delegation request (OesOrdReqT)' with 'Cancellation request(OesOrdCancelReqT)' Structure adds a time stamp for statistical delay
  * Field __ordReqOrigSendTime, The field consists ofAPIWhen sending autocomplete, And in return the commission to carry back to the client
  * Delegation request/Increased cancellation request timestamp field for statistical delay __ordReqOrigSendTime,
  * The field consists ofAPIWhen sending autocomplete, And in return the commission to carry back to the client
  * The adjustment of product risk level eOesSecurityRiskLevelT in OES_RISK_LEVEL_VERY_LOW Field Meaning:
        - redefine "Very low risk" => "The lowest risk"
  * Adjustment of customer status/Securities Account/Capital account status eOesAcctStatusT:
        - delete OES_ACCT_STATUS_CLOSE    (Cancellation) Wait
        - increase OES_ACCT_STATUS_DISABLED (unusual)
  * delete eOesSourceTypeT definition
  * Delete return message types 'Cancellation refused (OESMSG_RPT_CANCEL_REJECT)', And integrated into 'Commission rejected (OESMSG_RPT_ORDER_REJECT)' Message
  * Rename the return message type OESMSG_RPT_ORDER_REJECT => OESMSG_RPT_BUSINESS_REJECT (OESBusiness refusal, Entrust/Withdrawals and the like check failed wind control)
  * Increase the return on the message type subscribe OES_SUB_RPT_TYPE_BUSINESS_REJECT
  * The maximum number of entries to adjust the query response message carries query data
  * Adjustment 'Query request header(OesQryReqHeadT)' Some of the fields：
        - 'Query window size'Rename the field pageSize => maxPageSize
        - 'Queries starting position'Rename the field position => lastPosition
  * Adjustment 'Query response message header(OesQryRspHeadT)' Some of the fields：
        - 'The number of entries to query information'Rename the field itemCnt => itemCount
        - 'Location query to the last message'Rename the field position => lastPosition
  * Adjustment 'Query response message header(OesQryRspHeadT)' Some of the fields：
        - 'The number of entries to query information'Rename the field itemCnt => itemCount
        - 'Location query to the last message'Rename the field position => lastPosition
  * 'Stock holdings information (OesStkHoldingItemT)' Struct field increases:
        - Security Type (securityType)
        - Securities subtype (subSecurityType)
  * Adjustment 'Financial information(OesCashAssetItemT)' Some of the fields in:
        - 'current balance'Rename the field currentBal => currentTotalBal

OES_0.15.4.3 / 2017-10-27
==============================================

  * 'Principal structure rejection(OesOrdRejectT)' in
        - New field Client number (clientId)
        - New field Client Environment No. (clEnvId)
  * 'Refused withdrawals of structure(OesOrdCancelRejectT)' in
        - New field Client number (clientId)
        - New field Client Environment No. (clEnvId)
  * 'Denied access to payment of structure(OesFundTrsfRejectT)' in
        - New field Client number (clientId)
        - New field Client Environment No. (clEnvId)

OES_0.15.4.2 / 2017-10-16
==============================================

  * Refuse to delegate、Cancellation refused to return the message structure to increase the wrong reasons(ordRejReason)Field
  * New transactional request message 'Test request (OesTestRequestReqT)'
  * Return new message types 'Response test request (OesTestRequestRspT)'

OES_0.15.4.1 / 2017-09-19
==============================================

  * 'Access to payment information base (OesFundTrsfBaseInfoT)'in
        - New field If only allocation (isAllotOnly)
  * 'Access to payment of commission rewards structure(OesFundTrsfReportT)' in
        - New field If only allocation (isAllotOnly)
        - New field Serial transfer of funds (allotSerialNo)
  * 'Stock holdings basic information (OesStkHoldingBaseInfoT)'in
        - Delete field Cost of carry (costAmount)
        - New field Richu total cost of carry (originalCostAmt)
        - New field Japan total purchase amount (totalBuyAmt)
        - New field Japan sold a total amount (totalSellAmt)
        - New field Japan total purchase cost (totalBuyFee)
        - New field Japan sold a total cost (totalSellFee)
  * 'Stock holdings query results (OesStkHoldingItemT)' in
        - Delete field Cost of carry (costAmount)
        - New field Richu total cost of carry (originalCostAmt)
        - New field Japan total purchase amount (totalBuyAmt)
        - New field Japan sold a total amount (totalSellAmt)
        - New field Japan total purchase cost (totalBuyFee)
        - New field Japan sold a total cost (totalSellFee)
  * 'Access to payment and return query results (OesFundTrsfReportT/OesFundTransferSerialItemT)' in
        - New field Cabinet error code (counterErrCode)
            Record Cabinet error code when an error occurs Cabinet，wrong reason(rejReason)Field value'OESERR_COUNTER_ERR'
  * 'Commission and return query results (OesOrdCnfmT/OesOrdItemT)' in
        - New field Exchange error code (exchErrCode)
            Exchange Exchange record error code when an error occurs，wrong reason(ordRejReason)Field value'OESERR_EXCHANGE_ERR'
  * Return commission、Return on turnover increase in RBI timing information
  * Commissioned inquiry、Turnover increased query response structure RBI timing information
  * Adjustment costs（commission/Fixed costs）The accuracy rate support，From the ten-millionth of a millionth revised to
        - OES_FEE_RATE_UNIT From1000000change into10000000
  * Adjusted return message types and values ​​define the order
        - OESMSG_RPT_ORDER_INSERT, OESMSG_RPT_ORDER_REJECT, OESMSG_RPT_CANCEL_REJECT

OES_0.15.4 / 2017-09-04
==============================================

  * New transactional messages 'Cancellation request message (OESMSG_ORD_CANCEL_REQUEST)'
  * New structure 'Cancellation request (OesOrdCancelReqT)'
  * Return new message types 'Cancellation refused (OESMSG_RPT_CANCEL_REJECT)'，
   The corresponding return messages OesRptMsgBodyT::cancelRejectRsp
  * It is no longer included in the rejection message Principal Principal withdrawals, AllOESRejected a request cancellation and cancellation commission will reject the message carried by the new withdrawals return
  * Return new message types 'Information capital changes (OESMSG_RPT_CASH_ASSET_VARIATION)'，
   The corresponding return messages OesRptMsgBodyT::cashAssetRpt
  * Return new message types 'Position change information (stock) (OESMSG_RPT_STOCK_HOLDING_VARIATION)'，
   The corresponding return messages OesRptMsgBodyT::stkHoldingRpt
  * Return new message types 'Position change information (Options) (OESMSG_RPT_OPTION_HOLDING_VARIATION)'，
   The corresponding return messages OesRptMsgBodyT::optHoldingRpt
  * 'The delegate confirms information (OesOrdCnfmT)' Increased field:
        - Client number (clientId)
        - Client Environment No. (clEnvId)
        - Original order, commissioned by serial number (origClSeqNo)
        - Original order number of the client environment (origClEnvId)
        - Exchange Order Number (exchOrdId)
        - Commissioned by the return of the structure size increases24byte, Field offset position also changes
  * 'Return on turnover information (OesTrdCnfmT)' Increased field:
        - Client number (clientId)
        - Client Environment No. (clEnvId)
        - Return on turnover increased size of the structure8byte, Field offset position also changes
  * 'Stock holdings basic information (OesStkHoldingBaseInfoT)' Increased field:
        - Cost of carry (costAmount)
  * Finishing the following structure is defined, Adjust the field order, And removed the individual fields
        - Spot Products basic information (OesStockBaseInfoT)
        - Options Product basic information (OesOptionBaseInfoT)
        - Securities account basic information (OesInvAcctBaseInfoT)
  * Heavy naming 'Access to payment refused (OesFundTrsfRejectReportT)' => OesFundTrsfRejectT
  * Adjust enumerated type 'Access to payment commissioned by state (eOesFundTrsfStatusT)' The value
  * Query request type message by the head 'OesQryHeadT' Changed 'OesQryReqHeadT'
  * The type of query response message header by 'OesQryHeadT' Changed 'OesQryRspHeadT'
  * delete 'OesQryHeadT' Type Definition
  * 'Request information query results (OesOrdItemT)' Increased field:
        - Client number (clientId)
        - Client Environment No. (clEnvId)
        - Original order, commissioned by serial number (origClSeqNo)
        - Original order number of the client environment (origClEnvId)
        - Exchange Order Number (exchOrdId)
  * 'Auction results information (OesTrdItemT)' Increased field:
        - Client number (clientId)
        - Client Environment No. (clEnvId)
  * 'Stock holdings query results (OesStkHoldingItemT)' Increased field:
        - Cost of carry (costAmount)
        - Cost of carry price (costPrice)
  * Finishing the following structure is defined, Adjust the field order, And removed the individual fields
        - Spot product information query results (OesStockItemT)
        - Options Product Search results (OesOptionItemT)
        - Securities account information query results (OesInvAcctItemT)
  * APINo increase in the client environment (clEnvId), The following functions relate to the interface、data structure、Communication message of change:
        - The following parameters are changed interface functions (Increase parameter clEnvId):
            - Connect and log on to the specifiedOESNode and Service (OesApi_Logon)
            - Connect and log on toOESCluster Service (OesApi_LogonReplicaSet)
            - Connect and log on toOESCluster Service (OesApi_LogonPeerNodes)
            - Send Return synchronization message (OesApi_SendReportSynchronization)
        - The following communication message changed (Increase the field clEnvId):
            - Login request/Reply message (OesLogonReqT / OesLogonRspT)
        - The following communication message changed (Increase the field subscribeEnvId):
            - Return synchronous request/Reply message (OesReportSynchronizationReqT / OesReportSynchronizationRspT)
        - The following data structure changed (Increase the field clEnvId):
            - Client session information/Connecting channel information (OesApiSessionInfoT)
            - Remote host configuration information (OesApiRemoteCfgT)
  * APIIn New Interface 'Reset thread-level logger name (OesApi_ResetThreadLoggerName)'，
   Support for the current thread to set up a separate log file
  * Rename interface functions OesApi_SendFundTrsfReq => OesApi_SendFundTransferReq
  * New Interface 'ObtainAPIThe release number (OesApi_GetApiVersion)'
  * New Interface 'Get the current trading day (OesApi_GetTradingDay)'
  * New Interface 'Send cancellation request (OesApi_SendOrderCancelReq)'
        - Compared to the original way of cancellation, Cancellation request interface supported by clEnvId + clSeqNo Carried out withdrawals
  * Adjusted returns an interface type defined callback method F_OESAPI_ONMSG_T => F_OESAPI_ON_RPT_MSG_T
  * Adjust the query interface callback method type definition F_OESAPI_ONMSG_T => F_OESAPI_ON_QRY_MSG_T
  * Query interface callback method to increase OesQryCursorT Type Parameters，Which carries“Whether it is the last one”information
  * All query filter conditions(OesQryXXXFilterT) Increase userInfoField，
   This field in the corresponding query response message(OesQryXXXRspT) As they head back in response

OES_0.15.3 / 2017-08-14
==============================================

  * The current protocol version used(OES_APPL_VER_ID) upgrade to 0.15.3
  * The minimum compatible version of the protocol(OES_MIN_APPL_VER_ID) upgrade to 0.15.3
  * New Investors Category(eOesInvestorClassT) Enumeration defines
  * With the number of new shares、Winning record information(OesLotWinningBaseInfoT) in
        - delete Customer code(custId) Field
        - New Security Name(securityName) Field
  * Securities issuance basic information(OesIssueBaseInfoT) in
        - New Issue start date(startDate) Field
        - New Release the end of the day(endDate) Field
  * Customer base information(OesCustBaseInfoT) in
        - New Agency logo(institutionFlag) Field
        - New Investors Category(investorClass) Field
  * Securities account basic information(OesInvAcctBaseInfoT) Deleted The adequacy of management classification(qualificationClass) Field
  * Merge OES_0.12.9.12
    - fix: AgainstWindowsplatform, becauseGNULibofrecvThe method has problems when multiple threads, There will be different Socket Interfere with each other and the phenomenon of serial execution, So temporarily switch back to using only operate in blocking moderead/writemethod
    - Known Issues:
      - inWindowsunder, APIofSocketNon-blocking mode in question, Only work temporarily in blocking mode
  * Merge OES_0.12.9.11
    - fix: Cross-platform reconstruction process, perfectAPICorrectWindowsSupported platforms
    - fix: RepairWindowsunder，SocketFailure to properly set to non-blocking modeBUG
      - fix: RepairWindowsunder，becauseerrnoIncompatible lead to failure of network processingBUG
      - fix: RepairWindowsunder，Because it is not compatible with the file path handling，Cause the log failed to initializeBUG
      - fix: RepairWindowsunder，Individual functions are not compatible causes the compiler to issue warnings and runtime errors
      - fix: Because the Chinese character encoding repair inconsistent results inWindowsCompilation failed under question
      - refactor: inAPIHeader file referenced by default spk_platforms.h head File
      - refactor: ReconstructionAPISample code and sample configuration files

OES_0.15.2.2 / 2017-08-07
==============================================

  * When you logoes-serverEnd increaseIP、MACNon-null check
  * New Pending the implementation of the access to payment(OES_FUND_TRSF_STS_SUSPENDED)
  * Kim refused to return the message out of adjustment'Error code information'Field name rejReasonInfo => errorInfo
  * Adjusted return on access to payment execution message'Error code information'Field name rejReasonInfo => errorInfo

OES_0.15.2.1 / 2017-07-31
==============================================

  * The current protocol version used(OES_APPL_VER_ID) upgrade to 0.15.2
  * The minimum compatible version of the protocol(OES_MIN_APPL_VER_ID) upgrade to 0.15.2
  * New Reward structure is defined refused access to payment services(OesFundTrsfRejectT)
  * Access to payment service reject message type changes OesFundTrsfReqT => OesFundTrsfRejectT
  * Access to payment of commission rewards structure(OesFundTrsfReportT) In new fields Error code information(rejReasonInfo)
  * Heavy naming 'Access to payment commissioned by state' The macro definition
        - Adjustment OES_FUND_TRSF_STS_RECV => OES_FUND_TRSF_STS_UNDECLARED
        - Adjustment OES_FUND_TRSF_STS_DCLR => OES_FUND_TRSF_STS_DECLARED
        - Adjustment OES_FUND_TRSF_STS_DCLR_ROLLBACK => OES_FUND_TRSF_STS_UNDECLARED_ROLLBACK
        - Adjustment OES_FUND_TRSF_STS_DONE_ROLLBACK => OES_FUND_TRSF_STS_DECLARED_ROLLBACK
  * Error code when a transaction fails to insufficient permissions subdivision(For details, see README Error code table section)

OES_0.15.2 / 2017-07-18
==============================================

  * APINew Interface Send request access to payment commission(OesApi_SendFundTrsfReq) interface
  * APINew Interface Query with the number of new shares、In the ballot information(OesApi_QueryLotWinning) interface
  * New 'IPO、In the ballot information inquiry' Relevant messages defined
        - New field Query IPO、Information filtering conditions in the ballot(OesQryLotWinningFilterT)
        - New field IPO、Winning content(OesLotWinningItemT)
        - New field Query IPO、In the ballot information request(OesQryLotWinningReqT)
        - New field Query IPO、Response in the ballot information(OesQryLotWinningRspT)
  * New OESIn the ballot、With a number of record types(eOesLotTypeT)
  * New OESWith a number of reasons for failure(eOesLotRejReasonT)
  * Access to payment commissioned by state(eOesFundTrsfStatusT) The new state as follows
        - Cabinet to report before the instruction has to be rolled back(OES_FUND_TRSF_STS_UNDECLARED_ROLLBACK)
        - After the instruction has to be rolled back to report Cabinet(OES_FUND_TRSF_STS_DECLARED_ROLLBACK)
        - Access to payment instruction is completed，Waiting for the end of the transaction(OES_FUND_TRSF_STS_WAIT_DONE)

OES_0.15.1 / 2017-06-26
==============================================

  * The current protocol version used(OES_APPL_VER_ID) upgrade to 0.15.1
  * The minimum compatible version of the protocol(OES_MIN_APPL_VER_ID) upgrade to 0.15.1
  * 'Spot Products basic information(OesStockBaseInfoT)' in
        - Adjustment field isQualificationRequired => qualificationClass,
            Please refer to the value eOesQualificationClassT
        - New field Product risk level(securityRiskLevel)，Please refer to the value eOesSecurityRiskLevelT
        - New field Reverse repurchase deadline(repoExpirationDays)
        - New field Models accounting for the number of days(cashHoldDays) Field
  * 'Customer funds basic information(OesCashAssetBaseInfoT)'versus'Capital return information query(OesCashAssetItemT)' in
        - Rename the field Opening Balance(originalBal => beginningBal)
        - New field Beginning available balance(beginningAvailableBal)
        - New field Beginning desirable balance(beginningDrawableBal)
        - New field Current Reversal Amount(Net capital red red blue complement, reversalAmt)
  * 'Customer base information(OesCustBaseInfoT)' in
        - New field Level of risk(riskLevel)
        - New field The original level of risk(originRiskLevel)
  * 'Securities account basic information(OesInvAcctBaseInfoT)' in
        - Adjustment field '(Voucher account access restrictions, acctLimit)'
            - Types of uint32 => uint64
            - Heavy naming acctLimit => Limits
        - Adjustment field '(Shareholders' rights/Client privilege, acctRight)'
            - Types of uint32 => uint64
            - Heavy naming acctRight => permissions
        - New field The adequacy of management classification(qualificationClass)
  * 'Stock holdings basic information(OesStkHoldingBaseInfoT)'versus'Positions return information query(OesStkHoldingItemT)' in
        - New field Manual frozen positions(Net positions administrator freeze, manualFrzHld)
  * 'Commissioned query filter conditions(OesQryOrdFilterT)' in
        - New field Delegate start time(startTime) with End Time delegate(endTime)
  * 'Transaction query filter conditions(OesQryTrdFilterT)' in
        - New field The start time of the transaction(startTime) with Transaction end time(endTime)
  * 'Positions return information query(OesStkHoldingItemT)' In new fields Total positions(sumHld)
  * 'Capital return information query(OesCashAssetItemT)' in
        - New field current balance(currentBal)
        - Rename the field The current available balance(tradeAvlAmt => currentAvailableBal)
        - Rename the field Current desirable balance(withdrawAvlAmt => currentDrawableBal)
  * Add trading privileges enumerated values eOesTradingPermissionT, eOesTradingLimitT
  * Trading rights metadata definitions OesTradingPermissionEntryT
  * Rename the enumeration type eOesExchangeTypeT => eOesExchangeIdT

OES_0.12.9.12 / 2017-08-13
==============================================

  * fix: AgainstWindowsplatform, becauseGNULibofrecvThe method has problems when multiple threads, There will be different Socket Interfere with each other and the phenomenon of serial execution, So temporarily switch back to using only operate in blocking moderead/writemethod
  * Known Issues:
    - inWindowsunder, APIofSocketNon-blocking mode in question, Only work temporarily in blocking mode

OES_0.12.9.11 / 2017-08-12
==============================================

  * Cross-platform reconstruction process, perfectAPICorrectWindowsSupported platforms
    - fix: RepairWindowsunder，SocketFailure to properly set to non-blocking modeBUG
    - fix: RepairWindowsunder，becauseerrnoIncompatible lead to failure of network processingBUG
    - fix: RepairWindowsunder，Because it is not compatible with the file path handling，Cause the log failed to initializeBUG
    - fix: RepairWindowsunder，Individual functions are not compatible causes the compiler to issue warnings and runtime errors
    - fix: Because the Chinese character encoding repair inconsistent results inWindowsCompilation failed under question
    - refactor: Cross-platform reconstruction process, Perfect forWindowsSupported platforms, AndAPIHeader file referenced by defaultspk_platforms.h
    - refactor: ReconstructionAPISample code and sample configuration files

OES_0.12.9_RC1  2017-06-05
==============================================

  * The current protocol version used(OES_APPL_VER_ID) upgrade to 0.12.9
  * Adjusting commissions query resultsfeeRateAccuracy field，When the calculation mode is the commission 'Press Copies' Time，
   feeRate Field represents a ratio of units by 'Millionth' *> 'millionth'

OES_0.12.8.2 / 2017-05-16
==============================================

  * New 'Business type' IPO(OES_BS_TYPE_SUBSCRIPTION)
  * Heavy naming as follows'Business type' definition，Primitive type of trading will be discarded
        - Buy OES_BS_TYPE_B => OES_BS_TYPE_BUY
        - Sell OES_BS_TYPE_S => OES_BS_TYPE_SELL
        - Purchase OES_BS_TYPE_KB => OES_BS_TYPE_CREATION
        - redemption OES_BS_TYPE_KS => OES_BS_TYPE_REDEMPTION
        - Financing to buy OES_BS_TYPE_CB => OES_BS_TYPE_CREDIT_BUY
        - Short selling，Pledged reverse repurchase OES_BS_TYPE_CS => OES_BS_TYPE_CREDIT_SELL
        - Option to buy Open OES_BS_TYPE_BO => OES_BS_TYPE_BUY_OPEN
        - Option buying positions OES_BS_TYPE_BC => OES_BS_TYPE_BUY_CLOSE
        - Options sold Open OES_BS_TYPE_SO => OES_BS_TYPE_SELL_OPEN
        - Options open to sell OES_BS_TYPE_SC => OES_BS_TYPE_SELL_CLOSE
        - Open options covered OES_BS_TYPE_CO => OES_BS_TYPE_COVERED_OPEN
        - Covered options open OES_BS_TYPE_CC => OES_BS_TYPE_COVERED_CLOSE
        - Warrant OES_BS_TYPE_TE => OES_BS_TYPE_OPTION_EXERCISE
        - Lock underlying options OES_BS_TYPE_UF => OES_BS_TYPE_UNDERLYING_FREEZE
        - Unlock underlying options OES_BS_TYPE_UU => OES_BS_TYPE_UNDERLYING_UNFREEZE
  * New 'Securities issuance basic information(OesIssueBaseInfoT)'
  * 'Product basic information(OesStockBaseInfoT)' In new fields
        - New The need for proper management(isQualificationRequired)
        - New Whether to support the trading day rotation(isDayTrading)
        - New 100 face value of each bond accrued interest(bondInterest)，Accurate to the dollar after8Place
  * 'Product basic information(OesStockBaseInfoT)' Remove the field
        - delete Sell ​​funds are available(cashRealBack)
        - delete Whether to buy shares may sell(hldnRealBack)
  * 'Shareholder account basic information(OesInvAcctBaseInfoT)' In new fields IPO quota(subscriptionQuota)
  * 'The delegate confirms information(OesOrdCnfmT)' In new fields
        - New Freeze Interest(frzInterest)
        - New Interest has occurred(cumInterest)
  * 'Transaction confirmation information(OesTrdCnfmT)' In new fields Interest has occurred(cumInterest)
  * New 'The issuance of securities information inquiry' Relevant messages defined
        - New Query filtering condition securities issuance(OesQryIssueFilterT)
        - New The issuance of securities information content(OesIssueItemT)
        - New Query securities issuance information request(OesQryIssueReqT)
        - New Query response securities issuance information(OesQryIssueRspT)

OES_0.12.8.1 / 2017-04-24
==============================================

  * The minimum compatible version of the protocol(OES_MIN_APPL_VER_ID) upgrade to 0.12.8
  * Heavy naming 'The delegate confirms information(OesOrdCnfmT)'、'Transaction confirmation information(OesTrdCnfmT)' in
   __tgwSetIdx => __tgwGrpNo

OES_0.12.8 / 2017-04-17
==============================================

  * Upgrade to the current version of the agreement 0.12.8，Compatible version of the agreement to maintain the lowest at 0.12.6
  * Adjustment 'The delegate confirms information(OesOrdCnfmT)' Position of the part of the field
  * New 'The delegate confirms information(OesOrdCnfmT)' Shenzhen increase in multi-transaction gateway properties relatedOESInternal field __tgwSetIdx
  * New 'Transaction confirmation information(OesTrdCnfmT)' Shenzhen increase in multi-transaction gateway properties relatedOESInternal field __tgwSetIdx

OES_0.12.6.3 / 2017-03-24
==============================================

  * inmds_api.h、oes_api.hIncreasesutilReference library header files，apiUsers do not need to explicitly referencesutilLibrary header files

OES_0.12.6.2 / 2017-03-16
==============================================

  * Heavy naming 'Access to payment commission' News OESMSG_NONTRD_CASH_TRSF_REQ => OESMSG_NONTRD_FUND_TRSF_REQ
  * New 'Access to payment commissioned response-Business refusal'、'Access to payment reports commissioned by the Executive' Two types of return messages
  * delete 'Access to payment management logon message' Macro definition
  * Heavy naming 'Access to payment commission'Message structure is defined  OesCashTrsfReqT => OesFundTrsfReqT
  * 'Query access to payment information filtering water conditions' Renaming cashSeqNo —> clSeqNo
  * Adjust the query to 'Access to payment information flowing water' structure (And access to payment entrust the implementation of a consistent return structure)
  * Adjusting commissions query resultsfeeRateAccuracy field，When the calculation mode is the commission 'By Amount' Time，
   feeRate Field represents a ratio of units by 'One hundred thousandth' => 'millionth'
  * Adjustment 'Business type' In the subject option Lock(OES_BS_TYPE_UF)、Unlock underlying options(OES_BS_TYPE_UU)、
   Designated registration(OES_BS_TYPE_SSE_DESIGNATION)、Undo specified(OES_BS_TYPE_SSE_RECALL_DESIGNATION)、
   Hosted registration(OES_BS_TYPE_SZSE_DESIGNATION)、Managed Undo(OES_BS_TYPE_SZSE_CANCEL_DESIGNATION)
   Macro Value
  * New Reverse repurchase(OES_BS_TYPE_CS) Business type
  * Adjustment 'Cost calculation model' The macro definition eOesCalFeeModeT => eOesCalcFeeModeT
        - Adjustment OES_CAL_FEE_MODE_AMOUNT => OES_CALC_FEE_MODE_AMOUNT
        - Adjustment OES_CAL_FEE_MODE_QTY => OES_CALC_FEE_MODE_QTY
        - New OES_CALC_FEE_MODE_ORD (According to items costing)
  * Heavy naming 'Out payment direction' The macro definition eOesCashDirectT => eOesFundTrsfDirectT
        - Adjustment OES_CASH_DIRECT_IN => OES_FUND_TRSF_DIRECT_IN
        - Adjustment OES_CASH_DIRECT_OUT => OES_FUND_TRSF_DIRECT_OUT
  * Heavy naming 'Access to payment commissioned by state' The macro definition
        - Adjustment OES_CASH_TRSF_STS_RECV => OES_FUND_TRSF_STS_UNDECLARED
        - Adjustment OES_CASH_TRSF_STS_DCLR => OES_FUND_TRSF_STS_DECLARED
        - Adjustment OES_CASH_TRSF_STS_DONE => OES_FUND_TRSF_STS_DONE
        - Adjustment OES_CASH_TRSF_STS_INVALID_OES => OES_FUND_TRSF_STS_INVALID_OES
        - Adjustment OES_CASH_TRSF_STS_INVALID_COUNTER => OES_FUND_TRSF_STS_INVALID_COUNTER
  * Adjustment 'Product Level'(eOesSecurityLevelT) The enumeration values
  * delete Useless'Order Time Types'(eOesOrdTimeTypeT) The enumeration defines
  * delete Useless'Rights category'(eOesRightTypeT) The enumeration defines
  * 'Access to payment information commission basis' Increase User private information(userInfo) Field
  * increase 'Access to payment information entrusted return basis'

OES_0.12.3.5 / 2017-02-20
==============================================

  * Migration reported withdrawal than the macro definitions related
  * Delete sell macro definitions clearance threshold
  * New Bond、Fund types of securities，AdjustmentETFSecurities type macro definition of value
  * New Securities subtype definition
  * The delegate confirms、Return on turnover increase in latency statistics field
  * Spot products to increase basic information“Securities subtype”Field，And renaming“Buy Units”、“Sell ​​Unit”Field
  * ETFProduct basic information added“Security Type”、“Securities subtype”Field
  * ETFStocks increased basic information“Securities subtype”Field
  * Basic information product options added“Securities subtype”Field

OES_0.12.3 / 2017-01-10
==============================================

  * streamlineAPIDependent header files，And minimizeAPIRelease the number of headers package
  * Heavy naming protocol_parser/errors/oes_protocol_errors.h ==> errors/oes_errors.h
  * delete eOesHoldTypeT Enumeration type definition
  * OesHoldItemT Structure split into OesStkHoldingItemT、OesOptHoldingItemTTwo structures
  * Position a single query interface OesApi_QuerySingleHolding Split:
        - OesApi_QuerySingleStkHolding Query a single stock positions
        - OesApi_QuerySingleOptHolding Single query options positions
  * OesApi_QuerySingleStkHolding Parameter Type Change:
        - Parameters of four types of change OesHoldItemT => OesStkHoldingItemT(originalOesStockHoldInfoT)
  * OesApi_QuerySingleOptHolding Parameter Type Change:
        - Parameters of four types of change OesHoldItemT => OesOptHoldingItemT(originalOesOptionHoldInfoT)
  * Batch query interface positions OesApi_QueryHolding Split:
        - OesApi_QueryStkHolding Check stock positions
        - OesApi_QueryOptHolding Query options positions
  * OesApi_QueryStkHolding Parameter Type Change:
        - Parameter Two types of change OesQryHoldFilterT => OesQryStkHoldingFilterT
        - Parameters of Three pOnMsgCallback.pMsgBody Return data type change OesHoldItemT => OesStkHoldingItemT
  * OesApi_QueryOptHolding Parameter Type Change:
        - Parameter Two types of change OesQryHoldFilterT => OesQryOptHoldingFilterT
        - Parameters of Three pOnMsgCallback.pMsgBody Return data type change OesHoldItemT => OesOptHoldingItemT

OES_0.12.1 / 2016-12-21
==============================================

  * delete OesApi_IsBusinessError interface，Query interface not return less than -1000 mistake
  * The return value query interface changes:
        - A single query interface returns no data NEG(ENOENT)
        - Batch query returned no matching data interfaces 0
        - Single/batch Query is refusing to return to the server NEG(EINVAL)，Specific error messages by Log Print
  * Fine tuningoes_apiLog Format Printing
  * Delete the definition of the enumeration has not been used eOesEtfSubFlagSzT
  * Modify commission requestordTypeData dictionary eOesOrdTypeShT eOesOrdTypeSzT
  * Delegation request、The delegate confirms、Return on turnover ofuserInfoCommonwealth addedi64、i32Type field
  * Integrated query messageqryCnt、positionAnd other fields，Become a new structure OesQryHeadT

OES_0.12 / 2016-12-06
==============================================

  * Increase customer information query
  * Notes Supplementary information collation error number and error number defined in section
  * increase OesApi_GetErrorMsg with OesApi_GetErrorMsg2 method
  * Increased Protocol version number information in the login message, And compatibility checking protocol version number at login
  * Increase customer information query
  * ETFConstituent stocks increased query response belongsETFShen redemption codes
  * Commission of inquiry in response to increase customer code
  * Increase the default template configuration commission；Wild commission is set to increase template configuration items
  * The owners'(OwnerType)Configuration，And replace the original shareholder accounts optAcctLevel Field
  * Renaming Fields etfId ==> fundId
  * Return on turnover increase in the accumulated information in turnover、Accumulated transaction cost fields
  * The delegate confirms that the information added to the cumulative turnover、Cumulative transaction costs、Freeze amount、Freeze cost fields
