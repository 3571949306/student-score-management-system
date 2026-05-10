# Spring Security 学生成绩管理示例

这是一个 Spring Boot + Spring Security + Thymeleaf 示例项目，包含学生成绩管理、AI 成绩预测、账号管理和基于角色的访问控制。

## 当前特性

- **Spring Security**：表单登录、BCrypt 密码加密、CSRF 防护、基于角色的访问控制
- **双数据库支持**：H2 内嵌数据库（默认开发环境）+ MySQL 5.1（生产环境）
- **AI 成绩预测**：基于 Weka 随机森林算法预测学生成绩
- **Spring Data JPA**：实体关系管理（@ManyToMany）
- **Bean Validation**：数据验证注解
- **Thymeleaf 模板引擎**：服务端渲染 + CSRF Token
- **班级管理**：支持多班级成绩管理，学生按班级查看成绩
- **我的成绩**：学生可查看所有历史考试成绩汇总
- **自动创建账号**：添加成绩时自动为学生创建登录账号

## 快速开始

### 方式一：使用 H2 数据库（推荐，无需安装数据库）

直接启动即可，应用会自动创建 H2 文件数据库并初始化数据。

```bash
# Windows PowerShell
$env:JAVA_HOME = "C:\Users\tcw\.jdks\ms-17.0.19"
& "$env:JAVA_HOME\bin\java.exe" -jar target/spring-security-demo-1.0.0.jar
```

### 方式二：使用 MySQL 数据库（生产环境）

1. 执行初始化脚本：

```bash
mysql -u root -p < src/main/resources/sql/init.sql
```

2. 修改 `src/main/resources/application.properties`：

```properties
# 注释掉 H2 配置
# spring.profiles.active=h2

# 激活 MySQL 配置
spring.profiles.active=mysql
```

3. 检查 `src/main/resources/application-mysql.properties` 中的数据库连接信息。

4. 启动应用。

```bash
$env:JAVA_HOME = "C:\Users\tcw\.jdks\ms-17.0.19"
& "$env:JAVA_HOME\bin\java.exe" -jar target/spring-security-demo-1.0.0.jar
```

### H2/MySQL 切换说明

项目使用 Spring Profiles 实现双数据库无缝切换：

| Profile | 配置文件 | 数据库类型 | 说明 |
|---------|----------|-----------|------|
| `h2` | `application.properties` | H2 内嵌数据库 | 默认，无需安装数据库 |
| `mysql` | `application-mysql.properties` | MySQL 5.1+ | 生产环境使用 |

切换时只需修改 `spring.profiles.active` 的值。

## 初始账号

### 系统账号

| 用户名 | 密码 | 角色 | 权限 |
|--------|------|------|------|
| admin | 123 | 管理员 | 管理账号和用户分组，拥有成绩管理权限 |
| teacher | 123 | 老师 | 查看、添加、修改、删除学生成绩 |

### 学生账号（自动创建）

项目初始化时会自动创建 15 个学生账号，分为两个班级：

**高一(1)班：** 李明、王芳、张伟、刘洋、陈静、赵强、孙丽、周杰
**高一(2)班：** 吴敏、郑浩、马丽、林峰、黄婷、杨磊、徐超

所有学生账号密码默认为 `123`，学生登录后只能查看本班成绩。

## 页面导航

- 登录页：http://localhost:8080/login
- 成绩管理页：http://localhost:8080/scores
- 我的成绩页：http://localhost:8080/scores/my-exams（学生专用）
- AI 成绩预测：http://localhost:8080/prediction
- 管理员主页：http://localhost:8080/admin/main
- 用户管理：http://localhost:8080/admin/users
- H2 控制台（仅 H2 模式）：http://localhost:8080/h2-console

## 功能说明

### 成绩管理

- **老师/管理员**：可查看和管理所有班级成绩，支持按班级切换（一班/二班）、按考试类型筛选（期中/期末）
- **学生**：进入成绩管理页面后，自动显示本班成绩表，自己的成绩行高亮显示并自动滚动到可视区域
- 支持按学号、姓名、科目、成绩、考试、学期、日期排序
- 成绩以彩色徽章显示，直观区分等级（优秀/良好/中等/及格/不及格）
- 老师可添加、编辑、删除成绩，添加成绩时自动为学生创建登录账号

### 我的成绩（学生专用）

- 学生点击导航栏"我的成绩"可查看所有历史考试成绩汇总
- 按学期和考试分组展示，显示每次考试的总分
- 点击"查看班级排名"按钮可查看该次考试全班同学的成绩表

### AI 成绩预测

基于 Weka 机器学习库的随机森林回归算法：

- 根据历史成绩数据训练预测模型
- 输入学生姓名、科目、考试类型、学期等参数预测成绩
- 显示置信度和预测详情
- 首次启动时自动使用历史数据训练模型
- 学生登录后进入 AI 预测页面，系统自动生成预测结果

### 用户管理（管理员）

- 创建、编辑、删除用户账号
- 分配用户角色（老师/学生/管理员）
- 启用/禁用账号

## 项目结构

```
spring-security-demo/
├── src/main/java/com/example/securitydemo/
│   ├── config/
│   │   ├── DataInitializer.java          # 数据初始化
│   │   ├── GlobalExceptionHandler.java   # 全局异常处理
│   │   └── SecurityConfig.java           # Spring Security 配置
│   ├── controller/
│   │   ├── AdminUserController.java      # 用户管理控制器
│   │   ├── HomeController.java           # 首页控制器
│   │   ├── PredictionController.java     # AI 预测控制器
│   │   └── StudentScoreController.java   # 成绩管理控制器
│   ├── entity/
│   │   ├── StudentScore.java             # 学生成绩实体（含班级字段）
│   │   ├── SysRole.java                  # 角色实体
│   │   └── SysUser.java                  # 用户实体
│   ├── repository/
│   │   ├── StudentScoreRepository.java   # 成绩数据访问
│   │   ├── SysRoleRepository.java        # 角色数据访问
│   │   └── SysUserRepository.java        # 用户数据访问
│   └── service/
│       ├── DatabaseUserDetailsService.java # 用户认证服务
│       └── ScorePredictionService.java   # AI 预测服务
├── src/main/resources/
│   ├── static/css/
│   │   └── app.css                       # 全局样式
│   ├── templates/
│   │   ├── login.html                    # 登录页面
│   │   ├── login-success.html            # 登录成功页面
│   │   ├── scores.html                   # 成绩管理页面
│   │   ├── my-exams.html                 # 我的成绩页面（学生）
│   │   ├── prediction.html               # AI 预测页面（老师）
│   │   ├── prediction-student.html       # AI 预测页面（学生）
│   │   ├── admin-main.html               # 管理员主页
│   │   ├── admin-users.html              # 用户管理页面
│   │   ├── access-denied.html            # 无权访问页面
│   │   └── error.html                    # 错误页面
│   ├── application.properties            # H2 默认配置
│   └── application-mysql.properties      # MySQL 配置
├── pom.xml                               # Maven 依赖配置
└── README.md                             # 项目文档
```

## 技术栈

- Java 17
- Spring Boot 2.7.18
- Spring Security 5.7.x
- Spring Data JPA + Hibernate
- H2 Database（开发）/ MySQL 5.1（生产）
- Weka 3.8.6（机器学习）
- Thymeleaf
- Maven

## 数据库配置详情

### H2 模式（默认）

```properties
spring.datasource.driver-class-name=org.h2.Driver
spring.datasource.url=jdbc:h2:file:./data/spring_security_demo;AUTO_SERVER=TRUE
spring.datasource.username=sa
spring.datasource.password=
```

数据库文件存储在 `./data/` 目录下，支持多进程同时访问。

### MySQL 模式

```properties
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
spring.datasource.url=jdbc:mysql://localhost:3306/spring_security_demo?useSSL=false&serverTimezone=Asia/Shanghai&characterEncoding=utf8
spring.datasource.username=root
spring.datasource.password=root
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQL5InnoDBDialect
```

MySQL 5.1.49 驱动已包含在项目依赖中（runtime scope）。

## 安全特性

- **BCrypt 密码加密**：所有用户密码使用 BCrypt 算法加密存储
- **CSRF 防护**：所有表单提交必须携带 CSRF Token
- **基于角色的访问控制**：不同角色只能访问授权的页面和功能
- **会话管理**：登录后保持会话状态，支持安全注销

## 数据验证

成绩录入时自动验证：

- 姓名不能为空，最多 50 个字符
- 学号不能为空，最多 30 个字符
- 成绩必须在 0-150 之间
- 验证失败时显示友好的错误提示

## 全局异常处理

项目配置了统一的异常处理器，所有未捕获的异常都会跳转到错误页面显示友好提示，而不是直接暴露堆栈信息。

## 开发说明

### 添加新功能

1. 在 `entity/` 中创建实体类
2. 在 `repository/` 中创建数据访问接口
3. 在 `controller/` 中创建控制器
4. 在 `templates/` 中创建 Thymeleaf 模板
5. 在 `SecurityConfig` 中配置访问权限

### 测试

运行所有测试：

```bash
./mvnw test
```

### 打包

```bash
./mvnw clean package -DskipTests
```

## 更新日志

### v1.4.0（当前版本）

- 成绩表格重构：每个学生仅显示一行，各科成绩作为列展示
- 新增排名列，默认按总分降序排列，支持并列排名
- 全列排序功能：点击任意列（排名、学号、姓名、各科、总分）切换升降序
- 学生行参与排序，同时保持高亮和自动滚动到视野
- 修正登录页演示账号信息
- 更新 init.sql 脚本，完整初始化 15 个学生和 150 条成绩数据
