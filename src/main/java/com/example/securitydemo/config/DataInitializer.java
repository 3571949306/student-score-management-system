package com.example.securitydemo.config;

import com.example.securitydemo.entity.StudentScore;
import com.example.securitydemo.entity.SysRole;
import com.example.securitydemo.entity.SysUser;
import com.example.securitydemo.repository.StudentScoreRepository;
import com.example.securitydemo.repository.SysRoleRepository;
import com.example.securitydemo.repository.SysUserRepository;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Arrays;
import java.util.List;
import javax.annotation.PostConstruct;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

@Component
public class DataInitializer {

    private static final Logger log = LoggerFactory.getLogger(DataInitializer.class);

    // 15 students: 8 in class 1, 7 in class 2
    private static final String[][] CLASS1_STUDENTS = {
        {"李明", "20260101"},
        {"王芳", "20260102"},
        {"张伟", "20260103"},
        {"刘洋", "20260104"},
        {"陈静", "20260105"},
        {"赵强", "20260106"},
        {"孙丽", "20260107"},
        {"周杰", "20260108"}
    };

    private static final String[][] CLASS2_STUDENTS = {
        {"吴敏", "20260201"},
        {"郑浩", "20260202"},
        {"马丽", "20260203"},
        {"林峰", "20260204"},
        {"黄婷", "20260205"},
        {"杨磊", "20260206"},
        {"徐超", "20260207"}
    };

    private static final List<String> SUBJECTS = Arrays.asList("语文", "数学", "英语", "物理", "化学");
    private static final String CLASS1 = "高一(1)班";
    private static final String CLASS2 = "高一(2)班";

    private final SysUserRepository userRepository;
    private final SysRoleRepository roleRepository;
    private final StudentScoreRepository scoreRepository;
    private final PasswordEncoder passwordEncoder;

    public DataInitializer(SysUserRepository userRepository, SysRoleRepository roleRepository,
            StudentScoreRepository scoreRepository, PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.roleRepository = roleRepository;
        this.scoreRepository = scoreRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @PostConstruct
    public void init() {
        log.info("开始初始化系统角色和账号数据...");

        SysRole teacherRole = ensureRole("ROLE_TEACHER", "老师");
        SysRole studentRole = ensureRole("ROLE_STUDENT", "学生");
        SysRole adminRole = ensureRole("ROLE_ADMIN", "管理员");

        ensureUser("admin", "123", adminRole);
        ensureUser("teacher", "123", teacherRole);

        // Create all student accounts
        createStudentAccounts(CLASS1_STUDENTS, studentRole);
        createStudentAccounts(CLASS2_STUDENTS, studentRole);

        // Initialize scores if not exists
        if (!scoreRepository.existsByExamName("期中考试")) {
            initScores(CLASS1_STUDENTS, CLASS1, "期中考试", "高一上", LocalDate.of(2026, 4, 20));
            initScores(CLASS2_STUDENTS, CLASS2, "期中考试", "高一上", LocalDate.of(2026, 4, 20));
            initScores(CLASS1_STUDENTS, CLASS1, "期末考试", "高一上", LocalDate.of(2026, 7, 10));
            initScores(CLASS2_STUDENTS, CLASS2, "期末考试", "高一上", LocalDate.of(2026, 7, 10));
            log.info("已初始化所有成绩数据");
        }

        log.info("系统初始化完成。");
    }

    private void createStudentAccounts(String[][] students, SysRole studentRole) {
        for (String[] s : students) {
            String name = s[0];
            if (!userRepository.existsByUsername(name)) {
                SysUser user = new SysUser();
                user.setUsername(name);
                user.setPassword(passwordEncoder.encode("123"));
                user.setEnabled(true);
                user.addRole(studentRole);
                userRepository.save(user);
                log.info("创建学生账号: {} (密码: 123)", name);
            }
        }
    }

    private void initScores(String[][] students, String className, String examName, String semester, LocalDate examDate) {
        // Use deterministic scores based on student index and subject
        int[][] baseScores = {
            {115, 92, 128, 85, 90},   // student 0
            {122, 138, 132, 140, 135}, // student 1
            {88, 105, 75, 92, 98},     // student 2
            {105, 88, 110, 78, 85},    // student 3
            {118, 125, 120, 115, 110}, // student 4
            {95, 112, 98, 105, 92},    // student 5
            {108, 95, 115, 88, 95},    // student 6
            {82, 78, 85, 72, 80},      // student 7
        };

        for (int i = 0; i < students.length; i++) {
            String name = students[i][0];
            String number = students[i][1];
            int[] scores = baseScores[i % baseScores.length];

            // Add some variation for the second exam
            int examOffset = "期末考试".equals(examName) ? 5 : 0;

            for (int j = 0; j < SUBJECTS.size(); j++) {
                int score = Math.min(150, scores[j] + examOffset + (i * 3) % 10);
                StudentScore s = new StudentScore();
                s.setStudentName(name);
                s.setStudentNumber(number);
                s.setClassName(className);
                s.setSubject(SUBJECTS.get(j));
                s.setScore(BigDecimal.valueOf(score));
                s.setExamName(examName);
                s.setSemester(semester);
                s.setExamDate(examDate);
                s.setRemark("");
                scoreRepository.save(s);
            }
        }
    }

    private SysRole ensureRole(String name, String description) {
        return roleRepository.findByName(name)
                .map(r -> { r.setDescription(description); return r; })
                .orElseGet(() -> {
                    SysRole role = new SysRole();
                    role.setName(name);
                    role.setDescription(description);
                    return roleRepository.save(role);
                });
    }

    private void ensureUser(String username, String rawPassword, SysRole role) {
        userRepository.findByUsername(username).map(existingUser -> {
            existingUser.setPassword(passwordEncoder.encode(rawPassword));
            existingUser.setEnabled(true);
            existingUser.clearRoles();
            existingUser.addRole(role);
            return userRepository.save(existingUser);
        }).orElseGet(() -> {
            SysUser newUser = new SysUser();
            newUser.setUsername(username);
            newUser.setPassword(passwordEncoder.encode(rawPassword));
            newUser.setEnabled(true);
            newUser.addRole(role);
            return userRepository.save(newUser);
        });
    }
}
