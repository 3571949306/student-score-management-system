package com.example.securitydemo.entity;

import java.math.BigDecimal;
import java.time.LocalDate;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;
import javax.validation.constraints.DecimalMax;
import javax.validation.constraints.DecimalMin;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;

@Entity
@Table(name = "student_score")
public class StudentScore {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank(message = "姓名不能为空")
    @Size(max = 50, message = "姓名最多50个字符")
    @Column(nullable = false, length = 50)
    private String studentName;

    @NotBlank(message = "学号不能为空")
    @Size(max = 30, message = "学号最多30个字符")
    @Column(nullable = false, length = 30)
    private String studentNumber;

    @NotBlank(message = "班级不能为空")
    @Size(max = 30, message = "班级最多30个字符")
    @Column(nullable = false, length = 30)
    private String className;

    @NotBlank(message = "科目不能为空")
    @Size(max = 30, message = "科目最多30个字符")
    @Column(nullable = false, length = 30)
    private String subject;

    @NotNull(message = "成绩不能为空")
    @DecimalMin(value = "0", message = "成绩不能小于0")
    @DecimalMax(value = "150", message = "成绩不能大于150")
    @Column(nullable = false, precision = 5, scale = 2)
    private BigDecimal score;

    @NotBlank(message = "考试不能为空")
    @Size(max = 50, message = "考试名称最多50个字符")
    @Column(nullable = false, length = 50)
    private String examName;

    @NotBlank(message = "学期不能为空")
    @Size(max = 30, message = "学期最多30个字符")
    @Column(nullable = false, length = 30)
    private String semester;

    private LocalDate examDate;

    @Size(max = 200, message = "备注最多200个字符")
    @Column(length = 200)
    private String remark;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getStudentName() {
        return studentName;
    }

    public void setStudentName(String studentName) {
        this.studentName = studentName;
    }

    public String getStudentNumber() {
        return studentNumber;
    }

    public void setStudentNumber(String studentNumber) {
        this.studentNumber = studentNumber;
    }

    public String getClassName() {
        return className;
    }

    public void setClassName(String className) {
        this.className = className;
    }

    public String getSubject() {
        return subject;
    }

    public void setSubject(String subject) {
        this.subject = subject;
    }

    public BigDecimal getScore() {
        return score;
    }

    public void setScore(BigDecimal score) {
        this.score = score;
    }

    public String getExamName() {
        return examName;
    }

    public void setExamName(String examName) {
        this.examName = examName;
    }

    public String getSemester() {
        return semester;
    }

    public void setSemester(String semester) {
        this.semester = semester;
    }

    public LocalDate getExamDate() {
        return examDate;
    }

    public void setExamDate(LocalDate examDate) {
        this.examDate = examDate;
    }

    public String getRemark() {
        return remark;
    }

    public void setRemark(String remark) {
        this.remark = remark;
    }
}
