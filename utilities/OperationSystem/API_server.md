---
layout: default
title: API之設定
parent:   Operation System
grand_parent: Utilities
last_modified_date: 2024-01-02 13:33:58
tags: API
---

{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC 
{:toc}

---

# API之設定

## 背景

- [fastChat]()系統提供了網頁界面和OpenAI兼容的RESTful API，方便用戶進行模型服務和交換。可以像openAI一樣，經提供token後，使用雲端服務業者所提供的推理計算資源。
- see Shuo Yang and Siyuan Zhuang, (Jun 09, 2023) [Building a Truly "Open" OpenAI API Server with Open Models Locally](https://lmsys.org/blog/2023-06-09-api-server/) 

## API的使用需要一個API server隨時等候提供API服務嗎?

是的，通常情況下，API 的使用需要一個 API 伺服器（API Server）隨時等候提供 API 服務。API 伺服器是一個運行在網際網路上或內部網路中的伺服器，負責接收、處理和回應 API 請求。API 伺服器允許應用程式或服務通過 API 進行通信，進而實現資訊的交換和功能的擴展。

以下是一些有關 API 伺服器的關鍵概念：

1. **即時服務：** API 伺服器通常需要在任何時間都能夠即時處理來自客戶端的請求。這意味著伺服器應該是持續運行的，能夠迅速回應請求。

2. **標準通信協定：** API 伺服器通常使用標準的通信協定，例如 HTTP（通常使用 RESTful 或 [GraphQL](#graphql) 等風格）或 WebSocket。這有助於確保不同平台和程式語言的應用程式都能夠與 API 伺服器進行通信。

3. **請求和回應格式：** API 伺服器應該支援標準的請求和回應格式，例如 JSON 或 XML。這有助於確保數據的統一性和易於解析。

4. **授權和身份驗證：** API 伺服器通常實現授權和身份驗證機制，確保僅有合法的用戶和應用程式能夠存取受保護的 API 資源。

5. **日誌和監視：** API 伺服器通常需要具備日誌和監視機制，以便追踪請求、記錄錯誤並進行性能監視。

6. **擴展性：** 隨著應用程式的使用增加，API 伺服器應該具有擴展性，能夠處理更多的同時請求。

總的來說，API 伺服器是實現應用程式介面通信的中心構建塊，它提供了一個標準的、可靠的方式來連接不同的應用程式、服務和資源。

## GraphQL 伺服器的結構

GraphQL 伺服器的結構可以包含多個元件，這些元件協同工作以提供支援 GraphQL 查詢和操作的服務。以下是一個簡單的 GraphQL 伺服器的結構：

1. **Schema（模式）：**
   - GraphQL 的核心是它的模式，它定義了可用的資源、欄位和操作。模式描述了數據的結構和關聯，並提供客戶端查詢的指南。模式由 `Query`、`Mutation` 和 `Subscription` 等類型組成。

2. **Resolver（解析器）：**
   - 解析器是 GraphQL 伺服器的重要元件，負責將客戶端的查詢轉換為實際的數據。每個模式中的欄位都有一個相應的解析器，它定義了如何獲取該欄位的數據。解析器可以是函式或類別的方法。

3. **資料來源：**
   - 資料來源是實際存儲或提供數據的地方。這可以是資料庫、外部 API、內部服務或其他數據來源。解析器使用資料來源來檢索和修改數據。

4. **Middleware（中介軟體）：**
   - 中介軟體是位於解析器前後的功能元件，用於執行額外的邏輯，例如身份驗證、授權、日誌記錄等。中介軟體可以在整個查詢進程中加入額外的邏輯。

5. **Express（或其他 Web 框架）：**
   - 如果使用 Node.js，通常會使用像 Express 這樣的 Web 框架來建立 GraphQL 伺服器的 HTTP 端點。其他語言和平台也有相應的框架。

6. **WebSocket（可選）：**
   - 如果要支援即時數據，可以使用 WebSocket 來實現訂閱（Subscription）功能。WebSocket 允許伺服器主動推送數據給客戶端，實現即時通訊。

總的來說，GraphQL 伺服器的結構主要包含模式、解析器、資料來源、中介軟體以及與 Web 框架和可能的 WebSocket 集成。這種結構提供了一個靈活且擴展性強的方式，以滿足不同應用的需求。

## fastChat API

OpenAI-Compatible RESTful APIs & SDK
FastChat provides OpenAI-compatible APIs for its supported models, so you can use FastChat as a local drop-in replacement for OpenAI APIs. The FastChat server is compatible with both openai-python [library](https://github.com/openai/openai-python) and cURL commands. See [docs/openai_api.md](https://pypi.org/project/fschat/0.2.11/docs/openai_api.md).

Hugging Face Generation APIs
See fastchat/serve/huggingface_api.py.

LangChain Integration
See docs/langchain_integration.

## Terminology

### RESTful

RESTful（Representational State Transfer）是一種用於設計網路應用程式的軟體架構風格。它通常應用在 Web 服務的設計中，以實現分散式、可擴展且容易維護的系統。

以下是 RESTful 的一些主要特點和概念：

1. **資源（Resources）：** 在 REST 中，所有的資訊和功能都被視為資源。每個資源都有一個唯一的識別符號（通常是 URL），客戶端通過這些 URL 來訪問資源。

2. **表現層（Representation）：** 資源的狀態以及與之相關的操作被表示為資源的表現層。這可以是 JSON、XML 或其他格式，視應用程式的需求而定。

3. **狀態轉換（Stateless）：** 每個請求從客戶端到伺服器的過程中都包含了足夠的信息，以理解和處理請求。伺服器不需要保存客戶端的狀態。

4. **統一接口（Uniform Interface）：** RESTful 系統使用統一的接口，包括資源標識符、資源的表現層和自描述消息。這種統一性提高了系統的可見性、簡化了伺服器和客戶端的互操作性。

5. **無狀態（Stateless）：** 每一個請求從客戶端發送到伺服器時都應該包含足夠的信息，使得伺服器能夠理解並處理該請求。伺服器不應保存有關客戶端狀態的資訊。

6. **可緩存性（Cacheability）：** 資源的表現層可以被標記為可緩存或不可緩存。這允許客戶端和伺服器進行有效的快取管理。

7. **客戶端-伺服器架構（Client-Server Architecture）：** RESTful 架構將系統分為客戶端和伺服器，它們分別獨立進行演化，這提高了系統的可擴展性。

RESTful 風格的 API 被廣泛用於 Web 開發中，並且它的簡潔和易於理解的特點使其成為一種受歡迎的 API 設計方式。

### GraphQL

GraphQL（Graph Query Language）是一種用於 API 的查詢語言，由 Facebook 於2012年開發並在2015年開源。GraphQL 不同於傳統的 REST 架構，它提供了更靈活、高效和精確的數據檢索和操作方式。

以下是 GraphQL 的一些主要特點和概念：

1. **靈活的查詢：** 使用者可以定義自己需要的數據結構和內容，而不必像 REST 一樣僅能使用預定義的端點。這使得客戶端能夠更有效地檢索所需的數據。

2. **單一請求：** GraphQL 允許用戶通過一個請求獲取**多個數據資源**，而不是像 REST 一樣需要多個請求。這有助於減少過多的請求次數，提高效能。

3. **強類型和模式：** GraphQL 使用強類型和可定義的模式，用於描述可查詢的數據結構。這使得 API 更易於理解、開發和維護。

4. **自動完成：** GraphQL 支援自動完成（introspection），即客戶端能夠查詢可用的數據模式和操作，從而簡化了 API 的使用。

5. **即時數據：** GraphQL 支援即時數據，這意味著客戶端可以訂閱特定事件，並在數據有變更時即時收到通知。

6. **無過度取用：** GraphQL 中的每一個查詢都由客戶端指定，這樣就防止了過度取用（over-fetching）和不足取用（under-fetching）的問題。

7. **跨平台支援：** GraphQL 不與特定的後端技術或數據庫相關聯，這使得它能夠與各種後端技術和數據庫結合使用。

GraphQL 已經在多個大型應用程式和企業中得到廣泛應用，並且被視為一種現代化、靈活且效能優越的 API 設計方式。

### GraphQL和RESTful的比較與呼叫範例

GraphQL 和 RESTful 是兩種不同的 API 設計風格，各自有其優勢和用法。共同點：

1. **使用 HTTP 協議：** GraphQL 和 RESTful 都基於 HTTP 協議，可以在 Web 上使用。
2. **資源：** 兩者都將數據組織成資源，並使用 [URI]() 進行標識。

以下是它們的比較

項目|GraphQL|RESTful|
-|:-:|:-:
請求次數|客戶端可以定義所需的數據，只需進行一個請求，減少了過多的請求次數。|分開多次請求
欄位精確性|客戶端能夠精確指定所需的欄位，避免了過度取用或不足取用的問題。|**簡單性：** RESTful 較為簡單，易於理解和實現|
即時性|支援即時數據，使得客戶端能夠訂閱事件並即時收到更新。|
自動性|支援自動完成，客戶端能夠查詢可用的數據模式和操作。|**緩存管理：** 具備良好的緩存管理，使用 HTTP 標準的快取機制。
靈活性|結構較為靈活，可以適應不斷變化的客戶端需求。|**標準化：** 採用標準的 HTTP 方法（GET、POST、PUT、DELETE）和狀態碼，易於遵循標準
可見性|可見性較低|採用統一接口，提高系統的可見性

總的來說，GraphQL 和 RESTful 有各自的優勢，選擇取決於應用程式的需求和開發團隊的偏好。GraphQL 在需要更靈活數據查詢和即時數據的場景中表現較為出色，而 RESTful 則在簡單性和標準性方面有優勢。

1. **複雜性和簡單性：** 如果應用程式相對簡單，RESTful 可能更適合；如果需要更靈活的數據查詢，GraphQL 是一個不錯的選擇。
2. **即時數據需求：** 如果需要即時數據或具有複雜的查詢需求，GraphQL 是更合適的選擇。
3. **開發者社群：** 兩者都有強大的社群支援，但具體選擇可能取決於團隊的經驗和偏好。

## GraphQL 呼叫範例

以下是一個簡單的 GraphQL 查詢範例，假設有一個博客系統，我們想獲取某個作者的文章和評論：

```graphql
query {
  author(id: "123") {
    name
    posts {
      title
      content
      comments {
        text
      }
    }
  }
}
```

在這個例子中，我們只需一個請求就能夠獲取作者的名字、所有文章的標題和內容，以及每篇文章的評論。

## RESTful 呼叫範例

對應的 RESTful 請求可能需要多個端點，例如：

- 獲取作者信息：`GET /authors/123`
- 獲取作者的文章列表：`GET /authors/123/posts`
- 獲取文章的詳細內容：`GET /posts/456`
- 獲取文章的評論列表：`GET /posts/456/comments`

每個端點只返回特定的資訊，可能需要多次請求才能獲得所需的完整數據。


