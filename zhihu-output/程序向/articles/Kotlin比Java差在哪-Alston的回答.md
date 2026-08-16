---
id: "3560851530"
title: "Kotlin比Java差在哪?"
author: "Alston"
type: zhihu-answer
source: "https://www.zhihu.com/question/603984700/answer/3560851530"
created: "2024-07-13 19:01"
updated: "2024-07-13 19:17"
collected: "2024-07-13 19:01"
downloaded: "2026-08-16"
---
差在三兩下就把Java難搞的異步寫完了，太快下班領不到加班費

*需求：發送 N 個請求或許用戶信息，為避免將對方服務器打掛，我們5個一組並發，做完再做下一組，然後合併全部結果再返回。*

```kotlin
val scoped = CoroutineScope(Dispatchers.IO + SupervisorJob())

// 輸入N個用戶名，輸出N個用戶信息
suspend fun getUserDetails(names: List<String>): List<String> {
    return names.chunked(5).map { batch ->
        scoped.async {
            batch.map { async { sendRequest(it) } }   // 調用異步方法並取得結果
                 .awaitAll()  // 類似 js的 await Promise.all
                 .also { Log.info("got batch response") } // 順便打印日誌
        }.await()
    }.flatten()
}
// 模擬異步請求，返回用戶信息
suspend fun sendRequest(name: String): String {
    delay(1000)
    return name
}
```

Kotlin的並發基於協程，而開協程的成本相當低，大約只有線程的千分之一，隨便一台家用電腦都可以開啟百萬個協程，而且不用手動去管理協程生命週期。