---
id: "2309403879"
title: "Java有哪些有趣的jar包？"
author: "四猿外"
type: zhihu-answer
source: "https://www.zhihu.com/question/312737005/answer/2309403879"
created: "2022-01-13 18:11"
updated: "2022-01-13 18:16"
collected: "2022-01-13 18:11"
downloaded: "2026-08-16"
---
从业十几年的Java程序员来回答一波。

Java 最重要的优点之一，就是它的生态，有其琳琅满目的各种工具类库。

我在工作中用过很多jar，这次给大家分享几个 jar。

有了它们之后，你就可以和很多重复劳动说再见了。

## 1\. MapStruct

![](images/444_001.jpg)

**MapStruct是干什么的？**

MapStruct是个代码产生器，它能直接根据注解生成 Java 对象对应的转换器。

比如，直接把一个 A 类型的 Java 对象，给转成 B 类型的 Java 对象，只需要在他们之间配置上字段之间的映射关系即可。

**为什么在项目里用它？**

现在随便一个项目都是多层的，尤其是 Web 项目，经常需要在多层之间做对象模型转换，比如 DTO 转换成 BO。

> DTO（Data Transfer Object）：数据传输对象，Service 向外传输的对象。  
> BO（Business Object）：业务对象，由 Service 层输出的封装业务逻辑的对象。

但是这种转换工作就像是小时候，老师罚我们抄写名人名言 100 遍一样，十分枯燥，还容易出错。

像这样：

```text
public class CarMapper {
    CarDto carDoToCarDto(Car car) {
        CarDto carDto = new CarDto();
        carDto.setCarId(car.getCarId());
        carDto.setWheel(car.getWheel());
        carDto.setCarType(car.getCarType());
        carDto.setCarColor(car.getCarColor());
        ......
    }

}
```

要是 Car 有几十个字段，像 Car 一样的又有几十个类，你可以想一下，这种繁琐程度。

在 MapStruct 之前，我们都是通过 Apache 或者 Spring 的 BeanUtils 工具，去自动做这种事情。

但是这类工具有两个问题：

1.性能比较差

性能差主要是 Apache 的 BeanUtils 这套东西，它每次都要针对字段，做是否可读写的检查，还要根据字段生成对应的 PropertyDescriptor。

这些严重影响了它的性能，所以，在阿里 Java 手册里，也不推荐用它。

Spring 的 BeanUtils，虽然精简了很多 Apache 的 BeanUtils 的读写检查以及对应的属性信息记录，但是它依然是通过反射调用，而且是大量反射调用。这种性能也不能令人满意。

2.运行期做转换，出错就代表损失

BeanUtils 这类工具，有个统一的名称，叫做 Java 对象映射框架。

它们大部分的实现都是在运行期去执行代码，然后在 Java 对象之间去拷贝对应的值。

运行期间做这种事儿，有个最大的问题——整个项目启动运行后，才能发现错误。比如，转换的时候，类型不一致导致报错。

对于此种情况，咱们大家都知道，这事儿就像开业酬宾没搞好，变成了开业仇宾……

如果能写完代码，编译的时候就发现问题，这种损失就可以避免了。

MapStruct 的引入就是为了解决以上这两个问题。

MapStruct 首先是个代码产生器，它是根据注解，去产生一个专门用来转换的工具类，这个工具类，就像我们自己写的 Java 类一样，可以直接被使用，这样就避免了反射。

同时，它产生的转换类也特别简单，就是默认会在两个类型的 Java 对象之间，拷贝同名属性的值。

如果有了配置，属性不同名也可以拷贝。所以它的性能很好。

示例代码如下：

```text
@Mapper
public interface CarMapper {

    CarMapper INSTANCE = Mappers.getMapper( CarMapper.class );

    @Mapping(target = "seatCount", source = "numberOfSeats")
    CarDto carBoToCarDto(Car car);
}
```

MapStruct由于是个代码产生器，就带来了个巨大的好处，就是这家伙是在编译阶段就会生成对应的类，所以，如果有了类似类型转换不过去的问题，直接就编译报错了，根本等不到运行才发现。这样的话，就不会造成什么损失，这真是件十分 Nice 的事情。

**代码库地址**

[https://github.com/mapstruct/mapstruct](https://link.zhihu.com/?target=https%3A//github.com/mapstruct/mapstruct)

**推荐一些我认为的比较经典的书籍**。

![](images/444_002.jpg)

以上书籍，我已经打包整理好了，免费下载的方式看下面链接

[少走弯路，计算机豆瓣高分书单​mp.weixin.qq.com/s?\_\_biz=MzU3MTg3NDYwNg==&mid=100002250&idx=1&sn=d362fb3a5b4a58e6d9eeeb0334823a14&chksm=7cd8c58b4baf4c9d39105a24461352c9309858c0380964f59323cca6b2f15c20c908c10a0de9#rd​mp.weixin.qq.com/s?\_\_biz=MzU3MTg3NDYwNg==&mid=100002250&idx=1&sn=d362fb3a5b4a58e6d9eeeb0334823a14&chksm=7cd8c58b4baf4c9d39105a24461352c9309858c0380964f59323cca6b2f15c20c908c10a0de9#rd​mp.weixin.qq.com/s?\_\_biz=MzU3MTg3NDYwNg==&mid=100002250&idx=1&sn=d362fb3a5b4a58e6d9eeeb0334823a14&chksm=7cd8c58b4baf4c9d39105a24461352c9309858c0380964f59323cca6b2f15c20c908c10a0de9#rd](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzU3MTg3NDYwNg%3D%3D%26mid%3D100002250%26idx%3D1%26sn%3Dd362fb3a5b4a58e6d9eeeb0334823a14%26chksm%3D7cd8c58b4baf4c9d39105a24461352c9309858c0380964f59323cca6b2f15c20c908c10a0de9%23rd)

## 2\. Retrofit

![](images/444_003.jpg)

**Retrofit 是干什么的？**

Retrofit 就是一套 Http [客户端](https://www.zhihu.com/search?q=%E5%AE%A2%E6%88%B7%E7%AB%AF&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22answer%22%2C%22sourceId%22%3A2160698998%7D)，可以用来访问第三方的 Http 服务。

比如，咱们代码里想调用一个 Http 协议的 URL，就可以用它来访问这个 URL，获取响应结果。

**为什么在项目里用它？**

在公司里，我们有些项目有如下的特点： 1. 不是基于 Spring 的项目 2. 需要经常访问大量的第三方 Http 服务 3. 访问 Http 服务的模型通常是异步回调

以前的时候，我们访问 Http 服务，都是直接用的 HttpClient。

可是吧，HttpClient 用起来实在够麻烦的。主要也存在两个问题：

1.请求参数和 URL 拼接实在繁琐

请求参数和 URL 拼接实在是太烦人了。你想想，每调用一个接口，就需要自己去拼接参数，有的 URL，甚至十几二十个参数需要拼接。

拼接这事儿简单、枯燥、重复，还没有技术含量，但是工作量却不小，时间真的算浪费了。

```text
URIBuilder uriBuilder = new URIBuilder(uriBase);
uriBuilder.setParameter("a", "valuea");
uriBuilder.setParameter("b", "valueb");
uriBuilder.setParameter("c", "valuec");
uriBuilder.setParameter("d", "valued");
uriBuilder.setParameter("e", "valuee");
uriBuilder.setParameter("f", "valuef");
uriBuilder.setParameter("g", "valueg");
uriBuilder.setParameter("h", "valueh");
uriBuilder.setParameter("i", "valuei");
...
```

2.异步回调需要自己搞

异步回调这种模型不好处理，主要就是需要自己去搞线程池，还要对线程池管理，还要考虑出错的重试之类的容错问题，实在麻烦。

所以，我们就需要一套能用法简单，不用我们一直搞拼接参数，自己搞线程管理就能完成对第三方 Http 服务访问的库。

其实我们也想过用 Feign 这套框架的。但是，这套东西和 Spring 绑定的太紧了。如果离开 Spring，它的一些功能就没法简单的通过注解直接使用，必须自己写代码调用。

而且，Feign 要实现异步回调方式使用，尤其在协程方面，还是需要自己开发。

这时候，Retrofit 就跳进了我们的选型里。

Retrofit 的模型里，异步回调模型它支持的很好，我们只需要实现一个 Callable 就够了。

并且最清爽的是，它和 Spring 没什么关系。

```text
Retrofit retrofit = new Retrofit.Builder()
        .baseUrl("http://xxx.example.com/")
        .build();

public interface BlogService {
    @GET("blog/{id}")
    Call<ResponseBody> getBlog(@Path("id") int id);
}

BlogService service = retrofit.create(BlogService.class);

Call<ResponseBody> call = service.getBlog(2);
// 用法和OkHttp的call如出一辙,
// 回调
call.enqueue(new Callback<ResponseBody>() {
    @Override
    public void onResponse(Call<ResponseBody> call, Response<ResponseBody> response) {
        try {
            System.out.println(response.body().string());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void onFailure(Call<ResponseBody> call, Throwable t) {
        t.printStackTrace();
    }
});
```

你看，只需要写上这些代码，我们就不需要操心恼人的 Url 拼接和异步回调的管理问题了。全交给了 Retrofit，着实推荐。

**代码库地址**

[https://github.com/square/retrofit](https://link.zhihu.com/?target=https%3A//github.com/square/retrofit)

## 3\. Wiremock

![](images/444_004.jpg)

**Wiremock 是干什么的？**

Wiremock 是一个可以模拟服务的测试框架。

比如，你想测试访问阿里的支付相关接口的代码逻辑，就可以用它来做测试。

**为什么在项目里用它？**

比如，我们需要调用银行接口去做资金业务，调用微信接口去做微信登录……这些调用第三方服务的测试存在一个问题：

即太过依赖对方的平台。假如对方平台限制了一些 IP，或者限制了访问频率，又或者就是服务出现了维护，都会影响我们自身的功能测试。

为了解决上述问题，在之前，我们需要自己写代码模仿第三方的接口，等我们自己全部测试没问题了，再去和第三方联调。对于这种模拟出来的接口，我们称作挡板。

可是，这种方式是个苦活，没人愿意干。因为每接入一个第三方，可能都需要做挡板。辛苦做个挡板，就是单纯为了测试。如果第三方的接口做了改造，你这边还得跟着改。

大家可以想想，换成你自己，你愿意做这么件事儿吗？

这时候，Wiremock 的价值就体现出来了。有了 Wiremock，挡板这种东西就再也不存在了，直接在[单元测试](https://www.zhihu.com/search?q=%E5%8D%95%E5%85%83%E6%B5%8B%E8%AF%95&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22answer%22%2C%22sourceId%22%3A2160698998%7D)里模拟测试即可，像这样：

```text
WireMock.stubFor(get(urlPathMatching("/aliyun/.*"))
                .willReturn(aResponse()
                        .withStatus(200)
                        .withHeader("Content-Type", APPLICATION_JSON)
                        .withBody("\"testing-library\": \"WireMock\"")));

CloseableHttpClient httpClient = HttpClients.createDefault();
HttpGet request = new HttpGet(String.format("http://localhost:%s/aliyun/wiremock", port));
HttpResponse httpResponse = httpClient.execute(request);
String stringResponse = convertHttpResponseToString(httpResponse);

verify(getRequestedFor(urlEqualTo(ALIYUN_WIREMOCK_PATH)));
assertEquals(200, httpResponse.getStatusLine().getStatusCode());
assertEquals(APPLICATION_JSON, httpResponse.getFirstHeader("Content-Type").getValue());
assertEquals("\"testing-library\": \"WireMock\"", stringResponse);
```

**代码库地址**

[https://github.com/wiremock/wiremock](https://link.zhihu.com/?target=https%3A//github.com/wiremock/wiremock)

  

Java 最重要的优点之一，就是它的生态，有其琳琅满目的各种工具类库。

希望大家都“懒”一点，不要埋头去做无效的苦干，不要自己造轮子，你要相信：

**你遇到的问题，基本已经有很多人遇到过了，而且已经被牛人给解决了，把轮子都给你造好了。**

除了以上内容，我还写了很多程序员相关的学习技巧、架构经验、职场生存法则类的优质文章，总结成了一份电子书，我相信你看完之后，对你一定会对你有帮助。想获取电子书可以戳下面链接。

[百万收入程序员的成长之路​mp.weixin.qq.com/s/\_EoZ8Bolt7feU9NPdMHhWA](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s/_EoZ8Bolt7feU9NPdMHhWA)