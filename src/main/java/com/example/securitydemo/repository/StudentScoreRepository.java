package com.example.securitydemo.repository;

import com.example.securitydemo.entity.StudentScore;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface StudentScoreRepository extends JpaRepository<StudentScore, Long> {

    List<StudentScore> findByClassNameAndExamNameAndSemesterOrderByStudentNumberAsc(
            String className, String examName, String semester);

    List<StudentScore> findByStudentNameOrderBySemesterDescExamDateDesc(String studentName);

    List<StudentScore> findByStudentNameAndExamNameAndSemester(
            String studentName, String examName, String semester);

    boolean existsByExamName(String examName);

    @Query("SELECT DISTINCT s.examName FROM StudentScore s WHERE s.studentName = :studentName")
    List<String> findDistinctExamNameByStudentName(@Param("studentName") String studentName);

    @Query("SELECT DISTINCT s.semester FROM StudentScore s WHERE s.studentName = :studentName")
    List<String> findDistinctSemesterByStudentName(@Param("studentName") String studentName);

    List<StudentScore> findByStudentNameOrderByStudentNumberAsc(String studentName);
}
