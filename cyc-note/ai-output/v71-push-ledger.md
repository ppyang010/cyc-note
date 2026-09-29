# v7.1 AI 解析推送总台账

- 身份一律 `question_body.id`，不用 `question.id`
- 同步顺序：CHECK → CONFLICT 收集 `expectedTargetGenerationBatchNo` → 带 map 再 CHECK → APPLY → 复核 SKIP
- 本文件是**总表**。各批次明细仍在 `exam_ai_data/output/<任务>/` 的 `PUSH_LEDGER.md` / `apply-summary.json`
- 更新：2026-09-30（外科学公用 60 已写本地+DEV；UAT/PRD 未推）

## 环境

| 环境 | 是否本轮默认写入 |
|---|---|
| 本地 MySQL | 按任务 |
| DEV `todpublic-dev.dxy.net/EXAM-MS-EXAM-DEV` | 按任务 |
| UAT `todpublic.dxy.cn/EXAM-MS-EXAM-UAT` | 须明确下令 |
| PRD `todpublic.dxy.cn/EXAM-MS-EXAM-PRD` | 须明确下令 |

「生产没有的新解析」= 该口径 PRD 原先有效 v7.1 为 0，或 APPLY 操作为 INSERT。UPDATE 是覆盖已有解析，不是新题。

---

## 总表

| 任务 | exam_type | 批次号 | 题数 | 本地 | DEV | UAT | PRD | 相对生产 |
|---|---|---|---:|---|---|---|---|---|
| 内科学公用 基础题库 | 41 | `v71-zhuzhi41-basic-20260925` + retry | 6,673 | ✅ | ✅ | ❌ | ❌ | **新解析**（口径内 PRD 原 0） |
| 内科学 303 基础题库 | 42 | `v71-zhuzhi42-basic-20260926` + retry | 6,157 | ✅ | ✅ | ❌ | ❌ | **新解析**（口径内 PRD 原 0） |
| 妇产/儿科/全科 首轮 | 90/91/92 | `v71-zhuzhi90-91-92-basic-20260928` | 16,704 | ✅ | ✅ | ❌ | ❌ | **新解析**（口径内 PRD 原 0） |
| 妇产/儿科/全科 补材料 | 90/91/92 | `v71-zhuzhi90-91-92-retry-20260928` | 2,755 | ✅ | ✅ | ❌ | ❌ | **新解析**（相对首轮增量） |
| 心血管～内分泌 基础题库 | 43–48 | `v71-zhuzhi43-48-basic-20260928` | 11,403 | ✅ | ✅ | ❌ | ❌ | **新解析**（口径内 PRD 原 0） |
| 外科学公用 基础题库 | 60 | `v71-zhuzhi60-basic-20260930` | 5,834 | ✅ | ✅ | ❌ | ❌ | **新解析**（口径 7,236；DEV INSERT 5,503 / UPDATE 331） |
| 血液/结核/传染/风湿 | 49–52 | — | — | — | — | — | — | **按指令不跑** |
| 二试∪测试卷 | 9/11 等 | `v71-second-test-to-dev-20260924` | 5,314 | ✅ | ✅ | ✅ | ✅ | INSERT 5,312 / UPDATE 2 |
| 2026 执业还原真题 | 9 | `v71-zhizhi9-2026-prd-20260910` | 311 | ✅ | — | UAT 源 | ✅ | 全 INSERT |
| 2026 助理还原真题 | 11 | `v71-zhuli11-2026-prd-20260910` | 244 | ✅ | — | UAT 源 | ✅ | 全 INSERT |
| 主治 2026 Excel 还原真题 | 60–65/68/90/92 | `v71-zhuzhi-2026-excel-20260929` | 1,105 题 / 995 解析 | ❌ | ❌ | ✅ | ✅ | 先导题再解析，全 INSERT |
| isCorrectOption 定点修 | 3 题 | `v71-fix-option-flags-3q-20260924` | 3 | ✅ | ✅ | ✅ | ✅ | 改标，非新题 |
| optionText 定点修 | 5 题 | `v71-fix-option-text-5q-20260924` | 5 | ✅ | ✅ | ✅ | ✅ | 改文案，非新题 |

口径一律：**基础题库 `basic_question=1` + 有效题 + 有效目录**（二试/测试卷、2026 真题除外）。

---

## 1. 未上 PRD（已写本地 + DEV）

### 1.1 内科学公用 41

| 项 | 值 |
|---|---|
| 范围 | PRD 7,205 小题；X/ALFX 本口无 |
| 本地 | 首轮 supported 4,710 + 补材料 1,961 + 失败重跑 2 = **6,673** |
| DEV | 已 APPLY，复核 SKIP |
| 产物 | `output/v71-zhuzhi41-basic/` |
| 未入库 | 约 532 题仍不足/冲突 |

### 1.2 内科学 303（42）

| 项 | 值 |
|---|---|
| 范围 | PRD 8,850（1 题无选项未进） |
| 本地 | 合并 supported **6,157**（批次 `v71-zhuzhi42-basic-20260926` 等） |
| DEV | INSERT 5,013 / UPDATE 282；复核 SKIP 5,295（另有 retry 增量） |
| 产物 | `output/v71-zhuzhi42-basic/` |
| 未入库 | 约 2,695 题仍不足/冲突 |

### 1.3 妇产 90 / 儿科 91 / 全科 92（上一批已完成的新题）

| 项 | 值 |
|---|---|
| 范围 | 23,969（儿科 1 题无选项未进） |
| 首轮 | 16,704 supported → 本地 + DEV；DEV 复核 16,704 SKIP（2026-09-28 02:12 UTC） |
| 增量 | 补材料后净增 2,755 → 本地 + DEV；DEV 复核 2,755 SKIP（2026-09-28 02:51 UTC） |
| 本地合计 | 妇产 6,301 / 儿科 8,549 / 全科 4,752 = **19,602** |
| DEV 合计 | 约 **19,459** |
| 产物 | `output/v71-zhuzhi90-91-92-basic/merged-supported/`、`merged-final/` |

这是「上一次跑完、还没上线」的那一批。

---

### 1.4 主治内科分口 43–48（本轮新完成）

| 项 | 值 |
|---|---|
| 范围 | 15,049 小题（基础题库 + 有效题 + 有效目录） |
| 首轮 supported | **11,403** → 本地 + DEV |
| DEV | INSERT 11,005 / UPDATE 398；复核 **11,403 SKIP**（2026-09-29 02:24 UTC） |
| 分口 | 43 心血管 2,191 / 44 呼吸 2,102 / 45 消化 2,138 / 46 肾内 1,796 / 47 神经内 1,683 / 48 内分泌 1,493 |
| 产物 | `output/v71-zhuzhi43-48-basic/merged-supported/` |
| 扩资料重跑 | 不足 3,337 + 冲突 309 = **3,646**；批次 `v71-zhuzhi43-48-retry-20260929`；2 路 DeepSeek 进行中 |

### 1.5 外科学公用 60（本轮完成）

| 项 | 值 |
|---|---|
| 范围 | PRD 7,236 小题（基础题库 + 有效题 + 有效目录） |
| 首轮 supported | **5,834（80.6%）** → 本地 + DEV |
| 仍不足 / 冲突 | 1,225 / 177 |
| DEV | INSERT 5,503 / UPDATE 331；复核 **5,834 SKIP**（2026-09-29 22:29 UTC） |
| 产物 | `output/v71-zhuzhi60-basic/merged-supported/` |
| 批次 | `v71-zhuzhi60-basic-20260930` |

## 2. 生成中，尚未入库

### 2.1 43–48 扩资料重跑

- 输入：`output/v71-zhuzhi43-48-basic/retry-skip/`（教材命中 3,593 / 3,646）
- 调度：2 路 DeepSeek，8 批
- **不自动入库**；跑完须确认再写本地 / DEV 增量

### 2.2 明确不跑

49 血液 / 50 结核 / 51 传染 / 52 风湿。

---

## 3. 已上 PRD

### 3.1 二试个性化套 ∪ 执业/助理测试卷（5,314）

- 身份 `question_body.id`；重叠取测试卷更新版
- DEV / UAT / PRD 均 APPLY；PRD = P1 1,539 INSERT + P2 372 INSERT + P3 3,403（INSERT 3,401 / UPDATE 2）
- 合计 PRD：**INSERT 5,312 / UPDATE 2**
- 产物：`output/v71-sync-second-test-to-{dev,uat,prd-p1,prd-p2,prd-p3}/`
- 备注：UAT 批次名误用 DEV 名 `v71-second-test-to-dev-20260924`，数据无误

### 3.2 定点修正（已进三环境）

| 批次 | 题 | 动作 |
|---|---|---|
| `v71-fix-option-flags-3q-20260924` | 186035 / 187439 / 230421 | `isCorrectOption` UPDATE |
| `v71-fix-option-text-5q-20260924` | 173235 / 190384 / 195245 / 208522 / 230546 | `optionText` UPDATE |

### 3.3 2026 还原真题

| 考试 | 题数 | PRD |
|---|---:|---|
| 执业 9 | 311 | 全 INSERT，复核 SKIP |
| 助理 11 | 244 | 全 INSERT，复核 SKIP |
| 主治 Excel 还原真题 | 1,105 题 / 995 解析 | 先导题（批次 5213–5221）再解析，全 INSERT，复核 995 SKIP |

主治 Excel 产物：`output/v71-zhuzhi-2026/{uat,prd}-import/`。回滚档：`prd-import/ROLLBACK.md`。
执业/助理产物：`output/v71-2026-prd-sync-20260910/`

### 3.4 西综 30（2010–2026）

PRD 已导入约 **2,629 / 2,917**（覆盖约 90%），缺口约 288 题（不足/冲突跳过）。台账：`output/v71-xizong-prd-sync-20260909-years/`。本会话未再推。

---

## 4. 执考 9 / 助理 11 本地有、PRD 未在本表对账

本地：执业 9 **15,407**，助理 11 **8,458**。除上面「已上 PRD」外，还有历年真题、unresolved/insuff 补跑、非基础题库年卷、drift 修补等批次。**不能从本表断定未上 PRD**，需按 exam_type 拉 PRD 覆盖率。

---

## 5. 各任务产物目录

| 任务 | 路径 |
|---|---|
| 41 | `output/v71-zhuzhi41-basic/` |
| 42 | `output/v71-zhuzhi42-basic/` |
| 90/91/92 | `output/v71-zhuzhi90-91-92-basic/` |
| 43–48 | `output/v71-zhuzhi43-48-basic/` |
| 60 外科学公用 | `output/v71-zhuzhi60-basic/` |
| 二试+测试卷 | `output/v71-sync-second-test-to-*` |
| 选项标记 | `output/v71-fix-option-flags/` |
| 选项文案 | `output/v71-fix-option-text/` |
| 2026 执助 | `output/v71-2026-prd-sync-20260910/` |
| 主治 2026 Excel | `output/v71-zhuzhi-2026/{uat,prd}-import/` |

Obsidian 副本：`cyc-note/cyc-note/ai-output/v71-push-ledger.md`（与本文件同步）。
