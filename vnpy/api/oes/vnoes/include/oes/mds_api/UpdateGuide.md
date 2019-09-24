# MDS-API Update Guide    {#update_guide}

MDS_0.15.9 / 2019-05-31
-----------------------------------

### 1. APIUpdate Summary

  1. Compatible server v0.15.5.1 versionAPI, Customers can choose not to upgrade (We recommend upgrading, Shenzhen securities business to be compatible with a number of adjustment switch)
  2. fix: repairAPIWe can not support a value greater than1024File descriptor problem
  3. Shenzhen securities business to expand the maximum number of switches, To respond to market data content update
     - The modified version might be beforeAPIAffect: Securities will affect the real-time status messages delay calculation, The old version reads invalid RBI time
  4. Adjustment of prices data types(mdStreamType, eMdsMdStreamTypeT)The value, A snapshot of the market makes it possible to identify the particular data type
     - The changes will be compatibility issues, The client program can be identified by compiling need to adjust the wrong place (If there are no compilation errors do not need to adjust)
     - Market value of the data type as consistent as possible with the message type, However, the following types of special：
       - Shenzhen trading volume statistical indicators
       - The Shanghai Stock Exchange Level1 Quotes Snapshot-Bond
       - The Shanghai Stock Exchange Level1 Quotes Snapshot-fund
  5. Heavy naming securityType => mdProductType, In order to avoid the type of securities transaction and end confusion
    - securityType => mdProductType
    - eMdsSecurityTypeT => eMdsMdProductTypeT
  6. Delete obsolete virtual auction news message definition and data type definitions
  7. APIAdd the following interfaces
     | API                          | description
     | ---------------------------- | ---------------
     | MdsApi_QueryStockStaticInfo  | Query securities(stock/Bond/fund)Static information
     | MdsApi_QuerySnapshotList     | Batch Quote snapshot interfaces
     | MdsApi_InitAllByCfgStruct    | Structures in accordance with the configuration information to initialize the client environment interface
     | MdsApi_SendChangePasswordReq | Modify client login password
     | MdsApi_SetCustomizedIp       | Set the local custom clientIPaddress
     | MdsApi_GetCustomizedIp       | Get Local custom clientIP
     | MdsApi_SetCustomizedMac      | Set the local custom clientMACaddress
     | MdsApi_GetCustomizedMac      | Get Local custom clientMAC
     | MdsApi_SetCustomizedDriverId | Set the local serial number of the client custom
     | MdsApi_GetCustomizedDriverId | Get local client device serial number custom
  8. New error code1029、1034、1035、1036, Adjustment error code1007、1022Description information
     | error code | description
     | ---- | ---------------
     | 1007 | Non-service opening hours
     | 1022 | Not yet supported or not yet opened this business
     | 1029 | Password unchanged
     | 1034 | Password strength not sufficient
     | 1035 | Illegal product type
     | 1036 | Black and white list check failed

### 2. Server update summary

  1. fix: Repair ShanghaiL2The initial snapshot of the problem of the lowest price is not set
  2. fix: solve MdsApi_SubscribeByString String cache interface is too small, Can only subscribe14000Only issue securities
  3. fix: Eliminate unnecessary noise reduction options market, The number of options to fix prices relatively few problems（35%）
  4. fix: Repair when additional subscription prices, Subscribe to the whole market would wash away the question mark
  5. fix: Market Overview fix prices in exchange transmission time is negative issue
  6. Improve the single market snapshot query, Code and exchange market allows fuzzy matching data(You do not have to explicitly specify Exchange Symbol);
     And when there is noL1We will attempt to retrieve snapshotsL2Snapshot, The unified query results converted to a five-speed snapshots return
  7. AdjustmentL2Quotes multicast channel data case by case, The mixing channel number of transactions and transaction-commissioned push case by case basis, Case by case basis to replace the previous transaction/Transaction-way push commissioned respectively(APICompatibility, But the content of the channel has changed)
  8. Optimized snapshot of the deduplication processing market
  9. Other repair system defects, Improve security

### 3. Notes Description

  1. The following two reconstruction may cause compile errors, These two fields do not usually use, You can identify whether there is need to adjust where compile errors, If there are no compilation errors do not need to adjust
     - Heavy naming securityType => mdProductType
     - Adjustment of prices data types(mdStreamType, eMdsMdStreamTypeT)The value
  2. The server sideL2Quotes multicast channel data has been adjusted case by case, The hybrid push the channel number of transactions and transaction-commissioned case by case basis, Case by case basis to preserve the timing relationship between the commission and deal case by case basis
     - Before the deal case by case basis/Case by case basis is commissioned by two channels respectively push, After adjustments need to pay attention to whether it will affect the processing logic
  3. Server-side deduplication processing snapshot of the market has been optimized
     - When to tickType=0 When the mode of subscription prices, The server will duplicate a snapshot of the market to do the heavy processing, Send duplicate data will not be pushed
     - If you need to get to a point in time snapshot of all, can use tickType=1 Quotes subscription model。This mode of behavior and consistent with previous versions, As long as the market changes time, Even though the data will be repeated downstream push


---

MDS_0.15.7.4 / 2018-08-31
-----------------------------------

### 1. APIUpdate Summary

  1. Compatible server v0.15.5.1 versionAPI，Customers can choose not to upgrade (We recommend upgrading)
  2. fix: When multiple threads simultaneously fix initializationAPIThe log, Cause problems with duplicate log information output
  3. APIAdd the following interfaces
    | API                          | description
    | ---------------------------- | ---------------
    | MdsApi_SetLastError          | Set the current threadAPIError number
    | MdsApi_GetLastError          | Get the current thread LastAPICall the wrong number failed
    | MdsApi_HasMoreCachedData     | Not return channel acquisition data buffer callback processing length
    | MdsApi_SetThreadUsername     | Set the login user name for the current thread
    | MdsApi_SetThreadPassword     | Set login password of the current thread
  4. New section error code
    | error code | description
    | ---- | ---------------
    | 1031 | Illegal type of encryption
    | 1033 | No available node
  5. Reconstruction SubscribeByString interface, Subscribe to enhance market flexibility
  6. Increasing the types of data can be subscribed (DataType), To support a separate subscription prices and index options market
  7. Add message can be processed is compressed MdsApi_WaitOnMsgCompressible interface, Market data to support the docking compression

### 2. Server update summary

  1. fix: Repair ShanghaiL2The lowest incremental snapshot is not updated correctly(As long0)ofBUG
  2. fix: Repair market subscription list of counter defect（The same ticker codes were used as index and stock code specifies twice when，Subscribe to less than market indices problems）
  3. fix: Repair no interceptions off9:25Problems around obsolete virtual auction news
  4. Other repair system defects，Improve the management and fault recovery processing


---

MDS_0.15.5.16 / 2018-08-31
-----------------------------------

### 1. APIUpdate Summary

  1. Compatible server v0.15.5.1 versionAPI, Customers can choose not to upgrade (We recommend upgrading)
  2. fix: When multiple threads simultaneously fix initializationAPIThe log, Cause problems with duplicate log information output
  3. increase MdsApi_HasMoreCachedData interface, A return has been received but not yet cached data length processed callback
  4. increase MdsApi_GetLastError interface, Return for the lastAPICall the wrong number failed
  5. Set current thread to increase user login name/Interface login password
  6. Reconstruction SubscribeByString interface, Subscribe to enhance market flexibility
  7. Increasing the types of data can be subscribed (DataType), To support a separate subscription prices and index options market
  8. Add message can be processed is compressed MdsApi_WaitOnMsgCompressible interface, Market data to support the docking compression

### 2. Server update summary

  1. fix: Repair ShanghaiL2The lowest incremental snapshot is not updated correctly(As long0)ofBUG
  2. fix: Repair market subscription list of counter defect（The same ticker codes were used as index and stock code specifies twice when, Subscribe to less than market indices problems）
  3. fix: Repair no interceptions off9:25Problems around obsolete virtual auction news
  4. Repair system defects, Improve the management and fault recovery processing


---

MDS_0.15.5.11 / 2018-06-20
-----------------------------------

### 1. APIUpdate Summary

  1. Compatible server v0.15.5.1 versionAPI, Customers can choose not to upgrade (We recommend upgrading)
  2. fix: expandLevel2Incremental update message to support the maximum number of price changes and volume of commissioned Details, In the scene to repair the huge fluctuations in price because of the insufficient number of support led to the loss of price informationBUG 
     - If you are using an older version ofAPI, Then the server will no longer push incremental update news (Push only the full amount snapshot), In order to maintain compatibility
     - If you need to use the words of an incremental update message, We need to update to the latest versionAPI, Otherwise, no need to updateAPI
  3. Market conditions for subscription and subscription configurations increase 'Expiration time transaction-type data tickExpireType' (Compatible with previous versions)

### 2. Server update summary

  1. fix: Repair market due to publish services and forwarding services use the same request queue, Leading to sporadic market subscription request could not be processed correctlyBUG
  2. fix: Repair market fluctuated wildly in the scene because of an insufficient number of supported incremental update prices lead to the loss of price informationBUG
  3. fix: Correction ShanghaiL2（Incremental）Snapshots will be problems between the latest price is not the lowest and highest price
  4. fix: To avoid the same ticker codes were used as index and stock code specifies twice, Resulting in the index have subscribed for the number of0, Then do not push the issue of market indices
  5. Add the stock market for low-speed network forwarding service
  6. Shenzhen market of forwarding process optimization, Quotes delayed morning peak period to improve the problem of excessive


---

MDS_0.15.5.4 / 2018-02-22
-----------------------------------

### 1. APIUpdate Summary

  1. Compatible server v0.15.5.1 versionAPI, Customers can choose not to upgrade
  2. fix: ResolvedWindowsCompatibility issues under
  3. Adjustment Interface MdsApi_InitAll, Add a function parameter (pUdpTickOrderAddrKey), Case by case basis, respectively, to support subscription and transaction-traded market multicast delegate
     - Because of the increased interface parameters, You need to modify the program, The parameter passed NULL To
  4. Increase Interface MdsApi_GetLastRecvTime、MdsApi_GetLastSendTime, Used to obtain a recent interview with Channel/Time to send a message
  5. When the login fails, able to pass errno/SPK_GET_ERRNO() Get to the specific cause of failure

### 2. Server update summary

  1. fix: Optimization market push, Improve the fairness of the push service
  2. fix: Repair is not convert in the calculation of turnover turnover of Shenzhen case by case basisint64, Caused the overflowBUG
  3. fix: Repair ShanghaiL1Index snapshot securityType Incorrect, Values ​​are 1 ofBUG
  4. fix: Repair inquiryL1Snapshot, Not in accordance with the query securityType Conduct problems matching
  5. fix: repair mds_tester Problem query function can not be used
  6. Quotes multicast support the specified port number of the sender
  7. Optimization Shenzhen market acquisition, Quotes delayed morning peak period to improve the problem of excessive
  8. Quotes delayed sending multicast optimization
