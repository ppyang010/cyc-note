---
Title: "分布式事务seata分享草稿"
Url: ""
Author: ""
Origin: "WizNote"
Description: ""
Tags: []
Created: "2023-03-21 22:54:38"
Cover: ""
WizGuid: "9258c6b5-821b-4b1f-bf03-56a55c2c3e36"
WizType: "document"
WizLocation: "/dxy/init/"
WizDataMd5: "ca054ba6f9e410bf9075990de4222561"
Modified: "2023-04-05 21:39:33"
WizSyncedAt: "2026-07-29 15:36:28"
---

|  | XA/2PC | TCC | Saga | 可靠事件队列 |
| --- | --- | --- | --- | --- |
| 事务一致性 | 强 | 弱 | 弱 | 弱 |
| 复杂性 | 中 | 高 | 中 | 低 |
| 业务侵入性 | 小 | 大 | 小 | 中 |
| 使用局限性 | 大 | 大 | 中 | 小 |
| 性能 | 低 | 中 | 高 | 高 |
| 维护成本 | 低 | 高 | 中 | 低 |

| 隔离级别 | 脏读 | 不可重复读 | 幻读 |  |
| --- | --- | --- | --- | --- |
| 读未提交<br>(Read uncommitted) | 可能 | 可能 | 可能 |  |
| 读已提交<br>(Read committed) | 不可能 | 可能 | 可能 |  |
| 可重复读<br>(Repeatable read) | 不可能 | 不可能 | 可能 |  |
| 可串行化<br>(Serializable) | 不可能 | 不可能 | 不可能 |  |
|  |  |  |  |  |

---

@Override @GlobalTransactional(name="createOrder") public Order saveOrder(OrderVo orderVo) { log.info("=============用户下单================="); log.info("当前 XID: {}", RootContext.getXID()); // 保存订单 Order order = new Order(); order.setUserId(orderVo.getUserId()); order.setCommodityCode(orderVo.getCommodityCode()); order.setCount(orderVo.getCount()); order.setMoney(orderVo.getMoney()); order.setStatus(OrderStatus.INIT.getValue()); Integer saveOrderRecord = orderMapper.insert(order); log.info("保存订单{}", saveOrderRecord > 0 ? "成功" : "失败"); //扣减库存 storageFeignService.deduct(orderVo.getCommodityCode(), orderVo.getCount()); //扣减余额 Boolean debit= accountFeignService.debit(orderVo.getUserId(), orderVo.getMoney()); //更新订单 Integer updateOrderRecord = orderMapper.updateOrderStatus(order.getId(),OrderStatus.SUCCESS.getValue()); log.info("更新订单id:{} {}", order.getId(), updateOrderRecord > 0 ? "成功" : "失败"); return order; }

```

```

1

```
    @Override
```

2

```
    @GlobalTransactional(name="createOrder")
```

3

```
    public Order saveOrder(OrderVo orderVo) {
```

4

```
        log.info("=============用户下单=================");
```

5

```
        log.info("当前 XID: {}", RootContext.getXID());
```

6

```

```

7

```
        // 保存订单
```

8

```
        Order order = new Order();
```

9

```
        order.setUserId(orderVo.getUserId());
```

10

```
        order.setCommodityCode(orderVo.getCommodityCode());
```

11

```
        order.setCount(orderVo.getCount());
```

12

```
        order.setMoney(orderVo.getMoney());
```

13

```
        order.setStatus(OrderStatus.INIT.getValue());
```

14

```

```

15

```
        Integer saveOrderRecord = orderMapper.insert(order);
```

16

```
        log.info("保存订单{}", saveOrderRecord > 0 ? "成功" : "失败");
```

17

```

```

18

```
        //扣减库存
```

19

```
        storageFeignService.deduct(orderVo.getCommodityCode(), orderVo.getCount());
```

20

```
        //扣减余额
```

21

```
        Boolean debit= accountFeignService.debit(orderVo.getUserId(), orderVo.getMoney());
```

22

```

```

23

```
        //更新订单
```

24

```
        Integer updateOrderRecord =
```

25

```
            orderMapper.updateOrderStatus(order.getId(),OrderStatus.SUCCESS.getValue());
```

26

```
        log.info("更新订单id:{} {}", order.getId(), updateOrderRecord > 0 ? "成功" : "失败");
```

27

```

```

28

```
        return order;
```

29

```

```

30

```
    }
```

@Transactional @Override public void deduct(String commodityCode, int count){ log.info("=============扣减库存================="); log.info("当前 XID: {}", RootContext.getXID()); // 检查库存 checkStock(commodityCode,count); log.info("开始扣减 {} 库存", commodityCode); Integer record = storageMapper.reduceStorage(commodityCode,count); log.info("扣减 {} 库存结果:{}", commodityCode, record > 0 ? "操作成功" : "扣减库存失败"); }

```

```

1

```
@Transactional
```

2

```
@Override
```

3

```
public void deduct(String commodityCode, int count){
```

4

```
    log.info("=============扣减库存=================");
```

5

```
    log.info("当前 XID: {}", RootContext.getXID());
```

6

```
    // 检查库存
```

7

```
    checkStock(commodityCode,count);
```

8

```
    log.info("开始扣减 {} 库存", commodityCode);
```

9

```
    Integer record = storageMapper.reduceStorage(commodityCode,count);
```

10

```
    log.info("扣减 {} 库存结果:{}", commodityCode, record > 0 ? "操作成功" : "扣减库存失败");
```

11

```
}
```

@Transactional @Override public void debit(String userId, int money){ log.info("=============用户账户扣款================="); log.info("当前 XID: {}", RootContext.getXID()); checkBalance(userId, money); log.info("开始扣减用户 {} 余额", userId); Integer record = accountMapper.reduceBalance(userId,money); log.info("扣减用户 {} 余额结果:{}", userId, record > 0 ? "操作成功" : "扣减余额失败"); }

```

```

1

```
    @Transactional
```

2

```
    @Override
```

3

```
    public void debit(String userId, int money){
```

4

```
        log.info("=============用户账户扣款=================");
```

5

```
        log.info("当前 XID: {}", RootContext.getXID());
```

6

```
        checkBalance(userId, money);
```

7

```
        log.info("开始扣减用户 {} 余额", userId);
```

8

```
        Integer record = accountMapper.reduceBalance(userId,money);
```

9

```
        log.info("扣减用户 {} 余额结果:{}", userId, record > 0 ? "操作成功" : "扣减余额失败");
```

10

```
    }
```

从自己实现推导出 seata

自己实现

分布式微服务系统伪代码实现

修改下面的伪代码

public void createOrder(PaymentBill bill) { userTransaction.begin(); storageTransaction.begin(); orderTransaction.begin(); try { userAccountService.pay(bill); storageService.deliver(bill); orderTransaction.create(bill); userTransaction.commit(); storageTransaction.commit(); orderTransaction.commit(); } catch(Exception e) { userTransaction.rollback(); storageTransaction.rollback(); orderTransaction.rollback(); } }

20

1

```
public void createOrder(PaymentBill bill) {
```

2

```
    userTransaction.begin();
```

3

```
    storageTransaction.begin();
```

4

```
    orderTransaction.begin();
```

5

```

```

6

```
    try {
```

7

```
        userAccountService.pay(bill);
```

8

```
        storageService.deliver(bill);
```

9

```
        orderTransaction.create(bill);
```

10

```

```

11

```
        userTransaction.commit();
```

12

```
        storageTransaction.commit();
```

13

```
        orderTransaction.commit();
```

14

```
    } catch(Exception e) {
```

15

```
        userTransaction.rollback();
```

16

```
        storageTransaction.rollback();
```

17

```
        orderTransaction.rollback();
```

18

```
    }
```

19

```
}
```

20

```

```

public void createOrder(PaymentBill bill) { orderTransaction.begin(); try { userAccountFeginService.pay(bill.getMoney()); storageFeginService.deliver(bill.getItems()); orderTransaction.create(bill.getMoney(),bill.getItems()); orderTransaction.commit(); } catch(Exception e) { userAccountFeginService.rollbackPay(); storageFeginService.rollbackDeliver(); orderTransaction.rollback(); } }

13

1

```
public void createOrder(PaymentBill bill) {
```

2

```
     orderTransaction.begin();
```

3

```
    try {
```

4

```
        userAccountFeginService.pay(bill.getMoney());
```

5

```
        storageFeginService.deliver(bill.getItems());
```

6

```
        orderTransaction.create(bill.getMoney(),bill.getItems());
```

7

```
        orderTransaction.commit();
```

8

```
    } catch(Exception e) {
```

9

```
        userAccountFeginService.rollbackPay();
```

10

```
        storageFeginService.rollbackDeliver();
```

11

```
        orderTransaction.rollback();
```

12

```
    }
```

13

```
}
```

public void createOrder(PaymentBill bill) { try { userAccountFeginService.tryPay(bill); storageFeginService.trydeliver(bill); orderFeginService.tryCreate(bill); if(allSuccess){ userAccountFeginService.confirmPay(bill); storageFeginService.confirmdeliver(bill); orderFeginService.confirmCreate(bill); }else{ userAccountFeginService.rollbackPay(bill); storageFeginService.rollbackDeliver(bill); orderFeginService.rollbackCreate(bill); } } catch(Exception e) { userAccountFeginService.rollbackPay(bill); storageFeginService.rollbackDeliver(bill); orderFeginService.rollbackCreate(bill); } }

```
x
```

1

```
public void createOrder(PaymentBill bill) {
```

2

```
    try {
```

3

```
         userAccountFeginService.tryPay(bill);
```

4

```
         storageFeginService.trydeliver(bill);
```

5

```
         orderFeginService.tryCreate(bill);
```

6

```
        if(allSuccess){
```

7

```
            userAccountFeginService.confirmPay(bill);
```

8

```
            storageFeginService.confirmdeliver(bill);
```

9

```
            orderFeginService.confirmCreate(bill);
```

10

```
        }else{
```

11

```
            userAccountFeginService.rollbackPay(bill);
```

12

```
            storageFeginService.rollbackDeliver(bill);
```

13

```
            orderFeginService.rollbackCreate(bill);
```

14

```
        }
```

15

```
    } catch(Exception e) {
```

16

```
        userAccountFeginService.rollbackPay(bill);
```

17

```
        storageFeginService.rollbackDeliver(bill);
```

18

```
        orderFeginService.rollbackCreate(bill);
```

19

```
    }
```

20

```
}
```

public void createOrder(PaymentBill bill) { try { if(!userAccountFeginService.tryPay(bill)){ userAccountFeginService.rollbackPay(bill); } if(!storageFeginService.trydeliver(bill)){ userAccountFeginService.rollbackPay(bill); storageFeginService.rollbackDeliver(bill); } if(!orderFeginService.tryCreate(bill)){ userAccountFeginService.rollbackPay(bill); storageFeginService.rollbackDeliver(bill); orderFeginService.rollbackCreate(bill); } if(allSuccess){ userAccountFeginService.confirmPay(bill); storageFeginService.confirmdeliver(bill); orderFeginService.confirmCreate(bill); } } catch(Exception e) { userAccountFeginService.rollbackPay(bill); storageFeginService.rollbackDeliver(bill); orderFeginService.rollbackCreate(bill); } }

```
x
```

1

```
public void createOrder(PaymentBill bill) {
```

2

```
    try {
```

3

```

```

4

```
        if(!userAccountFeginService.tryPay(bill)){
```

5

```
            userAccountFeginService.rollbackPay(bill);
```

6

```
        }
```

7

```
        if(!storageFeginService.trydeliver(bill)){
```

8

```
            userAccountFeginService.rollbackPay(bill);
```

9

```
            storageFeginService.rollbackDeliver(bill);
```

10

```
        }
```

11

```
        if(!orderFeginService.tryCreate(bill)){
```

12

```
            userAccountFeginService.rollbackPay(bill);
```

13

```
            storageFeginService.rollbackDeliver(bill);
```

14

```
            orderFeginService.rollbackCreate(bill);
```

15

```
        }
```

16

```

```

17

```
        if(allSuccess){
```

18

```
            userAccountFeginService.confirmPay(bill);
```

19

```
            storageFeginService.confirmdeliver(bill);
```

20

```
            orderFeginService.confirmCreate(bill);
```

21

```
        }
```

22

```
    } catch(Exception e) {
```

23

```
        userAccountFeginService.rollbackPay(bill);
```

24

```
        storageFeginService.rollbackDeliver(bill);
```

25

```
        orderFeginService.rollbackCreate(bill);
```

26

```
    }
```

27

```
}
```

| 时间顺序 | 业务一 | 业务二 |  |  |
| --- | --- | --- | --- | --- |
|  | 开启全局事务 |  |  |  |
|  | 执行分支事务A<br>update tableA set status = 1<br>提交分支事务A |  |  |  |
|  |  | 开启本地事务<br>update tableA set status = 1<br>提交本地事务 |  |  |
|  |  |  |  |  |

| 时间顺序 | 业务一 | 业务二 | 数据状态 |
| --- | --- | --- | --- |
|  | 开启全局事务 |  | id=1<br>stock=10 |
|  | 执行分支事务A<br>update tableA set stock = stock -1<br>where id = 1<br>提交分支事务A |  | id=1<br>stock=9 |
|  |  | 开启本地事务<br>update tableA set stock = stock +10<br>where id = 1<br>提交本地事务 | id=1<br>stock=19 |
|  | 执行分支事务B异常<br>触发事务回滚 |  |  |
|  | 分支事务A回滚<br>after image 和 当前表数据 不一致<br>分支事务A回滚失败 |  |  |
|  | 全局事务回滚失败 |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

| 时间顺序 | 业务一 | 业务二 | 数据状态 |
| --- | --- | --- | --- |
|  | 开启全局事务 |  | id=1<br>stock=10 |
|  | 执行分支事务A<br>update tableA set stock = stock -1<br>where id = 1<br>提交分支事务A |  | id=1<br>stock=9 |
|  |  | 执行查询操作<br>select * from  tableA where id = 1<br>查询结果 stock = 9 | id=1<br>stock=9 |
|  | 执行分支事务B异常<br>触发事务回滚 |  |  |
|  | 分支事务A回滚 |  | id=1<br>stock=10 |
|  | 全局事务回滚 |  | id=1<br>stock=10 |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

resource_id，table_name，pk

============

TCC Demo 代码实现_Java_萧_InfoQ写作社区

https://xie.infoq.cn/article/e6539ce436294828b5c9420f9

TCC 分布式事务主要的三个阶段：

1.Try：主要是对业务系统做检测及资源预留

2.Confirm：确认执行业务操作

3.Cancel：取消执行业务操作

======

2023年3月24日 00:56:25

本地事务 隔离性的ppt

场景模拟要从头到尾么

在分布式事务如何产生  那边要不要加入伪代码

seata如何实现协调者的需求
