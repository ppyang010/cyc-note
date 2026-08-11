[Rust + DDD 三层架构：没有 Spring、没有 DI 容器，解耦能力一点不少DDD 分层架构在 Java 里有 - 掘金](https://juejin.cn/post/7637630256103981062?utm_source=gold_browser_extension) 

 一、缘起：为什么 Rust 后端更需要分层
---------------------

大家好，我是 Pico-CRM 的作者。

在做这个家政 CRM 项目的过程中，我发现一个现象：很多 Rust 后端项目要么不分层（一个 `main.rs` 打到尾），要么过度分层（把 Java 那套照搬过来，目录深到可怕）。

我的项目从一开始就定了三层：`domain`、`application`、`infrastructure`。到现在跑了几个月，改过数据库实现、换过文件存储后端、加了 N 个新功能——最让我意外的是，**没有一次改动需要修改 domain 层**。

> 提前声明：本文分享的是个人在单项目 MVP 阶段的实践，不构成架构标准。分层方案跟团队规模、项目复杂度强相关。

二、三层架构总览
--------

先看目录结构：

```bash
backend/src/
├── domain/                    
│   ├── crm/contact/           
│   ├── identity/auth/         
│   └── shared/file/           
├── application/               
│   ├── commands/crm/          
│   ├── queries/crm/           
│   └── mappers/               
└── infrastructure/            
    ├── repositories/          
    ├── queries/               
    ├── auth/                  
    └── gateways/              

```

依赖方向是**严格的单向**：

```null
domain ← application ← infrastructure

```

翻译成人话：

*   **domain** 不知道谁实现了它——只定义 trait，不引入任何框架
*   **application** 不知道 infrastructure 的存在——只依赖 domain trait
*   **infrastructure** 负责把 domain trait 用具体技术（SeaORM、S3、JWT）实现出来

没有循环引用，没有"infrastructure 突然被 domain import"的诡异情况。

三、Domain 层：trait 就是你的契约
-----------------------

Domain 层的 Cargo.toml 里没有 `sea-orm`，没有 `axum`，没有 `jsonwebtoken`。只有纯 Rust。

### 3.1 实体就是普通 struct

`Contact` 实体长这样——就是普通的 Rust struct，带行为方法：

```rust


#[derive(Debug, Clone)]
pub struct Contact {
    pub uuid: String,
    pub name: String,
    pub phone: String,
    pub address: Option<String>,
    pub tags: Vec<String>,
    pub follow_up_status: FollowUpStatus,
    pub inserted_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

impl Contact {
    pub fn verify(&self) -> Result<(), String> {
        if self.name.trim().is_empty() {
            return Err("姓名不能为空".to_string());
        }
        if self.phone.trim().is_empty() {
            return Err("电话不能为空".to_string());
        }
        Ok(())
    }
}

```

业务校验就放在实体自身的方法里，调用方不需要知道校验细节。

### 3.2 仓储用 trait 定义，不关心实现

举个例子，`ContactRepository` trait 只定义"能做什么"，不管你用 SeaORM、Diesel 还是内存 HashMap：

```rust


pub trait ContactRepository: Send + Sync {
    fn create_contact(
        &self, contact: Contact, creator_uuid: String,
    ) -> impl Future<Output = Result<Contact, String>> + Send;

    fn find_contact_by_phone_number(
        &self, phone_number: &str,
    ) -> impl Future<Output = Result<Option<Contact>, String>> + Send;

    fn update_contact(
        &self, contact: UpdateContact,
    ) -> impl Future<Output = Result<Contact, String>> + Send;

    fn delete_contact(
        &self, uuid: String,
    ) -> impl Future<Output = Result<(), String>> + Send;
}

```

注意 `impl Future` 做异步返回——这是 Rust 1.75 稳定的 RPITIT（Return Position Impl Trait In Traits），让异步 trait 不再需要 `async_trait` 宏。

### 3.3 外部服务也是 trait

文件存储也一样。domain 层定义 `FileStorageGateway` trait：

```rust


#[async_trait]
pub trait FileStorageGateway: Send + Sync {
    async fn upload_file(&self, request: FileUploadRequest)
        -> Result<FileUploadResponse, String>;
    async fn download_file(&self, request: FileDownloadRequest)
        -> Result<FileDownloadResponse, String>;
    async fn delete_file(&self, request: FileDeleteRequest)
        -> Result<(), String>;
    async fn list_files(&self, request: FileListRequest)
        -> Result<FileListResponse, String>;
}

```

Domain 层不关心文件是存 S3、阿里云 OSS 还是本地磁盘。它只管定义"需要什么能力"。

四、Application 层：泛型注入，告别 DI 容器
-----------------------------

Application 层的核心技巧：**用泛型 struct 接收 domain trait，构造器注入具体实现**。

```rust


pub struct ContactAppService<R: ContactRepository> {
    contact_repo: R,
}

impl<R: ContactRepository> ContactAppService<R> {
    pub fn new(contact_repo: R) -> Self {
        Self { contact_repo }
    }

    pub async fn create_contact(
        &self, contact: Contact, creator_uuid: String,
    ) -> Result<(), String> {
        
        let domain_contact: DomainContact = contact.try_into()?;

        
        domain_contact.verify()?;

        
        self.ensure_phone_number_available(&domain_contact.phone, None).await?;

        
        self.contact_repo.create_contact(domain_contact, creator_uuid).await?;
        Ok(())
    }
}

```

**没有 `#[Inject]`、没有 `@Autowired`、没有 DI 容器。**  全靠 Rust 的泛型参数 + `new()` 构造器。

测试怎么办？手写一个 mock struct 实现 trait 就行：

```rust
#[derive(Default)]
struct FakeContactRepository {
    existing: Arc<Mutex<Option<DomainContact>>>,
    created: Arc<Mutex<Vec<DomainContact>>>,
}

impl ContactRepository for FakeContactRepository {
    fn create_contact(&self, contact: DomainContact, creator_uuid: String)
        -> impl Future<Output = Result<DomainContact, String>> + Send {
        let created = self.created.clone();
        async move {
            created.lock().expect("lock").push(contact.clone());
            Ok(contact)
        }
    }
    
}

#[tokio::test]
async fn create_contact_rejects_duplicate_phone_number() {
    let repo = FakeContactRepository {
        existing: Arc::new(Mutex::new(Some())),
        ..Default::default()
    };
    let service = ContactAppService::new(repo);

    let err = service.create_contact(, creator_uuid)
        .await
        .expect_err("应该拒绝重复手机号");

    assert_eq!(err, "联系电话已存在");
}

```

不需要 Mockall、不需要 mock 框架——用 Rust 的 `Arc<Mutex<>>` 记录调用参数，手写实现 20 行搞定。

五、Infrastructure 层：把 trait 接上数据库
--------------------------------

Infrastructure 层负责用具体技术实现 domain trait。

### 5.1 SeaORM 仓储实现

```rust


pub struct SeaOrmContactRepository {
    db: DatabaseConnection,
    merchant_id: String,    
}

#[async_trait]
impl ContactRepository for SeaOrmContactRepository {
    fn create_contact(&self, contact: Contact, creator_uuid: String)
        -> impl Future<Output = Result<Contact, String>> + Send {
        let db = self.db.clone();
        let merchant_id = self.merchant_id.clone();
        async move {
            
            let entity = ContactMapper::to_active_entity(contact, creator_uuid)?;
            
            let new_entity = entity.insert(&db).await
                .map_err(|e| format!("create contact error: {}", e))?;
            
            Ok(ContactMapper::to_domain(new_entity))
        }
    }
}

```

### 5.2 两层 Mapper 的分工

你可能注意到上面有个 `ContactMapper`。这个项目里有两个 mapper 层，各司其职：

| Mapper 层 | 转换方向 | 所在位置 |
| --- | --- | --- |
| **infrastructure mapper** | SeaORM Entity ↔ Domain Entity | `infrastructure/mappers/` |
| **application mapper** | Domain Entity ↔ Shared DTO | `application/mappers/` |

为什么要拆两层？因为 **DTO 的字段和 DB Entity 的字段可能不一样**——DTO 可能合并了多个表的字段，或者对前端暴露的名称跟数据库列名不同。拆开之后，换 ORM 或改 API 格式都不会互相影响。

六、组装与替换成本
---------

到了 Handler 层，组装就是几行代码：

```rust


pub async fn fetch_contacts(params: ContactQuery) -> Result<ListResult<Contact>, ServerFnError> {
    let pool = expect_context::<Database>();
    let tenant = resolve_tenant_context().await?;

    
    let contact_query = SeaOrmContactQuery::new(pool.connection.clone(), tenant.merchant_id);
    let app_service = ContactQueryService::new(contact_query);

    app_service.fetch_contacts(params).await
}

```

这就是**构造器注入**的完整链路：

```arduino
main.rs 初始化 Database → 注入 Leptos Context
  → Handler 取 Database → new 出 Infrastructure 实现
    → 注入 Application Service
      → Application Service 只认 Domain Trait

```

现在想换存储后端？把 `SeaOrmContactQuery` 换成 `RedisContactQuery`，**只改 handler 里的一行**。Application 层一行不动。

七、不适用场景
-------

这个分层不是银弹。以下场景不建议这么搞：

*   **纯 CRUD 系统**：没有复杂业务规则，分层只增加文件数，不增加价值
*   **一个人写的微型项目**：5 个 API 以内，一个 `main.rs` + `schema.rs` 完全够了
*   **团队对 Rust trait 不够熟悉**：泛型约束 + RPITIT + `impl Future` 这套组合有学习曲线

但如果你满足以下条件，三层架构值得考虑：

*   有明确的业务规则（校验、状态机、跨聚合约束）
*   未来可能切换基础设施（数据库、存储、消息队列）
*   需要单元测试覆盖核心逻辑，但不想 mock 数据库

八、总结
----

用 Rust 写 DDD 三层架构的核心心得以一句话概括：**Rust 的 trait 系统天然就是依赖倒置的最佳载体**。

几个关键点：

*   **Domain 层零依赖**：trait 定义契约，不引入任何框架
*   **泛型注入替代 DI 容器**：`ContactAppService<R: ContactRepository>`，构造时传入具体实现
*   **测试不需要 Mockall**：手写 struct 实现 trait，20 行一个 mock
*   **替换成本极低**：换实现只需改 handler 里一行 new()
*   **依赖方向严格单向**：domain ← application ← infrastructure，不会出现循环引用

完整的代码在 GitHub 仓库 Pico-CRM，Rust 全栈（Axum + Leptos + SeaORM），还在持续迭代中。

你写 Rust 后端会分层吗？用的是什么方案？欢迎在评论区聊聊。

* * *

_上一篇讲了事件溯源在订单系统中的实战，上一篇拆解了多租户架构的真实取舍。如果你也在用 Rust 做后端，欢迎 Star 项目和交流。_