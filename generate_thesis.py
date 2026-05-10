import html
import os
import zipfile
from datetime import datetime


OUT_DIR = os.path.abspath("论文输出")
DOCX_PATH = os.path.join(OUT_DIR, "基于SpringBoot与SpringSecurity的学生成绩管理系统论文全文_表格ER图PNG版.docx")
MD_PATH = os.path.join(OUT_DIR, "基于SpringBoot与SpringSecurity的学生成绩管理系统论文全文_表格ER图PNG版.md")
ER_IMAGE_PATH = os.path.join(OUT_DIR, "学生成绩管理系统ER图.png")


TITLE = "基于 Spring Boot 与 Spring Security 的学生成绩管理系统的设计与实现"


SECTIONS = [
    ("封面", [
        "题目：" + TITLE,
        "学生姓名：__________",
        "学号：__________",
        "专业：__________",
        "指导教师：__________",
        "完成日期：2026年4月",
    ]),
    ("摘要", [
        "随着学校教学管理信息化水平的不断提高，学生成绩管理逐渐从传统的纸质记录和电子表格方式转向基于网络的信息管理系统。传统成绩管理方式在数据维护、权限划分、成绩查询和账号管理等方面存在效率较低、安全性不足和维护成本较高等问题。为提高成绩管理工作的规范性和便捷性，本文设计并实现了一套基于 Spring Boot 与 Spring Security 的学生成绩管理系统。",
        "系统采用 Java 作为主要开发语言，使用 Spring Boot 作为后端基础框架，结合 Spring Security 实现登录认证和角色权限控制，使用 Spring Data JPA 完成数据库访问，使用 Thymeleaf 完成页面渲染，使用 MySQL 存储用户、角色和学生成绩等业务数据。系统主要面向学生、老师和管理员三类用户。其中学生可以登录系统查看成绩；老师可以对学生成绩进行添加、修改、删除、查询和排序；管理员可以管理账号和用户分组，并拥有其他用户的相关操作权限。",
        "通过系统实现与功能测试可以看出，该系统能够完成基本的学生成绩管理业务，具备较清晰的功能结构和权限控制逻辑，能够满足小型教学管理场景下的成绩维护与查询需求。本文围绕系统需求分析、总体设计、数据库设计、详细实现和测试过程进行了完整阐述。",
        "关键词：Spring Boot；Spring Security；学生成绩管理；权限控制；MySQL；Thymeleaf",
    ]),
    ("Abstract", [
        "With the continuous improvement of information technology in school teaching management, student score management is gradually shifting from traditional paper records and spreadsheets to web-based information systems. Traditional methods have disadvantages in data maintenance, permission division, score query and account management. In order to improve the efficiency and security of score management, this thesis designs and implements a student score management system based on Spring Boot and Spring Security.",
        "The system uses Java as the main programming language, Spring Boot as the back-end framework, Spring Security for authentication and authorization, Spring Data JPA for database access, Thymeleaf for page rendering, and MySQL for data storage. The system includes three roles: student, teacher and administrator. Students can view scores, teachers can add, update, delete and sort score data, and administrators can manage accounts and role groups.",
        "The implementation and testing results show that the system can satisfy the basic needs of score management in small teaching scenarios. This thesis describes the system requirements, architecture design, database design, detailed implementation and testing process.",
        "Key words: Spring Boot; Spring Security; Student Score Management; Permission Control; MySQL; Thymeleaf",
    ]),
    ("目录", [
        "第一章 绪论",
        "第二章 相关技术介绍",
        "第三章 系统需求分析",
        "第四章 系统总体设计",
        "第五章 数据库设计",
        "第六章 系统详细设计与实现",
        "第七章 系统测试",
        "第八章 总结与展望",
        "参考文献",
        "致谢",
    ]),
    ("第一章 绪论", [
        "1.1 研究背景",
        "学生成绩是学校教学管理中的核心数据之一，成绩数据不仅反映学生阶段性学习效果，也为教师调整教学方案、学校开展教学评价提供依据。在传统管理方式中，成绩通常依赖纸质表格或单机电子表格进行记录和维护。当学生人数、科目数量和考试批次增加后，数据录入、查询、修改和统计的工作量会明显增大，同时也容易出现数据重复、记录不一致和权限边界模糊等问题。",
        "随着 Web 技术和数据库技术的发展，基于浏览器的成绩管理系统逐渐成为学校信息化建设的重要组成部分。通过 Web 系统可以将成绩数据集中存储在数据库中，并通过不同角色的权限控制实现分工协作。学生只需要登录系统即可查看个人成绩，老师可以维护所负责的成绩信息，管理员可以统一管理账号与用户分组。这种方式能够提高成绩管理效率，也能减少无关人员对敏感成绩数据的访问。",
        "本课题以学生成绩管理为业务背景，结合当前主流 Java Web 开发技术，设计并实现一套轻量级成绩管理系统。系统重点关注登录认证、角色权限控制、成绩数据增删改查以及账号分组管理，能够体现 Spring Boot 和 Spring Security 在实际业务系统中的应用过程。",
        "1.2 研究意义",
        "本系统的研究意义主要体现在三个方面。第一，在业务层面，系统能够为学校成绩管理提供一个统一的数据维护入口，减少教师手工整理成绩表的工作量。第二，在安全层面，系统通过角色权限划分控制不同用户的访问范围，避免学生修改成绩或普通用户访问管理员页面。第三，在学习实践层面，系统完整覆盖 Java Web 项目中的配置管理、实体建模、数据库访问、页面渲染和安全控制等关键内容，具有较强的实践价值。",
        "1.3 国内外研究现状",
        "目前，教育管理信息系统已经广泛应用于学校日常管理中，常见系统包括教务管理系统、学生信息管理系统、在线考试系统和成绩分析系统等。较成熟的系统通常具有完善的数据统计、权限管理和报表导出功能。对于中小型教学管理场景而言，系统不一定需要复杂的大型平台架构，但仍然需要具备稳定的数据存储、基本的权限控制和易用的业务操作界面。",
        "在技术方面，Spring Boot 凭借自动配置和快速开发的优势，被广泛用于 Java Web 应用开发。Spring Security 是 Spring 生态中常用的安全框架，可以较方便地实现认证和授权功能。MySQL 作为常用关系型数据库，适合存储结构化业务数据。本文基于这些成熟技术实现学生成绩管理系统，能够在较低开发复杂度下满足系统功能需求。",
        "1.4 论文主要研究内容",
        "本文主要研究内容包括：分析学生成绩管理系统的业务需求；设计学生、老师和管理员三类用户角色；完成系统数据库表结构设计；实现用户登录认证和角色权限控制；实现学生成绩的表格展示、添加、修改、删除和排序；实现管理员对账号和用户分组的管理；对系统主要功能进行测试并分析测试结果。",
        "1.5 论文组织结构",
        "本文共分为八章。第一章介绍研究背景、意义和主要内容；第二章介绍系统开发所使用的关键技术；第三章进行系统需求分析；第四章给出系统总体设计；第五章进行数据库设计；第六章阐述系统详细设计与实现；第七章进行系统测试；第八章总结系统开发成果并提出后续改进方向。",
    ]),
    ("第二章 相关技术介绍", [
        "2.1 Spring Boot 框架",
        "Spring Boot 是基于 Spring 框架的快速开发框架，能够通过自动配置、起步依赖和内嵌服务器简化 Java Web 项目的搭建过程。传统 Spring 项目需要编写大量 XML 或配置类，而 Spring Boot 通过约定优于配置的思想降低了项目初始化和依赖整合的复杂度。本系统使用 Spring Boot 2.7.18 作为基础框架，项目入口类为 SpringSecurityDemoApplication。",
        {"type": "table", "headers": ["技术名称", "版本或文件", "主要作用"], "rows": [
            ["Spring Boot", "2.7.18", "提供 Web 应用基础框架和自动配置能力"],
            ["Spring Security", "spring-boot-starter-security", "实现登录认证、授权和访问控制"],
            ["Spring Data JPA", "spring-boot-starter-data-jpa", "封装数据库访问，简化增删改查操作"],
            ["Thymeleaf", "spring-boot-starter-thymeleaf", "渲染登录、成绩管理和账号管理页面"],
            ["MySQL", "mysql-connector-java 5.1.49", "保存用户、角色、成绩等业务数据"],
            ["Maven", "pom.xml", "管理项目依赖、编译和打包"],
        ]},
        "2.2 Spring Security 安全框架",
        "Spring Security 是 Spring 生态中用于认证和授权的安全框架。认证用于确认用户身份，授权用于判断用户是否具备访问某一资源或执行某一操作的权限。本系统通过 SecurityConfig 配置登录页面、登录处理地址、退出登录地址、无权限跳转页面以及不同 URL 的访问角色。系统中 /admin/** 仅允许管理员访问，/scores/** 允许学生、老师和管理员访问，但成绩写操作进一步通过方法级权限限制，仅允许老师和管理员执行。",
        "2.3 Spring Data JPA",
        "Spring Data JPA 是 Spring 提供的数据访问框架，能够通过 Repository 接口简化数据库操作。开发者只需要定义实体类和继承 JpaRepository 的接口，就可以获得常见的增删改查能力。本系统定义了 SysUser、SysRole 和 StudentScore 三个主要实体，并通过 SysUserRepository、SysRoleRepository 和 StudentScoreRepository 完成数据访问。",
        "2.4 Thymeleaf 模板引擎",
        "Thymeleaf 是适用于 Spring Boot 的服务端模板引擎，能够将后端 Model 中的数据渲染到 HTML 页面中。本系统使用 Thymeleaf 实现登录页、登录成功页、成绩管理页、账号管理页、管理员主页和无权限提示页。页面文件统一存放在 src/main/resources/templates 目录下。",
        "2.5 MySQL 数据库",
        "MySQL 是常用的关系型数据库管理系统，具有开源、稳定、易部署等特点。本系统使用 MySQL 存储用户账号、角色、用户角色关系以及学生成绩数据。数据库连接参数配置在 application.properties 文件中，初始化脚本位于 src/main/resources/sql/init.sql。",
        "2.6 Maven 项目管理",
        "Maven 是 Java 项目常用的构建与依赖管理工具。本系统通过 pom.xml 管理 Spring Boot Web、Spring Security、Thymeleaf、Spring Data JPA 和 MySQL 驱动等依赖，并通过 Spring Boot Maven 插件完成项目打包。",
    ]),
    ("第三章 系统需求分析", [
        "3.1 可行性分析",
        "从技术可行性看，系统采用成熟的 Spring Boot、Spring Security、Spring Data JPA 和 MySQL 技术，开发资料丰富，集成难度较低。从经济可行性看，系统所使用的软件和框架均可免费使用，开发和部署成本较低。从操作可行性看，系统采用浏览器页面操作方式，用户只需通过登录页面进入系统即可使用相关功能，操作流程较为直观。",
        {"type": "table", "headers": ["可行性类型", "分析内容", "结论"], "rows": [
            ["技术可行性", "系统采用 Spring Boot、Spring Security、JPA、MySQL 等成熟技术", "可行"],
            ["经济可行性", "所用框架和数据库均可免费使用，部署成本较低", "可行"],
            ["操作可行性", "用户通过浏览器访问，页面以表格和表单为主", "可行"],
            ["维护可行性", "代码按 config、controller、entity、repository、service 分层", "可行"],
        ]},
        "3.2 功能需求分析",
        "系统需要实现用户登录功能。用户输入账号和密码后，系统应从数据库中读取用户信息并验证身份，登录成功后根据用户角色进入相应功能页面。系统需要实现成绩管理功能。成绩数据以表格形式展示，字段包括姓名、学号、科目、成绩、考试、学期、日期和备注。老师和管理员能够添加、修改、删除成绩，学生只能查看成绩。系统还需要支持成绩列表排序，用户可以按照学号、姓名、科目、成绩、考试、学期和日期进行排序。",
        "系统需要实现账号与用户分组管理功能。管理员可以新增账号、修改账号、删除账号，并为账号设置所属分组。系统分组包括老师、学生和管理员。管理员拥有其他用户的相关权限，可以访问成绩管理和账号管理页面。",
        {"type": "table", "headers": ["功能模块", "功能说明", "参与角色"], "rows": [
            ["登录认证", "用户输入账号和密码，系统完成身份验证", "学生、老师、管理员"],
            ["成绩查看", "以表格形式查看学生成绩数据", "学生、老师、管理员"],
            ["成绩维护", "添加、修改、删除学生成绩", "老师、管理员"],
            ["成绩排序", "按学号、姓名、科目、成绩、考试、学期、日期排序", "学生、老师、管理员"],
            ["账号管理", "新增、修改、删除用户账号", "管理员"],
            ["用户分组", "设置账号所属角色分组", "管理员"],
        ]},
        "3.3 用户角色需求",
        "学生角色主要用于查看成绩，不能添加、修改或删除成绩，也不能访问管理员账号管理页面。老师角色用于维护学生成绩，可以访问成绩管理页面，并执行成绩的增删改查操作。管理员角色用于系统管理，可以管理账号和用户分组，同时拥有成绩管理权限。",
        {"type": "table", "headers": ["角色", "初始账号", "权限范围"], "rows": [
            ["学生", "student / 123", "只能查看成绩，登录后可定位到姓名匹配的成绩行"],
            ["老师", "teacher / 123", "查看、添加、修改、删除学生成绩"],
            ["管理员", "damin / 123", "管理账号和用户分组，并拥有成绩管理权限"],
        ]},
        "3.4 非功能需求分析",
        "系统应具有基本安全性，能够防止未登录用户访问受保护页面，并限制不同角色的操作范围。系统应具有可维护性，代码按照配置层、控制层、实体层、数据访问层和页面层进行组织。系统应具有易用性，页面表格字段清晰，常用操作入口明确。系统应具有数据一致性，用户角色关系通过独立关联表维护，成绩数据通过数据库持久化保存。",
        "3.5 用例分析",
        "系统主要参与者包括学生、老师和管理员。学生登录系统后查看成绩；老师登录系统后维护成绩；管理员登录系统后管理账号和分组，并可以进入成绩管理页面。未登录用户访问系统受保护资源时会被重定向到登录页面；权限不足的用户访问管理员页面时会进入无权限提示页。",
    ]),
    ("第四章 系统总体设计", [
        "4.1 系统架构设计",
        "本系统采用典型的 Spring Boot 分层架构。控制层负责接收页面请求并返回视图；安全配置层负责登录认证和权限控制；数据访问层负责与数据库交互；实体层负责映射数据库表结构；视图层负责展示页面。该结构层次清晰，便于后续维护与扩展。",
        {"type": "table", "headers": ["层次", "对应包或目录", "主要职责"], "rows": [
            ["配置层", "config", "完成安全配置和基础数据初始化"],
            ["控制层", "controller", "接收页面请求，组织数据并返回视图"],
            ["服务层", "service", "加载用户认证信息"],
            ["数据访问层", "repository", "通过 JPA Repository 访问数据库"],
            ["实体层", "entity", "映射数据库表结构"],
            ["视图层", "templates、static/css", "展示页面和样式"],
        ]},
        "4.2 功能模块设计",
        "系统主要划分为五个模块。登录认证模块负责用户登录、退出和身份验证。权限控制模块负责不同角色对不同页面和操作的访问限制。学生成绩管理模块负责成绩数据的展示、添加、修改、删除和排序。账号管理模块负责管理员维护用户账号和分组。数据初始化模块负责系统启动时补齐基础账号、角色和成绩数据。",
        {"type": "table", "headers": ["模块名称", "主要功能", "核心文件"], "rows": [
            ["登录认证模块", "登录、退出、认证失败提示", "login.html、DatabaseUserDetailsService.java"],
            ["权限控制模块", "URL 访问限制和方法权限限制", "SecurityConfig.java、StudentScoreController.java"],
            ["成绩管理模块", "成绩列表、增删改查、排序、定位高亮", "StudentScoreController.java、scores.html"],
            ["账号管理模块", "账号新增、编辑、删除、分组设置", "AdminUserController.java、admin-users.html"],
            ["数据初始化模块", "初始化账号、角色和随机成绩", "DataInitializer.java、init.sql"],
        ]},
        "4.3 项目目录结构设计",
        "项目根目录包含 pom.xml、README.md、src 和 target 等内容。src/main/java/com/example/securitydemo 目录下包含 config、controller、entity、repository 和 service 等包。config 包中包含 SecurityConfig 和 DataInitializer；controller 包中包含 PageController、StudentScoreController 和 AdminUserController；entity 包中包含 SysUser、SysRole 和 StudentScore；repository 包中包含各实体对应的数据访问接口；service 包中包含 DatabaseUserDetailsService。src/main/resources 目录下包含 application.properties、sql/init.sql、static/css/app.css 和 templates 页面模板。",
        {"type": "table", "headers": ["目录或文件", "内容说明"], "rows": [
            ["pom.xml", "Maven 依赖和项目构建配置"],
            ["config", "安全配置类和数据初始化类"],
            ["controller", "页面控制器和业务请求处理"],
            ["entity", "用户、角色、成绩实体类"],
            ["repository", "数据库访问接口"],
            ["service", "Spring Security 用户认证服务"],
            ["templates", "Thymeleaf 页面模板"],
            ["static/css/app.css", "系统页面样式"],
            ["sql/init.sql", "数据库初始化脚本"],
        ]},
        "4.4 系统流程设计",
        "用户访问系统时首先进入登录页面。提交账号密码后，Spring Security 调用 DatabaseUserDetailsService 从数据库加载用户和角色信息。认证成功后进入登录成功页面，用户可根据权限进入成绩管理或管理员页面。访问成绩管理页面时，系统从数据库读取成绩数据并以表格形式展示。老师和管理员可以提交表单完成成绩新增或修改，也可以删除已有成绩。管理员进入账号管理页面后，可以维护用户基本信息和用户分组。",
    ]),
    ("第五章 数据库设计", [
        "5.1 数据库总体设计",
        "系统数据库名称为 spring_security_demo，主要包含 sys_user、sys_role、sys_user_role 和 student_score 四张表。sys_user 用于保存用户账号信息，sys_role 用于保存角色信息，sys_user_role 用于保存用户与角色之间的关联关系，student_score 用于保存学生成绩信息。",
        {"type": "table", "headers": ["数据表", "中文名称", "主要作用"], "rows": [
            ["sys_user", "用户表", "保存登录账号、密码和启用状态"],
            ["sys_role", "角色表", "保存老师、学生、管理员等角色"],
            ["sys_user_role", "用户角色关联表", "维护用户和角色之间的对应关系"],
            ["student_score", "学生成绩表", "保存学生成绩业务数据"],
        ]},
        "5.2 数据库 ER 图设计",
        "根据系统业务需求，数据库主要围绕用户、角色和学生成绩三个核心实体展开。其中用户和角色之间通过用户角色关联表形成多对多关系，一个用户可以拥有一个或多个角色，一个角色也可以被多个用户拥有。学生成绩表用于保存学生在不同科目和考试中的成绩信息。本系统数据库 ER 图如图 5-1 所示。",
        "图 5-1 学生成绩管理系统 ER 图",
        {"type": "image", "path": ER_IMAGE_PATH, "alt": "学生成绩管理系统 ER 图"},
        "+-------------------+          +-------------------+          +-------------------+",
        "|     sys_user      |          |   sys_user_role   |          |     sys_role      |",
        "+-------------------+          +-------------------+          +-------------------+",
        "| PK id             |<-------->| PK user_id        |          | PK id             |",
        "| username          |          | PK role_id        |<-------->| name              |",
        "| password          |          +-------------------+          | description       |",
        "| enabled           |                                             +-------------------+",
        "+-------------------+",
        "",
        "+------------------------+",
        "|     student_score      |",
        "+------------------------+",
        "| PK id                  |",
        "| student_name           |",
        "| student_number         |",
        "| subject                |",
        "| score                  |",
        "| exam_name              |",
        "| semester               |",
        "| exam_date              |",
        "| remark                 |",
        "+------------------------+",
        "从图 5-1 可以看出，sys_user 与 sys_role 并不直接关联，而是通过 sys_user_role 进行连接，这种设计便于后续扩展更多角色或为一个用户分配多个角色。student_score 表与账号表没有设置强外键关系，主要原因是成绩表中的 student_name 用于保存业务中的学生姓名，而系统登录账号 username 用于身份认证，两者在业务上可以进行匹配，例如 student 用户登录后可定位到 student_name 为 student 的成绩记录。",
        "5.3 用户表设计",
        "sys_user 表包含 id、username、password 和 enabled 字段。id 为主键并自增，username 表示登录账号且设置唯一约束，password 表示用户密码，enabled 表示账号是否启用。系统初始账号包括 teacher、student 和 damin，密码均为 123。",
        {"type": "table", "headers": ["字段名", "类型", "约束", "说明"], "rows": [
            ["id", "BIGINT", "主键、自增", "用户编号"],
            ["username", "VARCHAR(50)", "非空、唯一", "登录账号"],
            ["password", "VARCHAR(100)", "非空", "登录密码"],
            ["enabled", "TINYINT / Boolean", "非空", "账号是否启用"],
        ]},
        "5.4 角色表设计",
        "sys_role 表包含 id、name 和 description 字段。name 用于保存系统识别的角色名称，例如 ROLE_TEACHER、ROLE_STUDENT 和 ROLE_ADMIN；description 用于保存中文说明，例如老师、学生和管理员。",
        {"type": "table", "headers": ["字段名", "类型", "约束", "说明"], "rows": [
            ["id", "BIGINT", "主键、自增", "角色编号"],
            ["name", "VARCHAR(50)", "非空、唯一", "角色标识，如 ROLE_ADMIN"],
            ["description", "VARCHAR(100)", "可空", "角色中文说明"],
        ]},
        "5.5 用户角色关联表设计",
        "sys_user_role 表包含 user_id 和 role_id 两个字段，用于维护用户和角色之间的对应关系。通过该表可以灵活地为用户分配角色。本系统中 teacher 绑定老师角色，student 绑定学生角色，damin 绑定管理员角色。",
        {"type": "table", "headers": ["字段名", "类型", "约束", "说明"], "rows": [
            ["user_id", "BIGINT", "联合主键、外键", "关联 sys_user.id"],
            ["role_id", "BIGINT", "联合主键、外键", "关联 sys_role.id"],
        ]},
        "5.6 学生成绩表设计",
        "student_score 表是系统核心业务表，包含 id、student_name、student_number、subject、score、exam_name、semester、exam_date 和 remark 字段。student_name 表示学生姓名，student_number 表示学号，subject 表示科目，score 表示成绩，exam_name 表示考试名称，semester 表示学期，exam_date 表示考试日期，remark 表示备注。",
        {"type": "table", "headers": ["字段名", "类型", "约束", "说明"], "rows": [
            ["id", "BIGINT", "主键、自增", "成绩编号"],
            ["student_name", "VARCHAR(50)", "非空", "学生姓名"],
            ["student_number", "VARCHAR(30)", "非空", "学生学号"],
            ["subject", "VARCHAR(30)", "非空", "考试科目"],
            ["score", "DECIMAL(5,2)", "非空", "成绩分数"],
            ["exam_name", "VARCHAR(50)", "可空", "考试名称"],
            ["semester", "VARCHAR(30)", "可空", "所属学期"],
            ["exam_date", "DATE", "可空", "考试日期"],
            ["remark", "VARCHAR(200)", "可空", "备注信息"],
        ]},
        "5.7 数据初始化设计",
        "系统提供 init.sql 脚本用于创建数据库表和插入初始数据，同时 DataInitializer 类在系统启动时自动检查并补齐基础账号、角色和成绩数据。这样即使数据库只创建了基本表结构，系统启动后也能保证 teacher、student、damin 三个账号可用，并在成绩表为空时生成随机成绩数据。",
    ]),
    ("第六章 系统详细设计与实现", [
        "6.1 登录认证功能实现",
        "登录功能由 Spring Security 和自定义用户认证服务共同完成。用户在 login.html 页面输入账号和密码后，请求提交到 /login。SecurityConfig 中配置了登录页面、登录处理地址、登录成功地址和失败跳转地址。DatabaseUserDetailsService 实现 UserDetailsService 接口，根据用户名从 sys_user 表查询用户信息，并通过 SysRoleRepository 查询该用户拥有的角色，最后构造 Spring Security 所需的 UserDetails 对象。",
        {"type": "table", "headers": ["实现内容", "核心文件", "说明"], "rows": [
            ["登录页面", "login.html", "提供用户名和密码输入表单"],
            ["安全配置", "SecurityConfig.java", "配置登录地址、成功跳转和权限规则"],
            ["用户加载", "DatabaseUserDetailsService.java", "从数据库读取用户和角色"],
            ["角色查询", "SysRoleRepository.java", "根据用户名查询用户拥有的角色"],
        ]},
        "6.2 权限控制功能实现",
        "系统的权限控制主要在 SecurityConfig 中完成。/admin/** 路径仅允许 ROLE_ADMIN 用户访问；/scores/** 和 /user/** 允许 ROLE_STUDENT、ROLE_TEACHER 和 ROLE_ADMIN 访问。对于成绩的新增、修改和删除操作，StudentScoreController 使用 @PreAuthorize 注解限制只有老师和管理员能够执行。通过 URL 权限和方法权限结合的方式，系统能够同时控制页面访问和具体操作。",
        {"type": "table", "headers": ["访问路径或操作", "允许角色", "控制方式"], "rows": [
            ["/admin/**", "管理员", "SecurityConfig URL 权限"],
            ["/scores/**", "学生、老师、管理员", "SecurityConfig URL 权限"],
            ["/user/**", "学生、老师、管理员", "SecurityConfig URL 权限"],
            ["成绩新增", "老师、管理员", "@PreAuthorize 方法权限"],
            ["成绩修改", "老师、管理员", "@PreAuthorize 方法权限"],
            ["成绩删除", "老师、管理员", "@PreAuthorize 方法权限"],
        ]},
        "6.3 学生成绩管理功能实现",
        "学生成绩管理功能由 StudentScoreController、StudentScoreRepository、StudentScore 实体和 scores.html 页面共同实现。控制器接收 /scores 请求，通过 Repository 从数据库读取成绩列表，并根据请求参数设置排序字段和排序方向。页面通过 Thymeleaf 遍历成绩数据并生成表格。老师和管理员访问页面时可以看到成绩表单和操作按钮，学生访问页面时只能看到成绩列表。",
        "成绩新增功能通过 POST /scores 实现，控制器接收表单数据后调用 scoreRepository.save 方法保存。成绩修改功能通过 /scores/{id}/edit 加载待修改记录，并通过 POST /scores/{id} 保存修改结果。成绩删除功能通过 POST /scores/{id}/delete 完成。成绩排序功能通过 URL 参数 sort 和 direction 控制，支持按学号、姓名、科目、成绩、考试、学期和日期排序。",
        "系统还实现了学生登录后自动定位本人数据行的功能。当登录用户名与成绩表中的 student_name 一致时，访问成绩页面会自动重定向到带有锚点的地址，并通过页面样式高亮对应行。为了测试该功能，系统会固定补齐一条姓名为 student 的成绩数据。",
        "6.4 账号和用户分组管理实现",
        "账号管理功能由 AdminUserController 和 admin-users.html 页面实现。管理员可以查看所有账号，新增账号，编辑账号密码和启用状态，并为账号选择用户分组。账号与角色关系通过 sys_user_role 表维护。新增或修改账号时，控制器会先保存用户基本信息，再更新用户角色关系。",
        "6.5 页面设计实现",
        "系统页面采用 Thymeleaf 模板和 app.css 样式文件实现。login.html 为登录页面，login-success.html 为登录成功页面，scores.html 为成绩管理页面，admin-users.html 为账号管理页面，admin-main.html 为管理员主页，access-denied.html 为无权限提示页面。页面布局以表格和表单为主，突出系统管理功能，便于用户快速完成操作。",
        "6.6 数据访问层实现",
        "系统数据访问层使用 Spring Data JPA Repository 接口实现。SysUserRepository 提供根据用户名查询用户的方法；SysRoleRepository 提供根据用户名查询角色的方法；StudentScoreRepository 提供成绩数据的基本增删改查，并提供根据学生姓名查询成绩的方法。通过 Repository 接口，控制器无需直接编写复杂 SQL 即可完成常见数据操作。",
    ]),
    ("第七章 系统测试", [
        "7.1 测试环境",
        "系统测试环境包括 IntelliJ IDEA、JDK 17、MySQL 数据库和浏览器。项目使用 Spring Boot 2.7.18，数据库连接信息配置在 application.properties 中。测试前需要保证 spring_security_demo 数据库存在，并执行 init.sql 或通过系统启动初始化数据。",
        {"type": "table", "headers": ["环境项", "内容"], "rows": [
            ["开发工具", "IntelliJ IDEA"],
            ["运行环境", "JDK 17"],
            ["后端框架", "Spring Boot 2.7.18"],
            ["数据库", "MySQL"],
            ["浏览器", "Chrome、Edge 等现代浏览器"],
        ]},
        "7.2 登录功能测试",
        "分别使用 teacher、student 和 damin 三个账号登录系统，密码均为 123。测试结果显示，三个账号均可正常登录。输入错误用户名或密码时，系统会返回登录页并提示用户名或密码错误。",
        "7.3 权限控制测试",
        "使用 student 账号访问成绩管理页面，可以正常查看成绩，但页面不显示新增和修改表单，也无法执行成绩写操作。使用 teacher 账号访问成绩管理页面，可以执行成绩新增、修改和删除操作。使用 student 或 teacher 账号访问 /admin/users 页面时会被拒绝，使用 damin 账号可以正常访问账号管理页面。",
        "7.4 成绩管理测试",
        "使用 teacher 账号新增一条成绩记录，页面返回成绩列表后可以看到新增数据。选择已有成绩点击编辑，修改成绩后保存，表格中显示的成绩发生变化。点击删除按钮后，对应成绩记录被移除。点击表头中的排序链接，可以按照对应字段进行升序或降序排列。",
        "7.5 账号管理测试",
        "使用 damin 账号进入账号管理页面，新建账号并选择学生、老师或管理员分组，保存后账号出现在列表中。修改账号密码、启用状态和分组后，重新登录可以验证权限变化。删除非当前管理员账号后，该账号无法继续登录。",
        "7.6 测试结果分析",
        "通过以上测试可以看出，系统主要功能均能按照设计要求运行。登录认证、角色权限控制、成绩管理、账号管理和排序功能均达到预期效果。系统能够满足基本学生成绩管理场景的使用需求。",
        {"type": "table", "headers": ["测试编号", "测试内容", "输入或操作", "预期结果", "测试结论"], "rows": [
            ["T01", "学生登录", "student / 123", "登录成功，只能查看成绩", "通过"],
            ["T02", "老师登录", "teacher / 123", "登录成功，可维护成绩", "通过"],
            ["T03", "管理员登录", "damin / 123", "登录成功，可管理账号", "通过"],
            ["T04", "权限拦截", "学生访问 /admin/users", "进入无权限提示页", "通过"],
            ["T05", "新增成绩", "老师提交成绩表单", "成绩保存并显示在列表中", "通过"],
            ["T06", "修改成绩", "老师编辑已有成绩", "成绩内容更新", "通过"],
            ["T07", "删除成绩", "老师删除成绩", "成绩记录被移除", "通过"],
            ["T08", "成绩排序", "点击表头排序链接", "列表按对应字段排序", "通过"],
        ]},
    ]),
    ("第八章 总结与展望", [
        "8.1 工作总结",
        "本文设计并实现了一套基于 Spring Boot 与 Spring Security 的学生成绩管理系统。系统围绕学生成绩管理业务，完成了用户登录认证、角色权限控制、成绩数据增删改查、成绩排序、账号管理和用户分组管理等功能。系统采用分层结构组织代码，使用 MySQL 存储业务数据，使用 Thymeleaf 展示页面，整体结构清晰，便于理解和维护。",
        "8.2 系统不足",
        "由于开发时间和系统规模限制，本系统仍存在一些不足。首先，系统密码当前采用明文方式保存，安全性有待提高。其次，成绩查询功能还比较基础，目前主要支持排序，尚未实现按姓名、科目、考试名称等条件组合查询。再次，系统页面样式较简单，交互体验仍有提升空间。此外，系统暂未实现分页、成绩统计图表和 Excel 导入导出等功能。",
        "8.3 后续展望",
        "后续可以从以下方面对系统进行改进。第一，引入 BCrypt 等密码加密方式，提高账号安全性。第二，增加分页查询和多条件筛选功能，提高大量成绩数据下的使用效率。第三，增加班级、年级和课程管理模块，使系统业务模型更加完整。第四，增加 Excel 导入导出功能，方便教师批量维护成绩。第五，增加成绩统计和图表分析功能，为教学评价提供更直观的数据支持。",
    ]),
    ("参考文献", [
        "[1] Craig Walls. Spring in Action[M]. Manning Publications, 2018.",
        "[2] 汪云飞. Spring Boot 实战[M]. 北京：电子工业出版社，2018.",
        "[3] Spring 官方文档. Spring Boot Reference Documentation[EB/OL].",
        "[4] Spring 官方文档. Spring Security Reference Documentation[EB/OL].",
        "[5] MySQL 官方文档. MySQL 8.0 Reference Manual[EB/OL].",
        "[6] Thymeleaf 官方文档. Thymeleaf Documentation[EB/OL].",
        "[7] 孙卫琴. 精通 Spring 4.x 企业应用开发实战[M]. 北京：电子工业出版社，2017.",
        "[8] Bruce Eckel. Thinking in Java[M]. Prentice Hall, 2006.",
    ]),
    ("致谢", [
        "在本次毕业论文和系统设计实现过程中，我得到了指导教师和同学们的帮助与支持。指导教师在选题、系统设计和论文撰写方面给予了耐心指导，使我能够逐步明确系统需求和实现思路。在项目开发过程中，同学们也对系统功能测试和问题排查提出了许多有价值的建议。",
        "通过本次毕业设计，我对 Java Web 开发、Spring Boot 项目结构、Spring Security 权限控制和 MySQL 数据库设计有了更加深入的理解，也提升了独立分析问题和解决问题的能力。在此，向所有给予我帮助和支持的老师、同学和家人表示衷心感谢。",
    ]),
]


def paragraph_xml(text, style=None, bold=False, page_break_before=False):
    text = html.escape(text)
    ppr = ""
    if style or page_break_before:
        parts = []
        if style:
            parts.append(f'<w:pStyle w:val="{style}"/>')
        if page_break_before:
            parts.append("<w:pageBreakBefore/>")
        ppr = "<w:pPr>" + "".join(parts) + "</w:pPr>"
    rpr = "<w:rPr><w:b/></w:rPr>" if bold else ""
    return f"<w:p>{ppr}<w:r>{rpr}<w:t xml:space=\"preserve\">{text}</w:t></w:r></w:p>"


def table_xml(headers, rows):
    col_count = len(headers)
    grid = "".join('<w:gridCol w:w="2400"/>' for _ in range(col_count))

    def cell(value, header=False):
        shading = '<w:shd w:fill="D9EAF7"/>' if header else ""
        bold = "<w:b/>" if header else ""
        return (
            "<w:tc>"
            f"<w:tcPr><w:tcW w:w=\"2400\" w:type=\"dxa\"/>{shading}</w:tcPr>"
            "<w:p><w:r>"
            f"<w:rPr>{bold}</w:rPr>"
            f"<w:t xml:space=\"preserve\">{html.escape(str(value))}</w:t>"
            "</w:r></w:p>"
            "</w:tc>"
        )

    header_row = "<w:tr>" + "".join(cell(item, True) for item in headers) + "</w:tr>"
    body_rows = [
        "<w:tr>" + "".join(cell(row[index] if index < len(row) else "") for index in range(col_count)) + "</w:tr>"
        for row in rows
    ]
    return (
        "<w:tbl>"
        "<w:tblPr>"
        '<w:tblStyle w:val="TableGrid"/>'
        '<w:tblW w:w="0" w:type="auto"/>'
        '<w:tblBorders>'
        '<w:top w:val="single" w:sz="4" w:space="0" w:color="999999"/>'
        '<w:left w:val="single" w:sz="4" w:space="0" w:color="999999"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="999999"/>'
        '<w:right w:val="single" w:sz="4" w:space="0" w:color="999999"/>'
        '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="999999"/>'
        '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="999999"/>'
        '</w:tblBorders>'
        "</w:tblPr>"
        f"<w:tblGrid>{grid}</w:tblGrid>"
        + header_row
        + "".join(body_rows)
        + "</w:tbl>"
    )


def image_xml(relationship_id, alt_text):
    return f'''
<w:p>
  <w:pPr><w:jc w:val="center"/></w:pPr>
  <w:r>
    <w:drawing>
      <wp:inline distT="0" distB="0" distL="0" distR="0">
        <wp:extent cx="8230000" cy="5210000"/>
        <wp:effectExtent l="0" t="0" r="0" b="0"/>
        <wp:docPr id="1" name="{html.escape(alt_text)}" descr="{html.escape(alt_text)}"/>
        <wp:cNvGraphicFramePr>
          <a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>
        </wp:cNvGraphicFramePr>
        <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
              <pic:nvPicPr>
                <pic:cNvPr id="0" name="{html.escape(alt_text)}"/>
                <pic:cNvPicPr/>
              </pic:nvPicPr>
              <pic:blipFill>
                <a:blip r:embed="{relationship_id}"/>
                <a:stretch><a:fillRect/></a:stretch>
              </pic:blipFill>
              <pic:spPr>
                <a:xfrm>
                  <a:off x="0" y="0"/>
                  <a:ext cx="8230000" cy="5210000"/>
                </a:xfrm>
                <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
              </pic:spPr>
            </pic:pic>
          </a:graphicData>
        </a:graphic>
      </wp:inline>
    </w:drawing>
  </w:r>
</w:p>
'''


def build_document_xml():
    body = []
    body.append(paragraph_xml(TITLE, "Title", True))
    for title, paragraphs in SECTIONS:
        body.append(paragraph_xml(title, "Heading1", True, page_break_before=title in {"摘要", "第一章 绪论"}))
        for p in paragraphs:
            if isinstance(p, dict) and p.get("type") == "table":
                body.append(table_xml(p["headers"], p["rows"]))
            elif isinstance(p, dict) and p.get("type") == "image":
                body.append(image_xml("rId2", p.get("alt", "图片")))
            elif p.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.")):
                body.append(paragraph_xml(p, "Heading2", True))
            else:
                body.append(paragraph_xml(p))
    sect_pr = (
        "<w:sectPr>"
        "<w:pgSz w:w=\"11906\" w:h=\"16838\"/>"
        "<w:pgMar w:top=\"1440\" w:right=\"1440\" w:bottom=\"1440\" w:left=\"1440\" w:header=\"720\" w:footer=\"720\" w:gutter=\"0\"/>"
        "</w:sectPr>"
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" '
        'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
        'xmlns:o="urn:schemas-microsoft-com:office:office" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
        'xmlns:v="urn:schemas-microsoft-com:vml" '
        'xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture" '
        'xmlns:w10="urn:schemas-microsoft-com:office:word" '
        'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
        'xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" '
        'xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" '
        'xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" '
        'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" '
        'mc:Ignorable="w14 wp14">'
        "<w:body>"
        + "".join(body)
        + sect_pr
        + "</w:body></w:document>"
    )


CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>
"""

RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
"""

DOC_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/er-diagram.png"/>
</Relationships>
"""

STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:eastAsia="宋体" w:hAnsi="Times New Roman"/>
        <w:sz w:val="24"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:line="360" w:lineRule="auto"/>
        <w:ind w:firstLine="480"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:qFormat/>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:eastAsia="宋体" w:hAnsi="Times New Roman"/><w:sz w:val="24"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:basedOn w:val="Normal"/>
    <w:qFormat/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="720" w:after="480"/></w:pPr>
    <w:rPr><w:b/><w:rFonts w:ascii="Times New Roman" w:eastAsia="黑体" w:hAnsi="Times New Roman"/><w:sz w:val="36"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:qFormat/>
    <w:pPr><w:keepNext/><w:spacing w:before="360" w:after="240"/><w:outlineLvl w:val="0"/></w:pPr>
    <w:rPr><w:b/><w:rFonts w:ascii="Times New Roman" w:eastAsia="黑体" w:hAnsi="Times New Roman"/><w:sz w:val="32"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:qFormat/>
    <w:pPr><w:keepNext/><w:spacing w:before="240" w:after="120"/><w:outlineLvl w:val="1"/></w:pPr>
    <w:rPr><w:b/><w:rFonts w:ascii="Times New Roman" w:eastAsia="黑体" w:hAnsi="Times New Roman"/><w:sz w:val="28"/></w:rPr>
  </w:style>
</w:styles>
"""


def build_core_xml():
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>{html.escape(TITLE)}</dc:title>
  <dc:creator>Codex</dc:creator>
  <cp:lastModifiedBy>Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>
"""


APP_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Microsoft Word</Application>
</Properties>
"""


def write_docx():
    os.makedirs(OUT_DIR, exist_ok=True)
    with zipfile.ZipFile(DOCX_PATH, "w", zipfile.ZIP_DEFLATED) as docx:
        docx.writestr("[Content_Types].xml", CONTENT_TYPES)
        docx.writestr("_rels/.rels", RELS)
        docx.writestr("word/_rels/document.xml.rels", DOC_RELS)
        docx.writestr("word/document.xml", build_document_xml())
        docx.writestr("word/styles.xml", STYLES)
        if os.path.exists(ER_IMAGE_PATH):
            with open(ER_IMAGE_PATH, "rb") as f:
                docx.writestr("word/media/er-diagram.png", f.read())
        docx.writestr("docProps/core.xml", build_core_xml())
        docx.writestr("docProps/app.xml", APP_XML)


def write_markdown():
    lines = [f"# {TITLE}", ""]
    for title, paragraphs in SECTIONS:
        lines.append(f"## {title}")
        lines.append("")
        for p in paragraphs:
            if isinstance(p, dict) and p.get("type") == "table":
                headers = p["headers"]
                lines.append("| " + " | ".join(headers) + " |")
                lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
                for row in p["rows"]:
                    lines.append("| " + " | ".join(str(item) for item in row) + " |")
            elif isinstance(p, dict) and p.get("type") == "image":
                lines.append(f"![{p.get('alt', '图片')}]({p.get('path', '')})")
            elif p.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.")):
                lines.append(f"### {p}")
            else:
                lines.append(p)
            lines.append("")
    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    write_docx()
    write_markdown()
    print(DOCX_PATH)
    print(MD_PATH)
