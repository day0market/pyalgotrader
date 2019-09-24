# Swordfish-OES API    {#mainpage}

Swordfish fast order systemAPIInstructions for use


---
### Quick Start

#### 1.1 Sample Code

- See also oes_api/samples/c_sample Sample files directory
	- Sample configuration files <oes_client_sample.conf>
	- Sample Code <oes_client_sample.c>
	- Sample code for compilation <Makefile.sample>

oes_client_sample.c Summarized as follows：
~~~{.c}

/**
 * Send a delegation request
 *
 * prompt:
 * - able to pass OesApi_GetClEnvId() The method of obtaining the environment to the client used by the current channel number(clEnvId), Such as:
 *   <code>int8 clEnvId = OesApi_GetClEnvId(pOrdChannel);</code>
 *
 * @param   pOrdChannel     Session information entrusted channel
 * @param   mktId           Market Code (Mandatory) @see eOesMarketIdT
 * @param   pSecurityId     Stock code (Mandatory)
 * @param   pInvAcctId      Shareholders accounting code (Not fill)
 * @param   ordType         Delegate type (Mandatory) @see eOesOrdTypeT, eOesOrdTypeShT, eOesOrdTypeSzT
 * @param   bsType          Business type (Mandatory) @see eOesBuySellTypeT
 * @param   ordQty          The number of commissioned (Mandatory, Units of shares/Zhang)
 * @param   ordPrice        Order price (Mandatory, After four nearest element units，which is1yuan = 10000)
 * @return  greater or equal to0，success；Less than0，failure（Error number）
 */
static inline int32
_OesApiSample_SendOrderReq(OesApiSessionInfoT *pOrdChannel,
        uint8 mktId, const char *pSecurityId, const char *pInvAcctId,
        uint8 ordType, uint8 bsType, int32 ordQty, int32 ordPrice) {
    OesOrdReqT          ordReq = {NULLOBJ_OES_ORD_REQ};

    SLOG_ASSERT2(pOrdChannel
            && mktId > 0 && mktId < __OES_MKT_ID_MAX
            && pSecurityId && ordType < __OES_ORD_TYPE_FOK_MAX
            && bsType > 0 && bsType < __OES_BS_TYPE_MAX_TRADING
            && ordQty > 0 && ordPrice >= 0,
            "pOrdChannel[%p], mktId[%hhu], pSecurityId[%s], " \
            "ordType[%hhu], bsType[%hhu], ordQty[%d], ordPrice[%d]",
            pOrdChannel, mktId, pSecurityId ? pSecurityId : "NULL",
            ordType, bsType, ordQty, ordPrice);

    ordReq.clSeqNo = (int32) ++pOrdChannel->lastOutMsgSeq;
    ordReq.mktId = mktId;
    ordReq.ordType = ordType;
    ordReq.bsType = bsType;

    strncpy(ordReq.securityId, pSecurityId, sizeof(ordReq.securityId) - 1);
    if (pInvAcctId) {
        /* Shareholder accounts not fill */
        strncpy(ordReq.invAcctId, pInvAcctId, sizeof(ordReq.invAcctId) - 1);
    }

    ordReq.ordQty = ordQty;
    ordReq.ordPrice = ordPrice;

    return OesApi_SendOrderReq(pOrdChannel, &ordReq);
}


/**
 * Send cancellation request
 *
 * @param   pOrdChannel     Session information entrusted channel
 * @param   mktId           It was commissioned by the withdrawal of market codes (Mandatory) @see eOesMarketIdT
 * @param   pSecurityId     It was commissioned by the withdrawal of ticker (Optional, If not empty then check whether the order to be withdrawn matches)
 * @param   pInvAcctId      Was commissioned by the withdrawal of shareholder accounts codes (Optional, If not empty then check whether the order to be withdrawn matches)
 * @param   origClSeqNo     It was commissioned by the withdrawal of the serial number (If you use origClOrdId, It is not necessary to fill the field)
 * @param   origClEnvId     It was commissioned by the withdrawal of the client environment No. (Less than or equal0, Use the current session clEnvId)
 * @param   origClOrdId     It was commissioned by the withdrawal of the customer order number (If you use origClSeqNo, It is not necessary to fill the field)
 * @return  greater or equal to0，success；Less than0，failure（Error number）
 */
static inline int32
_OesApiSample_SendOrderCancelReq(OesApiSessionInfoT *pOrdChannel,
        uint8 mktId, const char *pSecurityId, const char *pInvAcctId,
        int32 origClSeqNo, int8 origClEnvId, int64 origClOrdId) {
    OesOrdCancelReqT    cancelReq = {NULLOBJ_OES_ORD_CANCEL_REQ};

    SLOG_ASSERT2(pOrdChannel && mktId > 0 && mktId < __OES_MKT_ID_MAX,
            "pOrdChannel[%p], mktId[%hhu]", pOrdChannel, mktId);

    cancelReq.clSeqNo = (int32) ++pOrdChannel->lastOutMsgSeq;
    cancelReq.mktId = mktId;

    if (pSecurityId) {
        /* When the cancellation was dismissed commissioned ticker time to fill */
        strncpy(cancelReq.securityId, pSecurityId, sizeof(cancelReq.securityId) - 1);
    }

    if (pInvAcctId) {
        /* When the cancellation was dismissed entrusted shareholder accounts do not fill */
        strncpy(cancelReq.invAcctId, pInvAcctId, sizeof(cancelReq.invAcctId) - 1);
    }

    cancelReq.origClSeqNo = origClSeqNo;
    cancelReq.origClEnvId = origClEnvId;
    cancelReq.origClOrdId = origClOrdId;

    return OesApi_SendOrderCancelReq(pOrdChannel, &cancelReq);
}


/**
 * Report on the implementation of the callback function processes the message
 *
 * @param   pRptChannel     Session information return channel
 * @param   pMsgHead        Header
 * @param   pMsgBody        Message body data
 * @param   pCallbackParams External incoming parameter
 * @return  greater or equal to0，success；Less than0，failure（Error number）
 */
static inline int32
_OesApiSample_HandleReportMsg(OesApiSessionInfoT *pRptChannel,
        SMsgHeadT *pMsgHead, void *pMsgBody, void *pCallbackParams) {
    OesRspMsgBodyT      *pRspMsg = (OesRspMsgBodyT *) pMsgBody;
    OesRptMsgT          *pRptMsg = &pRspMsg->rptMsg;

    assert(pRptChannel && pMsgHead && pRspMsg);

    switch (pMsgHead->msgId) {
    case OESMSG_RPT_ORDER_INSERT:               /* OESCommission has been generated (It has passed wind control inspection) */
        printf(">>> Recv OrdInsertRsp: {clSeqNo: %d, clOrdId: %lld}\n",
                pRptMsg->rptBody.ordInsertRsp.clSeqNo,
                pRptMsg->rptBody.ordInsertRsp.clOrdId);
        break;

    case OESMSG_RPT_BUSINESS_REJECT:            /* OESBusiness refusal (Like wind control check failed) */
        printf(">>> Recv OrdRejectRsp: {clSeqNo: %d, ordRejReason: %d}\n",
                pRptMsg->rptBody.ordRejectRsp.clSeqNo,
                pRptMsg->rptHead.ordRejReason);
        break;

    case OESMSG_RPT_ORDER_REPORT:               /* Exchange commission in return (Including the exchange commission rejected、The delegate confirms completion notification and cancellation) */
        printf(">>> Recv OrdCnfm: {clSeqNo: %d, clOrdId: %lld}\n",
                pRptMsg->rptBody.ordCnfm.clSeqNo,
                pRptMsg->rptBody.ordCnfm.clOrdId);
        break;

    case OESMSG_RPT_REPORT_SYNCHRONIZATION:     /* Return synchronous response */
    case ...:
         ...
    }

    return 0;
}


/**
 * Acquisition and processing returns (It can run as a main function thread)
 *
 * @param   pRptChannel     Session information return channel
 * @return  TRUE Treatment success; FALSE Processing failed
 */
void*
OesApiSample_ReportThreadMain(OesApiClientEnvT *pClientEnv) {
    static const int32  THE_TIMEOUT_MS = 1000;

    OesApiSessionInfoT  *pRptChannel = &pClientEnv->rptChannel;
    int32               ret = 0;

    while (1) {
        /* Wait for the return message arrives, And processes the message through the callback function */
        ret = OesApi_WaitReportMsg(pRptChannel, THE_TIMEOUT_MS,
                _OesApiSample_HandleReportMsg, NULL);
        if (unlikely(ret < 0)) {
            if (likely(SPK_IS_NEG_ETIMEDOUT(ret))) {
                /* Time-out check (Check that the session has timed out) */
                if (likely(_OesApiSample_OnTimeout(pClientEnv) == 0)) {
                    continue;
                }

                /* Session has timed out */
                goto ON_ERROR;
            }

            if (SPK_IS_NEG_EPIPE(ret)) {
                /* The line is disconnected */
            }
            goto ON_ERROR;
        }
    }

    return (void *) TRUE;

ON_ERROR:
    return (void *) FALSE;
}

~~~


#### 1.2 Compile and run the sample code

1. Into the sample code directory
	- ``cd oes_libs-xxx/include/oes_api/samples/c_sample``

2. Compiled code
	- ``make -f Makefile.sample``

3. Modify the configuration file，Confirm service address、And user name correctly
	- ``vi oes_client_sample.conf``

4. Running the sample program
	- ``./oes_client_sample``


---
### Upgrade guidelines and the revision of history

- See the upgrade guide <@ref update_guide>
- See a modified version of history <@ref changelog>


---
### common problem

- Prices and amounts
  - OESAll prices are`int32`The type of integer values，After four nearest element units，which is: 1yuan=10000
  - OESAll amounts are in`int64`The type of integer values，After four nearest element units，which is: 1yuan=10000

- Share units
  - OESAll the number of delegates、The number of units and other share transactions are`int32`or`int64`The type of integer values，With no decimal places
  - OESShare in bond trading unit is <b>'Zhang'</b>，Stock Trading share units <b>'share'</b>

- Prices are quoted range is not legitimate？
	- OESAll prices are`int32`The type of integer values，After four nearest element units，which is: 1yuan=10000

- How to distinguish the last record returned by the query？
  <br>OesApi_QueryOrderSynchronous function，It returns all queries to request information on behalf of the completion callback，inAction_OnQryOrdItem
  Callback function to identify the last ever thought of，return value>=0On behalf of the query to the number of records。

- How to ViewOrdRejectRspThe reasons for rejection？
  <br>useOesApi_GetErrorMsg(rptHead.ordRejReason)To acquire related error messages，Message headerstatus、detailStatus
  The main communication layer returns an error。

- clEnvId effect？
	- clEnvId No client environment，It is used to distinguish client instance reported delegate。For each client to assign different instance clEnvId，Such examples of these clients can maintain their own clSeqNo Without interfering with each other
	- The client can use different instances of the same clEnvId Login server。These use the same this time clEnvId The client instances share the same clSeqNo sequence
	- clEnvId The client is the range __[0~99]__ ([100~127] A reserved section，The client should be avoided)
	- able to pass OesApi_GetClEnvId() The client interface to obtain this instance is bound clEnvId
	- Service maintained by the information commission，Will record the transmission source client end of this delegate instance is bound clEnvId。Commissioned report message(OesOrdCnfmT.clEnvId) with Commissioned inquiry response(OesOrdItemT.clEnvId) This information will carry
	- Please refer to the configuration file settings oes_client_sample.conf in [oes_client].clEnvId Setting parameters


---
### OESError code table

| error code | Error Description                            |
| :---- | :--------------------------------- |
| 1001  | Error message format                         |
| 1002  | The current host is not the master node                    |
| 1003  | Library operation failed main memory                       |
| 1004  | Depending on the state and other basic data does not match，Unable to update data     |
| 1005  | Protocol version incompatible                       |
| 1006  | Data does not exist                           |
| 1007  | Non-service opening hours                       |
| 1008  | Illegal cursor positioning                       |
| 1009  | Illegal client login user name               |
| 1010  | Illegal Securities Code                       |
| 1011  | Illegal customer code                       |
| 1012  | Illegal client type                      |
| 1013  | The client has been disabled                       |
| 1014  | The client password is incorrect                      |
| 1015  | Repeat Client Login                       |
| 1016  | The number of clients connect too many                    |
| 1017  | Client accounts of others unauthorized operation             |
| 1018  | Modified beyond the scope of data                      |
| 1019  | Illegal application name                    |
| 1020  | Request condition conflict                       |
| 1021  | Illegal clientsIP/MACAddress Format            |
| 1022  | Not yet supported or not yet opened this business               |
| 1023  | The number of illegal client environment                    |
| 1024  | Exchange rejected                           |
| 1025  | Cabinet rejected                            |
| 1026  | Traffic over the limits                      |
| 1027  | Prohibit the use ofAPIlog in                      |
| 1028  | Illegal private equity fund product code                 |
| 1029  | Password unchanged                           |
| 1030  | Illegal source categories                       |
| 1031  | Illegal type of encryption                       |
| 1032  | Illegal client device serial number                 |
| 1033  | No available node                           |
| 1034  | Password strength not sufficient                         |
| 1035  | Illegal product type                       |
| 1036  | Black and white list check failed |
| 1101  | Login failed counter                         |
| 1102  | Failure to report the counter                       |
| 1103  | Obtained from the counter state failure                    |
| 1201  | Illegal securities account codes                    |
| 1202  | Illegal capital account codes                    |
| 1203  | Illegal access to payment direction                      |
| 1204  | Illegal Market Code                       |
| 1205  | Illegal securities category                       |
| 1206  | Illegal sale of type                       |
| 1207  | Illegal currency                           |
| 1208  | Illegal delegate type                       |
| 1209  | Invalid account status                       |
| 1210  | Request information not found                       |
| 1211  | Position information not found                       |
| 1212  | Gold out of the water is not found                      |
| 1213  | Repeat serial number                           |
| 1214  | The current period can not offer                      |
| 1215  | No operating authority                         |
| 1216  | Available/Less than desirable balance of funds                 |
| 1217  | Lack of available positions                         |
| 1218  | The number of commission is not legal within the range                 |
| 1219  | Non-integer multiples of the number of units                    |
| 1220  | UnlawfulPBUCode                        |
| 1221  | Price is not legal within the range                    |
| 1222  | Non-integer multiple of the unit price                    |
| 1223  | No limit price of market order fail                  |
| 1224  | The current period is not supported by market order                 |
| 1225  | Invalid Order Status                       |
| 1226  | Cancellation information does not match with the original commission                 |
| 1227  | Repeat withdrawals                            |
| 1228  | Position limit check failed                       |
| 1229  | Purchase check failed                       |
| 1230  | exceededETFThe largest proportion of cash alternative              |
| 1231  | Non-exercise date                            |
| 1232  | Securities suspension                            |
| 1233  | Contractual restrictions Open                         |
| 1234  | Day total subscription or redemption amount exceeds the limit          |
| 1235  | I. The number of the day or the cumulative net redemptions exceed the limit       |
| 1236  | Can not find previous closing price                       |
| 1237  | Daily withdrawal limit exceeding ratio                       |
| 1238  | Delegation request is too frequent                      |
| 1239  | Illegal access to payment transfer amount                  |
| 1240  | Repeat subscription commission                       |
| 1241  | Copies subscription amount over subscription commission               |
| 1242  | Limit access to payment amount in more than                    |
| 1243  | At the same time ban to do more gold out of the pen                  |
| 1244  | The number of new shares with illegal、Winning record type            |
| 1245  | Limit shareholder accounts buy transaction                 |
| 1246  | Limit shareholders sell transaction accounts                 |
| 1247  | Limit shareholder accounts reverse repurchase transactions             |
| 1248  | Limiting shareholders to subscribe for new shares trading accounts            |
| 1249  | Shareholder account does not have permission market order trade          |
| 1250  | Shareholder account no transaction permission of Securities on GEM        |
| 1251  | Shareholder account no trading rights grading Fund          |
| 1252  | No shareholder accounts QFII authority bonds        |
| 1253  | Customer risk rating lower than the risk level of demand for securities trading   |
| 1254  | Shareholder account does not have permission securities trading risk warning       |
| 1255  | Shareholders do not have permission trading account securities delisting finishing       |
| 1256  | No single shareholder account trading marketETFpermission         |
| 1257  | Shareholders account does not cross-market tradingETFpermission         |
| 1258  | No shareholder account transactions Monetary FundETFpermission       |
| 1259  | No cross-border transactions shareholder accountETFpermission          |
| 1260  | Allow only qualified investors to invest in such securities             |
| 1261  | Allow only qualified institutional investors to invest in such securities          |
| 1262  | Gold out of abnormality，To be human intervention             |
| 1263  | Trading day period is not the issue of securities               |
| 1264  | ThatETFProhibit purchase                        |
| 1265  | ThatETFProhibit redemption                        |
| 1266  | Limit shareholder accounts specified withdrawal                 |
| 1267  | Limit shareholder accounts for custody transfer                 |
| 1268  | Institutional clients/Cabinet business is not supported by bank transfer         |
| 1269  | This ban private equity trading securities             |
| 1270  | This customer transactions prohibited securities                    |
| 1271  | Shareholder account no trading authority Depositary Receipts          |
| 1272  | Permissions shareholder accounts did not trade stock enterprise innovation       |
| 1273  | Illegal access to payment transfer type                  |
| 1274  | Shareholder account no trading rights through depositary receipts of Shanghai and London     |
| 1275  | Shareholder account no trading rights Kechuang board     |
