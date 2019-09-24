# MDS-API Change Log    {#changelog}

MDS_0.15.9 / 2019-05-31
==============================================

  * fix: repairAPIWe can not support a value greater than1024File descriptor problem (becauseselectlimits, When the value is larger than the file descriptor1024Time, It causes a stack overflow)
  * fix: Shenzhen securities business to expand the maximum number of switches（The modified version will have beforeAPIThe impact of the delay statistics）, To respond to market data content update
  * Adjustment of prices data types(mdStreamType, eMdsMdStreamTypeT)The value, A snapshot of the market makes it possible to identify the particular data type
     - The changes will be compatibility issues, The client program can be identified by compiling need to adjust the wrong place (If there are no compilation errors do not need to adjust)
     - Market value of the data type as consistent as possible with the message type, However, the following types of special：
       - Shenzhen trading volume statistical indicators
       - The Shanghai Stock Exchange Level1 Quotes Snapshot-Bond
       - The Shanghai Stock Exchange Level1 Quotes Snapshot-fund
  * Heavy naming securityType => mdProductType, In order to avoid the type of securities transaction and end confusion
    - securityType => mdProductType
    - eMdsSecurityTypeT => eMdsMdProductTypeT
  * Delete obsolete virtual auction news message definition and data type definitions
  * Snapshot head adjustment MdsMktDataSnapshotHeadT The internal field definitions, will __origTickSeq Field split into __origTickSeq + __lastUpdateTime Two fields (Field for internal use, Protocol compatibility)
  * Increased modify client login password Interface
    - MdsApi_SendChangePasswordReq
  * Set to increase/Get Local custom clientIP/MACInterface address
    - MdsApi_SetCustomizedIp
    - MdsApi_GetCustomizedIp
    - MdsApi_SetCustomizedMac
    - MdsApi_GetCustomizedMac
  * Set to increase/Get the serial number of the interface device client custom
    - MdsApi_SetCustomizedDriverId
    - MdsApi_GetCustomizedDriverId
  * New error code
    - 1029, Password unchanged
    - 1034, Password strength not sufficient
    - 1036, Black and white list check failed

MDS_0.15.8 / 2019-02-22
==============================================

  * fix: repairAPIWe can not support a value greater than1024File descriptor problem (becauseselectlimits, When the value is larger than the file descriptor1024Time, It causes a stack overflow)
  * Heavy naming securityType => mdProductType, In order to avoid the type of securities transaction and end confusion
    - securityType => mdProductType
    - eMdsSecurityTypeT => eMdsMdProductTypeT
  * Delete obsolete virtual auction news message definition and data type definitions
  * Snapshot head adjustment MdsMktDataSnapshotHeadT The internal field definitions, will __origTickSeq Field split into __origTickSeq + __lastUpdateTime Two fields (Field for internal use, Protocol compatibility)
  * Increasing the network timeout when signing, Avoid because the system is busy Logon failed due to other reasons
  * Adjustment error description
    - 1007, Non-service opening hours
    - 1022, Not yet supported or not yet opened this business
    - 1035, Illegal product type

MDS_0.15.7.6 / 2018-11-28
==============================================

  * Add batch Quote snapshot interfaces
    - MdsApi_QuerySnapshotList
  * According to the configuration information structure, Increase initialize the client environment interface
    - MdsApi_InitAllByCfgStruct

MDS_0.15.7.6 / 2018-11-03
==============================================

  * Increase in inquiries Securities(stock/Bond/fund)Interface static information
    - MdsApi_QueryStockStaticInfo
  * New error code definitions
    - 1035, Illegal product type（MDSERR_ILLEGAL_PRODUCT_TYPE）

MDS_0.15.7.5 / 2018-08-31
==============================================

  * repair 'Returns the error message error number (MdsApi_GetErrorMsg)' interface, windowsPlatform get the error message is not accurate

MDS_0.15.7.4 / 2018-08-31
==============================================

  * Set current thread to increase user login name/Interface login password
    - MdsApi_SetThreadUsername
    - MdsApi_SetThreadPassword
  * Increase returns the current thread lastAPIInterface error numbers call failed
    - OesApi_GetLastError
    - OesApi_SetLastError
  * See additional error number mds_errors.h
  * Merge MDS_0.15.5.16
    - fix: When multiple threads simultaneously fix initializationAPIThe log, Cause problems with duplicate log information output
    - increase MdsApi_HasMoreCachedData interface, A return has been received but not yet cached data length processed callback
    - Reconstruction SubscribeByString interface
      - All products support subscription prices or market any product without subscription
      - Supported by .SH or .SZ Specifies the suffix to which it belongs Exchange ticker
      - Add to MdsHelper_SetTickTypeOnSubscribeByString interface, To setSubscribeByStringThe default mode used data (TickType)
      - When incremental subscription, Permit does not specify dataType (Less than0) The subscription before inherit the data type
    - Increasing the types of data can be subscribed (DataType), To support a separate subscription prices and index options market
      - MDS_SUB_DATA_TYPE_INDEX_SNAPSHOT, versusL1_SNAPSHOTDifference is that, INDEX_SNAPSHOTYou can subscribe to individual market index
      - MDS_SUB_DATA_TYPE_OPTION_SNAPSHOT, versusL1_SNAPSHOTDifference is that, OPTION_SNAPSHOTOptions can subscribe to a single market
    - Add message can be processed is compressed WaitOnMsg interface:
      - MdsApi_WaitOnMsgCompressible
      - MdsApi_WaitOnTcpChannelGroupCompressible
      - And without Compressible Compared suffix Interface, band Compressible Interface automatically detecting and processing the compressed message suffix, But it will therefore result in a small performance penalty

MDS_0.15.5.16 / 2018-08-31
==============================================

  * fix: When multiple threads simultaneously fix initializationAPIThe log, Cause problems with duplicate log information output
  * increase MdsApi_HasMoreCachedData interface, A return has been received but not yet cached data length processed callback
  * Set current thread to increase user login name/Interface login password
    - MdsApi_SetThreadUsername
    - MdsApi_SetThreadPassword
  * Increase return lastAPIInterface error numbers call failed
    - MdsApi_GetLastError
  * Reconstruction SubscribeByString interface
    - All products support subscription prices or market any product without subscription
    - Supported by .SH or .SZ Specifies the suffix to which it belongs Exchange ticker
    - Add to MdsHelper_SetTickTypeOnSubscribeByString interface, To setSubscribeByStringThe default mode used data (TickType)
    - When incremental subscription, Permit does not specify dataType (Less than0) The subscription before inherit the data type
  * Increasing the types of data can be subscribed (DataType), To support a separate subscription prices and index options market
    - MDS_SUB_DATA_TYPE_INDEX_SNAPSHOT, versusL1_SNAPSHOTDifference is that, INDEX_SNAPSHOTYou can subscribe to individual market index
    - MDS_SUB_DATA_TYPE_OPTION_SNAPSHOT, versusL1_SNAPSHOTDifference is that, OPTION_SNAPSHOTOptions can subscribe to a single market
  * Add message can be processed is compressed WaitOnMsg interface:
    - MdsApi_WaitOnMsgCompressible
    - MdsApi_WaitOnTcpChannelGroupCompressible
    - And without Compressible Compared suffix Interface, band Compressible Interface automatically detecting and processing the compressed message suffix, But it will therefore result in a small performance penalty

MDS_0.15.5.11 / 2018-06-05
==============================================

  * fix: expandLevel2Incremental update message to support the maximum number of price changes and volume of commissioned Details, In the scene to repair the huge fluctuations in price because of the insufficient number of support led to the loss of price informationBUG 
    - If you are using an older version ofAPI, Then the server will no longer push incremental update news (Push only the full amount snapshot), In order to maintain compatibility
    - If you need to use the words of an incremental update message, We need to update to the latest versionAPI, Otherwise, no need to updateAPI

MDS_0.15.5.10 / 2018-05-24
==============================================

  * Market conditions for subscription and subscription configurations increase 'Expiration time transaction-type data tickExpireType' (Compatible with previous versions)
  * Increase the subscription market conditions for internal use only a 'Internal channel number to be subscribed', The front end does not need to care and treatment (Compatible with previous versions)

MDS_0.15.5.4 / 2018-02-22
==============================================

  * Adjustment Interface MdsApi_InitAll, Add a function parameter (pUdpTickOrderAddrKey), Case by case basis, respectively, to support subscription and transaction-traded market multicast delegate
  * Merge MDS_0.15.5.2
    - fix: ResolvedWindowsCompatibility issues under
    - Increase Interface MdsApi_GetLastRecvTime、MdsApi_GetLastSendTime, Used to obtain a recent interview with Channel/Time to send a message
    - When the login fails, able to pass errno/SPK_GET_ERRNO() Get to the specific cause of failure

MDS_0.15.5.2 / 2018-01-29 (solveWindowsCompatibility issuesAPIupdated version)
==============================================

  * fix: ResolvedWindowsCompatibility issues under。include:
    - fix: inWindowsunder, APIofSocketNon-blocking mode in question, Only works in blocking mode
    - fix: inWindowsunder, When there is no market data, Quotes Subscribe transmission process will live long ram, Until heartbeat messages are triggered not return
    - fix: inWindowsunder, When run in debug mode, If the network connection, then an exception, On exit(shut downsocketConnection)An exception will be reported
    - fix: inWindowsunder, Can not be acquiredIPwithMACaddress, We need to explicitly provided local to the clientIPwithMAC
  * Increase Interface MdsApi_GetLastRecvTime、MdsApi_GetLastSendTime, Used to obtain a recent interview with Channel/Time to send a message
  * When the login fails, able to pass errno/SPK_GET_ERRNO() Get to the specific cause of failure

MDS_0.15.5.1 / 2017-11-22
==============================================

  * fix: repair MdsApi_InitAllByConvention() Interface always returns a connection failureBUG
  * Increase the value of the type of protocol version number MDS_APPL_VER_VALUE, To facilitate alignment version
  * increase MdsApi_IsValidTcpChannel、MdsApi_IsValidUdpChannel And other interfaces, For determining whether a channel has been connected and effective

MDS_0.15.5 / 2017-11-12
==============================================

  * New Interface 'ObtainAPIThe release number (MdsApi_GetApiVersion)'
  * RBI to open the default information for statistical delay, RBI time stamp information and the type of change timeval32 (STimeval32T) Types of
  * Server to delete theJSONAnd other communication protocol support, Instead only support binary protocol
  * In transaction-market push multicast data, And dividing the market push multicast channel, respectivelyL1Snapshot、L2Snapshot data and case by case basis
  * Adjustment Interface MdsApi_InitAll, To support simultaneous multiple multicast channel initialization
  * Increasing the associated channel group API interface, Simultaneously receiving a plurality of data to support the connecting channels

MDS_0.15.3.3 / 2017/08/20
==============================================

 * New Interface 'Reset thread-level logger name (MdsApi_ResetThreadLoggerName)', Support for the current thread to set up a separate log file

MDS_0.15.3 / 2017-08-14
==============================================

  * Merge MDS_0.12.9.12
    - fix: AgainstWindowsplatform, becauseGNULibofrecvThe method has problems when multiple threads, There will be different Socket Interfere with each other and the phenomenon of serial execution, So temporarily switch back to using only operate in blocking moderead/writemethod
    - Known Issues:
      - inWindowsunder, APIofSocketNon-blocking mode in question, Only work temporarily in blocking mode
  * Merge MDS_0.12.9.11
    - fix: Cross-platform reconstruction process, perfectAPICorrectWindowsSupported platforms
      - fix: RepairWindowsunder，SocketFailure to properly set to non-blocking modeBUG
      - fix: RepairWindowsunder，becauseerrnoIncompatible lead to failure of network processingBUG
      - fix: RepairWindowsunder，Because it is not compatible with the file path handling，Cause the log failed to initializeBUG
      - fix: RepairWindowsunder，Individual functions are not compatible causes the compiler to issue warnings and runtime errors
      - fix: Because the Chinese character encoding repair inconsistent results inWindowsCompilation failed under question
      - refactor: inAPIHeader file referenced by default spk_platforms.h head File
      - refactor: ReconstructionAPISample code and sample configuration files

MDS_0.15.2 / 2017-07-12
==============================================

  * API versus 0.12.9.7 The same version
    - Transaction-lost message no longer released(MDS_MSGTYPE_L2_TICK_LOST), The message is obsolete

MDS_0.15.1 / 2017-06-26
==============================================

  * fix: Amended version of the compiler error performance testing
  * API versus 0.12.8 The same version，No change

MDS_0.12.9.12 / 2017-08-13
==============================================

  * fix: AgainstWindowsplatform, becauseGNULibofrecvThe method has problems when multiple threads, There will be different Socket Interfere with each other and the phenomenon of serial execution, So temporarily switch back to using only operate in blocking moderead/writemethod
  * Known Issues:
    - inWindowsunder, APIofSocketNon-blocking mode in question, Only work temporarily in blocking mode

MDS_0.12.9.11 / 2017-08-12
==============================================

  * Cross-platform reconstruction process, perfectAPICorrectWindowsSupported platforms
    - fix: RepairWindowsunder，SocketFailure to properly set to non-blocking modeBUG
    - fix: RepairWindowsunder，becauseerrnoIncompatible lead to failure of network processingBUG
    - fix: RepairWindowsunder，Because it is not compatible with the file path handling，Cause the log failed to initializeBUG
    - fix: RepairWindowsunder，Individual functions are not compatible causes the compiler to issue warnings and runtime errors
    - fix: Because the Chinese character encoding repair inconsistent results inWindowsCompilation failed under question
    - refactor: Cross-platform reconstruction process, Perfect forWindowsSupported platforms, AndAPIHeader file referenced by defaultspk_platforms.h
    - refactor: Fine tuningAPISample code and sample configuration files

MDS_0.12.9.7 / 2017-07-12
==============================================

  * Transaction-lost message no longer released(MDS_MSGTYPE_L2_TICK_LOST), The message is obsolete

MDS_0.12.9_RC1 / 2017-06-05
==============================================

  * API versus 0.12.8 The same version，No change

MDS_0.12.8.1 / 2017-04-24 (APIUpdate instructions)
==============================================

### Change message codes
    1. Redefine a message type value of
    2. willLevel1Securities market split into full-size message'Level1Market snapshot'、'Index market snapshot'、'Options market snapshot'Three messages:
        - MDS_MSGTYPE_MARKET_DATA_SNAPSHOT_FULL_REFRESH (Level1 Market snapshot)
        - MDS_MSGTYPE_INDEX_SNAPSHOT_FULL_REFRESH       (Index market snapshot)
        - MDS_MSGTYPE_OPTION_SNAPSHOT_FULL_REFRESH      (Options market snapshot)
    3. NewLevel2Market news:
        - MDS_MSGTYPE_L2_MARKET_DATA_SNAPSHOT           (Level2 Market snapshot)
        - MDS_MSGTYPE_L2_BEST_ORDERS_SNAPSHOT           (Level2 Commissioned Queue Snapshots (buy one/Sell ​​a number of the top 50 pen commissioned))
        - MDS_MSGTYPE_L2_TRADE                          (Deal case by case basis)
        - MDS_MSGTYPE_L2_ORDER                          (Commissioned case by case basis (Shenzhen only))
        - MDS_MSGTYPE_L2_MARKET_OVERVIEW                (Market Overview news (Only Shanghai))
        - MDS_MSGTYPE_L2_VIRTUAL_AUCTION_PRICE          (Virtual auction news (Only Shanghai))
        - MDS_MSGTYPE_L2_MARKET_DATA_INCREMENTAL        (An incremental update message, only at TickType for AllIncrements There (Only Shanghai))
        - MDS_MSGTYPE_L2_BEST_ORDERS_INCREMENTAL        (An incremental update message, only at TickType for AllIncrements There (Only Shanghai))
    4. New message notification:
        - MDS_MSGTYPE_L2_TICK_LOST                      (Data loss case by case basis, Deal case by case basis/Transaction-commissioned data loss occurred, And can not be rebuilt, We will give up these missing data case by case basis)

### Change structure
    1. Deleted structures and fields
        - To remove unattached MdsMktDataSnapshotEntryMetaT Structure,
          Will be integrated into the field MdsMktDataSnapshotHeadT in, And delete the original meta.priceUnit (price unit) Field
        - delete MdsStockSnapshotBodyT.MDStreamID, MdsIndexSnapshotBodyT.MDStreamID Field
    2. Rename the structure and fields
        - Heavy naming MdsMktDataSnapshotEntryT -> MdsL1SnapshotBodyT
        - Heavy naming MdsIndexDataSnapshotEntryT -> MdsIndexSnapshotBodyT
        - Heavy naming MdsStockDataSnapshotEntryT -> MdsStockSnapshotBodyT
        - Heavy naming MdsStockSnapshotBodyT.PreCloseIOPV -> NAV
        - Rename price and split the original five-speed field MdsStockSnapshotBodyT.PriceLevel[5] -> BidLevels[5] + OfferLevels[5]
            - Refer to the following regular expressions can be replaced:
            - ``PriceLevel\[(\w+)\].BuyPrice -> BidLevels[\1].Price``
            - ``PriceLevel\[(\w+)\].BuyVolume -> BidLevels[\1].OrderQty``
            - ``PriceLevel\[(\w+)\].SellPrice -> OfferLevels[\1].Price``
            - ``PriceLevel\[(\w+)\].SellVolume -> OfferLevels[\1].OrderQty``
        - Rename the original snapshot of the total turnover of the market in the field TradeVolume -> TotalVolumeTraded
    3. The new structures and fields
        - for'Market conditions'、'Securities and real-time status'with'Market Overview news'Add a message __exchSendingTime with __mdsRecvTime Field，To facilitate the market than the actual delay
        - Spread'Full-size securities market news(MdsMktDataSnapshotT)'Definition, Add toLevel2Snapshot message body, The complete message is defined as follows:
            - MdsL2StockSnapshotBodyT             l2Stock;                  (Level2 Snapshot Quotes(stock、Bond、fund))
            - MdsL2StockSnapshotIncrementalT      l2StockIncremental;       (Level2 Quotes incremental snapshot update message)
            - MdsL2BestOrdersSnapshotBodyT        l2BestOrders;             (Level2 buy one／Sell ​​a top 50 pen commissioned Details)
            - MdsL2BestOrdersSnapshotIncrementalT l2BestOrdersIncremental;  (Level2 buy one／Sell ​​a top 50 pen commissioned incremental update details of the message)
            - MdsStockSnapshotBodyT               stock;                    (Level1 stock、Bond、Fund market data)
            - MdsStockSnapshotBodyT               option;                   (Level1/Level2 Options market data)
            - MdsIndexSnapshotBodyT               index;                    (Level1/Level2 Index market data)
            - MdsL2VirtualAuctionPriceT           l2VirtualAuctionPrice;    (Level2 Virtual auction (Only Shanghai))
            - MdsL2MarketOverviewT                l2MarketOverview;         (Level2 Market Overview (Only Shanghai))
        - New market structure is defined case by case basis:
            - MdsL2TradeT                               (Deal case by case basis)
            - MdsL2OrderT                               (Commissioned case by case basis)

### Quotes subscription-related changes
    1. Subscribe to redefine the market news, It includes the following fields and parameters:
        - Subscription model (subMode) @see eMdsSubscribedTickTypeT
            - 0: (Set) Resubscribe，Set the subscription list of stock
            - 1: (Append) Additional subscription，Increase the subscription list of stock
            - 2: (Delete) Delete subscription，Delete the subscription list of stock
        - Data Mode, Subscribe to the latest market snapshot or point of all data (tickType) @see eMdsSubscribedTickTypeT
            - 0: (LatestSimplified) Only subscribe to the latest market snapshot data, And ignore and skip the outdated data (This mode is recommended to)
        - Specifies the securities markets and types of subscriptions mark
            - It comprises the following fields:
                - sseStockFlag/sseIndexFlag/sseOptionFlag
                - szseStockFlag/szseIndexFlag/szseOptionFlag
            - Value Description @see eMdsMktSubscribeFlagT
                - 0: (Default) According to the subscription list subscription products market
                - 1: (All) Subscribe to market all products of this market and the type of securities
                - 2: (Disable) Disable the market all products of this market
        - Before it can push real-time market data, The need to push the stock market initial snapshot subscription products (isRequireInitialMktData)
            - 0: Do not need
            - 1: need, That ensures that the client has subscribed to receive at least one product market snapshot (if so)
        - Subscribe to the type of data (dataTypes) @see eMdsSubscribeDataTypeT
            - 0:      The default type of data (all)
            - 0x0001: L1Snapshot/index/Options
            - 0x0002: L2Snapshot
            - 0x0004: L2Commissioned queue
            - 0x0008: L2Deal case by case basis
            - 0x0010: L2Commissioned case by case basis（Shenzhen）
            - 0x0020: L2Virtual auction（Shanghai）
            - 0x0040: L2Market Overview（Shanghai）
            - 0x0100: Market conditions（Shanghai）
            - 0x0200: Securities and real-time status（Shenzhen）
            - 0xFFFF: All data
            - E.g, If you only need to subscribe 'L1Snapshot' with 'L2Snapshot', You can dataTypes Set as:
                - 0x01 | 0x02
        - Start time market data requests to subscribe (beginTime)
            - Less than 0: Get to start from scratch
            - equal 0: Began to get real-time quotes from the latest position
            - equal 0: Start getting from the specified start time (The format: HHMMSS or HHMMSSsss)
        - For ease of use, Expand the number of products per subscription request can specify to: 4000
    2. Adjusted market subscription response message
        - Subscribe to return the actual results of the market, Ie the actual number of products have been subscribed
    3. Rename the original subscription prices Interface
        - Heavy naming MdsApi_SubscribeMarketData -> MdsApi_SyncSubscribeOnLogon
          Send a message to subscribe the securities market，And synchronous waiting for a response message returned (Only for the initial subscription after the connection is established)
        - Heavy naming MdsApi_ResubscribeMarketData -> MdsApi_SubscribeMarketData
          Asynchronously send a subscription request real-time stock quotes，To re-subscribe、Additional market data subscriptions or delete subscriptions
    4. We added a few more quotes subscribe to the interface easy to use
        - MdsApi_SubscribeByString                      (Subscribe to securities market information based on a string of code list)
        - MdsApi_SubscribeByString2                     (Securities code list an array of pointers string subscription market information)
        - MdsApi_SubscribeByStringAndPrefixes           (Subscribe to the list of direct market information and a list of securities under the Securities Code code prefix of a string)
        - MdsApi_SubscribeByStringAndPrefixes2          (An array of pointers to strings of code list securities and securities market information code prefix Subscribe)
        - These string of subscription Interface, There is no limit to the number of products, You can pass a line of code to be subscribed to a list of all products
        - To simplify the use, Proposal directly using a subscription-based interface can be a string of, But if you need more fine-grained control,
          You also need MdsApi_SubscribeMarketData Subscribe interface
        - Subscribe to use the sample interface, Sample code can refer to:
            - mds_subscribe_sample.c The sample file function MdsApiSample_ResubscribeByCodeFile
    5. Adds several auxiliary(Binary)The subscription request information maintenance function
        - MdsHelper_ClearSubscribeRequestEntries        (Empty subscription product list information)
        - MdsHelper_SetSubscribeRequestMode             (Setting subscription model)
        - MdsHelper_SetSubscribeRequestTickType         (Set the data mode (TickType))
        - MdsHelper_SetSubscribeRequestDataTypes        (Set the type of subscription data)
        - MdsHelper_SetSubscribeRequestSubFlag          (Settings Specify the type of securities markets and subscription sign)
        - MdsHelper_AddSubscribeRequestEntry            (Subscribe to be added to the subscription product information)

### Quotes treatment related changes
    1. Configuring update subscription prices, Set the type of data that needs to subscribe
    2. Update market approach, The following new processing these market news (If you have subscribed to the words):
        - MDS_MSGTYPE_MARKET_DATA_SNAPSHOT_FULL_REFRESH (Level1 Market snapshot)
        - MDS_MSGTYPE_INDEX_SNAPSHOT_FULL_REFRESH       (Index market snapshot)
        - MDS_MSGTYPE_OPTION_SNAPSHOT_FULL_REFRESH      (Options market snapshot)
        - MDS_MSGTYPE_L2_MARKET_DATA_SNAPSHOT           (Level2 Market snapshot)
        - MDS_MSGTYPE_L2_BEST_ORDERS_SNAPSHOT           (Level2 Commissioned Queue Snapshots (buy one/Sell ​​a number of the top 50 pen commissioned))
        - MDS_MSGTYPE_L2_TRADE                          (Deal case by case basis)
        - MDS_MSGTYPE_L2_ORDER                          (Commissioned case by case basis (Shenzhen only))
        - MDS_MSGTYPE_L2_MARKET_OVERVIEW                (Market Overview news (Only Shanghai))
        - MDS_MSGTYPE_L2_VIRTUAL_AUCTION_PRICE          (Virtual auction news (Only Shanghai))
        - MDS_MSGTYPE_L2_MARKET_DATA_INCREMENTAL        (An incremental update message, only at TickType for AllIncrements There (Only Shanghai))
        - MDS_MSGTYPE_L2_BEST_ORDERS_INCREMENTAL        (An incremental update message, only at TickType for AllIncrements There (Only Shanghai))
    3. Sample code can refer to:
        - mds_subscribe_sample.c The sample file function MdsApiSample_HandleMsg
        - or, mds_client_sample.c The sample file function _MdsApiSample_HandleMsg

MDS_0.12.8.2 / 2017-05-16 (ChangeLog)
==============================================

  * Add to 'Case by case basis data loss news(MdsL2TickLostT)', System to notify the downstream transaction-data(Deal case by case basis/Commissioned case by case basis)Data loss occurred, And can not be rebuilt, We will give up these missing data case by case basis

MDS_0.12.8.1 / 2017-04-24 (ChangeLog)
==============================================

### Domain model related changes
    - To remove unattached MdsMktDataSnapshotEntryMetaT Structure,
      Will be integrated into the field MdsMktDataSnapshotHeadT in, And delete the original meta.priceUnit (price unit) Field
    - Heavy naming MdsMktDataSnapshotEntryT -> MdsL1SnapshotBodyT
    - Heavy naming MdsIndexDataSnapshotEntryT -> MdsIndexSnapshotBodyT
    - Heavy naming MdsStockDataSnapshotEntryT -> MdsStockSnapshotBodyT
    - Heavy naming MdsStockSnapshotBodyT.PreCloseIOPV -> NAV
    - redefine MdsStockSnapshotBodyT.PriceLevel[5] -> BidLevels[5] + OfferLevels[5]
        - ``PriceLevel\[(\w+)\].BuyPrice -> BidLevels[\1].Price``
        - ``PriceLevel\[(\w+)\].BuyVolume -> BidLevels[\1].OrderQty``
        - ``PriceLevel\[(\w+)\].SellPrice -> OfferLevels[\1].Price``
        - ``PriceLevel\[(\w+)\].SellVolume -> OfferLevels[\1].OrderQty``
    - Heavy naming MdsStockSnapshotBodyT.TradeVolume -> TotalVolumeTraded
    - Heavy naming MdsIndexSnapshotBodyT.TradeVolume -> TotalVolumeTraded
    - delete MdsStockSnapshotBodyT.MDStreamID, MdsIndexSnapshotBodyT.MDStreamID Field
    - for'Market conditions'with'Securities and real-time status'Add a message __exchSendingTime, __mdsRecvTime Field，
      To facilitate the market than the actual delay

### Communication protocols related changes
    - Redefine a message type value of
    - The securities market is split into full-size message'Level1Market snapshot'、'Index market snapshot'、'Options market snapshot'Three messages:
        - MDS_MSGTYPE_MARKET_DATA_SNAPSHOT_FULL_REFRESH
        - MDS_MSGTYPE_INDEX_SNAPSHOT_FULL_REFRESH
        - MDS_MSGTYPE_OPTION_SNAPSHOT_FULL_REFRESH
    - Adjustment subscription type（TickType）Enumeration type definitions and values
        - redefine MDS_TICK_TYPE_LATEST_ONLY -> MDS_TICK_TYPE_LATEST_SIMPLIFIED
            - Only subscribe to the latest market snapshot data, And ignore and skip the outdated data (Minimum amount of data pushed, It will not be sent the latest snapshot)
        - redefine MDS_TICK_TYPE_ALL_TICK -> MDS_TICK_TYPE_ALL_INCREMENTS
            - Subscribe to the stock market at all time points snapshot data (have to be aware of is，Will send extra this modeLevel2Quotes incremental snapshot update message)
        - New MDS_TICK_TYPE_LATEST_TIMELY
            - Only subscribe to the latest market snapshot data, And the latest data is sent immediately (It will be more timely access to the latest market active trading, But repeatedly sends the most recent snapshot)
    - For ease of use, Expand the number of products per subscription request can specify to: 4000
    - Subscribe to redefine the market news
        - Subscription model @see eMdsSubscribeModeT
        - Securities market and the type of subscription sign @see eMdsMktSubscribeFlagT
        - Data Mode @see eMdsSubscribedTickTypeT
        - The type of data @see eMdsSubscribeDataTypeT
        - Starting time (-1: Get to start from scratch, 0: Began to get real-time quotes from the latest position, >0: Start getting from the specified start time)
        - Whether the initial market data

### APIThe interface related changes
    - Heavy naming MdsApi_SubscribeMarketData -> MdsApi_SyncSubscribeOnLogon
    - Heavy naming MdsApi_ResubscribeMarketData -> MdsApi_SubscribeMarketData
    - Add a secondary stock market subscription Interface
        - MdsApi_SubscribeByString
        - MdsApi_SubscribeByStringAndPrefixes
        - MdsHelper_SetSubscribeRequestMode
        - MdsHelper_SetSubscribeRequestTickType
        - MdsHelper_SetSubscribeRequestDataTypes

MDS_0.12.6.3 / 2017-03-24
================================

  * increasemds_api.hThe header file references，APIUsers no longer need to explicitly referencesutilLibrary header files

MDS_0.12.3 / 2017-02-21
================================

  * streamlineAPIDependent header files，And minimizeAPIRelease the number of headers package
  * Heavy naming protocol_parser/errors/mds_protocol_errors.h -> errors/mds_errors.h
  * Reconstruction MdsApi_GetErrorMsg method，Support the unified business return error or system error messages
  * fix: repairAPISubscribe to parse the configuration，Exchange Symbol assignment errorsBUG
  * Adding auxiliary interfaces and sample code for real-time quotes subscription features
     - MdsApi_ResubscribeMarketData
     - MdsHelper_ClearSubscribeRequestEntries
     - MdsHelper_AddSubscribeRequestEntry
     - Sample code: mds_subscribe_sample.c

MDS_0.12.1 / 2016-12-21
================================

  * Rename the query interface
     - MdsApi_QryMktDataSnapshot -> MdsApi_QueryMktDataSnapshot
     - MdsApi_QrySecurityStatus -> MdsApi_QuerySecurityStatus
     - MdsApi_QryTrdSessionStatus -> MdsApi_QueryTrdSessionStatus
  * delete MdsApi_IsBusinessError interface，Query interface not return less than -1000 mistake
  * The return value query interface changes:
     - No data is returned NEG(ENOENT)
     - Query is refusing to return to the server NEG(EINVAL)，Specific error messages by Log Print

MDS_0.12 / 2016-12-06
==============================

  * Reconstruction of the definition of the error number，The error number from1000Start
  * increase MdsApi_GetErrorMsg with MdsApi_GetErrorMsg2 method
  * Increased Protocol version number information in the login message, And compatibility checking protocol version number at login
