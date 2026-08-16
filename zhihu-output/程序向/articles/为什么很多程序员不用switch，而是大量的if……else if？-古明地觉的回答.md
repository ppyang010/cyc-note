---
id: "2035922184"
title: "为什么很多程序员不用switch，而是大量的if……else if？"
author: "古明地觉"
type: zhihu-answer
source: "https://www.zhihu.com/question/475877331/answer/2035922184"
created: "2021-08-03 10:22"
updated: "2021-08-04 19:38"
collected: "2021-08-03 10:22"
downloaded: "2026-08-16"
---
不会吧还有人用if else和switch case？三目运算符？

不会吧？ 不会吧？大佬都是全都不用的！以JAVA为例

条件判断语句的四种写法，茴字的四种写法大家不会不知道吧

**1.正常人写法：**

```text
    private static String MAN = "man";
    private static String WOMAN = "woman";
    @Data
    static class Person{
        private String gender;
        private String name;
    }  
    public static void main(String[] args) {
        Person p = new Person();
        p.setGender(MAN);
        p.setName("张三");

        if(Objects.equals(p.getGender(),MAN)){
            System.out.println(p.getName() + "应该去男厕所");
        }

        if(Objects.equals(p.getGender(),WOMAN)){
            System.out.println(p.getName() + "应该去女厕所");
        }

    }
//输出 ：张三应该去男厕所
```

**2.Lambda策略模式写法：**

某些大公司P6级别以上（年薪30w-50w）标准写法，写if else是要被骂的

```text
    private static Map<String, Consumer<String>> FUNC_MAP = new ConcurrentHashMap<>();
    private static String MAN = "man";
    private static String WOMAN = "woman";
    static {
        FUNC_MAP.put(MAN,person ->{System.out.println(person + "应该去男厕所");});
        FUNC_MAP.put(WOMAN,person ->{System.out.println(person + "应该去女厕所");});
    }
    @Data
    static class Person{
        private String gender;
        private String name;
    }
    public static void main(String[] args) {
        Person p = new Person();
        p.setGender(MAN);
        p.setName("张三");
        Person p2 = new Person();
        p2.setGender(WOMAN);
        p2.setName("张三他老婆");

        FUNC_MAP.get(p.getGender()).accept(p.name);
        FUNC_MAP.get(p2.getGender()).accept(p2.name);

    }


//输出：
//张三应该去男厕所
//张三他老婆应该去女厕所
```

**3.DDD领域驱动设计思想+策略模式写法：**

某些大公司P7级别以上（年薪40w-70w）标准写法（笑）

```text
    private static String MAN = "man";
    private static String WOMAN = "woman";
    @Data
    static class Person{
        private String gender;
        private String name;

        private static Map<String, Consumer<String>> FUNC_MAP = new ConcurrentHashMap<>();
        static {
            FUNC_MAP.put(MAN,person ->{System.out.println(person + "应该去男厕所");});
            FUNC_MAP.put(WOMAN,person ->{System.out.println(person + "应该去女厕所");});
        }
        public void goToWC(){
            FUNC_MAP.get(gender).accept(name);
        }
    }

    static class PersonFactory{
        public static Person initPerson(String name ,String gender){
            Person p = new Person();
            p.setName(name);
            p.setGender(gender);
            return p;
        }
    }
    public static void main(String[] args) {
        Person p = PersonFactory.initPerson("张三",MAN);
        Person p2 = PersonFactory.initPerson("张三他老婆",WOMAN);
        p.goToWC();
        p2.goToWC();
    }


//输出：
//张三应该去男厕所
//张三他老婆应该去女厕所
```

某些奇葩公司就是喜欢这种语法，看起来够装逼，实际上效率并没有高多少，可读性差了很多，而且Debug比较麻烦

**4.Actor模型+领域驱动设计+策略模式+事件响应式架构**

真正的P8年薪百万架构师级写法，逼王才这么写代码，装逼的极限，内卷的奥义

Maven依赖：

依赖Akka框架 Actor模型，懂得都懂，大数据分布式计算Spark框架RDD依赖的框架，很复杂，源码是Scala语言，逼王必学。也可以Scala做架构，Java做上层，有兴趣可以了解一下，反正管他是什么，够牛逼就完了。哎，就是得有牌面。if else什么的太low，应届毕业生水平才写if else（魔怔领导原话）。

```text
       <dependency>
            <groupId>com.typesafe.akka</groupId>
            <artifactId>akka-actor_2.12</artifactId>
            <version>2.5.2</version>
        </dependency>
```

代码

```text
    private static String MAN = "man";
    private static String WOMAN = "woman";
    private static String WC_EVENT= "想上厕所";
    @Data
    static class Person extends UntypedActor {
        private String gender;
        private String name;

        public static Props props(final String name,final String gender) {
            return Props.create(new Creator<Person>() {
                private static final long serialVersionUID = 1L;
                @Override
                public Person create() throws Exception {
                    Person p = new Person();
                    p.setGender(gender);
                    p.setName(name);
                    return p;
                }
            });
        }
        @Override
        public void onReceive(Object message) throws Throwable {
            Pair<String,ActorRef> m = (Pair<String,ActorRef>)message;
            System.out.println(name + m.getLeft());
            m.getRight().tell(this, ActorRef.noSender());

        }
    }

    @Data
    static class Toilet extends UntypedActor {
        private static Map<String, Consumer<String>> FUNC_MAP = new ConcurrentHashMap<>();
        static {
            FUNC_MAP.put(MAN,person ->{System.out.println(person + "应该去男厕所");});
            FUNC_MAP.put(WOMAN,person ->{System.out.println(person + "应该去女厕所");});
        }

        public void wc(Person p ){
            FUNC_MAP.get(p.getGender()).accept(p.getName());
        }

        public static Props props() {
            return Props.create(Toilet.class);
        }

        @Override
        public void onReceive(Object message) throws Throwable {
            Person p = (Person) message;
            wc(p);
        }
    }

    public static void main(String[] args) {
        ActorSystem actorSystem = ActorSystem.create();
        ActorRef person = actorSystem.actorOf(Person.props("张三",MAN), "ZhangSan");
        ActorRef toilet = actorSystem.actorOf(Toilet.props(), "Toilet");
        Pair<String,ActorRef> message = Pair.of(WC_EVENT,toilet);
        person.tell(message,ActorRef.noSender());
    }
//输出
//张三想上厕所
//张三应该去男厕所
```

**5.Actor模型+领域驱动设计+策略模式+事件响应式架构+动态类模板构建+运行时编译**

为什么要写if else？为什么要创建类？为什么要写方法？真正的大佬（神经病）根本不需要写if else，也不需要创建class，甚至不需要命名方法。我上厕所就要写Toilet 类，开车就要写Car类，还得继承Actor的抽象类，太low，真正的Java不需要类型，不需要类，不需要if else，不需要命名方法，什么都不需要，便是Java的极致。我悟了。

Maven依赖：

咱还得整新活，javassist动态类加载，框架级代码才会用，运行时调编译器搞起，类型什么的根本不需要，咱就是要颠覆Java的根基，什么class，小孩才写class ，大人都是玩编译器。

```text
       <dependency>
            <groupId>com.typesafe.akka</groupId>
            <artifactId>akka-actor_2.12</artifactId>
            <version>2.5.2</version>
        </dependency>

        <dependency>
            <groupId>org.javassist</groupId>
            <artifactId>javassist</artifactId>
            <version>3.25.0-GA</version>
        </dependency>
```

代码：

```text
import akka.actor.ActorRef;
import akka.actor.ActorSystem;
import akka.actor.Props;
import akka.actor.UntypedActor;
import akka.japi.Creator;
import javassist.*;
import org.apache.commons.lang3.tuple.Pair;

import java.util.HashMap;
import java.util.Map;
import java.util.function.BiConsumer;
import java.util.function.Consumer;

public class DynamicActorTest {

    private static String MAN = "man";
    private static String WOMAN = "woman";
    private static String WC_EVENT= "想上厕所";
    private static String WC_OVER_EVENT = "上完厕所了";
    
    private static ActorSystem actorSystem = ActorSystem.create();

    /**
     * 创建一个动态类，并实例化为对象，该方法会根据参数动态构建Class
     * @param name 动态类名
     * @param function actor模型消息处理方法 两个参数 一个是自身，一个是消息
     * @param attrAndValues 动态类的 属性 和 属性值
     * @return actor引用
     * @throws Exception
     */
    public static ActorRef createDynamicClassImpl(String name, BiConsumer function, Pair<String, String>... attrAndValues) throws Exception {
        ClassPool pool = ClassPool.getDefault();
        // 动态定义包名 瞎几把写就行
        String className = "com.xxx.xxx.xxx." + name;
        // 创建一个空类
        CtClass cc = pool.makeClass(className);
        // 动态继承抽象类UntypedActor
        cc.setSuperclass(pool.get(UntypedActor.class.getName()));
        // 动态根据参数创建类的属性
        for (Pair<String, String> attrValue : attrAndValues) {
            CtField param = new CtField(pool.get(String.class.getName()), attrValue.getLeft(), cc);
            // 访问级别是 PUBLIC
            param.setModifiers(Modifier.PUBLIC);
            cc.addField(param, CtField.Initializer.constant(attrValue.getRight()));
        }

        //创建类一个属性叫function 类型是BiConsumer
        CtField param = new CtField(pool.get(BiConsumer.class.getName()), "function", cc);
        //访问级别是 PRIVATE
        param.setModifiers(Modifier.PRIVATE);
        cc.addField(param);
        //创建模板方法 方法是执行BiConsumer对应的lambda表达式
        CtMethod m = CtNewMethod.make(
                "public void onReceive(Object message) { function.accept($0 ,message);}",
                cc);
        cc.addMethod(m);
        // 动态添加构造函数
        CtConstructor cons = new CtConstructor(new CtClass[]{pool.get(BiConsumer.class.getName())}, cc);
        // 构造函数内容就是给function参数赋值
        cons.setBody("{ $0.function = $1 ;}");
        cc.addConstructor(cons);
        //-----------动态Actor类构建完毕------------
        // 实例化Actor
        Props p = Props.create(new Creator<UntypedActor>() {
            @Override
            public UntypedActor create() throws Exception {
                //反射创建对象
                return (UntypedActor)cc.toClass().getConstructor(BiConsumer.class).newInstance(function);
            }
        });
        return actorSystem.actorOf(p);
    }


    public static void main(String[] args) throws Exception {
        // class什么的根本不需要，直接动态创建类，对于复杂场景可以搞分布式remoteActor
        // 创建一个Car类(领域对象），并实例化，定义他的消息处理方法(或者你乐意叫领域驱动事件也可以)
        ActorRef car = createDynamicClassImpl("Car",(self, message)->{
            System.out.println(message);
            System.out.println("开车走咯~");
        });

        // 创建一个Toilet类，并实例化，定义他的消息处理方法(或者你乐意叫领域驱动事件也可以)
        ActorRef toilet = createDynamicClassImpl("Toilet", (self, message) ->{
            try {
                Map<String, Consumer<String>> FUNC_MAP = new HashMap<>();
                FUNC_MAP.put(MAN,person ->{System.out.println(person + "应该去男厕所");});
                FUNC_MAP.put(WOMAN,person ->{System.out.println(person + "应该去女厕所");});
                // 因为是无类型取值使用反射
                String gender = message.getClass().getField("gender").get(message).toString();
                String name = message.getClass().getField("name").get(message).toString();
                FUNC_MAP.get(gender).accept(name);
                car.tell(name+WC_OVER_EVENT,ActorRef.noSender());
            } catch (Exception e) {
                System.out.println("厕所不太欢迎这位");
            }

        });

        // 创建一个Person类，具有两个属性name和gender，并实例化，定义他的消息处理方法(或者你乐意叫领域驱动事件也可以)
        ActorRef person = createDynamicClassImpl("Person", (self, message) -> {
            Pair<String,ActorRef> pair = (Pair<String,ActorRef>) message;
            System.out.println(pair.getLeft());
            pair.getRight().tell(self,ActorRef.noSender());
        }, Pair.of("name", "张三"), Pair.of("gender", MAN));
        // 告诉张三想上厕所了 让他找厕所去
        person.tell(Pair.of(WC_EVENT,toilet), ActorRef.noSender());
    }
}
//输出:
//想上厕所
//张三应该去男厕所
//张三上完厕所了
//开车走咯~
```

这样写代码，基本会被开除，你已经无敌了 公司已经容不下你了。

总结，代码还是正常写就得了，能实现业务不出bug好维护的就是好代码，切勿为了装逼使用各种奇技淫巧，if else没啥不好的。