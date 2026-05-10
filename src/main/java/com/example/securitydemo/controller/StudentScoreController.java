package com.example.securitydemo.controller;

import com.example.securitydemo.entity.StudentScore;
import com.example.securitydemo.entity.SysRole;
import com.example.securitydemo.entity.SysUser;
import com.example.securitydemo.repository.StudentScoreRepository;
import com.example.securitydemo.repository.SysRoleRepository;
import com.example.securitydemo.repository.SysUserRepository;
import java.math.BigDecimal;
import java.util.*;
import java.util.stream.Collectors;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller
@RequestMapping("/scores")
public class StudentScoreController {

    private static final List<String> EXAM_SUBJECTS = Arrays.asList("语文", "数学", "英语", "物理", "化学");

    private final StudentScoreRepository scoreRepository;
    private final SysUserRepository userRepository;
    private final SysRoleRepository roleRepository;
    private final PasswordEncoder passwordEncoder;

    public StudentScoreController(StudentScoreRepository scoreRepository,
            SysUserRepository userRepository, SysRoleRepository roleRepository,
            PasswordEncoder passwordEncoder) {
        this.scoreRepository = scoreRepository;
        this.userRepository = userRepository;
        this.roleRepository = roleRepository;
        this.passwordEncoder = passwordEncoder;
    }

    static class StudentRow {
        private String studentName;
        private String studentNumber;
        private String className;
        private Map<String, BigDecimal> subjectScores = new LinkedHashMap<>();
        private BigDecimal total = BigDecimal.ZERO;
        private int rank = 0;

        public String getStudentName() { return studentName; }
        public void setStudentName(String studentName) { this.studentName = studentName; }
        public String getStudentNumber() { return studentNumber; }
        public void setStudentNumber(String studentNumber) { this.studentNumber = studentNumber; }
        public String getClassName() { return className; }
        public void setClassName(String className) { this.className = className; }
        public Map<String, BigDecimal> getSubjectScores() { return subjectScores; }
        public BigDecimal getTotal() { return total; }
        public void setTotal(BigDecimal total) { this.total = total; }
        public int getRank() { return rank; }
        public void setRank(int rank) { this.rank = rank; }

        public BigDecimal getScore(String subject) {
            return subjectScores.getOrDefault(subject, null);
        }
    }

    @GetMapping
    public String list(@RequestParam(required = false) String className,
            @RequestParam(defaultValue = "期中考试") String examName,
            @RequestParam(defaultValue = "高一上") String semester,
            @RequestParam(defaultValue = "total") String sortBy,
            @RequestParam(defaultValue = "desc") String sortDir,
            Authentication authentication,
            Model model) {
        String username = authentication.getName();
        boolean canEdit = canEdit(authentication);
        model.addAttribute("canEdit", canEdit);
        model.addAttribute("username", username);
        model.addAttribute("subjects", EXAM_SUBJECTS);
        model.addAttribute("currentExam", examName);
        model.addAttribute("currentSemester", semester);
        model.addAttribute("sortBy", sortBy);
        model.addAttribute("sortDir", sortDir);

        if (!canEdit) {
            List<StudentScore> myScores = scoreRepository.findByStudentNameAndExamNameAndSemester(username, examName, semester);
            String myClass = myScores.isEmpty() ? "" : myScores.get(0).getClassName();
            List<StudentScore> classScores = scoreRepository.findByClassNameAndExamNameAndSemesterOrderByStudentNumberAsc(myClass, examName, semester);

            List<StudentRow> rows = buildStudentRows(classScores);
            sortRows(rows, sortBy, sortDir, username);
            model.addAttribute("scores", rows);
            model.addAttribute("myClass", myClass);
            model.addAttribute("highlightName", username);

            List<String> exams = scoreRepository.findDistinctExamNameByStudentName(username);
            List<String> semesters = scoreRepository.findDistinctSemesterByStudentName(username);
            model.addAttribute("myExams", exams);
            model.addAttribute("mySemesters", semesters);

            return "scores";
        } else {
            String displayClass = className != null ? className : "高一(1)班";
            List<StudentScore> allScores = scoreRepository.findByClassNameAndExamNameAndSemesterOrderByStudentNumberAsc(displayClass, examName, semester);

            List<StudentRow> rows = buildStudentRows(allScores);
            sortRows(rows, sortBy, sortDir, null);
            model.addAttribute("scores", rows);
            model.addAttribute("selectedClass", displayClass);

            return "scores";
        }
    }

    private List<StudentRow> buildStudentRows(List<StudentScore> scores) {
        Map<String, StudentRow> studentMap = new LinkedHashMap<>();
        for (StudentScore s : scores) {
            StudentRow row = studentMap.computeIfAbsent(s.getStudentNumber(), k -> {
                StudentRow r = new StudentRow();
                r.setStudentName(s.getStudentName());
                r.setStudentNumber(s.getStudentNumber());
                r.setClassName(s.getClassName());
                return r;
            });
            row.getSubjectScores().put(s.getSubject(), s.getScore());
        }
        for (StudentRow row : studentMap.values()) {
            BigDecimal total = BigDecimal.ZERO;
            for (BigDecimal score : row.getSubjectScores().values()) {
                if (score != null) total = total.add(score);
            }
            row.setTotal(total);
        }
        return new ArrayList<>(studentMap.values());
    }

    private void sortRows(List<StudentRow> rows, String sortBy, String sortDir, String highlightName) {
        boolean ascending = "asc".equals(sortDir);

        rows.sort((a, b) -> {
            int cmp = compareRow(a, b, sortBy);
            return ascending ? cmp : -cmp;
        });

        int rank = 1;
        for (int i = 0; i < rows.size(); i++) {
            if (i > 0 && rows.get(i).getTotal().equals(rows.get(i - 1).getTotal())) {
                rows.get(i).setRank(rows.get(i - 1).getRank());
            } else {
                rows.get(i).setRank(rank);
            }
            rank++;
        }
    }

    private int compareRow(StudentRow a, StudentRow b, String sortBy) {
        if ("studentNumber".equals(sortBy)) {
            return a.getStudentNumber().compareTo(b.getStudentNumber());
        }
        if ("studentName".equals(sortBy)) {
            return a.getStudentName().compareTo(b.getStudentName());
        }
        if ("total".equals(sortBy) || sortBy == null) {
            return a.getTotal().compareTo(b.getTotal());
        }
        BigDecimal sa = a.getScore(sortBy);
        BigDecimal sb = b.getScore(sortBy);
        if (sa == null && sb == null) return 0;
        if (sa == null) return 1;
        if (sb == null) return -1;
        return sa.compareTo(sb);
    }

    @PostMapping
    @PreAuthorize("hasAnyRole('TEACHER', 'ADMIN')")
    @ResponseBody
    public String create(@Validated @ModelAttribute StudentScore score, BindingResult result, Authentication authentication) {
        if (result.hasErrors()) {
            return "error:" + result.getAllErrors().stream().map(e -> e.getDefaultMessage()).collect(Collectors.joining(", "));
        }
        scoreRepository.save(score);
        ensureStudentAccount(score.getStudentName());
        return "success";
    }

    @GetMapping("/{id}/data")
    @PreAuthorize("hasAnyRole('TEACHER', 'ADMIN')")
    @ResponseBody
    public Map<String, Object> edit(@PathVariable Long id) {
        StudentScore score = scoreRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("成绩不存在：" + id));
        Map<String, Object> data = new HashMap<>();
        data.put("studentName", score.getStudentName());
        data.put("studentNumber", score.getStudentNumber());
        data.put("className", score.getClassName());
        data.put("subject", score.getSubject());
        data.put("score", score.getScore());
        data.put("examName", score.getExamName());
        data.put("semester", score.getSemester());
        data.put("examDate", score.getExamDate() != null ? score.getExamDate().toString() : "");
        data.put("remark", score.getRemark());
        return data;
    }

    @PostMapping("/{id}")
    @PreAuthorize("hasAnyRole('TEACHER', 'ADMIN')")
    @ResponseBody
    public String update(@PathVariable Long id, @Validated @ModelAttribute StudentScore score, BindingResult result) {
        if (result.hasErrors()) {
            return "error:" + result.getAllErrors().stream().map(e -> e.getDefaultMessage()).collect(Collectors.joining(", "));
        }
        StudentScore existing = scoreRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("成绩不存在：" + id));
        existing.setStudentName(score.getStudentName());
        existing.setStudentNumber(score.getStudentNumber());
        existing.setClassName(score.getClassName());
        existing.setSubject(score.getSubject());
        existing.setScore(score.getScore());
        existing.setExamName(score.getExamName());
        existing.setSemester(score.getSemester());
        existing.setExamDate(score.getExamDate());
        existing.setRemark(score.getRemark());
        scoreRepository.save(existing);
        return "success";
    }

    @PostMapping("/{id}/delete")
    @PreAuthorize("hasAnyRole('TEACHER', 'ADMIN')")
    public String delete(@PathVariable Long id, RedirectAttributes redirectAttributes) {
        scoreRepository.deleteById(id);
        redirectAttributes.addFlashAttribute("message", "删除成功");
        return "redirect:/scores";
    }

    @PostMapping("/change-password")
    @ResponseBody
    public String changePassword(@RequestParam String studentName, @RequestParam String newPassword, Authentication authentication) {
        boolean isAdmin = isAdmin(authentication);
        boolean isSelf = authentication.getName().equals(studentName);
        if (!isAdmin && !isSelf) {
            return "error:无权操作";
        }
        SysUser user = userRepository.findByUsername(studentName).orElse(null);
        if (user == null) {
            return "error:该学生尚未创建登录账号";
        }
        user.setPassword(passwordEncoder.encode(newPassword));
        userRepository.save(user);
        return "success";
    }

    @GetMapping("/my-exams")
    public String myExams(Authentication authentication, Model model) {
        String username = authentication.getName();
        model.addAttribute("username", username);

        List<StudentScore> allScores = scoreRepository.findByStudentNameOrderBySemesterDescExamDateDesc(username);

        Map<String, List<StudentScore>> groupedScores = new LinkedHashMap<>();
        Map<String, BigDecimal> examTotals = new LinkedHashMap<>();
        BigDecimal grandTotal = BigDecimal.ZERO;
        int grandCount = 0;

        for (StudentScore s : allScores) {
            String key = s.getSemester() + " - " + s.getExamName();
            groupedScores.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
            examTotals.merge(key, s.getScore(), BigDecimal::add);
            grandTotal = grandTotal.add(s.getScore());
            grandCount++;
        }

        model.addAttribute("groupedScores", groupedScores);
        model.addAttribute("examTotals", examTotals);
        model.addAttribute("grandTotal", grandTotal);
        model.addAttribute("grandCount", grandCount);
        model.addAttribute("grandAvg", grandCount > 0 ? grandTotal.divide(BigDecimal.valueOf(grandCount), 1, java.math.RoundingMode.HALF_UP) : BigDecimal.ZERO);
        return "my-exams";
    }

    @GetMapping("/exam-view")
    public String examView(@RequestParam String studentName,
            @RequestParam String targetExam,
            @RequestParam String targetSemester,
            @RequestParam(defaultValue = "total") String sortBy,
            @RequestParam(defaultValue = "desc") String sortDir,
            Authentication authentication,
            Model model) {
        String currentUser = authentication.getName();
        boolean canEdit = canEdit(authentication);
        model.addAttribute("username", currentUser);
        model.addAttribute("canEdit", canEdit);
        model.addAttribute("subjects", EXAM_SUBJECTS);
        model.addAttribute("currentExam", targetExam);
        model.addAttribute("currentSemester", targetSemester);
        model.addAttribute("sortBy", sortBy);
        model.addAttribute("sortDir", sortDir);

        List<StudentScore> studentScores = scoreRepository.findByStudentNameAndExamNameAndSemester(studentName, targetExam, targetSemester);
        String className = studentScores.isEmpty() ? "" : studentScores.get(0).getClassName();

        List<StudentScore> classScores = scoreRepository.findByClassNameAndExamNameAndSemesterOrderByStudentNumberAsc(className, targetExam, targetSemester);

        List<StudentRow> rows = buildStudentRows(classScores);
        sortRows(rows, sortBy, sortDir, currentUser);
        model.addAttribute("scores", rows);
        model.addAttribute("examName", targetExam);
        model.addAttribute("semester", targetSemester);
        model.addAttribute("className", className);
        model.addAttribute("studentName", studentName);
        model.addAttribute("highlightName", studentName);

        if (!canEdit) {
            model.addAttribute("myClass", className);
            model.addAttribute("myExams", scoreRepository.findDistinctExamNameByStudentName(currentUser));
            model.addAttribute("mySemesters", scoreRepository.findDistinctSemesterByStudentName(currentUser));
        }

        return "scores";
    }

    private void ensureStudentAccount(String studentName) {
        if (userRepository.existsByUsername(studentName)) {
            return;
        }
        SysRole studentRole = roleRepository.findByName("ROLE_STUDENT")
                .orElseThrow(() -> new RuntimeException("学生角色不存在"));
        SysUser user = new SysUser();
        user.setUsername(studentName);
        user.setPassword(passwordEncoder.encode("123"));
        user.setEnabled(true);
        user.addRole(studentRole);
        userRepository.save(user);
    }

    private boolean canEdit(Authentication authentication) {
        return authentication.getAuthorities().stream()
                .map(GrantedAuthority::getAuthority)
                .anyMatch(role -> "ROLE_TEACHER".equals(role) || "ROLE_ADMIN".equals(role));
    }

    private boolean isAdmin(Authentication authentication) {
        return authentication.getAuthorities().stream()
                .map(GrantedAuthority::getAuthority)
                .anyMatch(role -> "ROLE_ADMIN".equals(role));
    }
}
