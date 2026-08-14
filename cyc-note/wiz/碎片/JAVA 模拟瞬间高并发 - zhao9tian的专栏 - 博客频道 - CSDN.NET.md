---
Title: "JAVA 模拟瞬间高并发 - zhao9tian的专栏 - 博客频道 - CSDN.NET"
Url: "http://blog.csdn.net/zhao9tian/article/details/40346899"
Author: ""
Origin: "WizNote"
Description: ""
Tags:
  - "0碎"
Created: "2017-07-05 15:10:06"
Cover: ""
WizGuid: "7b2737d6-f4cd-4015-bf2d-6b1e67aaf6f3"
WizType: ""
WizLocation: "/碎片/"
WizDataMd5: "b782f56899bdc8c1e5e13d25e985d804"
Modified: "2017-07-05 15:10:06"
WizSyncedAt: "2026-08-14 22:20:57"
---

前些日子接到了一个面试电话，面试内容我印象很深，如何模拟一个并发？当时我的回答虽然也可以算是正确的，但自己感觉缺乏实际可以操作的细节，只有一个大概的描述。

当时我的回答是：“线程全部在同一节点wait，然后在某个节点notifyAll。”

面试官：“那你听说过惊群效应吗？”

我：“我没有听过这个名词，但我知道瞬间唤醒所有的线程，会让CPU负载瞬间加大。”

面试官：“那你有什么改进的方式吗？”

我：“采用阻塞技术，在某个节点将所有的线程阻塞，在利用条件，线程的个数达到一定数量的时候，打开阻塞。”

面试官好像是比较满意，结束了这个话题。

面试结束后，我回头这个块进行了思考，要如何进行阻塞呢？我首先有一个思路就是，利用AtoInteger计算线程数，再利用synchronize方法块阻塞一个线程，根据AtoInteger的判断，执行sleep。

代码如下：

**[java]** [view plain](#) [copy](#) [print](#)[?](#)

1. /**
2. * Created with IntelliJ IDEA.
3. * User: 菜鸟大明
4. * Date: 14-10-21
5. * Time: 下午4:34
6. * To change this template use File | Settings | File Templates.
7. */
8. **public** **class** CountDownLatchTest1 **implements** Runnable{
9. **final** AtomicInteger number = **new** AtomicInteger();
10. **volatile** **boolean** bol = **false**;
11.
12. @Override
13. **public** **void** run() {
14. System.out.println(number.getAndIncrement());
15. **synchronized** (**this**) {
16. **try** {
17. **if** (!bol) {
18. System.out.println(bol);
19. bol = **true**;
20. Thread.sleep(10000);
21. }
22. } **catch** (InterruptedException e) {
23. e.printStackTrace();
24. }
25. System.out.println("并发数量为" + number.intValue());
26. }
27.
28. }
29.
30. **public** **static** **void** main(String[] args) {
31. ExecutorService pool = Executors. newCachedThreadPool();
32. CountDownLatchTest1 test = **new** CountDownLatchTest1();
33. **for** (**int** i=0;i<10;i++) {
34. pool.execute(test);
35. }
36. }
37. }

```
/**
 * Created with IntelliJ IDEA.
 * User: 菜鸟大明
 * Date: 14-10-21
 * Time: 下午4:34
 * To change this template use File | Settings | File Templates.
 */
public class CountDownLatchTest1 implements Runnable{
    final AtomicInteger number = new AtomicInteger();
    volatile boolean bol = false;

    @Override
    public void run() {
        System.out.println(number.getAndIncrement());
        synchronized (this) {
            try {
                if (!bol) {
                    System.out.println(bol);
                    bol = true;
                    Thread.sleep(10000);
                }
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.println("并发数量为" + number.intValue());
        }

    }

    public static void main(String[] args) {
        ExecutorService pool = Executors. newCachedThreadPool();
        CountDownLatchTest1 test = new CountDownLatchTest1();
        for (int i=0;i<10;i++) {
            pool.execute(test);
        }
    }
}
```

结果为：

**[java]** [view plain](#) [copy](#) [print](#)[?](#)

1. 0
2. 2
3. 1
4. 4
5. 3
6. **false**
7. 5
8. 6
9. 7
10. 8
11. 9
12. 并发数量为10
13. 并发数量为10
14. 并发数量为10
15. 并发数量为10
16. 并发数量为10
17. 并发数量为10
18. 并发数量为10
19. 并发数量为10
20. 并发数量为10
21. 并发数量为10

```
0
2
1
4
3
false
5
6
7
8
9
并发数量为10
并发数量为10
并发数量为10
并发数量为10
并发数量为10
并发数量为10
并发数量为10
并发数量为10
并发数量为10
并发数量为10
```

从结果上来看，应该是可以解决问题，利用了同步锁，volatile解决了同时释放的问题，难点就在于开关。

后来查找资料，找到了一个CountDownLatch的类，专门干这个的

CountDownLatch是一个同步辅助类，犹如倒计时计数器，创建对象时通过构造方法设置初始值，调用CountDownLatch对象的await()方法则处于等待状态，调用countDown()方法就将计数器减1，当计数到达0时，则所有等待者或单个等待者开始执行。

构造方法参数指定了计数的次数

**[java]** [view plain](#) [copy](#) [print](#)[?](#)

1. **new** CountDownLatch(1)

```
new CountDownLatch(1)
```

countDown方法，当前线程调用此方法，则计数减一

**[java]** [view plain](#) [copy](#) [print](#)[?](#)

1. cdAnswer.countDown();

```
cdAnswer.countDown();
```

awaint方法，调用此方法会一直阻塞当前线程，直到计时器的值为0

**[java]** [view plain](#) [copy](#) [print](#)[?](#)

1. cdOrder.await();

```
cdOrder.await();
```

直接贴代码，转载的代码

**[java]** [view plain](#) [copy](#) [print](#)[?](#)

1. /**
2. *
3. * @author Administrator
4. *该程序用来模拟发送命令与执行命令，主线程代表指挥官，新建3个线程代表战士，战士一直等待着指挥官下达命令，
5. *若指挥官没有下达命令，则战士们都必须等待。一旦命令下达，战士们都去执行自己的任务，指挥官处于等待状态，战士们任务执行完毕则报告给
6. *指挥官，指挥官则结束等待。
7. */
8. **public** **class** CountdownLatchTest {
9.
10. **public** **static** **void** main(String[] args) {
11. ExecutorService service = Executors.newCachedThreadPool(); //创建一个线程池
12. **final** CountDownLatch cdOrder = **new** CountDownLatch(1);//指挥官的命令，设置为1，指挥官一下达命令，则cutDown,变为0，战士们执行任务
13. **final** CountDownLatch cdAnswer = **new** CountDownLatch(3);//因为有三个战士，所以初始值为3，每一个战士执行任务完毕则cutDown一次，当三个都执行完毕，变为0，则指挥官停止等待。
14. **for**(**int** i=0;i<3;i++){
15. Runnable runnable = **new** Runnable(){
16. **public** **void** run(){
17. **try** {
18. System.out.println("线程" + Thread.currentThread().getName() +
19. "正准备接受命令");
20. cdOrder.await(); //战士们都处于等待命令状态
21. System.out.println("线程" + Thread.currentThread().getName() +
22. "已接受命令");
23. Thread.sleep((**long**)(Math.random()*10000));
24. System.out.println("线程" + Thread.currentThread().getName() +
25. "回应命令处理结果");
26.
27. } **catch** (Exception e) {
28. e.printStackTrace();
29. } **finally** {
30. cdAnswer.countDown(); //任务执行完毕，返回给指挥官，cdAnswer减1。
31. }
32. }
33. };
34. service.execute(runnable);//为线程池添加任务
35. }
36. **try** {
37. Thread.sleep((**long**)(Math.random()*10000));
38.
39. System.out.println("线程" + Thread.currentThread().getName() +
40. "即将发布命令");
41. cdOrder.countDown(); //发送命令，cdOrder减1，处于等待的战士们停止等待转去执行任务。
42. System.out.println("线程" + Thread.currentThread().getName() +
43. "已发送命令，正在等待结果");
44. cdAnswer.await(); //命令发送后指挥官处于等待状态，一旦cdAnswer为0时停止等待继续往下执行
45. System.out.println("线程" + Thread.currentThread().getName() +
46. "已收到所有响应结果");
47. } **catch** (Exception e) {
48. e.printStackTrace();
49. } **finally** {
50.
51. }
52. service.shutdown(); //任务结束，停止线程池的所有线程
53. }
54. }

```
/**
 *
 * @author Administrator
 *该程序用来模拟发送命令与执行命令，主线程代表指挥官，新建3个线程代表战士，战士一直等待着指挥官下达命令，
 *若指挥官没有下达命令，则战士们都必须等待。一旦命令下达，战士们都去执行自己的任务，指挥官处于等待状态，战士们任务执行完毕则报告给
 *指挥官，指挥官则结束等待。
 */
public class CountdownLatchTest {

    public static void main(String[] args) {
        ExecutorService service = Executors.newCachedThreadPool(); //创建一个线程池
        final CountDownLatch cdOrder = new CountDownLatch(1);//指挥官的命令，设置为1，指挥官一下达命令，则cutDown,变为0，战士们执行任务
        final CountDownLatch cdAnswer = new CountDownLatch(3);//因为有三个战士，所以初始值为3，每一个战士执行任务完毕则cutDown一次，当三个都执行完毕，变为0，则指挥官停止等待。
        for(int i=0;i<3;i++){
            Runnable runnable = new Runnable(){
                public void run(){
                    try {
                        System.out.println("线程" + Thread.currentThread().getName() +
                                "正准备接受命令");
                        cdOrder.await(); //战士们都处于等待命令状态
                        System.out.println("线程" + Thread.currentThread().getName() +
                                "已接受命令");
                        Thread.sleep((long)(Math.random()*10000));
                        System.out.println("线程" + Thread.currentThread().getName() +
                                "回应命令处理结果");

                    } catch (Exception e) {
                        e.printStackTrace();
                    } finally {
                        cdAnswer.countDown(); //任务执行完毕，返回给指挥官，cdAnswer减1。
                    }
                }
            };
            service.execute(runnable);//为线程池添加任务
        }
        try {
            Thread.sleep((long)(Math.random()*10000));

            System.out.println("线程" + Thread.currentThread().getName() +
                    "即将发布命令");
            cdOrder.countDown(); //发送命令，cdOrder减1，处于等待的战士们停止等待转去执行任务。
            System.out.println("线程" + Thread.currentThread().getName() +
                    "已发送命令，正在等待结果");
            cdAnswer.await(); //命令发送后指挥官处于等待状态，一旦cdAnswer为0时停止等待继续往下执行
            System.out.println("线程" + Thread.currentThread().getName() +
                    "已收到所有响应结果");
        } catch (Exception e) {
            e.printStackTrace();
        } finally {

        }
        service.shutdown(); //任务结束，停止线程池的所有线程
    }
}
```

执行结果：

**[java]** [view plain](#) [copy](#) [print](#)[?](#)

1. 线程pool-1-thread-2正准备接受命令
2. 线程pool-1-thread-3正准备接受命令
3. 线程pool-1-thread-1正准备接受命令
4. 线程main即将发布命令
5. 线程pool-1-thread-2已接受命令
6. 线程pool-1-thread-3已接受命令
7. 线程pool-1-thread-1已接受命令
8. 线程main已发送命令，正在等待结果
9. 线程pool-1-thread-2回应命令处理结果
10. 线程pool-1-thread-1回应命令处理结果
11. 线程pool-1-thread-3回应命令处理结果
12. 线程main已收到所有响应结果

```
线程pool-1-thread-2正准备接受命令
线程pool-1-thread-3正准备接受命令
线程pool-1-thread-1正准备接受命令
线程main即将发布命令
线程pool-1-thread-2已接受命令
线程pool-1-thread-3已接受命令
线程pool-1-thread-1已接受命令
线程main已发送命令，正在等待结果
线程pool-1-thread-2回应命令处理结果
线程pool-1-thread-1回应命令处理结果
线程pool-1-thread-3回应命令处理结果
线程main已收到所有响应结果
```

上述也是一种实现方式，用countDownLatch的await()方法，代替了synchronize 和 sleep的阻塞功能，通过countDown的方法来当做开关，和计算线程数量的一种方式。

区别的话，肯定是后者会好一些，因为第一种方式依靠sleep(xxx)来阻塞把握不好最短时间，太短了，可能来没有达到固定线程数就会打开开关。

至于两者性能上的区别，目前我还不得而知，有机会[测试](http://lib.csdn.net/base/softwaretest)一下。
