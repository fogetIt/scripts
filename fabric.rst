
智能合约
----------------------
::
    智能合约是运行于区块链上的应用程序，Fabric的智能合约称为链码，分为系统链码和用户链码，系统链码用来实现系统层面的功能，包括系统的配置，用户链码的部署、升级，用户交易的签名和验证策略等。用户链码实现用户的应用功能。

    链码被编译成一个独立的应用程序，运行于隔离的Docker容器中，在链码部署的时候会自动生成合约的Docker镜像。

    链码支持采用Go、Java、Nodejs编写，并提供相应的中间层供链码使用，链码可以使用GetState和PutState接口和Peer节点通信，存取K-V数据 。



节点
-------
- peers 组成 org ， orgs 组成 channel
- fabric 节点间通过 connection.json 互相寻址、通信

:fabric-ca: 会员注册和证书颁发节点

    - 每个 org 需要一个 ca 节点
    - fabric 系统的参与方（ orderer,peer,client ）都必须经过授权，需要拥有受信任的证书

:fabric-orderer: 共识网络节点

    - 每个 channel 需要一个 orderer 集群
    - 多方一起参与交易排序，生成新的区块，发送给 peer 节点

:fabric-peer: 区块链节点

    - 收到客户端交易提案，模拟执行交易，然后将原始交易提案和执行结果打包到一起，进行签名并发回给客户端
        - 交易提案中包含本次交易要调用的合约标识、合约方法和参数信息以及客户端签名等
        - 在模拟执行交易期间产生的数据修改不会写到账本上
    - 客户端收到各个 peer 的应答后，打包到一起组成一个交易并签名，发送给 orderer
    - peer 节点收到区块后，会对区块中的每笔交易进行校验
        - 检查交易依赖的输入输出是否符合当前区块链的状态，完成后
            - 负责将区块写入区块文件（交易共识系统排序后产生的区块数据），存储在本地文件系统
                - 每个文件有大小限制，存储一定数量的区块
                - 每个区块包含一条或多条交易
            - 修改 K-V 状态数据
                - 通过持有 CouchDB/LevelDB （世界状态数据库），提供给链码存取使用

工具
--------

:composer:

    - 二选一安装

    .. code-block:: bash

        npm i composer-cli
        docker pull hyperledger/composer-cli:x86_64-1.1.0

    - 添加管理员用户，并同步给节点
    - 部署业务网络（会生成一个镜像）
        - 通过 hyperledger/fabric-ccenv 镜像，为每个 peer 启动一个 chaincode 容器
        - chaincode 容器中包含了 java, node, go 的运行环境，用来保存和执行链码

:fabric-tools:

    - 二选一安装

    .. code-block:: bash

        curl https://nexus.hyperledger.org/content/repositories/releases/org/hyperledger/fabric/hyperledger-fabric/x86_64-1.1.0/hyperledger-fabric-x86_64-1.1.0.tar.gz | tar xzf
        export PATH=./bin:$PATH
        docker pull hyperledger/fabric-tools:x86_64-0.4.6

    :configtxgen:

        - 生成创世区块 orderer genesis block
            - 用来给 Orderer 节点做排序服务
        - 生成 channel configuration transaction
            - 用来配置和创建 channel 的配置文件
        - 生成组织锚节点 anchor peer transactions

    :configtxlator:
    :cryptogen: 根据网络用户拓扑关系（ .yaml 文件定义）生成各个节点（ peers,orderers,ca ）的证书
    :peer:


channel
----------

:频道:

    - Channel 本身存在于 orderer 结点内部，但需要使用 peer 节点 channel ... 命令进行维护
    - 两个 peer 结点必须同时处在同一个 Channel 中，才能发生交易
    - block 账本与 channel 是一对一的关系

:peer channel create: 在 orderer 结点内部创建一个 channel

    .. code-block:: bash

        peer channel create -o orderer.xxx:7050 -c mychannel -f channel.tx

:peer channel join:	  把 peer 加入一个 channel

    .. code-block:: bash

        peer channel join -b mychannel.block

:peer channel update: 升级 channel 的某一组织的配置

    .. code-block:: bash

        peer channel update -o orderer.xxx:7050 -c mychannel -f Org1MSPanchors.tx

:peer channel list:   列出当前系统中已经存在的 channel
:peer channel fetch:  获取 channel 中 newest,oldest 块数据或当前最新的配置数据

    .. code-block:: bash

        peer channel fetch config config_block.pb -o orderer.xxx:7050 -c mychannel