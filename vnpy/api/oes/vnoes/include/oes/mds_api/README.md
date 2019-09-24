# Swordfish-MDS API    {#mainpage}

Swordfish market data service systemAPIInstructions for use


---
### Quick Start

#### 1.1 Sample Code

- See also mds_api/samples Sample files directory
	- Sample configuration files <mds_client_sample.conf>
	- And the prices received code sample printed <mds_client_sample.c>
	- Quotes subscription and code samples received <mds_subscribe_sample.c>
	- Sample code for compilation <Makefile.sample>

mds_subscribe_sample.c Summarized as follows：
~~~{.c}

/**
 * By Securities Code List, Re-subscribe to market data (According to the code suffix to distinguish the particular market, If you do not specify a suffix, The default is on the card stock)
 *
 * @param   pTcpChannel         Session Information
 * @param   pCodeListString     Securities Code list of strings (A space or comma/semicolon/Vertical split string)
 * @return  TRUE success; FALSE failure
 */
static BOOL
MdsApiSample_ResubscribeByCodePostfix(MdsApiSessionInfoT *pTcpChannel,
        const char *pCodeListString) {
    return MdsApi_SubscribeByString(pTcpChannel,
            pCodeListString, (char *) NULL,
            MDS_EXCH_SSE, MDS_MD_PRODUCT_TYPE_STOCK, MDS_SUB_MODE_SET,
            MDS_SUB_DATA_TYPE_L1_SNAPSHOT
                    | MDS_SUB_DATA_TYPE_L2_SNAPSHOT
                    | MDS_SUB_DATA_TYPE_L2_BEST_ORDERS);
}


/**
 * Callback function message processing
 *
 * @param   pSessionInfo    Session Information
 * @param   pMsgHead        Header
 * @param   pMsgBody        Message body data
 * @param   pCallbackParams External incoming parameter
 * @return  greater or equal to0，success；Less than0，failure（Error number）
 */
static int32
MdsApiSample_HandleMsg(MdsApiSessionInfoT *pSessionInfo,
        SMsgHeadT *pMsgHead, void *pMsgBody, void *pCallbackParams) {
    MdsMktRspMsgBodyT   *pRspMsg = (MdsMktRspMsgBodyT *) pMsgBody;

    /*
     * Processing the message according to the message type Quote
     */
    switch (pMsgHead->msgId) {
    case MDS_MSGTYPE_L2_MARKET_DATA_SNAPSHOT:
    case MDS_MSGTYPE_L2_BEST_ORDERS_SNAPSHOT:
        /* deal withLevel2Snapshot market news */
        printf("... receivedLevel2Snapshot market news (exchId[%hhu], instrId[%d])\n",
                pRspMsg->mktDataSnapshot.head.exchId,
                pRspMsg->mktDataSnapshot.head.instrId);
        break;

    case MDS_MSGTYPE_L2_TRADE:
    case ...:
         ...
    }

    return 0;
}


int
main(int argc, char *argv[]) {
    /* Profiles */
    static const char   THE_CONFIG_FILE_NAME[] = "mds_client_sample.conf";
    /* Try waiting message arrives market timeout (millisecond) */
    static const int32  THE_TIMEOUT_MS = 1000;

    MdsApiClientEnvT    cliEnv = {NULLOBJ_MDSAPI_CLIENT_ENV};
    int32               ret = 0;

    /* Initialize the client environment (See profile: mds_client_sample.conf) */
    if (! MdsApi_InitAllByConvention(&cliEnv, THE_CONFIG_FILE_NAME)) {
        return -1;
    }

    /* According to resubscribe market securities code list (According to the code suffix to distinguish the particular market) */
    if (! MdsApiSample_ResubscribeByCodePostfix(&cliEnv.tcpChannel,
            "600000.SH, 600001.SH, 000001.SZ, 0000002.SZ")) {
        goto ON_ERROR;
    }

    while (1) {
        /* Wait for the market to reach the news, And processes the message through the callback function */
        ret = MdsApi_WaitOnMsg(&cliEnv.tcpChannel, THE_TIMEOUT_MS,
                MdsApiSample_HandleMsg, NULL);
        if (unlikely(ret < 0)) {
            if (likely(SPK_IS_NEG_ETIMEDOUT(ret))) {
                /* Time-out check (Check that the session has timed out) */
                continue;
            }

            if (SPK_IS_NEG_EPIPE(ret)) {
                /* The line is disconnected */
            }
            goto ON_ERROR;
        }
    }

    MdsApi_LogoutAll(&cliEnv, TRUE);
    return 0;

ON_ERROR:
    MdsApi_DestoryAll(&cliEnv);
    return -1;
}

~~~


#### 1.2 Compile and run the sample code

1. Into the sample code directory
	- ``cd mds_libs-xxx/include/mds_api/samples/``

2. Compiled code
	- ``make -f Makefile.sample``

3. Modify the configuration file，Confirm service address、And user name correctly
	- ``vi mds_client_sample.conf``

4. Running the sample program
	- ``./mds_subscribe_sample``
	- ``./mds_client_sample``


---
### Upgrade guidelines and the revision of history

- See the upgrade guide <@ref update_guide>
- See a modified version of history <@ref changelog>


---
### common problem

- Prices and amounts
	- MDSAll prices are`int32`The type of integer values，After four nearest element units, which is: 1yuan=10000
	- MDSAll amounts are in`int64`The type of integer values，After four nearest element units, which is: 1yuan=10000

- Share units
	- MDSAll the number of delegates、The number of units and other share transactions are`int32`or`int64`The type of integer values，With no decimal places
	- **note:** Shanghai share unit bond is <b>'hand'</b>，Instead of 'Zhang'，And various other

- MDSTime in the stock market(updateTime)Exchange is the right time？
	- Yes，The time comes Exchange，A generation time or data transmission time of the upstream market（If the acquisition is less than the market, then the generation time）


---
### MDSError code table

| error code | Error Description                            |
| :---- | :--------------------------------- |
| 1001  | Error message format                       |
| 1002  | The current host is not the master node                  |
| 1003  | Library operation failed main memory                     |
| 1004  | Depending on the state and other basic data does not match，Unable to update data   |
| 1005  | Protocol version incompatible                     |
| 1006  | Data does not exist                         |
| 1007  | Non-service opening hours                     |
| 1008  | Illegal cursor positioning                     |
| 1009  | Illegal client login user name             |
| 1010  | Illegal Securities Code                     |
| 1011  | Illegal customer code                     |
| 1012  | Illegal client type                    |
| 1013  | The client has been disabled                     |
| 1014  | The client password is incorrect                    |
| 1015  | Repeat Client Login                     |
| 1016  | The number of clients connect too many                  |
| 1017  | Client accounts of others unauthorized operation           |
| 1018  | Modified beyond the scope of data                    |
| 1019  | Illegal application name                  |
| 1020  | The query does not match                     |
| 1021  | Clientip/macMalformed Address            |
| 1022  | Not yet supported or not yet opened this business             |
| 1029  | Password unchanged                         |
| 1031  | Illegal type of encryption                     |
| 1033  | No available node                         |
| 1034  | Password strength not sufficient                       |
| 1035  | Illegal product type                     |
| 1036  | Black and white list check failed                 |
| 1301  | Subscribe to market failure                       |
