## 特點

### 用戶身份驗證

用戶可以使用其Google帳戶通過第三方OAuth進行登錄。

### 群組管理

創建多個財務報告群組以更好地組織數據。

### 類別創建

創建分類以便未來搜索功能。

### 記錄管理

創建和分析財務記錄。

### 匯入/匯出CSV文件進行數據操作

### 根據日期條件篩選記錄

### 記錄分頁

使用分頁方便地瀏覽財務記錄。

### Line Bot 整合

通過Line bot輕松輸入記錄，實現快速高效的追蹤。

### AWS 部署

在AWS（Linux）上部署，Cloudflare處理DNS以進行部署。

## 頁面/功能概述

### 首頁

用戶可以使用其Google帳戶登錄，或在網站上註冊。

透過 "About" 頁面瞭解有關第一個前端項目的信息。

訪問登錄頁面進行帳戶身份驗證。

### 群組頁面

通過選擇 "Groups" 探索群組頁面系統。

創建財務報告群組，具有CRUD功能。

在群組創建後進入財務記錄頁面。

### 財務記錄頁面

利用側邊欄快速在現有群組名稱之間切換。

創建、編輯和刪除分類。

根據指定日期導出CSV數據。

匯入CSV數據，並在記錄頁面之間切換進行詳細分析。

用於每日debit總額的債務分析條形圖。

### Line 頁面

用戶加入Line群組後會遇到兩個選擇：

- 通過輸入電子郵件進行帳戶檢索，綁定現有帳戶。
- 在Line上創建新帳戶。

成功創建後，用戶可以通過Line命令（/c 用於收入，/b 用於支出）輸入記錄。

### AWS EC2 + RDS 部署

使用AWS（EC2）+ RDS（MySQL）進行部署。

Nginx作為中介，Gunicorn作為Web伺服器。

### Cloudflare 整合

- 全球CDN實現內容分發。
- 防範DDoS攻擊，全球負載平衡提高性能。
- SSL/TLS保障連線安全性。
- Web應用程式防火牆（WAF）抵禦惡意攻擊。

## 數據庫結構
### User 表

| 欄位名稱     | 類型     | 說明                 |
|--------------|----------|----------------------|
| username     | 字符串   | 用戶名稱             |
| password     | 字符串   | 密碼                 |
| email        | 字符串   | 郵件地址             |
| line_user_id | 字符串   | Line用戶綁定碼       |

### Group 表

| 欄位名稱     | 類型     | 說明               |
|--------------|----------|--------------------|
| group_name   | 字符串   | 群組名稱           |
| created_by   | 外部鍵   | 關聯至 "User" 的外部鍵 |

### Category 表

| 欄位名稱     | 類型     | 說明               |
|--------------|----------|--------------------|
| name         | 字符串   | 類別名稱           |
| created_by   | 外部鍵   | 關聯至 "User" 的外部鍵 |
| group        | 外部鍵   | 關聯至 "Group" 的外部鍵 |

### FinancialRecord 表

| 欄位名稱     | 類型     | 說明               |
|--------------|----------|--------------------|
| group        | 外部鍵   | 關聯至 "Group" 的外部鍵 |
| category     | 外部鍵   | 關聯至 "Category" 的外部鍵 |
| name         | 字符串   | 名稱               |
| description  | 字符串   | 描述               |
| debit        | 數字     | 支出               |
| credit       | 數字     | 收入               |
| currency     | 字符串   | 幣值               |
| balance      | 數字     | 總額               |
| created_by   | 外部鍵   | 關聯至 "User" 的外部鍵 |

### Line_User 表

| 欄位名稱     | 類型     | 說明               |
|--------------|----------|--------------------|
| user         | 一對一關係 | 與 "User" 表單的一對一關係 |
| line_user_id | 字符串   | Line用戶編號       |
